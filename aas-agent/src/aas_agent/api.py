"""FastAPI app — OpenAI-compatible chat completions with multi-variant routing.

Each variant is advertised as a separate model ID on /v1/models. The user
picks their orchestration pattern in Open WebUI (or any client) by setting
the `model` field. Runners are lazily initialized on first request for
their model ID and cached for the lifetime of the process.

A shared MCP client provides tools, manual, and schema context to all
variants so that only the graph topology and system prompt differ.
"""

import asyncio
import json
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict

from aas_agent.mcp_client import MCPClientManager
from aas_agent.usage import (
    empty_usage,
    try_decode_usage_sentinel,
    usage_to_openai,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Model / variant registry
# ---------------------------------------------------------------------------
# _MODEL_INFO maps model_id → (variant, prompt_file_stem).
# All variants are tool-bearing. Open WebUI background tasks (title/tag/
# follow-up) are routed directly to the vLLM endpoint via Open WebUI's
# second OPENAI_API_BASE_URLS entry — they never hit this service.
# Verbose variants (``*-verbose``) are handled automatically — the suffix is
# stripped and ``extra['verbose']`` is set to ``True`` for stream/invoke.
_MODEL_INFO: dict[str, tuple[str, str]] = {
    "aas-agent:react":     ("react",        "system-prompt.md"),
    "aas-agent:plan":      ("plan_reflect", "system-prompt.md"),
    "aas-agent:reflexion": ("reflexion",    "system-prompt.md"),
}

# Auto-generate verbose variants for every model
for base_id, info in list(_MODEL_INFO.items()):
    _MODEL_INFO[base_id + "-verbose"] = info

_DELIMITER = "-verbose"

_PROMPT_DIR = Path(__file__).parent


# ---------------------------------------------------------------------------
# Shared resources (initialized in lifespan)
# ---------------------------------------------------------------------------
_mcp: MCPClientManager | None = None
_mcp_context: str = ""
_all_tools: list = []
_llm_base_url: str = ""
_llm_model: str = ""
_log_dir: Path | None = None
_inject_manual: bool = True
_inject_schema: bool = True

# Per-model runner cache + init lock
_runners: dict[str, Any] = {}
_runner_locks: dict[str, asyncio.Lock] = {}


# ---------------------------------------------------------------------------
# Validate required env vars at import time
# ---------------------------------------------------------------------------
_default_model: str = os.environ.get("AGENT_DEFAULT_MODEL") or ""
if not _default_model:
    raise RuntimeError("Missing required env var: AGENT_DEFAULT_MODEL")
if _default_model not in _MODEL_INFO:
    raise RuntimeError(
        f"AGENT_DEFAULT_MODEL={_default_model!r} is not registered. "
        f"Available: {sorted(_MODEL_INFO.keys())}"
    )

# ---------------------------------------------------------------------------
# Request / response models (OpenAI-compatible subset)
# ---------------------------------------------------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = _default_model
    messages: list[Message]
    stream: bool = False
    temperature: float | None = None
    max_tokens: int | None = None
    reasoning_effort: str | None = None
    chat_id: str | None = None


# ---------------------------------------------------------------------------
# Lazy runner initialization
# ---------------------------------------------------------------------------

def _resolve_prompt_file(prompt_file_stem: str) -> Path:
    override = os.environ.get("AGENT_SYSTEM_PROMPT_DIR", "")
    if override:
        candidate = Path(override) / prompt_file_stem
        if candidate.exists():
            return candidate
    return _PROMPT_DIR / prompt_file_stem


async def _get_runner(model_id: str, temperature: float | None = None) -> Any:
    """Return a ready-to-use agent runner for *model_id*, initializing it on first call."""
    if model_id in _runners and _runners[model_id] is not None:
        return _runners[model_id]

    # Ensure lock exists
    if model_id not in _runner_locks:
        _runner_locks[model_id] = asyncio.Lock()

    async with _runner_locks[model_id]:
        # Double-check after acquiring lock
        if model_id in _runners:
            runner = _runners[model_id]
            if runner is not None:
                return runner

        info = _MODEL_INFO.get(model_id)
        if info is None:
            raise ValueError(f"Unknown model: {model_id}")

        variant, prompt_file_stem = info

        system_prompt = _resolve_prompt_file(prompt_file_stem).read_text(encoding="utf-8")
        log.info("Loaded %s prompt for model %s (%d chars)", prompt_file_stem, model_id, len(system_prompt))

        runner_cls = _resolve_runner_class(variant)
        runner = runner_cls(
            mcp_client=_mcp,
            llm_base_url=_llm_base_url,
            llm_model=_llm_model,
            system_prompt=system_prompt,
            default_thinking=False,
            log_dir=_log_dir,
            temperature=temperature,
        )

        await runner._lazy_init(
            mcp_context=_mcp_context,
            all_tools=list(_all_tools),
        )

        log.info("Agent runner initialized for model %s (variant=%s)", model_id, variant)
        _runners[model_id] = runner
        return runner


def _resolve_runner_class(variant: str):
    """Map variant string to its Runner class."""
    if variant == "plan_reflect":
        from aas_agent.agent_plan import PlanReflectAgentRunner
        return PlanReflectAgentRunner
    elif variant == "reflexion":
        from aas_agent.reflexion import ReflexionAgentRunner
        return ReflexionAgentRunner
    else:
        from aas_agent.agent import AgentRunner
        return AgentRunner


# ---------------------------------------------------------------------------
# Lifespan — startup / shutdown (shared resources only)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _mcp, _mcp_context, _all_tools
    global _llm_base_url, _llm_model, _log_dir
    global _inject_manual, _inject_schema

    mcp_url = os.environ.get("MCP_SERVER_URL", "http://localhost:8110/mcp/")
    _llm_base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    _llm_model = os.environ.get("LLM_MODEL", "gpt-4o")

    def _env_bool(name: str, default: bool) -> bool:
        raw = os.environ.get(name)
        if raw is None:
            return default
        return raw.lower() in ("1", "true", "yes", "on")

    _inject_manual = _env_bool("AGENT_INJECT_MANUAL", True)
    _inject_schema = _env_bool("AGENT_INJECT_SCHEMA", True)

    log_dir_env = os.environ.get("AGENT_LOG_DIR", "")
    _log_dir = Path(log_dir_env) if log_dir_env else None
    if _log_dir:
        log.info("Conversation logging enabled → %s", _log_dir)

    _mcp = MCPClientManager(
        mcp_url,
        inject_manual=_inject_manual,
        inject_schema=_inject_schema,
    )
    log.info("Auto-injected resources: manual=%s, schema=%s", _inject_manual, _inject_schema)

    # Connect MCP and load shared context + tools
    for _retry in range(15):
        try:
            await _mcp.connect()
            break
        except Exception as e:
            if _retry == 14:
                log.critical("MCP connect failed after 15 retries: %s", e)
                raise
            log.warning("MCP connect attempt %d failed, retrying in 3s: %s", _retry + 1, e)
            await asyncio.sleep(3)

    _mcp_context = await _mcp.load_context()
    _all_tools = await _mcp.get_langchain_tools()
    log.info("Shared resources loaded — %d tools, %d chars context", len(_all_tools), len(_mcp_context))

    yield

    await _mcp.disconnect()
    _mcp = None
    _runners.clear()
    _runner_locks.clear()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title="AAS Agent", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": mid,
                "object": "model",
                "created": 0,
                "owned_by": "aas-hybrid-mcp",
            }
            for mid in _MODEL_INFO.keys()
        ],
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, http_request: Request):
    if _mcp is None:
        return {"error": "Agent not initialized"}, 503

    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created = int(time.time())

    headers = {k.lower(): v for k, v in http_request.headers.items()}
    client_id = _extract_client_id(request, headers)

    extra = request.model_extra or {}
    if extra:
        log.info("Extra body fields from client: %s", extra)
    custom_headers = {
        k: v for k, v in headers.items()
        if k.startswith("x-") and not k.startswith("x-forwarded")
    }
    if custom_headers:
        log.info("Custom headers from client: %s", custom_headers)

    original_model = request.model or _default_model

    # Strip verbose suffix for runner lookup; inject into extra for stream/invoke
    verbose = original_model.endswith(_DELIMITER)
    model = original_model[:-len(_DELIMITER)] if verbose else original_model

    try:
        runner = await _get_runner(model, temperature=request.temperature)
    except ValueError as e:
        return {"error": str(e)}, 400

    # Inject verbose flag + variant name into extra for trace header
    extra = dict(extra)
    if verbose:
        extra["verbose"] = True
    extra["variant"] = _MODEL_INFO[model][0]

    if request.stream:
        return StreamingResponse(
            _stream_sse(completion_id, created, model, runner, messages, client_id, extra or None),
            media_type="text/event-stream",
        )

    text, usage = await runner.invoke(messages, conversation_id=completion_id, chat_id=client_id, extra=extra or None)
    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": created,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
        ],
        "usage": usage_to_openai(usage),
    }


