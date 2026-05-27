"""Graph nodes for the custom ReAct variant.

Two nodes — ``agent`` and ``tools`` — wired in a loop:
    START → agent → (has tool calls?) → tools → agent → ... → END

The ``agent`` node invokes the LLM; if the response contains tool calls the
``tools`` node executes them via LangGraph's ``ToolNode`` and the loop
continues.  When the LLM responds without tool calls the graph ends.
"""

from typing import Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import ToolNode

from aas_agent.agent_react_state import ReactState


def make_agent_node(llm: BaseChatModel, system_prompt: str) -> Callable:
    """Return an async node function that calls the LLM."""

    async def agent_node(state: ReactState) -> dict:
        messages = state.get("messages", [])
        lc_messages = [SystemMessage(content=system_prompt)] + list(messages)
        response = await llm.ainvoke(lc_messages)
        tool_call_count = len(getattr(response, "tool_calls", []) or [])
        return {
            "messages": [response],
            "total_tool_calls": state.get("total_tool_calls", 0) + tool_call_count,
        }

    return agent_node


def route_after_agent(state: ReactState) -> str:
    """Return ``"tools"`` if the last AI message has tool calls, else ``"__end__"``."""
    messages = state.get("messages", [])
    for msg in reversed(messages):
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls is not None:
            return "tools" if len(tool_calls) > 0 else "__end__"
    return "__end__"
