"""Graph nodes for the ReWOO (Reasoning Without Observation) variant.

Pipeline: START → plan_node → execute_node → synthesize_node → END

The plan_node produces ALL tool calls upfront. The execute_node runs them
all in parallel via asyncio.gather. The synthesize_node combines all
observations into a single FinalAnswer.
"""

import asyncio
import json
import logging
import textwrap
from typing import Any, Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from aas_agent.qwen_parser import QwenOutputParser, _normalize_json_from_qwen
from aas_agent.rewoo_state import FinalAnswer, RewooPlan

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Plan node prompt
# ---------------------------------------------------------------------------

_PLAN_PROMPT = """You are a planner for the ReWOO (Reasoning Without Observation) protocol.

You plan ALL tool calls upfront before any are executed. The tools will run in parallel and their
results come back as observations (E#, E#N, etc.). You do NOT adapt based on intermediate results.

AVAILABLE MCP TOOLS (and example args):
"""

_PLAN_PROMPT_SUFFIX = """
INSTRUCTIONS:
1. Identify everything you need to find in ONE pass.
2. For each piece of information, create a RewooThought:
   - plan: your reasoning step (what you're doing and why)
   - tool_name: which MCP tool to call
   - tool_args: arguments to pass (empty dict {} for parameterless tools)
   - ref_id: evidence reference ID (E1, E2, E3...) — how you'll cite this result later
3. Think of the WHOLE chain at once. DO NOT wait for results.
4. Max {max_thoughts} thoughts. If you need more, combine related queries.
5. Reference prior evidence as E1, E2, etc.
6. Output ONLY a JSON object with keys: thoughts (list of objects) and synthesis_hint (string).

IMPORTANT: Every tool_name MUST be one of the tools listed above. Every tool_args MUST be valid for that tool.
"""


# ---------------------------------------------------------------------------
# Synthesize node prompt
# ---------------------------------------------------------------------------

_SYNTHESIZER_PROMPT = """You are the synthesizer for the ReWOO agent.

You have a complete plan with parallel observations. Synthesize the final answer.

Evidence references are in the format E#, E#N, etc. Each reference points to
a specific observation from a parallel tool call. Use these references when citing evidence.

RULES:
- Be direct and factual. Cite evidence references (E1, E2, etc.).
- Cross-reference evidence between different sources.
- Note gaps where no evidence exists.
- Calibrate confidence: high for verified hits, medium for derived, low for sparse.
- Output ONLY a JSON object: {answer, confidence, unresolved}.
"""


# ---------------------------------------------------------------------------
# Plan node
# ---------------------------------------------------------------------------


