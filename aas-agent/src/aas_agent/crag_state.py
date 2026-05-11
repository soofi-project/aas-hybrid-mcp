"""State and Pydantic schemas for the CRAG (Context Retrieval Augmented Generation) variant.

CRAG adds a relevance-evaluation loop to the retrieval chain:
  1. Executor runs ReAct to retrieve information
  2. Relevance evaluator scores the results (0.0-1.0)
  3. If score < threshold, a refine node generates better queries
  4. Loop repeats until relevance is sufficient or max refinements exhausted
  5. Synthesizer combines the good results into a FinalAnswer
"""

from operator import add
from typing import Annotated, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.managed.is_last_step import RemainingSteps
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class RelevanceScore(BaseModel):
    """Evaluation of how relevant a set of retrieved results is for the user query."""

    relevance_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Relevance score: 0.0 = completely irrelevant, 1.0 = perfectly relevant."
    )
    reason: str = Field(
        description="Short paragraph explaining the score. What matches? What's missing?"
    )
    needs_refinement: bool = Field(
        description="True if we should try different search parameters or alternative queries."
    )
    refinement_hint: str = Field(
        default="",
        description="If needs_refinement: concrete advice on what to change. Empty if not needed."
    )


class FinalAnswer(BaseModel):
    """The synthesized answer the finalizer produces from retrieved context."""

    answer: str = Field(
        description="User-facing answer based on the retrieved evidence. Be concise, factual, and actionable. Cite sources."
    )
    confidence: Literal["high", "medium", "low"] = Field(
        description="high = direct verified hits with high relevance; medium = good but partial; low = sparse or contradictory evidence."
    )
    unresolved: list[str] = Field(
        default_factory=list,
        description="Things the user asked for that could NOT be determined, each with a short reason."
    )


class RetrieverStep(BaseModel):
    """Record of one retrieval attempt in the CRAG pipeline."""

    query: str = Field(description="The query used for this retrieval attempt.")
    relevance_score: float = Field(description="Relevance score for this attempt.")
    result_summary: str = Field(description="Key findings from this retrieval step.")


class AgentState(TypedDict):
    """Shared state for the CRAG StateGraph."""

    messages: Annotated[list[BaseMessage], add_messages]
    evidence: Annotated[list[dict], add]  # {"query": str, "content": str, "relevance": float}
    retriever_steps: list[RetrieverStep]  # history of retrieval attempts
    refinement_count: int
    max_refinements: int
    relevance_threshold: float
    last_relevance: RelevanceScore | None
    remaining_steps: RemainingSteps
