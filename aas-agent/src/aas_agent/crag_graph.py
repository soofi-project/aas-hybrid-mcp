"""StateGraph builder for the CRAG (Context Retrieval Augmented Generation) variant.

Pipeline: executor → relevance → (refine → executor) → synthesizer
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph

from aas_agent.crag_nodes import (
    make_executor_node,
    make_refine_node,
    make_relevance_node,
    make_synthesizer_node,
    route_after_relevance,
)
from aas_agent.crag_state import AgentState


def build_crag_graph(
    exec_llm: BaseChatModel,
    tools: list[BaseTool],
    base_system: str,
    relevance_llm: BaseChatModel,
    refine_llm: BaseChatModel,
    synthesize_llm: BaseChatModel,
    max_refinements: int = 3,
    relevance_threshold: float = 0.7,
):
    """Compile the CRAG graph with the given LLMs and configuration.

    ``base_system`` is the auto-injected MCP context (manual + schema).
    """
    graph = StateGraph(AgentState)

    # Executor — bounded ReAct sub-loop for retrieval
    graph.add_node(
        "executor", make_executor_node(exec_llm.bind_tools(tools), tools, base_system)
    )

    # Relevance evaluator
    graph.add_node(
        "relevance", make_relevance_node(relevance_llm)
    )

    # Refinement — generates better queries when relevance is low
    graph.add_node(
        "refine", make_refine_node(refine_llm)
    )

    # Synthesizer — combines high-relevance evidence
    graph.add_node(
        "synthesize", make_synthesizer_node(synthesize_llm)
    )

    # Edges
    graph.add_edge(START, "executor")
    graph.add_edge("executor", "relevance")
    graph.add_edge("refine", "executor")
    graph.add_edge("synthesize", END)

    # Conditional routing from relevance
    graph.add_conditional_edges(
        "relevance",
        route_after_relevance,
        {
            "synthesize": "synthesize",
            "refine": "refine",
        },
    )

    return graph.compile()
