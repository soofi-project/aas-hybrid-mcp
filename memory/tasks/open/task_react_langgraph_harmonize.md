---
name: Task – ReAct auf eigenes LangGraph-Graph harmonisieren
description: agent.py (create_react_agent) auf agent_react_graph.py / agent_react_nodes.py / agent_react_state.py umbauen, analog zu Plan + Reflexion.
type: task
status: open
priority: low
---

## Background

Die drei Varianten sind strukturell inkonsistent:

- **Plan** → `agent_plan.py` + `agent_plan_graph.py` + `agent_plan_nodes.py` + `agent_plan_state.py`
- **Reflexion** → `reflexion.py` + `reflexion_graph.py` + `reflexion_graph_nodes.py` + `reflexion_state.py`
- **ReAct** → `agent.py` — nutzt `create_react_agent` aus `langgraph.prebuilt` direkt, kein eigenes Graph-File

`create_react_agent` ist eine Black-Box-Factory; der Graph ist nicht introspektierbar, Nodes
lassen sich nicht einzeln testen, und verbose-Streaming muss gegen das prebuilt-interne
Event-Schema (`"agent"` + `"tools"` Nodes) arbeiten statt gegen eigene benannte Nodes.

## Subtasks

### T1 — `agent_react_state.py`
State-Klasse analog zu `agent_plan_state.py` / `reflexion_state.py`:
- `messages: list[BaseMessage]`
- `total_tool_calls: int`
- ggf. `usage`-Feld falls Usage-Tracking harmonisiert werden soll

### T2 — `agent_react_nodes.py`
Zwei Nodes:
- `make_agent_node(llm, tools, system)` — LLM-Call + tool-call routing
- `make_tools_node(tools)` — ToolNode-Wrapper (oder `ToolNode` direkt)

Logik aus `agent.py` extrahieren; `get_current_utc_time`-Tool bleibt hier oder in eigenem `tools.py`.

### T3 — `agent_react_graph.py`
`build_react_graph(*, llm, tools, base_system, system_prompt)` analog zu
`build_plan_reflect_graph` / `build_reflexion_graph`:
```
START → agent_node → (tool_calls?) → tools_node → agent_node → ... → END
```
Routing-Funktion prüft ob letzter AIMessage tool_calls hat.

### T4 — `agent.py` umschreiben
`ReactAgentRunner` nutzt `build_react_graph` statt `create_react_agent`.
`stream` / `invoke` bleiben API-kompatibel — `api.py` bleibt unverändert.

`_REACT_NODES` in `verbose_stream_utils.py` ggf. anpassen wenn Nodes umbenannt werden.

### T5 — Tests
Vorhandene Agent-Tests gegen ReAct-Variante laufen lassen, sicherstellen
dass kein Regressionsbruch.

## Acceptance Criteria

- `aas-agent:react` via `api.py` weiterhin aufrufbar, gleiche Antwortqualität
- Verbose-Streaming zeigt sinnvolle Node-Transitions (kein Regression)
- Kein Import von `langgraph.prebuilt.create_react_agent` in `agent.py` mehr
- Dateistruktur analog zu Plan + Reflexion

## Non-Goals

- Keine funktionale Änderung des ReAct-Verhaltens
- Kein neues Feature, kein Prompt-Änderung
- `api.py` bleibt unberührt

## References

- Aktuell: `aas-agent/src/aas_agent/agent.py`
- Zielstruktur: `aas-agent/src/aas_agent/agent_plan_graph.py`, `reflexion_graph.py`
- Verbose-Streaming: `aas-agent/src/aas_agent/verbose_stream_utils.py`
