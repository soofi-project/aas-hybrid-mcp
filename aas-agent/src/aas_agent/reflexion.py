"""Reflexion agent variant — public runner with the same surface as AgentRunner.

Exposes ``initialize``, ``stream``, ``invoke``, and ``model_name`` so
``api.py`` can swap it in via the ``aas-agent:reflexion`` model ID.

Pipeline: executor → judge → (reflect → executor) → finalizer
"""

import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, AsyncIterator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from aas_agent.http_client import _build_http_client
from aas_agent.mcp_client import MCPClientManager
from aas_agent.reflexion_graph import build_reflexion_graph
from aas_agent.reflexion_state import TrialRecord
from aas_agent.trace import ConversationLogger
from aas_agent.agent import _format_tool_end, _format_tool_start
from aas_agent.usage import (
    accumulate_from_event,
    accumulate_from_messages,
    empty_usage,
    encode_usage_sentinel,
)
from aas_agent.verbose_stream_utils import node_transition_block

# Top-level langgraph nodes whose entry is rendered as a <think> block
# when streaming verbose. Matches the routing in ``reflexion_graph.py``.
_REFLEXION_NODES = frozenset({"executor", "judge", "reflect", "finalizer"})

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


class ReflexionAgentRunner:
    """Reflexion (Shinn et al. 2023) agent runner — drop-in replacement."""

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

        self._recursion_limit = os.environ.get("AGENT_RECURSION_LIMIT", "60")
        self._max_trials = os.environ.get("REFLEXION_MAX_TRIALS", "3")
        self._accept_threshold = float(os.environ.get("REFLEXION_ACCEPT_THRESHOLD", "0.7"))

    @property
    def model_name(self) -> str:
        return self._llm_model

    async def _lazy_init(self, mcp_context: str, all_tools: list) -> None:
        """Build Reflexion graph using pre-loaded shared resources."""
        tools = list(all_tools) + [get_current_utc_time]

        exec_llm = self._build_llm(enable_thinking=False, with_tools=True, streaming=True)
        structure_llm = self._build_llm(
            enable_thinking=False, with_tools=False, streaming=False
        )

        base_system = mcp_context
        if self._system_prompt:
            base_system = f"{self._system_prompt}\n\n---\n\n{mcp_context}"

        self._graph_thinking_off = build_reflexion_graph(
            exec_llm=exec_llm,
            tools=tools,
            base_system=base_system,
            judge_llm=structure_llm,
            reflect_llm=structure_llm,
            finalizer_llm=structure_llm,
            max_trials=int(self._max_trials),
            accept_threshold=self._accept_threshold,
        )
        self._graph_thinking_on = self._graph_thinking_off

        log.info(
            "Reflexion agent initialized — %d tools, threshold=%.1f, max_trials=%s",
            len(tools), self._accept_threshold, self._max_trials,
        )

    async def initialize(self) -> None:
        """Legacy: Connect MCP, load resources, build Reflexion graph."""
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
        model_kwargs: dict = {}
        if with_tools:
            model_kwargs["parallel_tool_calls"] = False

        if self._llm_base_url and "openai.com" not in self._llm_base_url:
            use_thinking = self._default_thinking and enable_thinking
            extra_body = {
                "chat_template_kwargs": {"enable_thinking": use_thinking}
            }
            llm_kwargs = {"http_client": _build_http_client()}
        else:
            use_thinking = enable_thinking
            extra_body = None
            llm_kwargs = {}

        return ChatOpenAI(
            base_url=self._llm_base_url,
            model=self._llm_model,
            streaming=streaming,
            stream_usage=True,
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
            "judgment": None,
            "reflection": None,
            "feedback_history": [],
            "trial_records": [],
            "current_trial": 1,
            "max_trials": int(self._max_trials),
            "accept_threshold": self._accept_threshold,
        }

    async def stream(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
        conversation_id: str = "",
        chat_id: str | None = None,
        extra: dict | None = None,
    ) -> AsyncIterator[str]:
        graph = self._select_graph(reasoning_effort)
        if graph is None:
            raise RuntimeError("Reflexion agent not initialized")

        lc = self._to_lc_messages(messages)
        initial_state = self._initial_state(lc)
        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)
        usage = empty_usage()

        try:
            if (extra or {}).get("verbose", False):
                config = {"recursion_limit": int(self._recursion_limit)}
                async for token in _stream_reflexion_verbose(graph, initial_state, config, trace, usage):
                    yield token
            else:
                config = {"recursion_limit": int(self._recursion_limit)}
                result = await graph.ainvoke(initial_state, config=config)
                accumulate_from_messages(result.get("messages", []), usage)
                for msg in reversed(result.get("messages", [])):
                    if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
                        text = msg.content.strip()
                        yield text
                        trace.append(text)
                        break
        except Exception:
            log.exception("Fatal error in Reflexion stream")
            err = "\n\n[stream error — see server logs]\n"
            yield err
            trace.append(err)
        finally:
            trace.set_usage(usage)
            yield encode_usage_sentinel(usage)
            trace.flush()

    async def invoke(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
        conversation_id: str = "",
        chat_id: str | None = None,
        extra: dict | None = None,
    ) -> tuple[str, dict]:
        """Non-streaming invocation — returns ``(response_text, usage)``."""
        graph = self._select_graph(reasoning_effort)
        if graph is None:
            raise RuntimeError("Reflexion agent not initialized")

        lc = self._to_lc_messages(messages)
        initial_state = self._initial_state(lc)
        config = {"recursion_limit": int(self._recursion_limit)}
        result = await graph.ainvoke(initial_state, config=config)

        usage = empty_usage()
        accumulate_from_messages(result.get("messages", []), usage)

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
        trace.set_usage(usage)
        trace.flush()
        return response, usage


