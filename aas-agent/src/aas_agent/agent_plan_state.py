"""State and Pydantic schemas for the plan/reflect agent variant.

The schemas here are *contracts with the LLM* — every Field description is
sent verbatim to the model via the system/user prompts, so they double as
inline prompts. Keep them short, imperative, and unambiguous.
"""

from operator import add
from typing import Annotated, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.managed.is_last_step import RemainingSteps
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class Step(BaseModel):
    """A single, atomic step the executor will carry out with tool calls."""

    id: int | None = Field(
        default=None,
        description="1-based step index (auto-assigned if not provided).",
    )
    intent: str = Field(
        description="What this step achieves, in one sentence. Phrase as a goal, not a tool call."
    )
    suggested_tool: str | None = Field(
        default=None,
        description="Optional tool hint. The executor may deviate if a better choice becomes obvious."
    )
    success_criteria: str = Field(
        description="Concrete observable that marks the step as done. Empty results count as evidence."
    )


class Plan(BaseModel):
    """The plan the planner produces before any tool is called."""

    goal: str = Field(
        description="Restate the user's request in one sentence, in English."
    )
    steps: list[Step] = Field(
        description="1 to 5 steps. Use a single step for deterministic queries; multiple steps when the asset must first be disambiguated."
    )
    fallback_notes: str = Field(
        default="",
        description="What to try if the primary plan yields nothing. Plain text, may be empty."
    )

    def auto_assign_step_ids(self) -> "Plan":
        """Auto-assign 1-based step indices if they were not provided by the model."""
        for i, step in enumerate(self.steps, start=1):
            if step.id is None or step.id == 0:
                step.id = i
        return self


class Evidence(BaseModel):
    """A single fact the executor learned from a tool call."""

    source: Literal["graph", "document", "concept", "manual", "spec", "other"] = Field(
        description="Where this fact came from: graph, document, manual, spec, or other."
    )
    tool: str = Field(description="Name of the MCP tool that produced the fact.")
    summary: str = Field(
        description="1-2 sentences capturing what was learned."
    )


class Reflection(BaseModel):
    """The reflector's decision after a step's tool calls completed."""

    decision: Literal[
        "step_done", "step_retry", "replan", "give_up", "all_done"
    ] = Field(
        description="step_done = step satisfied; step_retry = same step with hint; replan = plan no longer fits; give_up = cannot satisfy; all_done = last step finished."
    )
    evidence_collected: list[str] = Field(
        default_factory=list,
        description="Bullet-style facts learned in this step. Empty results count as evidence."
    )
    next_action_hint: str = Field(
        default="",
        description="For step_retry/replan: concrete hint what to change. Ignored for other decisions.",
    )
    reasoning: str = Field(
        description="One short paragraph justifying the decision."
    )


class FinalAnswer(BaseModel):
    """The structured response the finalizer emits to the user."""

    answer: str = Field(
        description="User-facing answer. Be concise and actionable. Cite sources inline. Do not fabricate."
    )
    evidence: list[Evidence] = Field(
        default_factory=list,
        description="All facts the answer rests on, with source and tool."
    )
    confidence: Literal["high", "medium", "low"] = Field(
        description="high = direct verified hit; medium = derived from partial matches; low = sparse or contradictory evidence."
    )
    unresolved: list[str] = Field(
        default_factory=list,
        description="Things the user asked for that could NOT be determined, each with a short reason."
    )


class AgentState(TypedDict):
    """Shared state for the plan/reflect StateGraph.

    ``messages`` carries the transcript and is the only field streamed
    back to the API layer. All other fields are internal control state.
    """

    messages: Annotated[list[BaseMessage], add_messages]
    plan: Plan | None
    current_step_idx: int
    step_attempts: int
    total_tool_calls: int
    replan_count: int
    evidence: Annotated[list[Evidence], add]
    last_reflection: Reflection | None
    remaining_steps: RemainingSteps
