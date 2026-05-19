"""Graph nodes for the plan/reflect agent variant.

Each node is an async callable taking ``AgentState`` and returning a
state-diff dict. State fields with ``Annotated[..., add_messages]`` or
``Annotated[..., operator.add]`` reducers accumulate; everything else is
overwritten by the diff.
"""

import logging
import os
from typing import Callable, Type

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from aas_agent.agent_plan_state import (
    AgentState,
    Evidence,
    FinalAnswer,
    Plan,
    Reflection,
    Step,
)

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Structured output helper
# ---------------------------------------------------------------------------

async def _structured_invoke(
    llm: BaseChatModel,
    model_cls: Type[BaseModel],
    messages: list[BaseMessage],
) -> BaseModel:
    """Invoke LLM with schema enforcement via with_structured_output.

    Tries function_calling first (schema passed as tool definition —
    most reliable for Qwen3.5-Instruct via vLLM), then falls back to
    json_mode (response_format=json_object) if that raises.
    """
    try:
        return await llm.with_structured_output(model_cls).ainvoke(messages)
    except Exception as e:
        log.debug("function_calling structured output failed (%s), retrying with json_mode", e)
        return await llm.with_structured_output(model_cls, method="json_mode").ainvoke(messages)


def _last_human_text(messages: list[BaseMessage]) -> str:
    """Return the most recent human-message content (the user's request)."""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content if isinstance(msg.content, str) else str(msg.content)
    return ""


def _format_step_brief(plan: Plan, step: Step, hint: str, prior: list[Evidence]) -> str:
    """Compose the per-step instruction the executor sub-agent receives."""
    parts: list[str] = [
        f"Plan goal: {plan.goal}",
        f"Step {step.id}/{len(plan.steps)} — {step.intent}",
        f"Success criteria: {step.success_criteria}",
    ]
    if step.suggested_tool:
        parts.append(f"Suggested tool: {step.suggested_tool}")
    if hint:
        parts.append(f"Retry hint (last attempt missed something): {hint}")
    if prior:
        joined = "\n".join(f"- [{e.source}/{e.tool}] {e.summary}" for e in prior)
        parts.append(f"Prior evidence collected so far:\n{joined}")
    parts.append(
        "Execute this step now. Stop the moment success_criteria is met "
        "or you have exhausted reasonable alternatives."
    )
    return "\n\n".join(parts)


def _summarize_recent_tool_traffic(messages: list[BaseMessage], limit: int = 12) -> str:
    """Compact rendering of the last few AI/Tool message pairs for the reflector."""
    relevant = [m for m in messages if isinstance(m, (AIMessage, ToolMessage))]
    recent = relevant[-limit:]
    out: list[str] = []
    for m in recent:
        if isinstance(m, AIMessage):
            if m.tool_calls:
                for tc in m.tool_calls:
                    out.append(f"[tool_call] {tc.get('name')}({tc.get('args')})")
            elif m.content:
                txt = m.content if isinstance(m.content, str) else str(m.content)
                out.append(f"[assistant] {txt[:600]}")
        elif isinstance(m, ToolMessage):
            txt = m.content if isinstance(m.content, str) else str(m.content)
            out.append(f"[tool_result {m.name or '?'}] {txt[:800]}")
    return "\n".join(out) if out else "(no tool traffic in this step)"


# ---------------------------------------------------------------------------
# Node factories
# ---------------------------------------------------------------------------

