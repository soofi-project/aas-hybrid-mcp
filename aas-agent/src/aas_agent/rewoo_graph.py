"""StateGraph builder for the ReWOO (Reasoning Without Observation) variant.

Pipeline: START → plan_node → execute_node → synthesize_node → END

Linear graph — no conditional edges. The plan_node determines ALL tool calls
upfront, execute_node runs them in parallel, and synthesize_node combines results.
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph

from aas_agent.rewoo_nodes import make_execute_node, make_plan_node, make_synthesize_node
from aas_agent.rewoo_state import RewooState


def build_rewoo_graph(
    *,
    plan_llm: BaseChatModel,
    synthesize_llm: BaseChatModel,
    tool_map: dict[str, BaseTool],
    base_system: str,
    max_thoughts: int = 10,
    parallel_batch_size: int = 5,
):
    """Compile the ReWOO graph with the given configuration.

    ``base_system`` is the auto-injected MCP context (manual + schema).
    """
    graph = StateGraph(RewooState)

    # Plan node — generates ALL tool calls upfront
    graph.add_node(
        "plan",
        make_plan_node(plan_llm, tool_map, base_system, max_thoughts),
    )

    # Execute node — runs ALL planned tool calls in parallel batches
    graph.add_node(
        "execute",
        make_execute_node(tool_map, parallel_batch_size),
    )

    # Synthesize node — combines observations into FinalAnswer
    graph.add_node(
        "synthesize",
        make_synthesize_node(synthesize_llm),
    )

    # Linear edges
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "execute")
    graph.add_edge("execute", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile()
