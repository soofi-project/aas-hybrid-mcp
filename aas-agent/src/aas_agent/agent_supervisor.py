"""Agent-supervisor agent variant — public runner with the same surface as AgentRunner.

Exposes ``initialize``, ``stream``, ``invoke``, ``direct_invoke``, and
``model_name`` so ``api.py`` can swap it in via the ``AGENT_VARIANT``
environment variable.

Architecture:
  START → supervisor_node → orchestrator_node → synthesize_node → END

The supervisor decomposes the user request into typed worker sub-tasks.
Each worker is a pre-compiled ReAct sub-graph with domain-specific tools.
The orchestrator runs all workers in parallel. The synthesizer combines results.
"""

import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, AsyncIterator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from aas_agent.http_client import _build_http_client
from aas_agent.mcp_client import MCPClientManager
from aas_agent.trace import ConversationLogger
from aas_agent.agent_supervisor_graph import build_supervisor_graph
from aas_agent.agent import _format_tool_end, _format_tool_start

log = logging.getLogger(__name__)


def _thinking_from_effort(
    reasoning_effort: str | None, default_thinking: bool
) -> bool:
    """Map OpenAI-style reasoning_effort to a boolean thinking-mode flag."""
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


class SupervisorAgentRunner:
    """Supervisor agent runner — drop-in replacement for AgentRunner."""

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

    @property
    def model_name(self) -> str:
        return self._llm_model

    async def _lazy_init(self, mcp_context: str, all_tools: list) -> None:
        """Build worker sub-graphs and supervisor graph using pre-loaded resources."""
        self._mcp_context = mcp_context
        tools = list(all_tools) + [get_current_utc_time]

        supervisor_llm = self._build_llm(enable_thinking=False, with_tools=False)
        worker_llm = self._build_llm(enable_thinking=False, with_tools=True)

        worker_subgraphs = {}
        from aas_agent.agent_supervisor_nodes import _WORKER_PROMPTS as _worker_prompts

        for worker_name in ("work_graph", "work_document", "work_template"):
            subgraph = self._build_worker_agent(worker_llm, tools, worker_name)
            worker_subgraphs[worker_name] = (subgraph, _worker_prompts[worker_name])

        log.info("Built worker sub-graphs for: %s", ", ".join(worker_subgraphs.keys()))

        self._graph_thinking_off = build_supervisor_graph(
            supervisor_llm=supervisor_llm,
            worker_subgraphs=worker_subgraphs,
            synthesize_llm=supervisor_llm,
            finalizer_prompt=None,
        )
        self._graph_thinking_on = self._graph_thinking_off

        log.info("Supervisor agent initialized — %d tools", len(tools))

    async def initialize(self) -> None:
        """Legacy: Connect MCP, load resources, build worker sub-graphs and supervisor graph."""
        await self._mcp.connect()
        mcp_context = await self._mcp.load_context()
        all_tools = await self._mcp.get_langchain_tools()
        return await self._lazy_init(mcp_context, all_tools)

    def _build_worker_agent(
        self,
        llm: ChatOpenAI,
        all_tools: list[BaseTool],
        worker_name: str,
    ) -> Any:
        """Build a compiled ReAct sub-graph for a worker."""
        from langchain_core.tools import BaseTool
        from aas_agent.agent_supervisor_nodes import _WORKER_PROMPTS as _worker_prompts, _WORKER_TOOLS as _worker_tools

        worker_tool_names = _worker_tools[worker_name]
        worker_tools = [t for t in all_tools if t.name in worker_tool_names]

        if not worker_tools:
            worker_tools = all_tools  # fallback

        system_prompt = _worker_prompts[worker_name]

        # Combine system-prompt.md + mcp_context for agent layer grounding
        base_context = self._mcp_context
        if self._system_prompt:
            base_context = f"{self._system_prompt}\n\n---\n\n{self._mcp_context}"
        system_prompt = f"{system_prompt}\n\n---\n\n{base_context}"

        return create_react_agent(model=llm, tools=worker_tools, prompt=SystemMessage(content=system_prompt))

    def _build_llm(
        self,
        enable_thinking: bool,
        with_tools: bool = True,
        streaming: bool = True,
    ) -> ChatOpenAI:
        """Construct a ChatOpenAI for supervisor/worker use."""
        model_kwargs: dict = {}
        if with_tools:
            model_kwargs["parallel_tool_calls"] = False

        if self._llm_base_url and "openai.com" not in self._llm_base_url:
            if not self._default_thinking:
                use_thinking = False
            else:
                use_thinking = enable_thinking
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
                continue  # graph's own prompts are authoritative
            elif role == "assistant":
                lc.append(AIMessage(content=content))
            else:
                lc.append(HumanMessage(content=content))
        return lc

    def _initial_state(self, messages: list) -> dict:
        return {
            "messages": messages,
            "plan": None,
            "task_queue": [],
            "worker_results": [],
            "supervisor_decision": None,
        }

    async def direct_invoke(self, messages: list[dict]) -> str:
        """Bypass the graph — Open WebUI title/tag generation."""
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
        """Stream tokens from supervisor, workers, and synthesized answer.

        When ``extra.get('verbose')`` is true, intermediate events are
        streamed as ``<antml:thinking>`` blocks.  Otherwise only the final
        synthesized answer is emitted.
        """
        graph = self._select_graph(reasoning_effort)
        if graph is None:
            raise RuntimeError("Supervisor agent not initialized")

        verbose = (extra or {}).get("verbose", False)
        lc = self._to_lc_messages(messages)
        initial_state = self._initial_state(lc)
        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)

        try:
            if verbose:
                async for token in _stream_supervisor_verbose(graph, initial_state, trace):
                    yield token
            else:
                result = await graph.ainvoke(initial_state)
                for msg in reversed(result.get("messages", [])):
                    if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
                        text = msg.content.strip()
                        yield text
                        trace.append(text)
                        break
        except Exception:
            log.exception("Fatal error in supervisor stream")
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
        """Non-streaming invocation — returns the synthesized answer."""
        graph = self._select_graph(reasoning_effort)
        if graph is None:
            raise RuntimeError("Supervisor agent not initialized")

        lc = self._to_lc_messages(messages)
        initial_state = self._initial_state(lc)
        result = await graph.ainvoke(initial_state)

        response = ""
        for msg in reversed(result.get("messages", [])):
            if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
                # Strip the metadata block (`````` section at end)
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


