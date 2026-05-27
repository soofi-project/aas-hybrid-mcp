"""State for the custom ReAct variant.

Minimal state mirroring the structure used by plan/reflect and reflexion —
a messages list managed by ``add_messages`` and a tool-call counter.
"""

from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class ReactState(TypedDict):
    """Shared state for the custom ReAct StateGraph."""

    messages: Annotated[list[BaseMessage], add_messages]
    total_tool_calls: int
