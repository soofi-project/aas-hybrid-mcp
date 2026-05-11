"""State and Pydantic schemas for the agent-supervisor variant.

Structure: Supervisor decomposes a user request into typed sub-tasks,
dispatches worker sub-graphs, and finally synthesizes the results.
"""

from operator import add
from typing import Annotated, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.managed.is_last_step import RemainingSteps
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class SupervisorDecision(BaseModel):
    """Output of the supervisor node — decides which workers to dispatch."""

    tasks: list["SupervisorTask"] = Field(
        description="Break the user request into sub-tasks, one per worker."
    )


class SupervisorTask(BaseModel):
    """A sub-task assigned to exactly one worker."""

    task_id: int | None = Field(
        default=None,
        description="Auto-assigned 0-based index if not provided."
    )
    worker: Literal["work_graph", "work_document", "work_template"] = Field(
        description="Which specialist worker handles this sub-task."
    )
    instruction: str = Field(
        description="What this worker needs to find/return. Phrase as a direct question or request."
    )
    expected_output: Literal["graph_query_result", "manual_content", "template_info"] = Field(
        description="What kind of result to expect — affects synthesis."
    )


class WorkerResult(BaseModel):
    """Structured output from a worker sub-graph."""

    task_id: int = Field(description="Which task this is the result for.")
    worker: str = Field(description="Worker name.")
    finding: str = Field(description="Key finding — 2-3 sentences.")
    details: str = Field(description="Full details with cited tool names and sources.")
    confidence: Literal["high", "medium", "low"] = Field(
        description="high = direct verified hit; medium = derived; low = sparse/failed."
    )


class FinalAnswer(BaseModel):
    """The synthesized answer the supervisor produces from all worker results."""

    answer: str = Field(
        description="User-facing answer combining worker findings. Be concise and actionable. Cite sources."
    )
    confidence: Literal["high", "medium", "low"] = Field(
        description="high = all workers done with direct hits; medium = some inferred; low = sparse/contradictory results."
    )
    unresolved: list[str] = Field(
        default_factory=list,
        description="Things the user asked for that NO worker could determine, each with a short reason."
    )


class AgentState(TypedDict):
    """Shared state for the supervisor StateGraph."""

    messages: Annotated[list[BaseMessage], add_messages]
    plan: SupervisorDecision | None
    task_queue: list[SupervisorTask]
    worker_results: Annotated[list[WorkerResult], add]
    supervisor_decision: str | None
    _worker_states: dict[str, list[BaseMessage]]  # task_id -> message history
    remaining_steps: RemainingSteps