def make_planner_node(
    llm: BaseChatModel,
    base_system: str,
    planner_prompt: str,
) -> Callable:
    """Plans the work as a ``Plan`` Pydantic object."""

    async def planner_node(state: AgentState) -> dict:
        user_request = _last_human_text(state["messages"])
        prior_plan = state.get("plan")
        replan_note = ""
        if prior_plan is not None:
            evidence = state.get("evidence", []) or []
            ev_summary = "\n".join(f"- {e.summary}" for e in evidence) or "(none)"
            replan_note = (
                "\n\nThis is a REPLAN. Previous plan and accumulated evidence:\n"
                f"Previous plan: {prior_plan.model_dump_json(indent=2)}\n"
                f"Evidence so far:\n{ev_summary}\n"
                "Take the new facts into account."
            )

        msgs: list[BaseMessage] = [
            SystemMessage(content=f"{planner_prompt}\n\n---\n\n{base_system}"),
            HumanMessage(content=f"User request:\n{user_request}{replan_note}\n\nOutput ONLY a JSON object with keys: goal, steps, fallback_notes."),
        ]
        plan: Plan = await _structured_invoke(llm, Plan, msgs)

        # Auto-assign step ids if Qwen didn't provide them
        plan = plan.auto_assign_step_ids()

        # Validate plan has at least one step — Qwen sometimes returns empty steps
        if not plan.steps or len(plan.steps) == 0:
            log.warning(
                "Planner returned 0 steps, retrying with explicit instruction (goal=%s)",
                plan.goal[:100] if plan.goal else "(empty)",
            )
            try:
                msgs_retry = list(msgs)
                msgs_retry.append(HumanMessage(content="\n\nCRITICAL: You MUST return at least one step in the steps array. Do NOT return an empty steps list. Even a single exploratory step is required."))
                plan = await _structured_invoke(llm, Plan, msgs_retry)
            except Exception as e2:
                log.error("Retry plan also failed: %s", e2)
                # Raise a descriptive error instead of crashing later
                raise RuntimeError(
                    f"Planner returned an invalid plan with 0 steps. "
                    f"Goal: {plan.goal}. The LLM model is not producing valid step plans. "
                    f"Consider using a larger model or checking the prompt."
                ) from e2
        log.info(
            "planner: %d steps (replan=%d)",
            len(plan.steps),
            state.get("replan_count", 0),
        )
        return {
            "plan": plan,
            "current_step_idx": 0,
            "step_attempts": 0,
            "replan_count": state.get("replan_count", 0)
            + (1 if prior_plan is not None else 0),
        }

    return planner_node


async def _execute_step_loop(
    llm: BaseChatModel,
    tools: list[BaseTool],
    prompt_text: str,
    user_request: str,
    max_iterations: int = 5,
) -> tuple[list[BaseMessage], int]:
    """Custom ReAct loop with a hard iteration cap.

    Unlike ``create_react_agent`` (no built-in ``max_iterations``),
    this loop stops after ``max_iterations`` LLM calls regardless of
    state.
    """
    messages: list[BaseMessage] = [
        SystemMessage(content=prompt_text),
        HumanMessage(content=user_request),
    ]
    tool_map = {t.name: t for t in tools}
    tool_calls_made = 0

    for _ in range(max_iterations):
        response = await llm.ainvoke(messages)

        if not isinstance(response, AIMessage) or not response.tool_calls:
            # No more tool calls — we're done
            messages.append(response)
            break

        # Execute all tool calls in this turn
        messages.append(response)
        for tc in response.tool_calls:
            tool_calls_made += 1
            tool = tool_map.get(tc["name"])
            if tool is None:
                messages.append(ToolMessage(
                    content=f"Unknown tool: {tc['name']}",
                    name=tc["name"],
                    tool_call_id=tc["id"],
                ))
                continue
            try:
                result = await tool.ainvoke(tc["args"])
                # LangChain tools may return str or dict — normalise
                if hasattr(result, "content"):
                    result_text = result.content
                else:
                    result_text = str(result)
                messages.append(ToolMessage(
                    content=result_text,
                    name=tc["name"],
                    tool_call_id=tc["id"],
                ))
            except Exception as exc:
                messages.append(ToolMessage(
                    content=f"Tool error: {exc}",
                    name=tc["name"],
                    tool_call_id=tc["id"],
                ))
        # Continue loop — next LLM call will process tool results

    return messages, tool_calls_made


def make_execute_step_node(
    llm: BaseChatModel,
    tools: list[BaseTool],
    base_system: str,
    executor_prompt: str,
    sub_recursion_limit: int,
) -> Callable:
    """Runs a bounded ReAct sub-loop scoped to the current step."""
    # Hard iteration cap — env-overridable (default: 5)
    max_iterations = int(os.environ.get("AGENT_STEP_ITERATION_LIMIT", "5"))

    prompt_text = f"{executor_prompt}\n\n---\n\n{base_system}"

    async def execute_step_node(state: AgentState) -> dict:
        plan = state["plan"]
        if plan is None:
            raise RuntimeError("execute_step called without a plan")
        idx = state["current_step_idx"]
        if idx >= len(plan.steps):
            raise RuntimeError(f"step index {idx} out of range ({len(plan.steps)} steps)")
        step = plan.steps[idx]

        last_refl = state.get("last_reflection")
        hint = (
            last_refl.next_action_hint
            if last_refl is not None and last_refl.decision == "step_retry"
            else ""
        )

        prior = state.get("evidence", []) or []
        brief = _format_step_brief(plan, step, hint, prior)
        user_request = _last_human_text(state["messages"])

        # Run the bounded loop
        produced, tool_calls_made = await _execute_step_loop(
            llm=llm,
            tools=tools,
            prompt_text=prompt_text,
            user_request=f"{brief}\n\n{user_request}",
            max_iterations=max_iterations,
        )

        return {
            "messages": produced,
            "total_tool_calls": state.get("total_tool_calls", 0) + tool_calls_made,
            "step_attempts": state.get("step_attempts", 0) + 1,
        }

    return execute_step_node


