"""Graph nodes for the Reflexion variant.

Pipeline: executor → judge → (reflect → executor) → finalizer
"""

import json
import logging
import os
from pathlib import Path
from typing import Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent

_TRAJECTORY_OUTPUT_CHARS = 200
_TRAJECTORY_ARGS_CHARS = 120

from aas_agent.qwen_parser import QwenOutputParser, _normalize_json_from_qwen
from aas_agent.reflexion_state import (
    FinalAnswer,
    Judgment,
    ReflectionFeedback,
    ReflexionState,
    TrialRecord,
)

log = logging.getLogger(__name__)

_SHARED_RULES_PATH = Path(__file__).parent / "synthesizer_rules.md"
_SHARED_SYNTHESIZER_RULES = (
    _SHARED_RULES_PATH.read_text(encoding="utf-8")
    if _SHARED_RULES_PATH.exists()
    else ""
)

# ---------------------------------------------------------------------------
# Node system prompts
# ---------------------------------------------------------------------------

_EXECUTOR_PROMPT = """You are an executor for the AAS Maintenance Assistant.
Retrieve information to answer the user's query using MCP tools.
Report your findings; do not synthesize the final answer.

When previous trials are listed below, treat them as your memory:
- "Previous Trial Tool Trajectory" is short-term memory — the actual
  tool calls and observation snippets from earlier attempts. Do not
  re-call a tool whose result is already there.
- "Previous Reflections" is long-term memory — verbal advice from the
  self-reflection step. Apply it to choose a different approach.
Fetch only what the latest reflection identifies as missing.
"""

_JUDGE_PROMPT = """You are an evaluator for the AAS Maintenance Assistant. Judge the quality of
a generated answer against the user query. Give a score (0.0–1.0) and verdict (accept/revise).
State what is missing or incorrect and whether the remaining attempts should succeed.

CRITICAL: The answer MUST be based on tool-call evidence. Reject answers that:
- Sound plausible but cite no specific data from tool results.
- Hallucinate domain knowledge (biology, finance, etc.) when the domain is
  industrial automation (robots, machines, sensors, AAS).
- Claim "data is missing" without showing which tools were tried and what returned.
Output ONLY a JSON object with keys: score, verdict, missing, reason.
"""

_REFLECT_PROMPT = """You are a reflection advisor for the AAS Maintenance Assistant.
You receive a failed answer attempt and its judgment. Analyze what went wrong
and propose a concrete strategy for the next attempt.

DOMAIN: Stay in industrial automation / AAS. The user asks about factory assets
(robots, machines, sensors). If previous attempts drifted into unrelated domains
(biology, finance, etc.), explicitly course-correct.

Write in first person as if the executor is reflecting on its own work.
Be specific: name the tools or queries that failed, explain why they were
insufficient, and describe exactly what to try differently. Keep examples
generic — the next attempt should rediscover specific templates, structure,
and paths through tool calls.

Example reflection (focus on the mechanism, not on specific templates or
semanticIds — the next attempt will rediscover those through tools):
"My traversal returned zero rows because I used a relationship label
that isn't in the schema. Next attempt: call get_graph_schema before
composing Cypher, then verify each relationship name along the path."

Output ONLY a JSON object with keys: strategy_hint, common_pitfalls, focus_areas.
"""

_FINALIZER_PROMPT = """You are a finalizer for the AAS Maintenance Assistant.
Synthesize the final answer from the best available evidence, including all trial histories.

Pattern-specific rules (Reflexion):
- Prefer the highest-scored trial answer (best_answer_text) as your primary
  basis, but acknowledge information gathered in other trials that is
  relevant to the user's request.
- If the judge never accepted (REFLEXION_MAX_TRIALS exhausted with verdict
  still "revise"), treat this as a forced-termination case (see hard rules
  below) — confidence is low, unresolved is non-empty.
- Output ONLY a JSON object with keys: answer, confidence, unresolved.
"""

