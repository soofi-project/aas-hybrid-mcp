"""StateGraph builder for the CRAG (Context Retrieval Augmented Generation) variant.

Pipeline: executor → relevance → (synthesize | refine → executor | discard → uncorrect → executor)

CRAG adds a relevance-evaluation loop to the retrieval chain:
  1. Executor runs ReAct to retrieve information
  2. Relevance evaluator scores the results (0.0-1.0) and decides an action
  3. correct → synthesize; incorrect → discard → uncorrect → executor; ambiguous → refine → executor
  4. Loop repeats until relevance is sufficient or max refinements exhausted
  5. Synthesizer combines the good results into a FinalAnswer
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph

from aas_agent.crag_nodes import (
    make_discard_node,
    make_executor_node,
    make_refine_node,
    make_uncorrect_node,
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
    relevance_threshold_low: float = 0.3,
):
    """Compile the CRAG graph with the given LLMs and configuration.

    ``base_system`` is the auto-injected MCP context (manual + schema).
    ``relevance_threshold`` is the upper threshold — correct if score >= this.
    ``relevance_threshold_low`` is the lower threshold — incorrect if score <= this.
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

    # Refine — generates supplementary queries for ambiguous evidence
    graph.add_node(
        "refine", make_refine_node(refine_llm)
    )

    # Discard — clears evidence after incorrect action
    graph.add_node(
        "discard", make_discard_node()
    )

    # Uncorrect — generates a fresh query when all evidence was discarded
    graph.add_node(
        "uncorrect", make_uncorrect_node(refine_llm)
    )

    # Synthesizer — combines evidence into a final answer
    graph.add_node(
        "synthesize", make_synthesizer_node(synthesize_llm)
    )

    # Edges
    graph.add_edge(START, "executor")
    graph.add_edge("executor", "relevance")
    graph.add_edge("refine", "executor")
    graph.add_edge("discard", "uncorrect")
    graph.add_edge("uncorrect", "executor")
    graph.add_edge("synthesize", END)

    # Conditional routing from relevance: 3-way action trigger
    graph.add_conditional_edges(
        "relevance",
        route_after_relevance,
        {
            "synthesize": "synthesize",
            "refine": "refine",
            "discard": "discard",
        },
    )

    return graph.compile()
