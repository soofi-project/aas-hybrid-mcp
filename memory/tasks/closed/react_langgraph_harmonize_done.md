---
name: ReAct LangGraph Harmonization Done
description: ReAct-Variante von create_react_agent auf eigenen StateGraph umgebaut, analog zu Plan + Reflexion.
type: task
status: done
---

## Was umgesetzt

- **`agent_react_state.py`** — `ReactState(TypedDict)` mit `messages` und `total_tool_calls`, analog zu Plan/Reflexion-States.
- **`agent_react_nodes.py`** — `make_agent_node()` (LLM-Call + System-Prompt-Injektion) und `route_after_agent()` (tool_calls → `"tools"` → END). `ToolNode` direkt im Graphen verwendet.
- **`agent_react_graph.py`** — `build_react_graph(*, llm, tools, system_prompt)` baut den StateGraph mit `agent`- und `tools`-Nodes, konditionalen Kanten.
- **`agent.py`** — `create_react_agent`-Import entfernt, `_lazy_init` ruft `build_react_graph` auf. Docstrings aktualisiert. API-kompatibel, `api.py` unberührt.
- **Verbose-Streaming** — Node-Name `"agent"` unverändert, `_REACT_NODES` in `verbose_stream_utils.py` braucht keine Änderung.

## Commit

`9b3cc10` — Replace create_react_agent with custom LangGraph StateGraph

## References

- `aas-agent/src/aas_agent/agent_react_graph.py`
- `aas-agent/src/aas_agent/agent_react_nodes.py`
- `aas-agent/src/aas_agent/agent_react_state.py`
- `aas-agent/src/aas_agent/agent.py`
