"""StateGraph builder for the Reflexion variant.

Pipeline: executor → judge → (reflect → executor) → finalizer
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph

from aas_agent.reflexion_graph_nodes import make_executor_node, make_judge_node, make_reflect_node, make_finalizer_node, route_after_judge
from aas_agent.reflexion_state import ReflexionState


def build_reflexion_graph(
    exec_llm: BaseChatModel,
    tools: list[BaseTool],
    base_system: str,
    judge_llm: BaseChatModel,
    reflect_llm: BaseChatModel,
    finalizer_llm: BaseChatModel,
    max_trials: int = 3,
    accept_threshold: float = 0.7,
):
    """Compile the Reflexion graph with the given LLMs and configuration."""
    graph = StateGraph(ReflexionState)

    graph.add_node(
        "executor", make_executor_node(exec_llm.bind_tools(tools), tools, base_system)
    )

    graph.add_node(
        "judge", make_judge_node(judge_llm)
    )

    graph.add_node(
        "reflect", make_reflect_node(reflect_llm)
    )

    graph.add_node(
        "finalizer", make_finalizer_node(finalizer_llm)
    )

    graph.add_edge(START, "executor")
    graph.add_edge("executor", "judge")
    graph.add_edge("reflect", "executor")
    graph.add_edge("finalizer", END)

    graph.add_conditional_edges(
        "judge",
        route_after_judge,
        {
            "finalizer": "finalizer",
            "reflect": "reflect",
        },
    )

    return graph.compile()
