"""StateGraph builder for the custom ReAct variant.

Layered on top of ``agent_react_nodes`` — this file owns only graph wiring
and edges.  The runner (``agent.py``) owns LLM construction and the public
API.
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from aas_agent.agent_react_nodes import make_agent_node, route_after_agent
from aas_agent.agent_react_state import ReactState


def build_react_graph(
    *,
    llm: BaseChatModel,
    tools: list[BaseTool],
    system_prompt: str,
):
    """Compile the ReAct graph with the given LLM, tools, and system prompt.

    The graph has two nodes:

    - ``agent`` — calls the LLM (with tools bound).
    - ``tools`` — executes tool calls via LangGraph's ``ToolNode``.

    Loop: agent → (has tool calls?) → tools → agent → ... → END
    """
    graph = StateGraph(ReactState)

    graph.add_node("agent", make_agent_node(llm.bind_tools(tools), system_prompt))
    graph.add_node("tools", ToolNode(tools))

    graph.add_edge(START, "agent")
    graph.add_edge("tools", "agent")

    graph.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            "__end__": END,
        },
    )

    return graph.compile()