__all__ = ["SupervisorAgentRunner"]


async def _stream_supervisor_verbose(
    graph, initial_state: dict, trace
) -> AsyncIterator[str]:
    """Verbose stream for supervisor agent — events as antml:thinking blocks.

    Streams worker tasks, tool calls, and node summaries as collapsible reasoning
    sections, plus the final synthesized answer."""
    in_tool_block = False
    try:
        async for event in graph.astream_events(initial_state, version="v2"):
            try:
                kind = event.get("event")
                name = event.get("name", "")
                metadata = event.get("metadata") or {}
                node = metadata.get("langgraph_node", "")

                # Tool calls from workers
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

                # Worker LLM tokens (inside worker sub-graphs)
                if kind == "on_chat_model_stream" and node.startswith("work_"):
                    chunk = event.get("data", {}).get("chunk")
                    content = getattr(chunk, "content", None) if chunk else None
                    if isinstance(content, str) and content:
                        trace.append(content)
                        yield content
                    continue

                # Supervisor/orchestrator/synthesize node summaries
                if kind == "on_chain_end":
                    if name == "supervisor":
                        output = event.get("data", {}).get("output") or {}
                        plan = output.get("plan")
                        if plan is not None:
                            tasks = getattr(plan, "tasks", None) or []
                            task_summaries = [f"{t.worker}: {t.instruction[:80]}" if hasattr(t, "worker") else str(t) for t in tasks]
                            decision = "; ".join(task_summaries) if task_summaries else str(plan)
                            token = f"\n\n<think>\n**Supervisor decision**: {decision}\n</think>\n\n"
                            trace.append(token)
                            yield token
                        continue
                    if name == "orchestrator":
                        output = event.get("data", {}).get("output") or {}
                        results = output.get("worker_results", [])
                        if results:
                            lines = ["**Worker Results**"]
                            for r in results:
                                if isinstance(r, dict):
                                    lines.append(f"- {r.get('worker', '?')}: {str(r.get('finding', r.get('result', '')))[:200]}")
                                elif hasattr(r, "worker"):
                                    lines.append(f"- {r.worker}: {str(r.finding)[:200]}")
                                else:
                                    lines.append(f"- {str(r)[:200]}")
                            body = "\n".join(lines)
                            token = f"\n\n<think>\n{body}\n</think>\n\n"
                            trace.append(token)
                            yield token
                        continue
                    if name == "synthesize":
                        output = event.get("data", {}).get("output") or {}
                        msgs = output.get("messages", [])
                        for m in msgs:
                            if isinstance(m, AIMessage) and isinstance(getattr(m, "content", None), str):
                                text = m.content.strip()
                                if text:
                                    yield text
                                    trace.append(text)
                        continue
            except Exception:
                log.exception("Error handling supervisor stream event kind=%s", event.get("event"))
    except Exception:
        log.exception("Fatal error in supervisor verbose stream")
        err = "\n\n[stream error — see server logs]\n"
        yield err
        trace.append(err)
    finally:
        if in_tool_block:
            yield "\n</think>\n\n"
        trace.flush()

