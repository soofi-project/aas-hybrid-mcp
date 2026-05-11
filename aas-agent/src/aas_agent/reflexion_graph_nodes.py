"""Graph nodes for the Reflexion variant.

Pipeline: executor → judge → (reflect → executor) → finalizer
"""

import json
import logging
import os
from typing import Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool

from aas_agent.qwen_parser import QwenOutputParser, _normalize_json_from_qwen
from aas_agent.reflexion_state import (
    FinalAnswer,
    Judgment,
    ReflectionFeedback,
    ReflexionState,
    TrialRecord,
)

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Node system prompts
# ---------------------------------------------------------------------------

_EXECUTOR_PROMPT = """You are an executor for the AAS Maintenance Assistant answering the user's query.

You have access to multiple MCP tools including graph queries (search_graph, get_asset, list_assets),
manual/document lookups (get_manual_page, get_manual_index), and template discovery (search_idt_templates).

Your job: produce a complete, accurate answer to the user's query.
- Use tools to retrieve relevant information before answering.
- Cross-reference evidence between graph, manual, and template sources.
- Be thorough and precise. Never fabricate content.
- When you're confident you have enough information, provide a clear, direct answer.
- Structure your answer to address ALL parts of the user's query.
"""

_JUDGE_PROMPT = """You are an evaluator for the AAS Maintenance Assistant. Judge the quality of
a generated answer against the user query. Give a score (0.0–1.0) and verdict (accept/revise).
State what is missing or incorrect and whether the remaining attempts should succeed.
Output ONLY a JSON object with keys: score, verdict, missing, reason.
"""

_REFLECT_PROMPT = """You are a reflection advisor for the AAS Maintenance Assistant.
You receive a failed answer attempt and its judgment. Propose a concrete strategy
for the next attempt.

Output ONLY a JSON object with keys: strategy_hint, common_pitfalls, focus_areas.
"""

_FINALIZER_PROMPT = """You are a finalizer for the AAS Maintenance Assistant.
Synthesize the final answer from the best available evidence, including all trial histories.
Output ONLY a JSON object with keys: answer, confidence, unresolved.
"""


# ---------------------------------------------------------------------------
# Executor node
# ---------------------------------------------------------------------------

async def _run_executor_subloop(
    llm: BaseChatModel,
    tools: list[BaseTool],
    prompt_text: str,
    user_request: str,
    max_iterations: int = 5,
) -> tuple[list, str]:
    """Bounded ReAct loop — produces messages and final answer text."""
    messages = [
        SystemMessage(content=prompt_text),
        HumanMessage(content=user_request),
    ]
    tool_map = {t.name: t for t in tools}
    tool_calls = 0

    for _ in range(max_iterations):
        response = await llm.ainvoke(messages)
        if not isinstance(response, AIMessage) or not response.tool_calls:
            messages.append(response)
            break

        messages.append(response)
        for tc in response.tool_calls:
            tool_calls += 1
            tool = tool_map.get(tc["name"])
            if tool is None:
                messages.append(ToolMessage(
                    content=f"Unknown tool: {tc['name']}", name=tc["name"], tool_call_id=tc["id"]
                ))
                continue
            try:
                result = await tool.ainvoke(tc["args"])
                result_text = getattr(result, "content", str(result))
                messages.append(ToolMessage(
                    content=result_text, name=tc["name"], tool_call_id=tc["id"]
                ))
            except Exception as exc:
                messages.append(ToolMessage(
                    content=f"Tool error: {exc}", name=tc["name"], tool_call_id=tc["id"]
                ))

    # Extract answer from last non-tool-call message
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

        # Build prompt with accumulated feedback
        prompt_parts = [_EXECUTOR_PROMPT, "\n\n---\n\n", base_system]

        feedback_history = state.get("feedback_history", [])
        if feedback_history:
            prompt_parts.append("\n\n## Previous Attempts & Feedback\n\n")
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

        log.info(
            "executor trial %d: answer_len=%d messages=%d",
            state.get("current_trial", 1), len(answer), len(msgs),
        )

        return {
            "messages": msgs,
            "last_answer_text": answer,
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
        pass

    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict) and "score" in normalized:
        try:
            return Judgment.model_validate(normalized)
        except Exception:
            pass

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "score" in parsed and "verdict" in parsed:
            # LLM often returns missing as a string — coerce to list
            if isinstance(parsed.get("missing"), str):
                parsed["missing"] = [parsed["missing"]] if parsed["missing"] else []
            return Judgment.model_validate(parsed)
    except (json.JSONDecodeError, Exception):
        pass

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

        ctx = (
            f"User query:\n{user_request}\n\n"
            f"Latest answer (trial #{current_trial}):\n{state.get('last_answer_text', '')}\n\n"
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
            f"### Reflection after Trial {current_trial}\n\n"
            f"**Judge score:** {judgment.score:.2f}/{judgment.verdict}\n\n"
            f"**Missing:** {judgment.missing}\n\n"
            f"**Reason:** {judgment.reason}\n\n"
            f"**Strategy hint:** {reflection.strategy_hint}\n\n"
            f"**Common pitfalls to avoid:** {'; '.join(reflection.common_pitfalls)}\n\n"
            f"**Focus areas:** {'; '.join(reflection.focus_areas)}\n"
        )

        log.info(
            "reflect: trial %d — strategy=%s",
            current_trial,
            reflection.strategy_hint[:100],
        )

        return {
            "reflection": reflection,
            "feedback_history": [feedback_text],
        }

    return reflect_node


def _parse_reflection(content: str) -> ReflectionFeedback | None:
    try:
        parser = QwenOutputParser(pydantic_model=ReflectionFeedback)
        return parser.parse(content)
    except Exception:
        pass

    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict) and "strategy_hint" in normalized:
        try:
            return ReflectionFeedback.model_validate(normalized)
        except Exception:
            pass

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "strategy_hint" in parsed:
            if isinstance(parsed.get("common_pitfalls"), str):
                parsed["common_pitfalls"] = [parsed["common_pitfalls"]] if parsed["common_pitfalls"] else []
            return ReflectionFeedback.model_validate(parsed)
    except json.JSONDecodeError:
        pass

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
            ctx += "\n"

        if best_answer_text:
            ctx += f"## Best Available Answer (score={best_score:.2f})\n{best_answer_text}\n\n"
        elif last_answer:
            ctx += f"## Last Available Answer\n{last_answer}\n\n"

        ctx += (
            f"Use the best available answer as your starting point. Improve it if possible.\n"
            f"Output ONLY a JSON object: {{answer, confidence, unresolved}}"
        )

        msgs = [
            SystemMessage(content=_FINALIZER_PROMPT),
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
        pass

    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict) and "answer" in normalized and "confidence" in normalized:
        try:
            _coerce_final_answer(normalized)
            return FinalAnswer.model_validate(normalized)
        except Exception:
            pass

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "answer" in parsed and "confidence" in parsed:
            _coerce_final_answer(parsed)
            return FinalAnswer.model_validate(parsed)
    except json.JSONDecodeError:
        pass

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
