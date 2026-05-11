"""Graph nodes for the CRAG (Context Retrieval Augmented Generation) variant.

Pipeline: executor → relevance → (refine → executor) → synthesizer

Each node factory receives its LLM and tools to avoid rebuilding inside nodes.
"""

import asyncio
import json
import logging
from typing import Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from aas_agent.crag_state import AgentState, FinalAnswer, RetrieverStep, RelevanceScore
from aas_agent.qwen_parser import QwenOutputParser, _normalize_json_from_qwen

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Worker system prompts (injected into executor + refinements)
# ---------------------------------------------------------------------------

_EXECUTOR_PROMPT = """You are a retrieval specialist for the AAS Maintenance Assistant.

You have access to multiple MCP tools including graph queries (search_graph, get_asset,
list_assets), manual/document lookups (get_manual_page, get_manual_index), and template
discovery (search_idt_templates).

Your job: retrieve the BEST possible information to answer the user's query.
- Try multiple search approaches if the first query seems unfruitful.
- Cross-reference evidence between graph, manual, and template sources.
- For each source, try at least one alternative phrasing.
- Be thorough — the quality of your retrieval directly determines the quality of the final answer.
- Never fabricate content — if nothing matches, report that clearly.
- Do NOT synthesize a final answer — just retrieve and report your findings.
"""

_RELEVANCE_PROMPT = """You are a relevance evaluator. Judge how well the retrieved evidence
answers a user query. Rate relevance 0.0-1.0 and explain your scoring.
State whether refinement is needed (with a concrete hint) or not.
"""

_REFINE_PROMPT = """You are a query refiner for the AAS Maintenance Assistant.
Generate a BETTER query or alternative search strategy for the next retrieval attempt.
Output ONLY a JSON object with keys: query (string), suggestion (string describing what to try differently).
"""

_SYNTHESIZER_PROMPT = """You are a synthesizer. Combine the retrieved evidence into
a final answer. Use HIGH-RELEVANCE findings as primary evidence. State gaps clearly.
Output ONLY a JSON object with keys: answer, confidence, unresolved (list).
"""


# ---------------------------------------------------------------------------
# Executor node — bounded ReAct sub-loop (like plan_reflect's executor)
# ---------------------------------------------------------------------------


async def _run_executor_subloop(
    llm: BaseChatModel,
    tools: list[BaseTool],
    prompt_text: str,
    user_request: str,
    max_iterations: int = 5,
) -> tuple[list[BaseMessage], int]:
    """Bounded ReAct loop — same pattern as plan_reflect's executor."""
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

    return messages, tool_calls


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
        if refinement:
            # Apply refinement hint
            query_text = refinement.get("new_query", refinement.get("query", user_request))
            instruction = (
                f"Previous retrieval attempts failed.\n"
                f"{refinement.get('refinement_note', refinement.get('suggestion', 'Try a different approach.'))}\n\n"
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
    """Evaluates relevance of retrieved evidence against the user query."""

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

        # Combine evidence for evaluation
        evidence_parts = []
        for i, ev in enumerate(evidence):
            content = ev.get("content", "") if isinstance(ev, dict) else str(ev)
            evidence_parts.append(f"--- Evidence {i+1} ---\n{content[:1200]}")

        combined = "\n\n".join(evidence_parts)

        ctx = (
            f"User query:\n{user_request}\n\n"
            f"Retrieved evidence:\n{combined}\n\n"
            f"Rate relevance 0.0-1.0 and explain. Include needs_refinement and refinement_hint.\n"
            f"Output ONLY a JSON object with keys: relevance_score, reason, needs_refinement, refinement_hint."
        )

        msgs = [
            SystemMessage(content=_RELEVANCE_PROMPT),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        relevance = _parse_relevance(content)
        if relevance is None:
            relevance = RelevanceScore(
                relevance_score=0.5,
                reason="Failed to parse relevance score, defaulting to medium.",
                needs_refinement=True,
                refinement_hint="Try alternative retrieval strategy.",
            )

        return {
            "last_relevance": relevance,
        }

    return relevance_node


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
# Refine node
# ---------------------------------------------------------------------------


def make_refine_node(llm: BaseChatModel) -> Callable:
    """Generates a new query based on low relevance feedback."""

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
            "refinement_note": f"Query refinement: {suggestion}",
        }

        log.info(
            "refine: attempt %d, new_query=%s",
            state.get("refinement_count", 0) + 1,
            new_query[:100],
        )

        return {"_refinement": refinement}

    return refine_node


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

        ctx = (
            f"User request:\n{user_request}\n\n"
            f"Retrieval history:\n{step_history}\n\n"
            f"Evidence:\n{'---\n'.join(ev_blocks)}\n\n"
            f"Synthesize a final answer from this evidence. Cite sources. Note gaps.\n"
            f"Output ONLY a JSON object: {{answer, confidence, unresolved}}"
        )

        msgs = [
            SystemMessage(content=_SYNTHESIZER_PROMPT),
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
                final.confidence = "high"
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
        updated_steps = list(steps) + [step]

        return {
            "messages": [AIMessage(content=rendered)],
            "retriever_steps": updated_steps,
        }

    return synthesizer_node


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
            return FinalAnswer.model_validate(normalized)
        except Exception:
            pass

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "answer" in parsed and "confidence" in parsed:
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
    """Conditional edge after relevance evaluation."""
    relevance = state.get("last_relevance")
    if relevance is None:
        return "synthesize"

    max_refinements = state.get("max_refinements", 3)
    threshold = state.get("relevance_threshold", 0.7)

    if relevance.relevance_score >= threshold:
        return "synthesize"

    if state.get("refinement_count", 0) >= max_refinements:
        log.info("CRAG: max refinements (%d) reached → synthesize", max_refinements)
        return "synthesize"

    if relevance.needs_refinement:
        return "refine"

    return "synthesize"


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
