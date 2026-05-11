"""Graph nodes for the agent-supervisor variant.

The supervisor decomposes a query into worker sub-tasks. An orchestrator
node runs each worker as a compiled ReAct sub-graph (built at init time).
The synthesizer combines all findings.

Architecture:
  START → supervisor_node → orchestrator_node → synthesize_node → END
"""

import asyncio
import json
import logging
from typing import Any, Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from aas_agent.agent_supervisor_state import (
    AgentState,
    FinalAnswer,
    SupervisorDecision,
    SupervisorTask,
    WorkerResult,
)
from aas_agent.qwen_parser import QwenOutputParser, _normalize_json_from_qwen

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Worker sub-graph system prompts
# ---------------------------------------------------------------------------

_WORKER_PROMPTS = {
    "work_graph": """You are a graph specialist for the AAS Maintenance Assistant.

You have access to Neo4j graph data through MCP tools (search_graph, get_asset,
list_assets, etc.). Answer queries about asset relationships, equipment layout,
connectivity, and structural data.

Rules:
- Use Cypher queries to explore the graph.
- Cite AAS IDs, Asset names, and relationship types in findings.
- Never fabricate results — if nothing matches, say so clearly.
- Be thorough: try alternative query phrasings if the first attempt is unfruitful.""",

    "work_document": """You are a document specialist for the AAS Maintenance Assistant.

You have access to equipment manuals, documentation, and reference materials
through MCP tools (get_manual_page, get_manual_index, etc.). Answer queries
about procedures, specifications, and operational guides.

Rules:
- Search the manual index first when unsure which page to look at.
- Quote exact sections when possible.
- Cite which manual/page the information came from.
- Never fabricate content — if nothing matches, say so clearly.""",

    "work_template": """You are a data-structure specialist for the AAS Maintenance Assistant.

You investigate ITD templates, submodel schemas, element types, and AAS structure
through MCP tools (search_idt_templates, get_template_info, etc.). Determine which
template or structure matches a query about AAS data layout.

Rules:
- Discover the right template before diving into detailed queries.
- Explain which structural hypotheses you're testing.
- Cite template IDs, element types, and semantic IDs.
- Never guess templates — confirm with actual tool results.""",
}

_WORKER_TOOLS = {
    "work_graph": ["search_graph", "get_asset", "list_assets"],
    "work_document": ["get_manual_page", "get_manual_index", "search_manual"],
    "work_template": ["search_idt_templates", "get_template_info"],
}

# ---------------------------------------------------------------------------
# Supervisor system prompt
# ---------------------------------------------------------------------------

_SUPERVISOR_PROMPT = """You are a supervisor coordinating specialist workers for a factory maintenance assistant.

Analyze the user's request and create sub-tasks, assigning each to exactly one
worker. Workers are specialists:

- **work_graph**: Neo4j graph queries, asset lookups, relationship traversal.
- **work_document**: Manual pages, PDF content, documentation lookup.
- **work_template**: ITD template discovery, schema/element type investigation.

Rules:
1. Create MINIMUM necessary tasks. If one worker can answer fully, use only that one.
2. Create multiple tasks in PARALLEL only when the query truly spans domains.
3. Each task must have a clear, self-contained instruction.
4. Output ONLY a JSON object with key "tasks" (list of task objects).
"""

# ---------------------------------------------------------------------------
# Supervisor node
# ---------------------------------------------------------------------------


def make_supervisor_node(llm: BaseChatModel) -> Callable:
    """Decomposes the user request into SupervisorTask[]."""

    async def supervisor_node(state: AgentState) -> dict:
        user_request = _last_human_text(state["messages"])

        prior_results = state.get("_prior_results", [])
        prior_context = ""
        if prior_results:
            parts = []
            for wr in prior_results:
                parts.append(
                    f"Previous result (task {wr.get('task_id')}, worker {wr.get('worker')}):\n"
                    f"  Finding: {wr.get('finding', '')[:200]}\n  Confidence: {wr.get('confidence', '?')}"
                )
            prior_context = "\n\nPrior results to consider:\n" + "\n".join(parts)

        msgs: list = [
            SystemMessage(content=_SUPERVISOR_PROMPT),
            HumanMessage(content=f"User request:\n{user_request}{prior_context}\n\n"
                                 f"Output ONLY a JSON object with key 'tasks'."),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        # Parse SupervisorDecision
        decision = _parse_supervisor_output(content)
        if decision is None:
            # Hard fallback: single work_graph task
            log.warning("Supervisor failed to parse, falling back to graph scan")
            decision = SupervisorDecision(tasks=[
                SupervisorTask(
                    task_id=0,
                    worker="work_graph",
                    instruction=user_request,
                    expected_output="graph_query_result",
                )
            ])

        # Auto-assign task ids
        for i, task in enumerate(decision.tasks):
            if task.task_id is None:
                task.task_id = i

        log.info("supervisor: %d tasks dispatched", len(decision.tasks))

        return {
            "plan": decision,
            "task_queue": decision.tasks,
        }

    return supervisor_node


def _parse_supervisor_output(content: str) -> SupervisorDecision | None:
    """Try various JSON parsing strategies for supervisor output."""
    # Strategy 1: Qwen parser
    try:
        parser = QwenOutputParser(pydantic_model=SupervisorDecision)
        return parser.parse(content)
    except Exception:
        pass

    # Strategy 2: normalize + validate
    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict) and "tasks" in normalized:
        try:
            return SupervisorDecision.model_validate(normalized)
        except Exception:
            pass

    # Strategy 3: try raw JSON
    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "tasks" in parsed:
            return SupervisorDecision.model_validate(parsed)
    except json.JSONDecodeError:
        pass

    # Strategy 4: extract JSON object from mixed text
    try:
        extracted = _extract_json_from_text(content)
        if extracted and "tasks" in extracted:
            return SupervisorDecision.model_validate(extracted)
    except Exception:
        pass

    return None