def make_reflector_node(
    llm: BaseChatModel,
    reflector_prompt: str,
) -> Callable:
    """Decides what comes after a step's tool traffic."""

    async def reflector_node(state: AgentState) -> dict:
        plan = state["plan"]
        if plan is None:
            raise RuntimeError("reflector called without a plan")
        idx = state["current_step_idx"]
        step = plan.steps[idx]
        is_last = idx == len(plan.steps) - 1
        attempts = state.get("step_attempts", 0)
        replans = state.get("replan_count", 0)
        total_calls = state.get("total_tool_calls", 0)

        recent = _summarize_recent_tool_traffic(state["messages"])
        user_request = _last_human_text(state["messages"])

        ctx = (
            f"User request:\n{user_request}\n\n"
            f"Plan goal: {plan.goal}\n"
            f"Step {step.id}/{len(plan.steps)}: {step.intent}\n"
            f"Success criteria: {step.success_criteria}\n"
            f"This is the LAST step: {is_last}\n"
            f"Attempts on this step so far: {attempts}\n"
            f"Replans so far: {replans}\n"
            f"Total tool calls so far: {total_calls}\n\n"
            f"Recent tool traffic:\n{recent}\n\n"
            "Output ONLY a JSON object with keys: decision, evidence_collected, next_action_hint, reasoning."
        )

        msgs: list[BaseMessage] = [
            SystemMessage(content=reflector_prompt),
            HumanMessage(content=ctx),
        ]
        try:
            refl: Reflection = await _structured_invoke(llm, Reflection, msgs)
        except Exception as e:
            log.warning("Structured output parsing failed: %s, retrying with stronger JSON hint...", e)
            msgs_strict = list(msgs)
            msgs_strict.append(HumanMessage(content="\n\nCRITICAL: Your ENTIRE response must be valid JSON only. Do not include any text outside the JSON object."))
            refl = await _structured_invoke(llm, Reflection, msgs_strict)

        # Hard contradiction guard: a step_done / all_done with no collected
        # evidence is a confident-empty conclusion off a single (or no) tool
        # call. Per the reflector's own rules, that requires at least two
        # exhausted hypotheses. Force a retry so the executor broadens its
        # search before we declare emptiness as fact. The attempt/replan caps
        # still bound the loop.
        if refl.decision in ("step_done", "all_done") and not refl.evidence_collected:
            log.info(
                "reflector: blocking premature %s (empty evidence) → step_retry",
                refl.decision,
            )
            refl = Reflection(
                decision="step_retry",
                evidence_collected=[],
                next_action_hint=(
                    "No evidence was recorded — try a different template "
                    "hypothesis or a broader semanticId-based traversal "
                    "before concluding emptiness."
                ),
                reasoning=(
                    f"Reflector attempted '{refl.decision}' but evidence is empty; "
                    f"forcing retry to satisfy the two-hypothesis rule. "
                    f"Original reasoning: {refl.reasoning}"
                ),
            )

        # Project the reflector's bullet facts into structured Evidence so the
        # finalizer has a consistent shape to work with. Preserve the source
        # category from the most recent executor evidence if identifiable;
        # otherwise default to "other".
        default_source = "other"
        if state.get("evidence"):
            # Inherit the most common source category from prior evidence so
            # the finalizer doesn't see everything as "other".
            from collections import Counter
            source_counts = Counter(e.source for e in state["evidence"] if e.source != "other")
            default_source = source_counts.most_common(1)[0][0] if source_counts else "other"

        new_evidence = [
            Evidence(source=default_source, tool=f"step-{step.id}", summary=fact)
            for fact in refl.evidence_collected
        ]

        log.info(
            "reflector: decision=%s attempts=%d evidence=%d",
            refl.decision,
            attempts,
            len(new_evidence),
        )
        return {"last_reflection": refl, "evidence": new_evidence}

    return reflector_node


