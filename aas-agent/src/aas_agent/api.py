"""FastAPI app — OpenAI-compatible chat completions endpoint."""

import json
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict

from aas_agent.agent import AgentRunner
from aas_agent.mcp_client import MCPClientManager

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


# Exposed model IDs — users pick one in Open WebUI's model dropdown to toggle
# the Qwen3 thinking mode on or off. Both share the same tools, resources,
# system prompt, and underlying weights; only the chat-template flag differs.
MODEL_ID_NO_THINK = "aas-agent"
MODEL_ID_THINK = "aas-agent-think"


def _effort_for_model(model_name: str | None) -> str | None:
    """Map the requested model name to a reasoning_effort override.

    ``aas-agent-think`` forces thinking on; ``aas-agent`` forces it off.
    Anything else (or missing) returns None, so the request's own
    ``reasoning_effort`` field and the deployment default apply.
    """
    if model_name == MODEL_ID_THINK:
        return "high"
    if model_name == MODEL_ID_NO_THINK:
        return "off"
    return None


# ---------------------------------------------------------------------------
# Request / response models (OpenAI-compatible subset)
# ---------------------------------------------------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")  # capture unknown Open WebUI fields

    model: str = "aas-agent"
    messages: list[Message]
    stream: bool = False
    temperature: float | None = None
    max_tokens: int | None = None
    reasoning_effort: str | None = None  # "off" | "low" | "medium" | "high"
    chat_id: str | None = None           # Open WebUI conversation ID (non-standard)


def _last_user_content(messages: list[dict]) -> str:
    for msg in reversed(messages):
        if msg.get("role") == "user":
            return msg.get("content", "")
    return ""


def _is_utility_request(messages: list[dict]) -> bool:
    """Detect Open WebUI background tasks (title, tags, follow-up suggestions)."""
    return _last_user_content(messages).startswith("### Task:")


# ---------------------------------------------------------------------------
# Lifespan — startup / shutdown
# ---------------------------------------------------------------------------

_runner: AgentRunner | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _runner

    def _env_bool(name: str, default: bool) -> bool:
        raw = os.environ.get(name)
        if raw is None:
            return default
        return raw.lower() in ("1", "true", "yes", "on")

    mcp_url = os.environ.get("MCP_SERVER_URL", "http://localhost:8110/mcp/")
    llm_base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    llm_model = os.environ.get("LLM_MODEL", "gpt-4o")
    default_thinking = _env_bool("AGENT_DEFAULT_THINKING", False)
    inject_manual = _env_bool("AGENT_INJECT_MANUAL", True)
    inject_schema = _env_bool("AGENT_INJECT_SCHEMA", True)

    log_dir_env = os.environ.get("AGENT_LOG_DIR", "")
    log_dir = Path(log_dir_env) if log_dir_env else None
    if log_dir:
        log.info("Conversation logging enabled → %s", log_dir)

    # By default the prompt ships next to the source as `system-prompt.md`.
    # AGENT_SYSTEM_PROMPT_FILE overrides the path (e.g. for a bind-mounted
    # editable copy in docker-compose).
    default_prompt_file = Path(__file__).parent / "system-prompt.md"
    prompt_file = Path(os.environ.get("AGENT_SYSTEM_PROMPT_FILE") or default_prompt_file)
    system_prompt = prompt_file.read_text(encoding="utf-8")
    log.info("Loaded system prompt from %s (%d chars)", prompt_file, len(system_prompt))

    mcp = MCPClientManager(
        mcp_url,
        inject_manual=inject_manual,
        inject_schema=inject_schema,
    )
    log.info(
        "Auto-injected resources: manual=%s, schema=%s",
        inject_manual, inject_schema,
    )
    _runner = AgentRunner(
        mcp,
        llm_base_url,
        llm_model,
        system_prompt,
        default_thinking=default_thinking,
        log_dir=log_dir,
    )
    await _runner.initialize()

    yield

    await mcp.disconnect()
    _runner = None


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
                "id": MODEL_ID_NO_THINK,
                "object": "model",
                "created": 0,
                "owned_by": "aas-hybrid-mcp",
            },
            {
                "id": MODEL_ID_THINK,
                "object": "model",
                "created": 0,
                "owned_by": "aas-hybrid-mcp",
            },
        ],
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if _runner is None:
        return {"error": "Agent not initialized"}, 503

    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created = int(time.time())

    # Session ID handling — prioritize client-provided ID, fallback to header, then generate
    client_id = _extract_client_id(request)
    
    # Log all non-standard fields Open WebUI sends — helps discover the session ID field.
    extra = request.model_extra or {}
    if extra:
        log.info("Extra request fields from client: %s", extra)

    model = request.model or MODEL_ID_NO_THINK
    effort = _effort_for_model(model) or request.reasoning_effort

    # Utility calls (title gen, tags, follow-up suggestions) from Open WebUI:
    # bypass LangGraph, call LLM directly, skip logging.
    if _is_utility_request(messages):
        text = await _runner.direct_invoke(messages)
        return {
            "id": completion_id,
            "object": "chat.completion",
            "created": created,
            "model": model,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }

    if request.stream:
        return StreamingResponse(
            _stream_sse(completion_id, created, model, messages, effort, client_id, extra or None),
            media_type="text/event-stream",
        )

    text = await _runner.invoke(messages, reasoning_effort=effort, conversation_id=completion_id, chat_id=client_id, extra=extra or None)
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
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


def _extract_client_id(request: ChatCompletionRequest) -> str:
    """Extract client session ID from request.

    Priority order:
    1. ``chat_id`` from request body (Open WebUI non-standard field)
    2. ``client_id`` from extra fields (Open WebUI internal)
    3. Generate new UUID if nothing found
    """
    if request.chat_id:
        return request.chat_id
    if "client_id" in (request.model_extra or {}):
        return str(request.model_extra["client_id"])
    return f"client-{uuid.uuid4().hex[:12]}"


async def _stream_sse(
    completion_id: str,
    created: int,
    model: str,
    messages: list[dict],
    reasoning_effort: str | None,
    client_id: str,
    extra: dict | None = None,
):
    """Yield OpenAI-compatible SSE chunks.

    The try/finally ensures the terminating ``done_chunk`` and ``[DONE]``
    sentinel are always emitted - otherwise an exception inside the agent
    stream leaves the HTTP chunked transfer unfinished and clients see a
    ``TransferEncodingError``.
    """
    try:
        async for token in _runner.stream(messages, reasoning_effort=reasoning_effort, conversation_id=completion_id, chat_id=client_id, extra=extra):
            if not isinstance(token, str):
                token = str(token)
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
        yield "data: [DONE]\n\n"


# ---------------------------------------------------------------------------
# Entry point (for pyproject.toml console_scripts)
# ---------------------------------------------------------------------------

def main():
    uvicorn.run(app, host="0.0.0.0", port=8120)


if __name__ == "__main__":
    main()