_FINALIZER_PROMPT_FULL = (
    f"{_FINALIZER_PROMPT}\n\n---\n\n{_SHARED_SYNTHESIZER_RULES}"
    if _SHARED_SYNTHESIZER_RULES
    else _FINALIZER_PROMPT
)


# ---------------------------------------------------------------------------
# Executor node
# ---------------------------------------------------------------------------

def _extract_trajectory(messages: list) -> list[dict]:
    """Walk a sub-loop's messages and produce the structured short-term memory.

    Pairs each AI tool call with the matching ToolMessage observation so
    the next trial sees both intent and outcome in compact form.
    """
    trajectory: list[dict] = []
    pending: dict[str, dict] = {}
    for msg in messages:
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
            for tc in msg.tool_calls:
                call_id = tc.get("id") or ""
                name = tc.get("name", "tool")
                args = tc.get("args", {})
                try:
                    args_str = json.dumps(args, ensure_ascii=False)
                except (TypeError, ValueError):
                    args_str = str(args)
                if len(args_str) > _TRAJECTORY_ARGS_CHARS:
                    args_str = args_str[:_TRAJECTORY_ARGS_CHARS] + "..."
                entry = {"tool": name, "args": args_str, "output": ""}
                trajectory.append(entry)
                if call_id:
                    pending[call_id] = entry
        elif isinstance(msg, ToolMessage):
            call_id = getattr(msg, "tool_call_id", "")
            content = msg.content if isinstance(msg.content, str) else str(msg.content)
            if len(content) > _TRAJECTORY_OUTPUT_CHARS:
                content = content[:_TRAJECTORY_OUTPUT_CHARS] + "..."
            if call_id and call_id in pending:
                pending[call_id]["output"] = content
            elif trajectory and not trajectory[-1]["output"]:
                trajectory[-1]["output"] = content
    return trajectory


def _render_trajectory(trajectory: list[dict]) -> str:
    """Render a trajectory list as compact markdown for prompt injection."""
    if not trajectory:
        return ""
    lines = []
    for i, step in enumerate(trajectory, 1):
        lines.append(f"{i}. `{step['tool']}({step['args']})`")
        if step["output"]:
            lines.append(f"   → {step['output']}")
    return "\n".join(lines)


async def _run_executor_subloop(
    llm: BaseChatModel,
    tools: list[BaseTool],
    prompt_text: str,
    user_request: str,
    max_iterations: int = 5,
) -> tuple[list, str]:
    """ReAct loop via LangGraph's create_react_agent for robust tool calling."""
    react_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt_text,
    )

    result = await react_agent.ainvoke(
        {"messages": [HumanMessage(content=user_request)]},
        config={"recursion_limit": max_iterations * 6},
    )

    messages = result.get("messages", [])

    # Extract answer from last non-tool-call AIMessage
    answer = ""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.tool_calls:
            continue
        if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
            answer = msg.content.strip()
            break

    return messages, answer


def make_executor_node(
    llm: BaseChatModel,
    tools: list[BaseTool],
    base_system: str,
) -> Callable:
    iteration_limit = int(os.environ.get("AGENT_STEP_ITERATION_LIMIT", "5"))

    async def executor_node(state: ReflexionState) -> dict:
        user_request = _last_human_text(state)

        # Build prompt: executor instructions + system prompt + MCP context + memory
        prompt_parts = [_EXECUTOR_PROMPT, "\n\n---\n\n", base_system]

        trial_records = state.get("trial_records", [])
        if trial_records:
            prompt_parts.append(
                "\n\n## Previous Trial Tool Trajectory (short-term memory)\n\n"
            )
            for tr in trial_records:
                rendered = _render_trajectory(tr.tool_trajectory)
                if rendered:
                    prompt_parts.append(
                        f"### Trial {tr.trial} (score={tr.score:.2f})\n{rendered}\n\n"
                    )

        feedback_history = state.get("feedback_history", [])
        if feedback_history:
            prompt_parts.append(
                "\n\n## Previous Reflections (long-term memory)\n\n"
            )
            for fb in feedback_history:
                prompt_parts.append(str(fb))
                prompt_parts.append("\n\n")
            prompt_parts.append("## Current attempt — improve on all previous feedback.\n\n")

        prompt = "".join(prompt_parts)

        msgs, answer = await _run_executor_subloop(
            llm=llm,
            tools=tools,
            prompt_text=prompt,
            user_request=user_request,
            max_iterations=iteration_limit,
        )

        trajectory = _extract_trajectory(msgs)

        log.info(
            "executor trial %d: answer_len=%d messages=%d tool_steps=%d",
            state.get("current_trial", 1), len(answer), len(msgs), len(trajectory),
        )

        return {
            "messages": msgs,
            "last_answer_text": answer,
            "last_trial_trajectory": trajectory,
        }

    return executor_node


