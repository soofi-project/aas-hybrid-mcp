"""ReWOO agent variant — public runner with the same surface as AgentRunner.

Exposes ``initialize``, ``stream``, ``invoke``, ``direct_invoke``, and
``model_name`` so ``api.py`` can swap it in via the ``AGENT_VARIANT``
environment variable.

Pipeline (linear): START → plan_node → execute_node → synthesize_node → END

The plan_node produces ALL tool calls upfront. The execute_node runs them
in parallel via asyncio.gather. The synthesize_node combines observations.
"""

import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, AsyncIterator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from aas_agent.http_client import _build_http_client
from aas_agent.mcp_client import MCPClientManager
from aas_agent.trace import ConversationLogger
from aas_agent.agent import _format_tool_end, _format_tool_start
from aas_agent.rewoo_graph import build_rewoo_graph
from aas_agent.rewoo_state import RewooState

log = logging.getLogger(__name__)


def _thinking_from_effort(
    reasoning_effort: str | None, default_thinking: bool
) -> bool:
    if reasoning_effort is None:
        return default_thinking
    return reasoning_effort.lower() != "off"


@tool
def get_current_utc_time() -> str:
    """Return the current UTC time as an ISO-8601 string (seconds precision).

    Call this whenever you need to write a timestamp into an AAS field
    (incident logs, service request notifications, maintenance entries).
    Do not fabricate timestamps.
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class RewooAgentRunner:
    """ReWOO (Reasoning Without Observation) agent runner — drop-in replacement."""

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
        self._graph_thinking_off = None
        self._graph_thinking_on = None
        self._mcp_context = ""

        import os
        self._recursion_limit = int(os.environ.get("AGENT_RECURSION_LIMIT", "60"))
        self._max_thoughts = int(os.environ.get("REWOO_MAX_THOUGHTS", "10"))
        self._parallel_batch_size = int(os.environ.get("REWOO_PARALLEL_BATCH", "5"))

    @property
    def model_name(self) -> str:
        return self._llm_model

    async def _lazy_init(self, mcp_context: str, all_tools: list) -> None:
        """Build ReWOO graph using pre-loaded shared resources."""
        self._mcp_context = mcp_context
        base_system = mcp_context
        if self._system_prompt:
            base_system = f"{self._system_prompt}\n\n---\n\n{mcp_context}"
        tools = list(all_tools) + [get_current_utc_time]

        plan_llm = self._build_llm(enable_thinking=False, with_tools=False, streaming=False)
        synthesize_llm = self._build_llm(enable_thinking=False, with_tools=False, streaming=False)
        tool_map = {t.name: t for t in tools}

        self._graph_thinking_off = build_rewoo_graph(
            plan_llm=plan_llm,
            synthesize_llm=synthesize_llm,
            tool_map=tool_map,
            base_system=base_system,
            max_thoughts=self._max_thoughts,
            parallel_batch_size=self._parallel_batch_size,
        )
        self._graph_thinking_on = self._graph_thinking_off

        log.info(
            "ReWOO agent initialized — %d tools, max_thoughts=%d, batch=%d",
            len(tools), self._max_thoughts, self._parallel_batch_size,
        )

    async def initialize(self) -> None:
        """Legacy: Connect MCP, load resources, build ReWOO graph."""
        await self._mcp.connect()
        mcp_context = await self._mcp.load_context()
        all_tools = await self._mcp.get_langchain_tools()
        return await self._lazy_init(mcp_context, all_tools)

    def _build_llm(
        self,
        enable_thinking: bool,
        with_tools: bool = True,
        streaming: bool = True,
    ) -> ChatOpenAI:
        """Construct a ChatOpenAI for ReWOO use."""
        model_kwargs: dict = {}
        if with_tools:
            model_kwargs["parallel_tool_calls"] = False

        if self._llm_base_url and "openai.com" not in self._llm_base_url:
            use_thinking = self._default_thinking and enable_thinking
            extra_body = {"chat_template_kwargs": {"enable_thinking": use_thinking}}
            llm_kwargs = {"http_client": _build_http_client()}
        else:
            use_thinking = enable_thinking
            extra_body = None
            llm_kwargs = {}

        return ChatOpenAI(
            base_url=self._llm_base_url,
            model=self._llm_model,
            streaming=streaming,
            model_kwargs=model_kwargs,
            extra_body=extra_body,
            **llm_kwargs,
        )

    def _select_graph(self, reasoning_effort: str | None) -> Any:
        thinking = _thinking_from_effort(reasoning_effort, self._default_thinking)
        return self._graph_thinking_on if thinking else self._graph_thinking_off

    def _to_lc_messages(self, messages: list[dict]) -> list:
        lc: list = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                continue
            elif role == "assistant":
                lc.append(AIMessage(content=content))
            else:
                lc.append(HumanMessage(content=content))
        return lc

    def _initial_state(self, messages: list) -> dict:
        return {
            "messages": messages,
            "plan": None,
            "observations": {},
        }

    async def direct_invoke(self, messages: list[dict]) -> str:
        """Bypass the graph."""
        llm = self._build_llm(enable_thinking=False, with_tools=False)
        lc = self._to_lc_messages(messages)
        result = await llm.ainvoke(lc)
        return result.content if isinstance(result.content, str) else str(result.content)

    async def stream(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
        conversation_id: str = "",
        chat_id: str | None = None,
        extra: dict | None = None,
    ) -> AsyncIterator[str]:
        """Stream the synthesized answer."""
        graph = self._select_graph(reasoning_effort)
        if graph is None:
            raise RuntimeError("ReWOO agent not initialized")

        lc = self._to_lc_messages(messages)
        initial_state = self._initial_state(lc)
        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)

        try:
            if (extra or {}).get("verbose", False):
                config = {"recursion_limit": int(self._recursion_limit)}
                async for token in _stream_rewoo_verbose(graph, initial_state, config, trace):
                    yield token
            else:
                config = {"recursion_limit": int(self._recursion_limit)}
                result = await graph.ainvoke(initial_state, config=config)
                for msg in reversed(result.get("messages", [])):
                    if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
                        text = msg.content.strip()
                        yield text
                        trace.append(text)
                        break
        except Exception:
            log.exception("Fatal error in ReWOO stream")
            err = "\n\n[stream error — see server logs]\n"
            yield err
            trace.append(err)
        finally:
            trace.flush()

    async def invoke(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
        conversation_id: str = "",
        chat_id: str | None = None,
        extra: dict | None = None,
    ) -> str:
        """Non-streaming invocation."""
        graph = self._select_graph(reasoning_effort)
        if graph is None:
            raise RuntimeError("ReWOO agent not initialized")

        lc = self._to_lc_messages(messages)
        initial_state = self._initial_state(lc)
        config = {"recursion_limit": int(self._recursion_limit)}
        result = await graph.ainvoke(initial_state, config=config)

        response = ""
        for msg in reversed(result.get("messages", [])):
            if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
                text = msg.content.strip()
                meta_match = re.search(r'\n<thinking_process>.*$', text, re.DOTALL)
                if meta_match:
                    text = text[:meta_match.start()].strip()
                response = text
                break

        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)
        trace.append(response)
        trace.flush()
        return response


__all__ = ["RewooAgentRunner"]


async def _stream_rewoo_verbose(
    graph, initial_state: dict, config: dict, trace
) -> AsyncIterator[str]:
    """Verbose stream for ReWOO — events as antml:thinking blocks."""
    in_tool_block = False
    try:
        async for event in graph.astream_events(initial_state, config=config, version="v2"):
            try:
                kind = event.get("event")
                name = event.get("name", "")
                metadata = event.get("metadata") or {}
                node = metadata.get("langgraph_node", "")

                if kind == "on_tool_start":
                    in_tool_block = True
                    token = _format_tool_start(event)
                    trace.append(token, strip_leading_newlines=True)
                    yield token
                    continue
                if kind == "on_tool_end":
                    token = _format_tool_end(event)
                    trace.append(token)
                    yield token
                    in_tool_block = False
                    continue

                if kind == "on_chain_end":
                    if name in ("plan", "execute", "synthesize"):
                        output = event.get("data", {}).get("output") or {}
                        if name == "plan" and "plan" in output:
                            p = output["plan"]
                            if hasattr(p, "thoughts"):
                                lines = ["**Plan**"]
                                for t in p.thoughts:
                                    plan_text = getattr(t, "plan", "")[:100]
                                    tool_name = getattr(t, "tool_name", "?")
                                    ref_id = getattr(t, "ref_id", "?")
                                    lines.append(f"- _{plan_text}_ → `{tool_name}` → `{ref_id}`")
                                if hasattr(p, "synthesis_hint") and p.synthesis_hint:
                                    lines.append(f"_Hint: {p.synthesis_hint[:200]}_")
                                body = "\n".join(lines)
                                token = f"\n\n<think>\n{body}\n</think>\n\n"
                                trace.append(token)
                                yield token
                        elif name == "synthesize":
                            msgs = output.get("messages", [])
                            for m in msgs:
                                if isinstance(m, AIMessage) and isinstance(getattr(m, "content", None), str):
                                    text = m.content.strip()
                                    if text:
                                        yield text
                                        trace.append(text)
            except Exception:
                log.exception("Error handling ReWOO stream event kind=%s", event.get("event"))
    except Exception:
        log.exception("Fatal error in ReWOO verbose stream")
        err = "\n\n[stream error — see server logs]\n"
        yield err
        trace.append(err)
    finally:
        if in_tool_block:
            yield "\n</think>\n\n"
        trace.flush()
