"""State and Pydantic schemas for the Reflexion variant.

Reflexion (Shinn et al. 2023) — agent with iterative self-reflection:
  1. Executor attempts to answer using ReAct
  2. Evaluator judges the answer for correctness/completeness
  3. If inadequate, a reflection node generates verbal feedback
  4. Loop repeats with the feedback injected as additional context
  5. Finalizer produces the answer when evaluator approves or max trials exhausted
"""

from typing import Annotated, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.managed.is_last_step import RemainingSteps
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class Judgment(BaseModel):
    """Evaluator's judgment of an attempted answer."""

    score: float = Field(ge=0.0, le=1.0, description="Quality score: 0.0 = useless, 1.0 = excellent.")
    verdict: Literal["accept", "revise"] = Field(
        description="accept = good enough to return; revise = needs improvement."
    )
    missing: list[str] = Field(
        default_factory=list,
        description="Facts or aspects that are missing or incorrect in the answer."
    )
    reason: str = Field(
        description="Explanation of the judgment and what to fix."
    )


class ReflectionFeedback(BaseModel):
    """Reflection feedback generated after a failed judgment."""

    strategy_hint: str = Field(
        description="Concrete advice on how to improve the next attempt. What to try differently?"
    )
    common_pitfalls: list[str] = Field(
        default_factory=list,
        description="Things to avoid based on the failure."
    )
    focus_areas: list[str] = Field(
        default_factory=list,
        description="Specific areas the executor should pay attention to."
    )


class FinalAnswer(BaseModel):
    """The final answer synthesized by the finalizer."""

    answer: str = Field(description="User-facing answer. Be concise, factual, and actionable.")
    confidence: Literal["high", "medium", "low"] = Field(description="high = accepted by evaluator; medium = best attempt but low score; low = very uncertain.")
    unresolved: list[str] = Field(default_factory=list, description="Things that could not be determined.")


class TrialRecord(BaseModel):
    """Record of one reflexion trial."""

    trial: int
    score: float
    verdict: Literal["accept", "revise"]
    summary: str


class ReflexionState(TypedDict):
    """Shared state for the Reflexion StateGraph."""

    messages: Annotated[list[BaseMessage], add_messages]
    judgment: Judgment | None
    reflection: ReflectionFeedback | None
    feedback_history: list[str]  # verbal feedback, accumulated by the reflect node which returns the full list
    trial_records: list[TrialRecord]  # history of all trials
    current_trial: int
    max_trials: int
    accept_threshold: float
    last_answer_text: str  # most recent executor answer (overwritten each trial)
    best_answer_text: str  # highest-scored answer across all trials
    remaining_steps: RemainingSteps