# ---------------------------------------------------------------------------
# Judge node
# ---------------------------------------------------------------------------

def make_judge_node(llm: BaseChatModel) -> Callable:
    async def judge_node(state: ReflexionState) -> dict:
        user_request = _last_human_text(state)
        answer = state.get("last_answer_text", "")
        trial = state.get("current_trial", 1)

        ctx = (
            f"User query:\n{user_request}\n\n"
            f"Generated answer (trial #{trial}):\n{answer}\n\n"
        )

        # Include trial history if this is trial 2+
        trials = state.get("trial_records", [])
        if trials:
            ctx += "\n## Previous Trials\n\n"
            for t in trials:
                ctx += f"- Trial {t.trial}: score={t.score:.2f}, verdict={t.verdict}\n"
                ctx += f"  Summary: {t.summary[:300]}\n\n"

        ctx += (
            f"\nJudge quality 0.0-1.0 and decide accept/revise.\n"
            f"Include missing items and reason.\n"
            f"Output ONLY a JSON object: {{score, verdict, missing, reason}}"
        )

        msgs = [
            SystemMessage(content=_JUDGE_PROMPT),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        judgment = _parse_judgment(content)
        if judgment is None:
            judgment = Judgment(
                score=0.5,
                verdict="revise",
                missing=["Could not parse judgment"],
                reason="Parse failure, defaulting to revise.",
            )

        # Record this trial and increment counter for next iteration
        new_record = TrialRecord(
            trial=trial,
            score=judgment.score,
            verdict=judgment.verdict,
            summary=answer[:500] if answer else "(empty answer)",
            tool_trajectory=list(state.get("last_trial_trajectory", [])),
        )
        existing = list(state.get("trial_records", []))
        existing.append(new_record)

        # Track best-scoring answer across all trials
        best_answer = state.get("best_answer_text", "")
        existing_best_score = max((t.score for t in existing), default=0.0)
        if judgment.score >= existing_best_score:
            best_answer = answer

        return {
            "judgment": judgment,
            "trial_records": existing,
            "current_trial": trial + 1,
            "best_answer_text": best_answer,
        }

    return judge_node


def _parse_judgment(content: str) -> Judgment | None:
    try:
        parser = QwenOutputParser(pydantic_model=Judgment)
        return parser.parse(content)
    except Exception:
        log.debug("Failed to parse judgment via QwenOutputParser")

    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict) and "score" in normalized:
        try:
            return Judgment.model_validate(normalized)
        except Exception:
            log.debug("Failed to validate normalized judgment via pydantic")

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "score" in parsed and "verdict" in parsed:
            # LLM often returns missing as a string — coerce to list
            if isinstance(parsed.get("missing"), str):
                parsed["missing"] = [parsed["missing"]] if parsed["missing"] else []
            return Judgment.model_validate(parsed)
    except (json.JSONDecodeError, Exception):
        log.debug("Failed to parse judgment via raw JSON")

    return None


# ---------------------------------------------------------------------------
# Reflect node
# ---------------------------------------------------------------------------