def _extract_json_from_text(text: str) -> dict | None:
    """Find the outermost JSON object in text."""
    depth = 0
    start = -1
    for i, ch in enumerate(text):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start >= 0:
                try:
                    return json.loads(text[start:i+1])
                except json.JSONDecodeError:
                    pass
    return None


# ---------------------------------------------------------------------------
# Orchestrator node — runs worker sub-graphs in parallel
# ---------------------------------------------------------------------------


def make_orchestrator_node(
    worker_subgraphs: dict[str, Any],
) -> Callable:
    """Runs all tasks in the task_queue as parallel worker sub-graphs."""

    async def orchestrator_node(state: AgentState) -> dict:
        plan = state.get("plan")
        if plan is None:
            # No plan — supervisor didn't run or failed
            return {"worker_results": []}

        tasks = plan.tasks
        if not tasks:
            return {"worker_results": []}

        # Build one invocation per task
        invocations = []
        for task in tasks:
            worker_name = task.worker
            if worker_name not in worker_subgraphs:
                log.warning("Worker '%s' not found, skipping task %d", worker_name, task.task_id)
                continue

            subgraph, task_prompt = worker_subgraphs[worker_name]
            agent = subgraph  # pre-compiled StateGraph
            lc_messages = _to_lc_messages(task, task_prompt)

            invocations.append({
                "task": task,
                "agent": agent,
                "lc_messages": lc_messages,
            })

        if not invocations:
            return {"worker_results": []}

        # Run all workers in parallel
        results = await asyncio.gather(
            *[
                _run_worker(inv["task"], inv["agent"], inv["lc_messages"])
                for inv in invocations
            ],
            return_exceptions=True,
        )

        # Aggregate results
        worker_results: list[WorkerResult] = []
        for task, result in zip([inv["task"] for inv in invocations], results):
            if isinstance(result, Exception):
                log.error("Worker %s (task %d) failed: %s", task.worker, task.task_id, result)
                worker_result = WorkerResult(
                    task_id=task.task_id,
                    worker=task.worker,
                    finding=f"Worker '{task.worker}' failed: {result}",
                    details=f"Error running worker {task.worker} for task {task.task_id}.",
                    confidence="low",
                )
            else:
                worker_result = WorkerResult(
                    task_id=task.task_id,
                    worker=task.worker,
                    finding=result["finding"],
                    details=result["details"],
                    confidence=result["confidence"],
                )
            worker_results.append(worker_result)

        log.info("orchestrator: completed %d of %d tasks", len(worker_results), len(tasks))

        return {"worker_results": worker_results}

    return orchestrator_node


async def _run_worker(
    task: SupervisorTask,
    agent: Any,
    lc_messages: list,
) -> dict:
    """Run a single worker sub-graph and return {finding, details, confidence}."""
    try:
        result = await agent.ainvoke(
            {"messages": lc_messages},
            config={"recursion_limit": 50},
        )
    except Exception as e:
        raise e

    # Extract answer text
    answer_text = ""
    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
            answer_text = msg.content.strip()
            break

    if not answer_text:
        return {
            "finding": f"Worker '{task.worker}' produced no output.",
            "details": "Empty output from worker sub-graph.",
            "confidence": "low",
        }

    # Confidence heuristic
    fl = answer_text.lower()
    if any(kw in fl for kw in ["error", "exception", "failed", "unhandled"]):
        confidence = "low"
    elif any(kw in fl for kw in ["not found", "no results", "does not exist", "returned nothing"]):
        confidence = "medium"
    else:
        confidence = "high"

    # Extract top-level finding (first 2-3 sentences)
    sentences = [s.strip() for s in answer_text.replace("\n", ". ").split(". ") if s.strip()]
    finding = ". ".join(sentences[:3]) + "." if sentences else answer_text[:200]

    return {
        "finding": finding,
        "details": answer_text,
        "confidence": confidence,
    }