def _extract_client_id(
    request: ChatCompletionRequest,
    headers: dict[str, str] | None = None,
) -> str | None:
    if request.chat_id:
        return request.chat_id
    if "client_id" in (request.model_extra or {}):
        return str(request.model_extra["client_id"])
    if headers:
        for h in ("x-openwebui-chat-id", "x-chat-id"):
            if h in headers:
                return headers[h]
    return None


async def _stream_sse(
    completion_id: str,
    created: int,
    model: str,
    runner: Any,
    messages: list[dict],
    client_id: str | None,
    extra: dict | None = None,
):
    usage = empty_usage()
    try:
        async for token in runner.stream(messages, conversation_id=completion_id, chat_id=client_id, extra=extra):
            if not isinstance(token, str):
                token = str(token)
            # Runners yield a ``__usage__:{...}`` sentinel in their finally
            # block. Capture it and skip emitting as visible content — usage
            # is reported in the OpenAI-style chunk just before [DONE].
            decoded = try_decode_usage_sentinel(token)
            if decoded is not None:
                usage = decoded
                continue
            chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": model,
                "choices": [
                    {"index": 0, "delta": {"content": token}, "finish_reason": None}
                ],
            }
            yield f"data: {json.dumps(chunk)}\n\n"
    except Exception:
        log.exception("Error while streaming agent response")
        err_chunk = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": "\n\n[stream error — see server logs]"},
                    "finish_reason": None,
                }
            ],
        }
        yield f"data: {json.dumps(err_chunk)}\n\n"
    finally:
        done_chunk = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        }
        yield f"data: {json.dumps(done_chunk)}\n\n"
        # Final usage chunk (OpenAI sends this when stream_options.include_usage=true).
        usage_chunk = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [],
            "usage": usage_to_openai(usage),
        }
        yield f"data: {json.dumps(usage_chunk)}\n\n"
        yield "data: [DONE]\n\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    uvicorn.run(app, host="0.0.0.0", port=8120)


if __name__ == "__main__":
    main()
