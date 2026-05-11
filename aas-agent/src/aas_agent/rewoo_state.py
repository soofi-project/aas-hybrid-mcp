"""State and Pydantic schemas for the ReWOO (Reasoning Without Observation) variant.

ReWOO eliminates the sequential ReAct loop by:
1. Planning ALL tool calls upfront (Thought + ToolCall pairs)
2. Executing them in parallel via asyncio.gather
3. Synthesizing from all observations at once
"""

from typing import Annotated, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.managed.is_last_step import RemainingSteps
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class RewooPlan(BaseModel):
    """The full plan ReWOO produces upfront before any tool is called."""

    thoughts: list["RewooThought"] = Field(
        description="Each thought contains a plan, the tool call to execute, and the result placeholder."
    )
    synthesis_hint: str = Field(
        default="",
        description="Guidance for the final synthesis step. What to look for, what to cross-reference."
    )


class RewooThought(BaseModel):
    """A single thought with its associated tool call."""

    plan: str = Field(
        description="Reasoning step — what you're doing and why. Reference E# for prior evidence."
    )
    tool_name: str = Field(
        description="The tool to execute for this thought (e.g. search_graph, get_manual_page)."
    )
    tool_args: dict = Field(
        default_factory=dict,
        description="Arguments to pass to the tool. Empty dict for parameterless tools."
    )
    ref_id: str = Field(
        description="The evidence reference ID for this thought (E1, E2, E3...) — this will be how you cite the result later."
    )


class FinalAnswer(BaseModel):
    """The synthesized answer from all observations."""

    answer: str = Field(
        description="User-facing answer. Be concise, factual, and actionable. Cite evidence references."
    )
    confidence: Literal["high", "medium", "low"] = Field(
        description="high = direct verified hits; medium = partial/derived; low = sparse or contradictory."
    )
    unresolved: list[str] = Field(
        default_factory=list,
        description="Things the user asked for that could NOT be determined, each with a short reason."
    )


class RewooState(TypedDict):
    """Shared state for the ReWOO StateGraph. Linear: START → plan → execute → synthesize → END."""

    messages: Annotated[list[BaseMessage], add_messages]
    plan: RewooPlan | None
    observations: dict[str, str]  # E# → observation text
    remaining_steps: RemainingSteps
