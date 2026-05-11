"""CRAG agent variant — public runner with the same surface as AgentRunner.

Exposes ``initialize``, ``stream``, ``invoke``, ``direct_invoke``, and
``model_name`` so ``api.py`` can swap it in via the ``AGENT_VARIANT``
environment variable.

Pipeline: executor → relevance → (refine → executor) → synthesizer
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

from aas_agent.mcp_client import MCPClientManager
from aas_agent.trace import ConversationLogger
from aas_agent.crag_graph import build_crag_graph

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


class CragAgentRunner:
    """CRAG (Context Retrieval Augmented Generation) agent runner — drop-in replacement."""

    def __init__(
        self,
        mcp_client: MCPClientManager,
        llm_base_url: str,
        llm_model: str,
        system_prompt: str,
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

        # Budgets from env (defaults match plan_reflect)
        self._recursion_limit = os.environ.get("AGENT_RECURSION_LIMIT", "60")
        self._max_refinements = os.environ.get("CRAG_MAX_REFINEMENTS", "3")
        self._relevance_threshold = float(os.environ.get("CRAG_RELEVANCE_THRESHOLD", "0.7"))

    @property
    def model_name(self) -> str:
        return self._llm_model

    async def initialize(self) -> None:
        """Connect MCP, load resources, build CRAG graph."""
        await self._mcp.connect()

        mcp_context = await self._mcp.load_context()
        all_tools = await self._mcp.get_langchain_tools()
        all_tools.append(get_current_utc_time)

        # Build LLMs
        # Executor needs tools; structured LLMs (relevance/refine/synthesize) don't
        exec_llm = self._build_llm(enable_thinking=False, with_tools=True, streaming=True)
        structure_llm = self._build_llm(
            enable_thinking=False, with_tools=False, streaming=False
        )

        self._graph_thinking_off = build_crag_graph(
            exec_llm=exec_llm,
            tools=all_tools,
            base_system=mcp_context,
            relevance_llm=structure_llm,
            refine_llm=structure_llm,
            synthesize_llm=structure_llm,
            max_refinements=int(self._max_refinements),
            relevance_threshold=self._relevance_threshold,
        )

        # Build thinking variant
        if "openai.com" not in self._llm_base_url and self._default_thinking:
            exec_llm_think = self._build_llm(enable_thinking=True, with_tools=True, streaming=True)
            structure_llm_think = self._build_llm(
                enable_thinking=True, with_tools=False, streaming=False
            )
            self._graph_thinking_on = build_crag_graph(
                exec_llm=exec_llm_think,
                tools=all_tools,
                base_system=mcp_context,
                relevance_llm=structure_llm_think,
                refine_llm=structure_llm_think,
                synthesize_llm=structure_llm_think,
                max_refinements=int(self._max_refinements),
                relevance_threshold=self._relevance_threshold,
            )
        else:
            self._graph_thinking_on = self._graph_thinking_off

        log.info(
            "CRAG agent initialized — %d tools, threshold=%.1f, max_refinements=%s",
            len(all_tools), self._relevance_threshold, self._max_refinements,
        )

    def _build_llm(
        self,
        enable_thinking: bool,
        with_tools: bool = True,
        streaming: bool = True,
    ) -> ChatOpenAI:
        """Construct a ChatOpenAI for CRAG use."""
        model_kwargs: dict = {}
        if with_tools:
            model_kwargs["parallel_tool_calls"] = False

        if self._llm_base_url and "openai.com" not in self._llm_base_url:
            use_thinking = self._default_thinking and enable_thinking
            extra_body = {
                "chat_template_kwargs": {"enable_thinking": use_thinking}
            }
        else:
            use_thinking = enable_thinking
            extra_body = None

        return ChatOpenAI(
            base_url=self._llm_base_url,
            model=self._llm_model,
            streaming=streaming,
            model_kwargs=model_kwargs,
            extra_body=extra_body,
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
            "evidence": [],
            "retriever_steps": [],
            "refinement_count": 0,
            "max_refinements": int(self._max_refinements),
            "relevance_threshold": self._relevance_threshold,
            "last_relevance": None,
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
            raise RuntimeError("CRAG agent not initialized")

        lc = self._to_lc_messages(messages)
        initial_state = self._initial_state(lc)
        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)

        try:
            result = await graph.ainvoke(initial_state)
            for msg in reversed(result.get("messages", [])):
                if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
                    text = msg.content.strip()
                    yield text
                    trace.append(text)
                    break
        except Exception:
            log.exception("Fatal error in CRAG stream")
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
            raise RuntimeError("CRAG agent not initialized")

        lc = self._to_lc_messages(messages)
        initial_state = self._initial_state(lc)
        result = await graph.ainvoke(initial_state)

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


__all__ = ["CragAgentRunner"]