def _to_lc_messages(task: SupervisorTask, task_prompt: str) -> list:
    """Convert a task into LangChain messages for the worker sub-graph."""
    return [
        HumanMessage(content=task_prompt),
        HumanMessage(
            content=(
                f"Task {task.task_id} ({task.worker}):\n"
                f"{task.instruction}\n\n"
                f"Expected output: {task.expected_output}\n\n"
                f"Complete this task. Be thorough, cite your tools, and do not fabricate results."
            )
        ),
    ]


# ---------------------------------------------------------------------------
# Synthesize node
# ---------------------------------------------------------------------------


def make_synthesize_node(llm: BaseChatModel, finalizer_prompt: str | None = None) -> Callable:
    """Combines all worker results into a FinalAnswer."""

    async def synthesize_node(state: AgentState) -> dict:
        results = state.get("worker_results", [])
        plan = state.get("plan")

        user_request = _last_human_text(state["messages"])

        # Build evidence block from worker results
        ev_blocks = []
        for wr in results:
            if isinstance(wr, WorkerResult):
                ev_blocks.append(
                    f"[Task {wr.task_id} / {wr.worker}] "
                    f"Confidence: {wr.confidence}\n"
                    f"Finding: {wr.finding}\n"
                    f"Details: {wr.details}"
                )
            elif isinstance(wr, dict):
                # Raw result dict from orchestrator (fallback)
                ev_blocks.append(
                    f"[Worker {wr.get('worker', '?')}] "
                    f"Confidence: {wr.get('confidence', '?')}\n"
                    f"Finding: {wr.get('finding', '(empty)')[:300]} "
                )
            else:
                ev_blocks.append(str(wr))

        evidence_block = "\n\n".join(ev_blocks) or "(no results from workers)"

        # Determine overall confidence
        confidences = [wr.confidence if isinstance(wr, WorkerResult) else wr.get("confidence", "low") for wr in results]
        if not confidences:
            overall_confidence = "low"
        elif all(c == "high" for c in confidences):
            overall_confidence = "high"
        elif any(c == "low" for c in confidences):
            overall_confidence = "medium"
        else:
            overall_confidence = "high"

        ctx = (
            f"User request:\n{user_request}\n\n"
            f"Worker results:\n{evidence_block}\n\n"
            f"Synthesize a unified answer from these worker findings. "
            f"Be direct and factual. Cite which workers provided which findings. "
            f"Note any unresolved aspects.\n\n"
            f"Output ONLY a JSON object with keys: answer, confidence, unresolved."
        )

        msgs: list = [
            SystemMessage(content=finalizer_prompt or "You are a supervisor that synthesizes findings from specialist worker agents."),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        final = _parse_final_answer(content)

        # Ensure overall confidence accounts for all workers
        if final.confidence == "high" and overall_confidence != "high":
            final.confidence = overall_confidence

        # Render with metadata
        text = final.answer.rstrip()
        meta_lines = [f"**confidence:** {final.confidence}"]
        if final.unresolved:
            meta_lines.append("**unresolved:**")
            for u in final.unresolved:
                meta_lines.append(f"- {u}")

        rendered = text + "\n\n<think>\n" + "\n".join(meta_lines) + "\n</think>\n"

        log.info(
            "synthesize: confidence=%s results=%d unresolved=%d",
            final.confidence, len(results), len(final.unresolved),
        )

        return {"messages": [AIMessage(content=rendered)]}

    return synthesize_node


def _parse_final_answer(content: str) -> FinalAnswer:
    """Parse FinalAnswer from LLM output with various strategies."""
    try:
        parser = QwenOutputParser(pydantic_model=FinalAnswer)
        return parser.parse(content)
    except Exception:
        pass

    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict):
        required_keys = {"answer", "confidence"}
        if required_keys.issubset(normalized.keys()):
            if isinstance(normalized.get("unresolved"), str):
                normalized["unresolved"] = [normalized["unresolved"]] if normalized["unresolved"] else []
            return FinalAnswer.model_validate(normalized)

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "answer" in parsed and "confidence" in parsed:
            if isinstance(parsed.get("unresolved"), str):
                parsed["unresolved"] = [parsed["unresolved"]] if parsed["unresolved"] else []
            return FinalAnswer.model_validate(parsed)
    except json.JSONDecodeError:
        pass

    # Fallback: bare text as answer
    return FinalAnswer(
        answer=content.strip()[:2000] if content.strip() else "No results from workers.",
        confidence="low",
        unresolved=["Could not determine answer from worker results."],
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _last_human_text(messages: list[dict]) -> str:
    """Return the most recent human-text from the original messages."""
    for msg in reversed(messages):
        if isinstance(msg, dict):
            role = msg.get("role", "")
            content = msg.get("content", "")
        else:
            role = getattr(msg, "type", "")
            content = getattr(msg, "content", "")
        if role in ("human", "user") and content:
            return content if isinstance(content, str) else str(content)
    return ""