__all__ = ["ReflexionAgentRunner"]


async def _stream_reflexion_verbose(
    graph, initial_state: dict, config: dict, trace, usage: dict
) -> AsyncIterator[str]:
    """Verbose stream for Reflexion — events as antml:thinking blocks."""
    in_tool_block = False
    try:
        async for event in graph.astream_events(initial_state, config=config, version="v2"):
            try:
                if accumulate_from_event(event, usage):
                    continue

                nt = node_transition_block(event, _REFLEXION_NODES)
                if nt:
                    trace.append(nt, strip_leading_newlines=True)
                    yield nt
                    continue

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

                if kind == "on_chat_model_stream" and node == "executor":
                    chunk = event.get("data", {}).get("chunk")
                    content = getattr(chunk, "content", None) if chunk else None
                    if isinstance(content, str) and content:
                        trace.append(content)
                        yield content
                    continue

                if kind == "on_chain_end":
                    if name in ("judge", "reflect", "finalizer"):
                        output = event.get("data", {}).get("output") or {}
                        if name == "judge" and "judgment" in output:
                            j = output["judgment"]
                            score = getattr(j, "score", "?")
                            verdict = getattr(j, "verdict", "?")
                            reason = getattr(j, "reason", "")[:200]
                            token = f"\n\n<think>\n**Judge**: score={score}, verdict={verdict}\n_reason: {reason}_\n</think>\n\n"
                            trace.append(token)
                            yield token
                        elif name == "reflect" and "reflection" in output:
                            r = output["reflection"]
                            hint = getattr(r, "strategy_hint", "")[:200]
                            token = f"\n\n<think>\n**Reflect**: {hint}\n</think>\n\n"
                            trace.append(token)
                            yield token
                        elif name == "finalizer":
                            msgs = output.get("messages", [])
                            for m in msgs:
                                if isinstance(m, AIMessage) and isinstance(getattr(m, "content", None), str):
                                    text = m.content.strip()
                                    if text:
                                        yield text
                                        trace.append(text)
            except Exception:
                log.exception("Error handling Reflexion stream event kind=%s", event.get("event"))
    except Exception:
        log.exception("Fatal error in Reflexion verbose stream")
        err = "\n\n[stream error — see server logs]\n"
        yield err
        trace.append(err)
    finally:
        if in_tool_block:
            yield "\n</think>\n\n"
        # Outer stream() flushes — extra flush here would emit a _2.md duplicate.
