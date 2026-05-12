"""Graph nodes for the CRAG (Context Retrieval Augmented Generation) variant.

Pipeline (post-relevance routing):
    executor → relevance → {
        correct   → synthesize,
        ambiguous → refine    → executor (retry with supplementary query),
        incorrect → discard   → uncorrect → executor (retry with fresh query),
    }
Capped by CRAG_MAX_REFINEMENTS — on cap, route forced to synthesize.

Each node factory receives its LLM and tools to avoid rebuilding inside nodes.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

from aas_agent.crag_state import AgentState, FinalAnswer, RetrieverStep, RelevanceScore
from aas_agent.qwen_parser import QwenOutputParser, _normalize_json_from_qwen

log = logging.getLogger(__name__)

_SHARED_RULES_PATH = Path(__file__).parent / "synthesizer_rules.md"
_SHARED_SYNTHESIZER_RULES = (
    _SHARED_RULES_PATH.read_text(encoding="utf-8")
    if _SHARED_RULES_PATH.exists()
    else ""
)

# ---------------------------------------------------------------------------
# Worker system prompts (injected into executor + refinements)
# ---------------------------------------------------------------------------

_EXECUTOR_PROMPT = """You are a retrieval specialist for the AAS Maintenance Assistant.

You have access to MCP tools for graph queries, document/manual lookup,
template discovery, semanticId resolution, and write operations. The exact
tool list is provided via the tool schemas — call them by their actual
names, never invent or guess a name.

Your job: retrieve the BEST possible information to answer the user's query.
- Try multiple search approaches if the first query seems unfruitful.
- Cross-reference evidence between graph, document, and template sources.
- For each source, try at least one alternative phrasing.
- Be thorough — the quality of your retrieval directly determines the quality of the final answer.
- Never fabricate content — if nothing matches, report that clearly.
- Do NOT synthesize a final answer — just retrieve and report your findings.
"""

_RELEVANCE_PROMPT = """You are a relevance evaluator. Judge how well the retrieved evidence
answers a user query. Rate relevance 0.0-1.0 and decide on an action.

Decide on an action:
    - correct: evidence sufficiently answers the query → synthesize immediately
    - incorrect: evidence is totally irrelevant or wrong → discard and retry from scratch
    - ambiguous: partial evidence, some useful info but incomplete → keep and supplement

State whether refinement is needed (with a concrete hint) or not.
"""

_REFINE_PROMPT = """You are a query refiner for the AAS Maintenance Assistant.
Generate a BETTER query or alternative search strategy for the next retrieval attempt.
Output ONLY a JSON object with keys: query (string), suggestion (string describing what to try differently).
"""

_SYNTHESIZER_PROMPT = """You are a synthesizer. Combine the retrieved evidence into
a final answer.

Pattern-specific rules (CRAG):
- The retrieved evidence has been scored for relevance by an earlier node.
  Use HIGH-RELEVANCE findings as primary evidence; treat low-relevance items
  as supplementary or skeptically.
- State gaps clearly. If the relevance pipeline forced termination at
  CRAG_MAX_REFINEMENTS without producing high-relevance evidence, treat
  this as a forced-termination case (see hard rules below).