def make_finalizer_node(
    llm: BaseChatModel,
    finalizer_prompt: str,
) -> Callable:
    """Synthesizes the user-facing FinalAnswer from accumulated evidence."""

    async def finalizer_node(state: AgentState) -> dict:
        plan = state["plan"]
        evidence = state.get("evidence", []) or []
        last_refl = state.get("last_reflection")
        user_request = _last_human_text(state["messages"])

        ev_block = "\n".join(
            f"- [{e.source}/{e.tool}] {e.summary}" for e in evidence
        ) or "(no evidence collected)"
        refl_block = (
            f"Last reflection decision: {last_refl.decision}\n"
            f"Reasoning: {last_refl.reasoning}"
            if last_refl is not None
            else "(no reflection recorded)"
        )
        plan_block = plan.model_dump_json(indent=2) if plan is not None else "(no plan)"

        ctx = (
            f"User request:\n{user_request}\n\n"
            f"Plan:\n{plan_block}\n\n"
            f"All evidence:\n{ev_block}\n\n"
            f"{refl_block}\n\n"
            "Produce the FinalAnswer.\n\nOutput ONLY a JSON object with keys: answer, evidence, confidence, unresolved."
        )

        msgs: list[BaseMessage] = [
            SystemMessage(content=finalizer_prompt),
            HumanMessage(content=ctx),
        ]
        try:
            final: FinalAnswer = await _structured_invoke(llm, FinalAnswer, msgs)
        except Exception as e:
            log.warning("Structured output parsing failed: %s, retrying with stronger JSON hint...", e)
            msgs_strict = list(msgs)
            msgs_strict.append(HumanMessage(content="\n\nCRITICAL: Your ENTIRE response must be valid JSON only. Do not include any text outside the JSON object."))
            final = await _structured_invoke(llm, FinalAnswer, msgs_strict)

        # Render to a single text answer with a foldable metadata block at the
        # end (Open WebUI collapses <think>...</think>). The streaming layer
        # picks this up as the final assistant message.
        text = final.answer.rstrip()
        meta_lines = [
            f"**confidence:** {final.confidence}",
        ]
        if final.evidence:
            meta_lines.append("**evidence:**")
            for e in final.evidence:
                meta_lines.append(f"- [{e.source}/{e.tool}] {e.summary}")
        if final.unresolved:
            meta_lines.append("**unresolved:**")
            for u in final.unresolved:
                meta_lines.append(f"- {u}")

        rendered = text + "\n\n<think>\n" + "\n".join(meta_lines) + "\n</think>\n"

        log.info(
            "finalizer: confidence=%s evidence=%d unresolved=%d",
            final.confidence,
            len(final.evidence),
            len(final.unresolved),
        )
        return {"messages": [AIMessage(content=rendered)]}

    return finalizer_node


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def route_after_reflector(
    state: AgentState,
    *,
    max_step_attempts: int,
    max_replans: int,
    max_total_tool_calls: int,
) -> str:
    """Conditional edge: pick the next node after the reflector ran."""
    refl = state.get("last_reflection")
    if refl is None:
        # Should not happen — finalize defensively.
        return "finalizer"

    plan = state["plan"]
    idx = state["current_step_idx"]
    is_last = plan is not None and idx >= len(plan.steps) - 1
    attempts = state.get("step_attempts", 0)
    replans = state.get("replan_count", 0)
    total_calls = state.get("total_tool_calls", 0)
    remaining = state.get("remaining_steps")
    # Safety: if the langgraph step budget is nearly out, finalize.
    if remaining is not None and remaining <= 4:
        log.warning("route: recursion budget low (remaining=%s) → finalizer", remaining)
        return "finalizer"
    if total_calls >= max_total_tool_calls:
        log.warning("route: total_tool_calls cap reached (%d) → finalizer", total_calls)
        return "finalizer"

    if refl.decision == "all_done":
        return "finalizer"
    if refl.decision == "give_up":
        return "finalizer"
    if refl.decision == "step_done":
        if is_last:
            return "finalizer"
        # Advance to next step is handled by the advancer node before execute.
        return "advance_step"
    if refl.decision == "step_retry":
        if attempts >= max_step_attempts:
            log.info("route: retries exhausted (%d) → forcing replan", attempts)
            if replans >= max_replans:
                return "finalizer"
            return "planner"
        return "execute_step"
    if refl.decision == "replan":
        if replans >= max_replans:
            log.info("route: replan cap reached (%d) → finalizer", replans)
            return "finalizer"
        return "planner"

    # Defensive default
    return "finalizer"


async def advance_step_node(state: AgentState) -> dict:
    """Trivial node that bumps the step index after a successful step."""
    return {
        "current_step_idx": state.get("current_step_idx", 0) + 1,
        "step_attempts": 0,
    }
