"""Plan/reflect agent variant — public runner with the same surface as AgentRunner.

Exposes ``initialize``, ``stream``, ``invoke``, ``direct_invoke``, and
``model_name`` so ``api.py`` can swap it in via the ``AGENT_VARIANT``
environment variable.

Streaming notes
---------------
The planner, reflector, and finalizer do plain LLM ``ainvoke`` calls
(plain text, no ``with_structured_output``) and parse JSON ourselves
via ``QwenOutputParser``. Their output is rendered as a foldable
``<think>`` block (or, for the finalizer, the final answer text) once
the node ends. The executor sub-loop's tool calls and any free-form
assistant tokens it emits are streamed live, so the user sees activity
throughout most of a turn. Total blocking time is roughly the sum of one
structured planner call, one reflector call per step, and one finalizer
call — usually 2–3 seconds extra over the prebuilt react agent.
"""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncIterator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from aas_agent.agent import _format_tool_end, _format_tool_start, _thinking_from_effort
from aas_agent.agent_plan_graph import build_plan_reflect_graph
from aas_agent.agent_plan_state import Plan, Reflection
from aas_agent.mcp_client import MCPClientManager
from aas_agent.trace import ConversationLogger

log = logging.getLogger(__name__)


_PROMPT_DIR = Path(__file__).parent / "agent_plan_prompts"


