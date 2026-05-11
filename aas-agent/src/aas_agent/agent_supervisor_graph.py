"""StateGraph builder for the agent-supervisor variant.

Architecture: START → supervisor_node → orchestrator_node → synthesize_node → END
"""

from langchain_core.language_models import BaseChatModel
from langgraph.graph import END, START, StateGraph

from aas_agent.agent_supervisor_nodes import make_orchestrator_node, make_supervisor_node, make_synthesize_node
from aas_agent.agent_supervisor_state import AgentState


def build_supervisor_graph(
    supervisor_llm: BaseChatModel,
    worker_subgraphs: dict[str, tuple],
    synthesize_llm: BaseChatModel,
    finalizer_prompt: str | None = None,
):
    """Compile the supervisor graph with pre-built worker sub-graphs.

    ``worker_subgraphs`` is a dict mapping worker names to (subgraph, system_prompt) tuples.
    Each entry is a pre-compiled LangGraph StateGraph ready to invoke.
    """
    graph = StateGraph(AgentState)

    # Supervisor node — decomposes request into tasks
    graph.add_node(
        "supervisor", make_supervisor_node(supervisor_llm)
    )

    # Orchestrator — executes all worker sub-graphs in parallel
    graph.add_node(
        "orchestrator", make_orchestrator_node(worker_subgraphs)
    )

    # Synthesizer — combines all results into FinalAnswer
    graph.add_node(
        "synthesize", make_synthesize_node(synthesize_llm, finalizer_prompt)
    )

    # Edges
    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", "orchestrator")
    graph.add_edge("orchestrator", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile()