def make_plan_node(
    llm: BaseChatModel,
    tool_map: dict[str, BaseTool],
    base_system: str,
    max_thoughts: int,
) -> Callable:
    """Plans ALL tool calls upfront based on the user request."""

    # Build tool reference list from tool_map (include MCP context for available tools)
    tool_refs = _build_tool_refs(tool_map)

    async def plan_node(state: dict) -> dict:
        user_request = _last_human_text(state)

        prompt = (
            f"User request:\n{user_request}\n\n"
            f"{_PLAN_PROMPT}{tool_refs}\n{base_system}\n{_PLAN_PROMPT_SUFFIX.format(max_thoughts=max_thoughts)}\n"
            f"Output ONLY a JSON object with keys: thoughts (list), synthesis_hint (string)."
        )

        msgs: list = [
            SystemMessage(content=_PLAN_PROMPT.replace("{max_thoughts}", str(max_thoughts)).rstrip()),
            HumanMessage(content=prompt),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        plan = _parse_plan(content, max_thoughts)
        if plan is None:
            # Hard fallback: single search_graph call
            log.warning("ReWOO plan parsing failed, falling back to single graph search")
            plan = RewooPlan(
                thoughts=[
                    RewooThought(
                        plan=f"Search the graph for the user's request: {user_request}",
                        tool_name="search_graph",
                        tool_args={"query": user_request},
                        ref_id="E1",
                    )
                ],
                synthesis_hint="Combine the search results into a coherent answer.",
            )

        # Enforce max thoughts
        if len(plan.thoughts) > max_thoughts:
            plan.thoughts = plan.thoughts[:max_thoughts]
            log.info("Truncated plan thoughts from %d to %d", len(plan.thoughts), max_thoughts)

        # Validate tool calls exist
        valid_tools = set(tool_map.keys())
        invalid = []
        for t in plan.thoughts:
            if t.tool_name not in valid_tools:
                invalid.append(t.tool_name)
        if invalid:
            log.warning("Invalid tools in plan: %s", invalid)
            plan.thoughts = [t for t in plan.thoughts if t.tool_name in valid_tools]
            if not plan.thoughts:
                plan = RewooPlan(
                    thoughts=[
                        RewooThought(
                            plan=f"Default fallback: {user_request}",
                            tool_name="search_graph",
                            tool_args={"query": user_request},
                            ref_id="E1",
                        )
                    ],
                    synthesis_hint="Use the default search results to answer the user request.",
                )

        return {
            "plan": plan,
            "observations": {},
        }

    return plan_node


def _build_tool_refs(tool_map: dict[str, BaseTool]) -> str:
    """Build a reference list of available tools with name, description AND argument schema."""
    refs = []
    for name, tool in sorted(tool_map.items()):
        desc = getattr(tool, "description", "")[:120]
        args_schema = getattr(tool, "args_schema", None)
        params_text = ""
        if args_schema is not None:
            try:
                if hasattr(args_schema, "model_json_schema"):
                    schema = args_schema.model_json_schema()
                elif hasattr(args_schema, "schema"):
                    schema = args_schema.schema()
                else:
                    schema = {}
                props = schema.get("properties", {})
                if props:
                    param_lines = []
                    for fname, finfo in props.items():
                        ftype = finfo.get("type", "str")
                        fdesc = finfo.get("description", "")
                        param_lines.append(f"    - `{fname}` ({ftype})")
                        if fdesc:
                            param_lines[-1] += f" — {fdesc[:80]}"
                    params_text = "\n" + "\n".join(param_lines)
            except Exception:
                pass
        refs.append(f"  • **{name}**: {desc}")
        if params_text:
            refs.append(f"    Args:{params_text}")
    return "\n".join(refs)


def _parse_plan(content: str, max_thoughts: int) -> RewooPlan | None:
    """Parse RewooPlan from LLM output."""
    try:
        parser = QwenOutputParser(pydantic_model=RewooPlan)
        plan = parser.parse(content)
        # Filter to valid tools (we don't have tool_map here, so allow all)
        return plan
    except Exception:
        pass

    normalized = _normalize_json_from_qwen(content)
    if normalized and isinstance(normalized, dict) and "thoughts" in normalized:
        try:
            return RewooPlan.model_validate(normalized)
        except Exception:
            pass

    try:
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and "thoughts" in parsed:
            return RewooPlan.model_validate(parsed)
    except json.JSONDecodeError:
        pass

    return None


# ---------------------------------------------------------------------------
# Execute node — parallel execution
# ---------------------------------------------------------------------------


def make_execute_node(
    tool_map: dict[str, BaseTool],
    max_batch_size: int,
) -> Callable:
    """Executes ALL planned tool calls in parallel batches."""

    async def execute_node(state: dict) -> dict:
        plan = state.get("plan")
        if plan is None:
            return {"observations": {}, "thoughts": []}

        tasks = []
        for thought in plan.thoughts:
            tasks.append({
                "thought": thought,
                "tool_name": thought.tool_name,
                "tool_args": thought.tool_args,
                "ref_id": thought.ref_id,
            })

        # Execute in parallel batches
        observations = {}
        for i in range(0, len(tasks), max_batch_size):
            batch = tasks[i:i + max_batch_size]
            batch_obs = await _execute_batch(batch, tool_map)
            observations.update(batch_obs)

        log.info("execute: %d observations from %d tasks", len(observations), len(tasks))

        return {
            "observations": observations,
            "thoughts": [
                {"plan": t.plan, "tool_name": t.tool_name, "tool_args": t.tool_args, "ref_id": t.ref_id}
                for t in plan.thoughts
            ],
        }

    return execute_node


async def _execute_batch(
    batch: list[dict],
    tool_map: dict[str, BaseTool],
) -> dict[str, str]:
    """Execute a batch of tool calls in parallel, return {ref_id: observation}."""
    coros = []
    for task in batch:
        coros.append(_execute_single(task, tool_map))

    results = await asyncio.gather(*coros, return_exceptions=True)

    observations = {}
    for task, result in zip(batch, results):
        ref_id = task["ref_id"]
        if isinstance(result, Exception):
            observations[ref_id] = f"Error executing {task['tool_name']}: {result}"
        else:
            observations[ref_id] = result

    return observations


async def _execute_single(task: dict, tool_map: dict[str, BaseTool]) -> str:
    """Execute a single tool call and return the observation text."""
    tool_name = task["tool_name"]
    tool_args = task["tool_args"] if task["tool_args"] else {}
    tool = tool_map.get(tool_name)

    if tool is None:
        return f"Tool '{tool_name}' not found in available tools."

    try:
        result = await tool.ainvoke(tool_args)
        content = getattr(result, "content", str(result))
        # Truncate to avoid overwhelming the synthesizer
        if isinstance(content, str) and len(content) > 3000:
            content = content[:3000] + "\n... [truncated]"
        return content
    except Exception as exc:
        return f"Tool '{tool_name}' failed: {exc}"


# ---------------------------------------------------------------------------
# Synthesize node
# ---------------------------------------------------------------------------


def make_synthesize_node(llm: BaseChatModel) -> Callable:
    """Combines all observations into a FinalAnswer."""

    async def synthesize_node(state: dict) -> dict:
        plan = state.get("plan")
        observations = state.get("observations", {})
        thoughts = state.get("thoughts", [])
        user_request = _last_human_text(state)

        if not plan:
            return {
                "messages": [AIMessage(content="No plan was generated. No answer available.")],
            }

        # Build observations block
        obs_blocks = []
        for t in plan.thoughts:
            ref_id = t.ref_id if hasattr(t, "ref_id") else thoughts[plan.thoughts.index(t)].get("ref_id", "??") if isinstance(t, dict) else ""
            observation = observations.get(ref_id, f"(no observation for {ref_id})")

            thought_desc = t.plan if hasattr(t, "plan") else t.get("plan", "??")
            tool_name = t.tool_name if hasattr(t, "tool_name") else t.get("tool_name", "??")

            obs_blocks.append(
                f"--- {ref_id} (thought: {thought_desc[:80]}) ---\n"
                f"Tool: {tool_name}\nObservation:\n{observation}"
            )

        observation_block = "\n\n".join(obs_blocks)

        # Build synthesis context
        synthesis_hint = plan.synthesis_hint if hasattr(plan, "synthesis_hint") else ""
        synthesis_context = f"Synthesis guidance: {synthesis_hint}\n\n" if synthesis_hint else ""

        ctx = (
            f"User request:\n{user_request}\n\n"
            f"{synthesis_context}"
            f"Observations:\n{observation_block}\n\n"
            f"Synthesize a unified answer from these parallel observations. "
            f"Reference evidence by its ID (E1, E2, etc.). "
            f"Note any gaps where an observation is missing or empty.\n\n"
            f"Output ONLY a JSON object with keys: answer, confidence, unresolved."
        )

        msgs: list = [
            SystemMessage(content=_SYNTHESIZER_PROMPT),
            HumanMessage(content=ctx),
        ]

        response = await llm.ainvoke(msgs)
        content = response.content
        if isinstance(content, list):
            content = content[0].text if content else ""

        final = _parse_final_answer(content)

        # Confidence calibration based on observation quality
        valid_observations = [
            obs for obs in observations.values()
            if obs and "error" not in obs.lower() and "not found" not in obs.lower()
        ]
        if len(valid_observations) < len(plan.thoughts):
            final.confidence = "medium"  # some failed
        elif all("not found" in obs.lower() for obs in valid_observations):
            final.confidence = "medium"  # everything returned nothing
        elif len(valid_observations) >= max(2, len(plan.thoughts) * 0.7):
            final.confidence = "high"
        else:
            final.confidence = "medium"

        # Render with metadata
        text = final.answer.rstrip()
        meta_lines = [f"**confidence:** {final.confidence}"]
        if final.unresolved:
            meta_lines.append("**unresolved:**")
            for u in final.unresolved:
                meta_lines.append(f"- {u}")

        # Add reasoning block
        plan_json = plan.model_dump_json(indent=2) if hasattr(plan, "model_dump_json") else str(plan)
        obs_json = json.dumps(observations, indent=2) if observations else "()"
        rendered = (
            text + "\n\n<think>\n"
            f"Plan:\n{plan_json}\n\n"
            f"Observations:\n{obs_json}\n\n"
            + "\n".join(meta_lines) + "\n</think>\n"
        )

        log.info(
            "synthesize: confidence=%s observations=%d unresolved=%d thoughts=%d",
            final.confidence, len(observations), len(final.unresolved), len(plan.thoughts),
        )

        return {"messages": [AIMessage(content=rendered)]}

    return synthesize_node


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
        answer=content.strip()[:2000] if content.strip() else "No observations available.",
        confidence="low",
        unresolved=["Could not synthesize from parallel observations."],
    )


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