def make_reflect_node(llm: BaseChatModel) -> Callable:
    async def reflect_node(state: ReflexionState) -> dict:
        user_request = _last_human_text(state)
        judgment = state.get("judgment")
        trials = state.get("trial_records", [])
        current_trial = state.get("current_trial", 1)

        completed_trial = current_trial - 1
        ctx = (
            f"User query:\n{user_request}\n\n"
            f"Latest answer (trial #{completed_trial}):\n{state.get('last_answer_text', '')}\n\n"
            f"Judgment:\n"
            f"  Score: {judgment.score if judgment else 'N/A'}\n"
            f"  Verdict: {judgment.verdict if judgment else 'N/A'}\n"
            f"  Missing: {judgment.missing if judgment else 'N/A'}\n"
            f"  Reason: {judgment.reason if judgment else 'N/A'}\n\n"
            f"Previous trials:\n"
        )
        for t in trials:
            ctx += f"- Trial {t.trial}: score={t.score:.2f}\n"

        ctx += (
            f"\nPropose a concrete strategy for the next attempt.\n"
            f"Output ONLY a JSON object: {{strategy_hint, common_pitfalls, focus_areas}}"
        )

        msgs = [
            SystemMessage(content=_REFLECT_PROMPT),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        reflection = _parse_reflection(content)
        if reflection is None:
            reflection = ReflectionFeedback(
                strategy_hint="Try a completely different approach. Consider using different tools or search terms.",
                common_pitfalls=["Avoid repeating the same failed strategy."],
                focus_areas=["Re-examine the user's core question from scratch."],
            )

        # Render feedback for the next executor attempt
        feedback_text = (
            f"### Reflection after Trial {completed_trial}\n\n"
            f"**Judge score:** {judgment.score:.2f}/{judgment.verdict}\n\n"
            f"**Missing:** {judgment.missing}\n\n"
            f"**Reason:** {judgment.reason}\n\n"
            f"**Strategy hint:** {reflection.strategy_hint}\n\n"
            f"**Common pitfalls to avoid:** {'; '.join(reflection.common_pitfalls)}\n\n"
            f"**Focus areas:** {'; '.join(reflection.focus_areas)}\n"
        )

        log.info(
            "reflect: trial %d — strategy=%s",
            completed_trial,
            reflection.strategy_hint[:100],
        )

        existing_feedback = list(state.get("feedback_history", []))
        existing_feedback.append(feedback_text)

        return {
            "reflection": reflection,
            "feedback_history": existing_feedback,
        }

    return reflect_node


def _coerce_reflection_fields(d: dict) -> None:
    """Normalize ReflectionFeedback fields so pydantic validation passes."""
    for field in ("common_pitfalls", "focus_areas"):
        val = d.get(field)
        if isinstance(val, str):
            d[field] = [val] if val.strip() else []


def _parse_reflection(content: str) -> ReflectionFeedback | None:
    try:
        parser = QwenOutputParser(pydantic_model=ReflectionFeedback)
        return parser.parse(content)
    except Exception:
        log.debug("Failed to parse reflection via QwenOutputParser")

    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict) and "strategy_hint" in normalized:
        _coerce_reflection_fields(normalized)
        try:
            return ReflectionFeedback.model_validate(normalized)
        except Exception:
            log.debug("Failed to validate normalized reflection via pydantic")

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "strategy_hint" in parsed:
            _coerce_reflection_fields(parsed)
            return ReflectionFeedback.model_validate(parsed)
    except json.JSONDecodeError:
        log.debug("Failed to parse reflection via raw JSON")

    return None


# ---------------------------------------------------------------------------
# Finalizer node
# ---------------------------------------------------------------------------