- Output ONLY a JSON object with keys: answer, confidence, unresolved (list).
"""

_SYNTHESIZER_PROMPT_FULL = (
    f"{_SYNTHESIZER_PROMPT}\n\n---\n\n{_SHARED_SYNTHESIZER_RULES}"
    if _SHARED_SYNTHESIZER_RULES
    else _SYNTHESIZER_PROMPT
)


# ---------------------------------------------------------------------------
# Executor node — bounded ReAct sub-loop via create_react_agent
# ---------------------------------------------------------------------------


async def _run_executor_subloop(
    llm: BaseChatModel,
    tools: list[BaseTool],
    prompt_text: str,
    user_request: str,
    max_iterations: int = 5,
) -> tuple[list[BaseMessage], int]:
    """Bounded ReAct via create_react_agent (Qwen+vLLM compatible)."""
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt_text,
    )

    result = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(content=user_request),
            ]
        },
        config={"recursion_limit": max_iterations * 6},
    )

    produced = result.get("messages", [])
    tool_calls = sum(
        1 for m in produced
        if isinstance(m, AIMessage) and getattr(m, "tool_calls", None)
    )
    return produced, tool_calls


def make_executor_node(
    llm: BaseChatModel,
    tools: list[BaseTool],
    base_system: str,
) -> Callable:
    """Runs a bounded ReAct sub-loop for retrieval, returns evidence + messages."""

    max_iterations = int(__import__("os").environ.get("AGENT_STEP_ITERATION_LIMIT", "5"))

    async def executor_node(state: AgentState) -> dict:
        user_request = _last_human_text(state)

        # Determine if refinement was requested
        refinement = state.get("_refinement")
        discarding = state.get("_discard", False)

        if refinement:
            # Apply refinement hint
            query_text = refinement.get("new_query", refinement.get("query", user_request))
            instruction = (
                f"{refinement.get('refinement_note', 'Try a different approach.')}\n\n"
                f"Please try this query:\n{query_text}"
            )
        else:
            # Normal retrieval with context from prior steps
            prior_steps = state.get("retriever_steps", [])
            if prior_steps:
                attempts = []
                for i, step in enumerate(prior_steps):
                    attempts.append(
                        f"Attempt {i+1}: query='{step.get('query', '')[:80]}' score={step.get('relevance_score', 0):.1f}"
                    )
                context = "\nPrior attempts:\n" + "\n".join(attempts)
            else:
                context = ""
            instruction = f"{user_request}\n\n{context}" if context else user_request

        prompt = f"{_EXECUTOR_PROMPT}\n\n---\n\n{base_system}"

        # Run bounded ReAct sub-loop
        produced, tool_calls_made = await _run_executor_subloop(
            llm=llm,
            tools=tools,
            prompt_text=prompt,
            user_request=instruction,
            max_iterations=max_iterations,
        )

        # Extract answer text
        answer = ""
        for msg in reversed(produced):
            if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
                answer = msg.content.strip()
                break

        if not answer:
            answer = f"Retrieval completed with {tool_calls_made} tool calls. No direct answer produced."

        # Evidence entry
        evidence_entry = {"query": instruction, "content": answer, "relevance": 0.0}

        log.info(
            "executor: tool_calls=%d evidence_len=%d",
            tool_calls_made, len(answer),
        )

        return {
            "evidence": [evidence_entry],
            "messages": produced,
            "total_tool_calls": state.get("total_tool_calls", 0) + tool_calls_made,
        }

    return executor_node


# ---------------------------------------------------------------------------
# Relevance node
# ---------------------------------------------------------------------------


def make_relevance_node(llm: BaseChatModel) -> Callable:
    """Evaluates relevance of each evidence item individually against the user query.

    Paper-aligned: per-document scoring (§4.2) with deterministic 3-way action trigger (§4.3).
    One LLM call scores all items; action is derived from individual scores.
    """

    async def relevance_node(state: AgentState) -> dict:
        user_request = _last_human_text(state)
        evidence = state.get("evidence", [])

        if not evidence:
            return {
                "last_relevance": RelevanceScore(
                    relevance_score=0.0,
                    reason="No evidence retrieved.",
                    needs_refinement=True,
                    refinement_hint="Try different retrieval tools or parameters.",
                )
            }

        # Build per-evidence-item prompt
        evidence_parts = []
        for i, ev in enumerate(evidence):
            content = ev.get("content", "") if isinstance(ev, dict) else str(ev)
            query_str = ev.get("query", "") if isinstance(ev, dict) else ""
            evidence_parts.append(
                f"[E{i}] query='{query_str[:80]}'\ncontent: {content[:600]}"
            )

        upper = state.get("relevance_threshold", 0.7)
        lower = state.get("relevance_threshold_low", 0.3)
        ctx = (
            f"User query:\n{user_request}\n\n"
            f"Retrieved evidence items (score each individually):\n"
            + "\n\n".join(evidence_parts)
            + f"\n\n"
            f"For EACH evidence item [E0], [E1], etc., rate relevance 0.0-1.0.\n"
            f"Then compute the aggregated score (average) and decide action:\n"
            f"  - correct: at least ONE item >= {upper} → synthesize\n"
            f"  - incorrect: ALL items <= {lower} → discard and retry\n"
            f"  - ambiguous: otherwise → keep partial evidence, supplement\n\n"
            f"Output ONLY a JSON object with keys:\n"
            f"  item_scores: list of objects with item_idx and score\n"
            f"  relevance_score: aggregated score (float, average of items >= {lower})\n"
            f"  reason: short explanation\n"
            f"  needs_refinement: boolean\n"
            f"  refinement_hint: string\n"
            f"  action: 'correct' | 'incorrect' | 'ambiguous'\n"
        )

        msgs = [
            SystemMessage(content=_RELEVANCE_PROMPT),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        relevance_data = _parse_relevance_with_items(content)
        if relevance_data is None:
            # Fallback: holistic scoring (original behavior)
            combined = "\n\n".join(ep for ep in evidence_parts)[:6000]
            fallback_ctx = (
                f"User query:\n{user_request}\n\n"
                f"Retrieved evidence:\n{combined}\n\n"
                f"Rate relevance 0.0-1.0 and decide on an action.\n"
                f"Thresholds — correct >= {upper}, incorrect <= {lower}, else ambiguous.\n\n"
                f"Output ONLY a JSON object with keys: "
                f"relevance_score, reason, needs_refinement, refinement_hint, action."
            )
            fallback_msgs = [
                SystemMessage(content=_RELEVANCE_PROMPT),
                HumanMessage(content=fallback_ctx),
            ]
            fb_response = await llm.ainvoke(fallback_msgs)
            fb_content = fb_response.content
            if isinstance(fb_content, list):
                fb_content = fb_content[0].text if fb_content else ""
            relevance = _parse_relevance(fb_content)
            if relevance is None:
                relevance = RelevanceScore(
                    relevance_score=0.5,
                    reason="Failed to parse relevance score, defaulting to medium.",
                    needs_refinement=True,
                    refinement_hint="Try alternative retrieval strategy.",
                )
            return _finalize_relevance(relevance, evidence, state, upper, lower, None)

        return _finalize_relevance(
            relevance_data.relevance,
            evidence,
            state,
            upper,
            lower,
            relevance_data.item_scores,
        )

    return relevance_node


# ---------------------------------------------------------------------------
# Per-item scoring data structure
# ---------------------------------------------------------------------------


class _PerItemRelevance(BaseModel):
    """Parsed per-evidence-item scoring result."""

    relevance: RelevanceScore
    item_scores: list[dict]  # [{"item_idx": int, "score": float}, ...]


def _parse_relevance_with_items(content: str) -> _PerItemRelevance | None:
    """Parse per-item relevance scores + aggregated decision from LLM output."""
    try:
        normalized = _normalize_json_from_qwen(content)
        if not normalized:
            normalized = json.loads(content.strip())
    except (json.JSONDecodeError, TypeError):
        return None

    if not isinstance(normalized, dict):
        return None

    # Extract item_scores
    item_scores_raw = normalized.get("item_scores", [])
    if not isinstance(item_scores_raw, list):
        return None

    item_scores = []
    for item in item_scores_raw:
        if isinstance(item, dict) and "item_idx" in item and "score" in item:
            item_scores.append({
                "item_idx": int(item["item_idx"]),
                "score": float(item["score"]),
            })

    if not item_scores:
        return None

    # Remove item_scores from normalized, use rest for RelevanceScore
    relevance_dict = {k: v for k, v in normalized.items() if k != "item_scores"}
    if "relevance_score" not in relevance_dict:
        return None

    try:
        relevance = RelevanceScore.model_validate(relevance_dict)
    except Exception:
        return None

    return _PerItemRelevance(relevance=relevance, item_scores=item_scores)


def _finalize_relevance(
    relevance: RelevanceScore,
    evidence: list,
    state: AgentState,
    upper: float,
    lower: float,
    item_scores: list[dict] | None,
) -> dict:
    """Apply per-item scores to evidence, enforce action based on paper §4.3 rules."""

    # Paper §4.3: deterministic action from per-item scores
    if item_scores:
        scores = [it["score"] for it in item_scores]
        has_high = any(s >= upper for s in scores)
        all_low = all(s <= lower for s in scores)

        if has_high:
            relevance.action = "correct"
        elif all_low:
            relevance.action = "incorrect"
        else:
            relevance.action = "ambiguous"

        # Compute aggregated score from items above the low threshold
        relevant_scores = [s for s in scores if s > lower]
        if relevant_scores:
            relevance.relevance_score = round(sum(relevant_scores) / len(relevant_scores), 2)
    else:
        # Holistic fallback: single score determines action
        score = relevance.relevance_score
        if score >= upper:
            relevance.action = "correct"
        elif score <= lower:
            relevance.action = "incorrect"
        else:
            relevance.action = "ambiguous"

    # Assign per-item scores to evidence entries
    updated = []
    for i, ev in enumerate(evidence):
        entry = dict(ev)
        if isinstance(entry, dict):
            if item_scores:
                matching = [it for it in item_scores if it["item_idx"] == i]
                if matching:
                    entry["relevance"] = matching[0]["score"]
                else:
                    entry["relevance"] = relevance.relevance_score
            else:
                entry["relevance"] = relevance.relevance_score
        updated.append(entry)

    log.info(
        "relevance: aggregated=%.2f action=%s items=%s scores=%s",
        relevance.relevance_score,
        relevance.action,
        len(item_scores) if item_scores else 0,
        [it["score"] for it in item_scores] if item_scores else "[holistic]",
    )

    if relevance.action == "incorrect":
        return {
            "last_relevance": relevance,
            "refinement_count": state.get("refinement_count", 0) + 1,
            "_discard": True,
        }

    return {
        "last_relevance": relevance,
        "evidence": updated,
        "refinement_count": state.get("refinement_count", 0) + 1,
    }


def _parse_relevance(content: str) -> RelevanceScore | None:
    """Parse RelevanceScore from LLM output."""
    try:
        parser = QwenOutputParser(pydantic_model=RelevanceScore)
        return parser.parse(content)
    except Exception:
        pass

    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict) and "relevance_score" in normalized:
        try:
            return RelevanceScore.model_validate(normalized)
        except Exception:
            pass

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "relevance_score" in parsed:
            return RelevanceScore.model_validate(parsed)
    except json.JSONDecodeError:
        pass

    return None


# ---------------------------------------------------------------------------
# Refine node — used for "ambiguous" action (keep evidence, supplement)
# ---------------------------------------------------------------------------


def make_refine_node(llm: BaseChatModel) -> Callable:
    """Generates a supplementary query to expand partial evidence."""

    async def refine_node(state: AgentState) -> dict:
        user_request = _last_human_text(state)
        relevance = state.get("last_relevance")
        prior_steps = state.get("retriever_steps", [])

        # Build context
        attempts = []
        for i, step in enumerate(prior_steps):
            attempts.append(
                f"Attempt {i+1}: '{step.get('query', '?')[:100]}' → Score: {step.get('relevance_score', 0):.1f}"
            )
        context = "\n".join(attempts) if attempts else "(no prior attempts)"

        hint = relevance.refinement_hint if relevance else "Try a completely different approach."

        ctx = (
            f"User query:\n{user_request}\n\n"
            f"Retrieval history:\n{context}\n\n"
            f"Previous best relevance score: {relevance.relevance_score if relevance else 'N/A'}\n"
            f"Refinement hint: {hint}\n\n"
            f"Generate a NEW, improved query for retrieval. "
            f"Output ONLY a JSON object with keys: query, suggestion.\n"
            f"The query should be specific and testable with MCP tools."
        )

        msgs = [
            SystemMessage(content=_REFINE_PROMPT),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        # Parse query + suggestion
        try:
            parsed = json.loads(content.strip())
            new_query = parsed.get("query", user_request) if isinstance(parsed, dict) else user_request
            suggestion = parsed.get("suggestion", hint) if isinstance(parsed, dict) else hint
        except json.JSONDecodeError:
            new_query = f"{user_request} ({hint})"
            suggestion = hint

        refinement = {
            "new_query": new_query,
            "refinement_note": f"Supplementary retrieval: {suggestion}",
        }

        log.info(
            "refine(ambiguous): attempt %d, new_query=%s",
            state.get("refinement_count", 0) + 1,
            new_query[:100],
        )

        return {
            "_refinement": refinement,
            "_discard": False,  # clear discard flag for next executor run
        }

    return refine_node


# ---------------------------------------------------------------------------
# Uncorrect node — used for "incorrect" action (discard & retry from scratch)
# ---------------------------------------------------------------------------


def make_uncorrect_node(llm: BaseChatModel) -> Callable:
    """Generates a completely fresh query when previous evidence was discarded."""

    async def uncorrect_node(state: AgentState) -> dict:
        user_request = _last_human_text(state)
        relevance = state.get("last_relevance")
        prior_steps = state.get("retriever_steps", [])

        # Build context from failed attempts
        failures = []
        for i, step in enumerate(prior_steps):
            failures.append(
                f"Attempt {i+1}: '{step.get('query', '?')[:100]}' → Score: {step.get('relevance_score', 0):.1f}"
            )
        context = "\n".join(failures) if failures else ""

        hint = relevance.refinement_hint if relevance else "Try a completely different approach."

        ctx = (
            f"User query:\n{user_request}\n\n"
            f"Previous retrieval attempts all failed:\n{context}\n\n"
            f"Refinement hint: {hint}\n\n"
            f"All previous evidence has been discarded. Generate a FRESH query "
            f"using a completely different retrieval strategy.\n"
            f"Output ONLY a JSON object with keys: query, suggestion."
        )

        msgs = [
            SystemMessage(content=_REFINE_PROMPT),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        # Parse query + suggestion
        try:
            parsed = json.loads(content.strip())
            new_query = parsed.get("query", user_request) if isinstance(parsed, dict) else user_request
            suggestion = parsed.get("suggestion", hint) if isinstance(parsed, dict) else hint
        except json.JSONDecodeError:
            new_query = user_request
            suggestion = hint

        refinement = {
            "new_query": new_query,
            "refinement_note": f"Retrieval restart (all previous evidence was discarded): {suggestion}",
        }

        log.info(
            "uncorrect(incorrect): attempt %d, new_query=%s",
            state.get("refinement_count", 0) + 1,
            new_query[:100],
        )

        return {
            "_refinement": refinement,
            "_discard": False,  # already discarded, clear for next executor run
        }

    return uncorrect_node


# ---------------------------------------------------------------------------
# Discard node — clears evidence after "incorrect" action
# ---------------------------------------------------------------------------


def make_discard_node() -> Callable:
    """Resets evidence list when previous retrieval was totally irrelevant."""

    def discard_node(state: AgentState) -> dict:
        old_count = len(state.get("evidence", []))
        log.info("discard: cleared %d stale evidence entries", old_count)
        return {
            "evidence": [],
        }

    return discard_node


# ---------------------------------------------------------------------------
# Synthesizer node
# ---------------------------------------------------------------------------


def make_synthesizer_node(llm: BaseChatModel) -> Callable:
    """Combines evidence into a FinalAnswer."""

    async def synthesizer_node(state: AgentState) -> dict:
        user_request = _last_human_text(state)
        evidence = state.get("evidence", [])
        steps = state.get("retriever_steps", [])

        # Separate by relevance
        high_ev = [e for e in evidence if isinstance(e, dict) and e.get("relevance", 0) >= 0.7]
        medium_ev = [e for e in evidence if isinstance(e, dict) and 0.4 <= e.get("relevance", 0) < 0.7]

        # Build evidence block
        ev_blocks = []
        if high_ev:
            ev_blocks.append("### HIGH-RELEVANCE FINDINGS")
            for i, ev in enumerate(high_ev):
                ev_blocks.append(
                    f"[Evidence {i+1} (relevance={ev.get('relevance', 0):.2f}):\n"
                    f"{ev.get('content', '(empty)')[:600]}"
                )
        if medium_ev:
            ev_blocks.append("\n### PARTIAL FINDINGS")
            for i, ev in enumerate(medium_ev):
                ev_blocks.append(
                    f"[Evidence {i+len(high_ev)+1} (relevance={ev.get('relevance', 0):.2f}):\n"
                    f"{ev.get('content', '(empty)')[:600]}"
                )
        if not ev_blocks:
            ev_blocks.append("(no useful evidence)")

        step_history = "\n".join(
            f"- Attempt {i+1}: '{step.get('query', '?')[:60]}' → {step.get('relevance_score', 0):.1f}"
            for i, step in enumerate(steps)
        ) if steps else "(single attempt)"

        separator = "-----\n"
        ev_text = separator.join(ev_blocks)
        ctx = (
            f"User request:\n{user_request}\n\n"
            f"Retrieval history:\n{step_history}\n\n"
            f"Evidence:\n{ev_text}\n\n"
            f"Synthesize a final answer from this evidence. Cite sources. Note gaps.\n"
            f"Output ONLY a JSON object: {{answer, confidence, unresolved}}"
        )

        msgs = [
            SystemMessage(content=_SYNTHESIZER_PROMPT_FULL),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        final = _parse_final_answer(content)

        # Confidence calibration
        confidences = [ev.get("relevance", 0) for ev in evidence if isinstance(ev, dict)]
        if not confidences:
            final.confidence = "low"
        elif all(c >= 0.7 for c in confidences):
            avg = sum(confidences) / len(confidences)
            if avg >= 0.85:
                final.confidence = "high"
            else:
                final.confidence = "medium"
        elif any(c >= 0.7 for c in confidences):
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
            "synthesize: confidence=%s evidence=%d unresolved=%d steps=%d",
            final.confidence, len(evidence), len(final.unresolved), len(steps),
        )

        # Final retriever step record
        step = RetrieverStep(
            query=user_request,
            relevance_score={
                "high": 1.0,
                "medium": 0.7,
                "low": 0.3,
            }.get(final.confidence, 0.5),
            result_summary=final.answer[:200],
        )
        updated_steps = list(state.get("retriever_steps", [])) + [step]

        # Clear transient flags
        return {
            "messages": [AIMessage(content=rendered)],
            "retriever_steps": updated_steps,
            "_refinement": None,
            "_discard": False,
        }

    return synthesizer_node


def _coerce_final_answer(d: dict) -> dict:
    """Normalize FinalAnswer fields so pydantic validation passes."""
    conf = d.get("confidence")
    if isinstance(conf, (int, float)):
        d["confidence"] = "high" if conf >= 0.7 else ("medium" if conf >= 0.4 else "low")
    elif isinstance(conf, str) and conf not in ("high", "medium", "low"):
        try:
            numeric = float(conf)
            d["confidence"] = "high" if numeric >= 0.7 else ("medium" if numeric >= 0.4 else "low")
        except (ValueError, TypeError):
            d["confidence"] = "low"
    unresolved = d.get("unresolved")
    if not isinstance(unresolved, list):
        d["unresolved"] = [unresolved] if unresolved and unresolved is not False else []
    return d


def _parse_final_answer(content: str) -> FinalAnswer:
    """Parse FinalAnswer from LLM output."""
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
        answer=content.strip()[:2000] if content.strip() else "No results from retrieval pipeline.",
        confidence="low",
        unresolved=["Could not synthesize a confident answer."],
    )


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------


def route_after_relevance(state: AgentState) -> str:
    """Conditional edge after relevance evaluation — 3-way action trigger (Paper §4.3).

    correct → synthesize
    incorrect → discard_evidence → uncorrect → executor
    ambiguous → refine → executor
    """
    relevance = state.get("last_relevance")
    if relevance is None:
        return "synthesize"

    max_refinements = state.get("max_refinements", 3)

    if state.get("refinement_count", 0) >= max_refinements:
        log.info("CRAG: max refinements (%d) reached → synthesize", max_refinements)
        return "synthesize"

    action = getattr(relevance, "action", "correct")
    if action == "correct":
        return "synthesize"
    elif action == "incorrect":
        log.info("CRAG: action=incorrect → discard & uncorrect")
        return "discard"
    else:  # ambiguous
        log.info("CRAG: action=ambiguous → refine & supplement")
        return "refine"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _last_human_text(state: dict) -> str:
    """Extract last human/text content from state messages."""
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
