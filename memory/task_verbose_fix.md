---
name: Task - Verbose Markers Fix
description: Angleiche verbose/non-verbose Verhalten aller Agent-Variants
type: task
status: open
priority: medium
---

## Summary

Plan/reflect ist immer full-verbose — kein Gate, nicht abschaltbar.
Die anderen Varianten haben ein Gate aber inkonsistenter Inhalt:
react streamt non-verbose raw LLM tokens, die graph-basierten geben nur
finale Antwort. Verbose-Inhalt variiert: tool calls, chain events, oder
beides. Ziel: alle 5 Varianten konsistent machen.

**Erwartetes Ergebnis:**
- Non-verbose: immer nur finale Antwort im stream
- Verbose: `<antml:thinking>` blocks mit tools, node transitions, budget

## Subtasks

### T1: Plan/reflect verbose-Gate
**File:** `aas-agent/src/aas_agent/agent_plan.py:278-378`
- `stream()` mit `if (extra or {}).get("verbose", False)` umschalten (Pattern: crag/reflexion/rewoo)
- Non-verbose: `graph.ainvoke()` → nur finalizer message extrahieren + streamen
- Verbose: bestehender full `astream_events` loop unverändert (tools + plan + reflection + executor + finalizer)
- `invoke()` liefert bereits nur final text → kein change nötig

### T2: React non-verbose angleichen
**File:** `aas-agent/src/aas_agent/agent.py:210-264`
- Non-verbose: LLM tokens blocken, stattdessen `agent.ainvoke()` → finale
  AI message extrahieren → als single chunk streamen (konsistent mit graph-varianten)
- Verbose: bestehender `astream_events` loop mit tool-start/end + LLM tokens bleibt
- `invoke()` unverändert

### T3: Node-Transitions im verbose stream
**Files:** alle `_stream_*_verbose()` + plan/reflect verbose branch
- `on_chain_start` events als `<antml:thinking>` block einfügen
- Pro Variante die relevanten Nodes:
  - **React:** `agent` entry/exit
  - **Plan/reflect:** `planner`, `execute_step`, `reflector`, `finalizer`, `route`
  - **CRAG:** `executor`, `relevance`, `refine`, `uncorrect`, `discard`, `synthesize`
  - **Reflexion:** `executor`, `judge`, `reflect`, `finalizer`
  - **ReWOO:** `plan`, `execute`, `synthesize`
- Format: `**Node**: `{name}`` im `<antml:thinking>` block

### T4: Shared tool-formatting deduplizieren
**File:** `aas-agent/src/aas_agent/agent.py:298-322` als Quelle
- `_format_tool_start` / `_format_tool_end` sind hier definiert und werden
  von crag.py, reflexion.py, rewoo.py importiert
- Plan/reflect verwendet dieselben — sicherstellen alle von `agent.py`
  importieren, keine doppelten Definitionen

## Files Affected

| File | Subtask |
|---|---|
| `aas-agent/src/aas_agent/agent_plan.py` | T1 |
| `aas-agent/src/aas_agent/agent.py` | T2, T4 |
| `aas-agent/src/aas_agent/crag.py` | T3 |
| `aas-agent/src/aas_agent/reflexion.py` | T3 |
| `aas-agent/src/aas_agent/rewoo.py` | T3 |

## Acceptance Criteria

- `aas-agent:plan` (non-verbose) → nur finale Antwort im stream
- `aas-agent:plan-verbose` → tools + plan + reflection + node transitions + finalizer
- `aas-agent:react` (non-verbose) → nur finale Antwort
- `aas-agent:react-verbose` → tool calls + LLM tokens + node transitions
- Alle 5 variants non-verbose = final answer only, verbose = thinking blocks
- Bind-mount → kein rebuild, container restart genügt
- `./down.sh && ./up.sh --vllm` → alle variants manuell testen
