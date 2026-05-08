"""StateGraph builder for the plan/reflect agent variant.

Layered on top of ``agent_plan_nodes`` — this file owns only graph wiring,
budgets, and edges. The runner (``agent_plan.py``) owns LLM construction
and the public API.
"""

from functools import partial

from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph

from aas_agent.agent_plan_nodes import (
    advance_step_node,
    make_execute_step_node,
    make_finalizer_node,
    make_planner_node,
    make_reflector_node,
    route_after_reflector,
)
from aas_agent.agent_plan_state import AgentState


def build_plan_reflect_graph(
    *,
    executor_llm: BaseChatModel,
    structured_llm: BaseChatModel,
    tools: list[BaseTool],
    base_system: str,
    planner_prompt: str,
    executor_prompt: str,
    reflector_prompt: str,
    finalizer_prompt: str,
    max_step_attempts: int = 3,
    max_replans: int = 2,
    max_total_tool_calls: int = 30,
    sub_recursion_limit: int = 8,
):
    """Compile the plan/reflect graph with the given budgets and prompts.

    Two LLM clients are required:

    - ``executor_llm`` — bound for tool calls (``parallel_tool_calls=False``
      is fine here because the executor sub-agent does bind tools).
    - ``structured_llm`` — used by planner / reflector / finalizer via
      plain ``ainvoke`` (no ``with_structured_output``). These nodes parse
      JSON from the LLM text response ourselves via ``QwenOutputParser``.

    ``base_system`` is the auto-injected MCP context (manual + graph
    schema). It is appended to the planner and executor system prompts so
    both nodes share ground truth without re-fetching MCP resources.
    """
    graph = StateGraph(AgentState)

    graph.add_node(
        "planner", make_planner_node(structured_llm, base_system, planner_prompt)
    )
    graph.add_node(
        "execute_step",
        make_execute_step_node(
            executor_llm,
            tools,
            base_system,
            executor_prompt,
            sub_recursion_limit=sub_recursion_limit,
        ),
    )
    graph.add_node("reflector", make_reflector_node(structured_llm, reflector_prompt))
    graph.add_node("advance_step", advance_step_node)
    graph.add_node("finalizer", make_finalizer_node(structured_llm, finalizer_prompt))

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "execute_step")
    graph.add_edge("execute_step", "reflector")
    graph.add_edge("advance_step", "execute_step")
    graph.add_edge("finalizer", END)

    router = partial(
        route_after_reflector,
        max_step_attempts=max_step_attempts,
        max_replans=max_replans,
        max_total_tool_calls=max_total_tool_calls,
    )
    graph.add_conditional_edges(
        "reflector",
        router,
        {
            "execute_step": "execute_step",
            "advance_step": "advance_step",
            "planner": "planner",
            "finalizer": "finalizer",
        },
    )

    return graph.compile()
