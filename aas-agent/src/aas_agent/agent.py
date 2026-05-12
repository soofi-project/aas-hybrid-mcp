"""LangGraph ReAct agent — orchestrates MCP tools with schema-aware context."""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncIterator

_TOOL_OUTPUT_CHARS = 3000
_TOOL_ARGS_CHARS = 800

from langchain_core.messages import AIMessageChunk, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from aas_agent.http_client import _build_http_client
from aas_agent.mcp_client import MCPClientManager
from aas_agent.trace import ConversationLogger

log = logging.getLogger(__name__)


@tool
def get_current_utc_time() -> str:
    """Return the current UTC time as an ISO-8601 string (seconds precision).

    Call this whenever you need to write a timestamp into an AAS field
    (incident logs, service request notifications, maintenance entries).
    Do not fabricate timestamps.
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _build_system_message(system_prompt: str, mcp_context: str) -> str:
    """Combine the base system prompt with auto-injected MCP resource context."""
    if not mcp_context:
        return system_prompt
    return f"{system_prompt}\n\n---\n\n{mcp_context}"


def _thinking_from_effort(
    reasoning_effort: str | None, default_thinking: bool
) -> bool:
    """Map OpenAI-style reasoning_effort to a boolean thinking-mode flag.

    ``"off"`` disables thinking; any of ``"low" | "medium" | "high"`` enables it.
    ``None`` falls back to the deployment default.
    """
    if reasoning_effort is None:
        return default_thinking
    return reasoning_effort.lower() != "off"


class AgentRunner:
    """Wraps a LangGraph ReAct agent with MCP tool/resource integration.

    Two ReAct graphs are pre-built — one with the underlying LLM in
    thinking mode, one without — so ``reasoning_effort`` on an incoming
    request can toggle between them without rebuilding the graph.
    """

    def __init__(
        self,
        mcp_client=None,
        llm_base_url: str = "",
        llm_model: str = "",
        system_prompt: str = "",
        default_thinking: bool = False,
        log_dir: Path | None = None,
    ) -> None:
        self._mcp = mcp_client
        self._llm_base_url = llm_base_url
        self._llm_model = llm_model
        self._system_prompt = system_prompt
        self._default_thinking = default_thinking
        self._log_dir = log_dir
        self._agent_thinking_off = None
        self._agent_thinking_on = None
        self._full_system_message: str = ""
        self._recursion_limit = int(os.environ.get("AGENT_RECURSION_LIMIT", "60"))

    @property
    def model_name(self) -> str:
        return self._llm_model

    async def _lazy_init(self, mcp_context: str, all_tools: list) -> None:
        """Build both ReAct graphs using pre-loaded shared resources.

        Called by api.py after the shared MCP client has connected and loaded
        context + tools. Avoids a redundant connect/load cycle per variant.
        """
        self._full_system_message = _build_system_message(
            self._system_prompt, mcp_context
        )
        log.info(
            "System message: %d chars (prompt=%d, context=%d)",
            len(self._full_system_message),
            len(self._system_prompt),
            len(mcp_context),
        )

        tools = list(all_tools) + [get_current_utc_time]

        self._agent_thinking_off = create_react_agent(
            model=self._build_llm(enable_thinking=False),
            tools=tools,
            prompt=self._full_system_message,
        )
        self._agent_thinking_on = create_react_agent(
            model=self._build_llm(enable_thinking=True),
            tools=tools,
            prompt=self._full_system_message,
        )
        log.info(
            "Agent initialized with %d tools (default_thinking=%s)",
            len(tools), self._default_thinking,
        )

    async def initialize(self) -> None:
        """Legacy: Connect MCP, load resources, build both ReAct graphs."""
        await self._mcp.connect()
        mcp_context = await self._mcp.load_context()
        all_tools = await self._mcp.get_langchain_tools()
        return await self._lazy_init(mcp_context, all_tools)

    def _build_llm(self, enable_thinking: bool, with_tools: bool = True, extra_body: dict | None = None) -> ChatOpenAI:
        """Construct the LLM with optional vLLM thinking support.

        For vLLM (Qwen) thinking is disabled by default because the chat
        template ignores system prompts when thinking is enabled, causing
        the model to fall back to generic greetings.

        ``with_tools=False`` omits ``parallel_tool_calls`` — OpenAI rejects
        that parameter when no tools are bound to the request.
        """
        model_kwargs: dict = {}

        if with_tools:
            model_kwargs["parallel_tool_calls"] = False

        if self._llm_base_url and "openai.com" not in self._llm_base_url:
            # vLLM: respect _default_thinking from AGENT_DEFAULT_THINKING env var.
            # When False, force thinking off regardless of enable_thinking.
            if not self._default_thinking:
                use_thinking = False
            else:
                use_thinking = enable_thinking
            log.info(
                "LLM backend: %s (vLLM, thinking=%s [default_thinking=%s])",
                self._llm_base_url, use_thinking, self._default_thinking,
            )
        else:
            use_thinking = enable_thinking
            log.info(
                "LLM backend: %s (OpenAI-compatible, thinking=%s)",
                self._llm_base_url, enable_thinking,
            )

        if self._llm_base_url and "openai.com" not in self._llm_base_url:
            extra_body = {
                "chat_template_kwargs": {"enable_thinking": use_thinking}
            }
            llm_kwargs = {"http_client": _build_http_client()}
        else:
            extra_body = None
            llm_kwargs = {}
        # api_key intentionally omitted — ChatOpenAI reads OPENAI_API_KEY from
        # the container env (loaded via ${SECRETS_PATH} in default mode, or
        # set to "dummy" via .env.vllm in vLLM mode).
        return ChatOpenAI(
            base_url=self._llm_base_url,
            model=self._llm_model,
            streaming=True,
            model_kwargs=model_kwargs,
            extra_body=extra_body,
            **llm_kwargs,
        )

    def _select_agent(self, reasoning_effort: str | None):
        thinking = _thinking_from_effort(reasoning_effort, self._default_thinking)
        return self._agent_thinking_on if thinking else self._agent_thinking_off

    def _to_langchain_messages(self, messages: list[dict]) -> list:
        """Convert OpenAI-format messages to LangChain message objects.

        System messages from the incoming list are intentionally skipped —
        ``create_react_agent`` injects its own system prompt via the ``prompt``
        argument, and a second system message can cause models (especially
        Qwen/vLLM) to ignore the graph's system prompt entirely.
        """
        lc_messages: list = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                continue  # graph's prompt is authoritative, skip incoming system msgs
            if role == "assistant":
                lc_messages.append(AIMessageChunk(content=content))
            else:
                lc_messages.append(HumanMessage(content=content))
        return lc_messages

    async def stream(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
        conversation_id: str = "",
        chat_id: str | None = None,
        extra: dict | None = None,
    ) -> AsyncIterator[str]:
        """Stream LLM token deltas from the agent.

        When ``extra.get('verbose')`` is true, tool invocations are wrapped
        in ``<antml:thinking>`` blocks so clients like Open WebUI render them
        as collapsible reasoning sections.  Otherwise only LLM token deltas
        are emitted.
        """
        agent = self._select_agent(reasoning_effort)
        if agent is None:
            raise RuntimeError("Agent not initialized")

        verbose = (extra or {}).get("verbose", False)
        lc_messages = self._to_langchain_messages(messages)
        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)

        in_tool_block = False
        try:
            async for event in agent.astream_events(
                {"messages": lc_messages},
                config={"recursion_limit": self._recursion_limit},
                version="v2",
            ):
                try:
                    kind = event.get("event")
                    if kind == "on_chat_model_stream":
                        chunk = event.get("data", {}).get("chunk")
                        content = getattr(chunk, "content", None) if chunk else None
                        if isinstance(content, str) and content:
                            trace.append(content)
                            yield content
                    elif verbose and kind == "on_tool_start":
                        in_tool_block = True
                        token = _format_tool_start(event)
                        trace.append(token, strip_leading_newlines=True)
                        yield token
                    elif verbose and kind == "on_tool_end":
                        token = _format_tool_end(event)
                        trace.append(token)
                        yield token
                        in_tool_block = False
                except Exception:
                    log.exception("Error handling stream event kind=%s", event.get("event"))
        except Exception:
            log.exception("Fatal error in astream_events loop")
            err = "\n\n[stream error — see server logs]\n"
            trace.append(err)
            yield err
        finally:
            if in_tool_block:
                yield "\n</think>\n\n"
            trace.flush()

    async def invoke(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
        conversation_id: str = "",
        chat_id: str | None = None,
        extra: dict | None = None,
    ) -> str:
        """Non-streaming invocation — returns full response text."""
        agent = self._select_agent(reasoning_effort)
        if agent is None:
            raise RuntimeError("Agent not initialized")

        lc_messages = self._to_langchain_messages(messages)
        result = await agent.ainvoke(
            {"messages": lc_messages},
            config={"recursion_limit": self._recursion_limit},
        )

        response = ""
        for msg in reversed(result.get("messages", [])):
            if hasattr(msg, "content") and msg.content:
                response = msg.content
                break

        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)
        trace.append(response)
        trace.flush()
        return response


def _format_tool_start(event: dict) -> str:
    """Render an ``on_tool_start`` event as the opening of a <think> block."""
    name = event.get("name", "tool")
    raw_input = event.get("data", {}).get("input", {})
    # LangGraph wraps the real args under an "input" key on some versions
    if isinstance(raw_input, dict) and set(raw_input.keys()) == {"input"}:
        raw_input = raw_input["input"]
    try:
        args_str = json.dumps(raw_input, ensure_ascii=False, indent=2)
    except (TypeError, ValueError):
        args_str = str(raw_input)
    if len(args_str) > _TOOL_ARGS_CHARS:
        args_str = args_str[:_TOOL_ARGS_CHARS] + "\n... [truncated]"
    return f"\n\n<think>\n**Tool** `{name}`\n\n```json\n{args_str}\n```\n\n"


def _format_tool_end(event: dict) -> str:
    """Render an ``on_tool_end`` event as the closing of a <think> block."""
    output = event.get("data", {}).get("output")
    text = getattr(output, "content", None) if output is not None else None
    if text is None:
        text = str(output) if output is not None else "(empty)"
    if len(text) > _TOOL_OUTPUT_CHARS:
        text = text[:_TOOL_OUTPUT_CHARS] + "\n... [truncated]"
    return f"**Result**\n\n```\n{text}\n```\n</think>\n\n"