@tool
def get_current_utc_time() -> str:
    """Return the current UTC time as an ISO-8601 string (seconds precision).

    Call this whenever you need to write a timestamp into an AAS field
    (incident logs, service request notifications, maintenance entries).
    Do not fabricate timestamps.
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_prompt(name: str) -> str:
    return (_PROMPT_DIR / f"{name}.md").read_text(encoding="utf-8")


def _format_plan_block(plan: Plan) -> str:
    """Render a Plan object as a foldable <think> block."""
    lines = [
        "**Plan**",
        f"_Goal:_ {plan.goal}",
        "",
    ]
    for step in plan.steps:
        suggestion = f" _(suggested: `{step.suggested_tool}`)_" if step.suggested_tool else ""
        lines.append(f"**Step {step.id}** — {step.intent}{suggestion}")
        lines.append(f"  - success: {step.success_criteria}")
    if plan.fallback_notes:
        lines.append("")
        lines.append(f"_Fallback:_ {plan.fallback_notes}")
    body = "\n".join(lines)
    return f"\n\n<think>\n{body}\n</think>\n\n"


def _format_reflection_block(refl: Reflection) -> str:
    """Render a Reflection object as a foldable <think> block."""
    lines = [
        f"**Reflection** — decision: `{refl.decision}`",
        f"_Reasoning:_ {refl.reasoning}",
    ]
    if refl.evidence_collected:
        lines.append("_Evidence:_")
        for fact in refl.evidence_collected:
            lines.append(f"- {fact}")
    if refl.next_action_hint:
        lines.append(f"_Hint:_ {refl.next_action_hint}")
    body = "\n".join(lines)
    return f"\n\n<think>\n{body}\n</think>\n\n"


class PlanReflectAgentRunner:
    """Plan/reflect agent runner — drop-in replacement for ``AgentRunner``."""

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
        self._legacy_system_prompt = system_prompt
        self._default_thinking = default_thinking
        self._log_dir = log_dir
        self._graph_thinking_off = None
        self._graph_thinking_on = None
        self._base_system: str = ""

        self._recursion_limit = int(os.environ.get("AGENT_RECURSION_LIMIT", "60"))
        self._max_step_attempts = int(os.environ.get("AGENT_MAX_STEP_ATTEMPTS", "3"))
        self._max_replans = int(os.environ.get("AGENT_MAX_REPLANS", "2"))
        self._max_total_tool_calls = int(
            os.environ.get("AGENT_MAX_TOTAL_TOOL_CALLS", "30")
        )
        self._sub_recursion_limit = int(
            os.environ.get("AGENT_SUBLOOP_RECURSION_LIMIT", "8")
        )

    @property
    def model_name(self) -> str:
        return self._llm_model

    async def _lazy_init(self, mcp_context: str, all_tools: list) -> None:
        """Build both graphs using pre-loaded shared resources."""
        self._base_system = mcp_context
        log.info(
            "Plan/reflect base system context: %d chars (manual + schema)",
            len(self._base_system),
        )

        tools = list(all_tools) + [get_current_utc_time]

        planner_prompt = _read_prompt("planner")
        executor_prompt = _read_prompt("executor")
        reflector_prompt = _read_prompt("reflector")
        finalizer_prompt = _read_prompt("finalizer")

        common_kwargs = dict(
            tools=tools,
            base_system=self._base_system,
            planner_prompt=planner_prompt,
            executor_prompt=executor_prompt,
            reflector_prompt=reflector_prompt,
            finalizer_prompt=finalizer_prompt,
            max_step_attempts=self._max_step_attempts,
            max_replans=self._max_replans,
            max_total_tool_calls=self._max_total_tool_calls,
            sub_recursion_limit=self._sub_recursion_limit,
        )

        self._graph_thinking_off = build_plan_reflect_graph(
            executor_llm=self._build_llm(enable_thinking=False, with_tools=True),
            structured_llm=self._build_llm(
                enable_thinking=False, with_tools=False, streaming=False
            ),
            **common_kwargs,
        )
        self._graph_thinking_on = build_plan_reflect_graph(
            executor_llm=self._build_llm(enable_thinking=True, with_tools=True),
            structured_llm=self._build_llm(
                enable_thinking=True, with_tools=False, streaming=False
            ),
            **common_kwargs,
        )
        log.info(
            "Plan/reflect agent initialized — %d tools, budgets: "
            "recursion=%d, step_attempts=%d, replans=%d, tool_calls=%d, sub=%d",
            len(tools),
            self._recursion_limit,
            self._max_step_attempts,
            self._max_replans,
            self._max_total_tool_calls,
            self._sub_recursion_limit,
        )

    async def initialize(self) -> None:
        """Legacy: Connect MCP, load resources, build both graphs."""
        await self._mcp.connect()
        mcp_context = await self._mcp.load_context()
        all_tools = await self._mcp.get_langchain_tools()
        return await self._lazy_init(mcp_context, all_tools)

    def _build_llm(
        self,
        enable_thinking: bool,
        with_tools: bool = True,
        streaming: bool = True,
        extra_body: dict | None = None,
    ) -> ChatOpenAI:
        """Construct a ChatOpenAI bound for vLLM thinking when applicable.

        For vLLM (Qwen) thinking is disabled by default because the chat
        template ignores system prompts when thinking is enabled, causing
        the model to fall back to generic greetings.

        ``streaming=False`` is used for the structured-output LLM: we do
        synchronous JSON parsing on the *full* response text, so streaming
        would produce partial content that cannot be parsed.
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
            extra_body = {
                "chat_template_kwargs": {"enable_thinking": use_thinking}
            }
        else:
            use_thinking = enable_thinking
            extra_body = extra_body  # use caller-provided or None

        return ChatOpenAI(
            base_url=self._llm_base_url,
            model=self._llm_model,
            streaming=streaming,
            model_kwargs=model_kwargs,
            extra_body=extra_body,
        )

    def _select_graph(self, reasoning_effort: str | None):
        thinking = _thinking_from_effort(reasoning_effort, self._default_thinking)
        return self._graph_thinking_on if thinking else self._graph_thinking_off

    def _to_langchain_messages(self, messages: list[dict]) -> list:
        lc: list = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                lc.append(SystemMessage(content=content))
            elif role == "assistant":
                lc.append(AIMessage(content=content))
            else:
                lc.append(HumanMessage(content=content))
        return lc

    def _initial_state(self, messages: list) -> dict:
        return {
            "messages": messages,
            "plan": None,
            "current_step_idx": 0,
            "step_attempts": 0,
            "total_tool_calls": 0,
            "replan_count": 0,
            "evidence": [],
            "last_reflection": None,
        }

    async def direct_invoke(self, messages: list[dict]) -> str:
        """Bypass the graph — Open WebUI title/tag generation lands here."""
        llm = self._build_llm(enable_thinking=False, with_tools=False)
        lc = self._to_langchain_messages(messages)
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
        """Stream tokens, tool events, plan, reflection, and final answer."""
        graph = self._select_graph(reasoning_effort)
        if graph is None:
            raise RuntimeError("Plan/reflect agent not initialized")

        lc = self._to_langchain_messages(messages)
        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)

        config = {"recursion_limit": self._recursion_limit}
        in_tool_block = False

        try:
            async for event in graph.astream_events(
                self._initial_state(lc), config=config, version="v2"
            ):
                try:
                    kind = event.get("event")
                    name = event.get("name", "")
                    metadata = event.get("metadata") or {}
                    node = metadata.get("langgraph_node", "")

                    # Tool calls happen only inside the executor's nested
                    # ReAct sub-agent. The metadata's ``langgraph_node`` for
                    # those events points at the *sub-agent's* node ("agent"
                    # / "tools"), not "execute_step". Forward unconditionally
                    # — no other node binds tools.
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

                    # Free-form chat-model tokens. planner/reflector/finalizer
                    # don't stream (they do synchronous JSON parse after
                    # ``ainvoke``), so skip them and only stream the executor's
                    # real-time tokens. Anything else (executor, nested
                    # sub-agent) is the user-visible model thinking.
                    if kind == "on_chat_model_stream" and node not in (
                        "planner", "reflector", "finalizer"
                    ):
                        chunk = event.get("data", {}).get("chunk")
                        content = getattr(chunk, "content", None) if chunk else None
                        if isinstance(content, str) and content:
                            trace.append(content)
                            yield content
                        continue

                    # Node-end summaries.
                    if kind == "on_chain_end":
                        if name == "planner":
                            output = event.get("data", {}).get("output") or {}
                            plan = output.get("plan")
                            if isinstance(plan, Plan):
                                token = _format_plan_block(plan)
                                trace.append(token)
                                yield token
                            continue
                        if name == "reflector":
                            output = event.get("data", {}).get("output") or {}
                            refl = output.get("last_reflection")
                            if isinstance(refl, Reflection):
                                token = _format_reflection_block(refl)
                                trace.append(token)
                                yield token
                            continue
                        if name == "finalizer":
                            output = event.get("data", {}).get("output") or {}
                            msgs = output.get("messages") or []
                            if msgs and isinstance(msgs[-1], AIMessage):
                                content = msgs[-1].content
                                text = content if isinstance(content, str) else str(content)
                                trace.append(text)
                                yield text
                            continue
                except Exception:
                    log.exception("Error handling stream event kind=%s", event.get("event"))
        except Exception:
            log.exception("Fatal error in plan/reflect astream_events loop")
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
        """Non-streaming variant — returns the finalizer's rendered text."""
        graph = self._select_graph(reasoning_effort)
        if graph is None:
            raise RuntimeError("Plan/reflect agent not initialized")

        lc = self._to_langchain_messages(messages)
        config = {"recursion_limit": self._recursion_limit}
        result = await graph.ainvoke(self._initial_state(lc), config=config)

        response = ""
        for msg in reversed(result.get("messages", [])):
            if isinstance(msg, AIMessage) and msg.content:
                content = msg.content
                response = content if isinstance(content, str) else str(content)
                break

        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)
        trace.append(response)
        trace.flush()
        return response


__all__ = ["PlanReflectAgentRunner"]