def make_finalizer_node(llm: BaseChatModel) -> Callable:
    async def finalizer_node(state: ReflexionState) -> dict:
        user_request = _last_human_text(state)
        trials = state.get("trial_records", [])
        best_score = max((t.score for t in trials), default=0.0)

        best_answer_text = state.get("best_answer_text", "")
        last_answer = state.get("last_answer_text", "")

        ctx = (f"User query:\n{user_request}\n\n")
        if trials:
            ctx += "## Trial History\n\n"
            for t in trials:
                ctx += f"- Trial {t.trial}: score={t.score:.2f}, verdict={t.verdict}\n"
            ctx += "\n## All Trial Answers\n"
            for t in trials:
                ctx += f"### Trial {t.trial} (score={t.score:.2f}, verdict={t.verdict})\n{t.summary}\n\n"

        if best_answer_text:
            ctx += f"## Best Available Answer (score={best_score:.2f})\n{best_answer_text}\n\n"
        elif last_answer:
            ctx += f"## Last Available Answer\n{last_answer}\n\n"

        ctx += (
            f"Use the best available answer as your starting point. Improve it if possible.\n"
            f"Output ONLY a JSON object: {{answer, confidence, unresolved}}"
        )

        msgs = [
            SystemMessage(content=_FINALIZER_PROMPT_FULL),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        final = _parse_final_answer(content)

        # Calibrate confidence
        if not trials:
            final.confidence = "low"
        elif best_score >= 0.8:
            final.confidence = "high"
        elif best_score >= 0.5:
            final.confidence = "medium"
        else:
            final.confidence = "low"

        # Render with metadata
        text = final.answer.rstrip()
        meta_lines = [f"**confidence:** {final.confidence}"]
        if final.unresolved:
            meta_lines.append("**unresolved:**")
            for u in final.unresolved:
                meta_lines.append(f"- {u}")

        rendered = text + "\n\n<think>\n" + "\n".join(meta_lines) + "\n</think>\n"

        log.info(
            "finalizer: best_score=%.2f confidence=%s unresolved=%d",
            best_score, final.confidence, len(final.unresolved),
        )

        return {
            "messages": [AIMessage(content=rendered)],
        }

    return finalizer_node


def _coerce_final_answer(d: dict) -> dict:
    """Normalize FinalAnswer fields so pydantic validation passes."""
    if isinstance(d.get("confidence"), (int, float)):
        c = d["confidence"]
        d["confidence"] = "high" if c >= 0.7 else ("medium" if c >= 0.4 else "low")
    unresolved = d.get("unresolved")
    if not isinstance(unresolved, list):
        d["unresolved"] = [unresolved] if unresolved and unresolved is not False else []
    return d


def _parse_final_answer(content: str) -> FinalAnswer:
    try:
        parser = QwenOutputParser(pydantic_model=FinalAnswer)
        return parser.parse(content)
    except Exception:
        log.debug("Failed to parse final answer via QwenOutputParser")

    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict) and "answer" in normalized and "confidence" in normalized:
        try:
            _coerce_final_answer(normalized)
            return FinalAnswer.model_validate(normalized)
        except Exception:
            log.debug("Failed to validate normalized final answer via pydantic")

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "answer" in parsed and "confidence" in parsed:
            _coerce_final_answer(parsed)
            return FinalAnswer.model_validate(parsed)
    except (json.JSONDecodeError, Exception):
        log.debug("Failed to parse final answer via raw JSON")

    return FinalAnswer(
        answer=content.strip()[:2000] if content.strip() else "No results from Reflexion pipeline.",
        confidence="low",
        unresolved=["Could not synthesize a confident answer."],
    )


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def route_after_judge(state: ReflexionState) -> str:
    """Conditional edge after judge evaluation."""
    judgment = state.get("judgment")
    if judgment is None:
        return "finalizer"

    if judgment.verdict == "accept":
        return "finalizer"

    threshold = state.get("accept_threshold", 0.7)
    if judgment.score >= threshold:
        return "finalizer"

    max_trials = state.get("max_trials", 3)
    current = state.get("current_trial", 2)

    if current > max_trials:
        log.info("Reflexion: max trials (%d) reached → finalizer", max_trials)
        return "finalizer"

    return "reflect"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _last_human_text(state: dict) -> str:
    """Extract last human/user text from state messages."""
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, dict):
            role = msg.get("role", "")
            content = msg.get("content", "")
        else:
            role = getattr(msg, "type", "")
            content = getattr(msg, "content", "")
        if role in ("human", "user") and content:
            return content if isinstance(content, str) else str(content)
    return ""
