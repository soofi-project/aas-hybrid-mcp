"""LangGraph ReAct agent — orchestrates MCP tools with schema-aware context."""

import json
import logging
from typing import AsyncIterator

_TOOL_OUTPUT_CHARS = 500
_TOOL_ARGS_CHARS = 800

from langchain_core.messages import AIMessageChunk, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from aas_agent.mcp_client import MCPClientManager

log = logging.getLogger(__name__)


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
        mcp_client: MCPClientManager,
        llm_base_url: str,
        llm_model: str,
        llm_api_key: str,
        system_prompt: str,
        default_thinking: bool = False,
    ) -> None:
        self._mcp = mcp_client
        self._llm_base_url = llm_base_url
        self._llm_model = llm_model
        self._llm_api_key = llm_api_key
        self._system_prompt = system_prompt
        self._default_thinking = default_thinking
        self._agent_thinking_off = None
        self._agent_thinking_on = None
        self._full_system_message: str = ""

    @property
    def model_name(self) -> str:
        return self._llm_model

    async def initialize(self) -> None:
        """Connect MCP, load resources, build both ReAct graphs."""
        await self._mcp.connect()

        mcp_context = await self._mcp.load_context()
        self._full_system_message = _build_system_message(
            self._system_prompt, mcp_context
        )
        log.info(
            "System message: %d chars (prompt=%d, context=%d)",
            len(self._full_system_message),
            len(self._system_prompt),
            len(mcp_context),
        )

        tools = await self._mcp.get_langchain_tools()

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

    def _build_llm(self, enable_thinking: bool) -> ChatOpenAI:
        """Construct the LLM with optional vLLM thinking support."""

        model_kwargs = {
            "parallel_tool_calls": False
        }

        # Only enable Qwen thinking when NOT using OpenAI
        if self._llm_base_url and "openai.com" not in self._llm_base_url:
            model_kwargs["extra_body"] = {
                "chat_template_kwargs": {
                    "enable_thinking": enable_thinking
                }
            }
        log.info("LLM backend: %s", self._llm_base_url)
        return ChatOpenAI(
            base_url=self._llm_base_url,
            model=self._llm_model,
            api_key=self._llm_api_key,
            streaming=True,
            model_kwargs=model_kwargs,
        )

    def _select_agent(self, reasoning_effort: str | None):
        thinking = _thinking_from_effort(reasoning_effort, self._default_thinking)
        return self._agent_thinking_on if thinking else self._agent_thinking_off

    def _to_langchain_messages(self, messages: list[dict]) -> list:
        """Convert OpenAI-format messages to LangChain message objects."""
        lc_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessageChunk(content=content))
            else:
                lc_messages.append(HumanMessage(content=content))
        return lc_messages

    async def stream(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
    ) -> AsyncIterator[str]:
        """Stream LLM token deltas from the agent.

        Tool invocations are wrapped in ``<think>...</think>`` blocks so
        clients like Open WebUI render them as collapsible reasoning
        sections alongside any native LLM thinking tokens.
        """
        agent = self._select_agent(reasoning_effort)
        if agent is None:
            raise RuntimeError("Agent not initialized")

        lc_messages = self._to_langchain_messages(messages)

        in_tool_block = False
        try:
            async for event in agent.astream_events(
                {"messages": lc_messages}, version="v2"
            ):
                try:
                    kind = event.get("event")
                    if kind == "on_chat_model_stream":
                        chunk = event.get("data", {}).get("chunk")
                        content = getattr(chunk, "content", None) if chunk else None
                        if isinstance(content, str) and content:
                            yield content
                    elif kind == "on_tool_start":
                        in_tool_block = True
                        yield _format_tool_start(event)
                    elif kind == "on_tool_end":
                        yield _format_tool_end(event)
                        in_tool_block = False
                except Exception:
                    # Never let a bad event kill the whole stream.
                    log.exception("Error handling stream event kind=%s", event.get("event"))
        except Exception:
            log.exception("Fatal error in astream_events loop")
            yield "\n\n[stream error — see server logs]\n"
        finally:
            if in_tool_block:
                yield "\n</think>\n\n"

    async def invoke(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
    ) -> str:
        """Non-streaming invocation — returns full response text."""
        agent = self._select_agent(reasoning_effort)
        if agent is None:
            raise RuntimeError("Agent not initialized")

        lc_messages = self._to_langchain_messages(messages)
        result = await agent.ainvoke({"messages": lc_messages})

        # Last AI message contains the response
        for msg in reversed(result.get("messages", [])):
            if hasattr(msg, "content") and msg.content:
                return msg.content
        return ""


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
