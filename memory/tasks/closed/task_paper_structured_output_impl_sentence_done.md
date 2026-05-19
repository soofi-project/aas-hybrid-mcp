---
name: Task – Paper: Satz zu with_structured_output in Implementierungssektion
description: Einen Satz zur API-seitigen Schema-Enforcement via with_structured_output in die Paper-Implementierungssektion einfügen.
type: task
status: closed
priority: medium
---

## Background

Während der Eval-Vorbereitung (2026-05-19) wurde festgestellt, dass der Plan- und
Reflexion-Variant JSON-Ausgaben des LLM manuell parste — mit zunehmend komplexen
Repair-Hacks (`_qwen_structured_invoke`, `_repair_json_string`, `_coerce_and_validate`).
Konkrete Fehler: fehlendes Komma zwischen JSON-Feldern, `steps` als Liste von Strings
statt Step-Dicts. Ursache: kleinere Modelle (27B, 9B, 2B) folgen JSON-Formatting-
Instruktionen nicht zuverlässig wenn das LLM nur per Prompt gebeten wird, JSON zurückzugeben.

**Fix:** `agent_plan_nodes.py` und `reflexion_graph_nodes.py` auf
`llm.with_structured_output(ModelCls)` umgestellt. Das übergibt das Pydantic-Schema
als Tool-Definition an die API (function_calling), mit json_mode als Fallback. Kein
manuelles Parsen mehr. Serverseitig keine Änderung nötig — Qwen3.5-Instruct unterstützt
Tool Calling via vLLM + LiteLLM out of the box.

## Subtask

### T1 — Satz in Implementierungssektion einfügen

Genauer Wortlaut (abgestimmt):

> "Structured LLM outputs (planner, judge, reflector) are enforced via LangChain's
> `with_structured_output` using OpenAI tool-calling, eliminating brittle text-parsing
> across all model sizes."

**Wo:** Implementierungssektion des Papers (`paper/etfa2026/`), im Abschnitt der
Agent-Varianten (Plan-and-Solve / Reflexion) oder im Abschnitt zur Eval-Methodik —
dort wo die technische Zuverlässigkeit der Eval-Pipeline beschrieben wird.

**Warum ins Paper:**
- Direkte Evidenz für die Layered-Determinism-These: Schema-Enforcement auf LLM-Output-Ebene
  (nicht nur auf Write-Tool- oder Graph-Query-Ebene).
- Methodischer Integritätspunkt für die Skalierungs-Studie: bei 2B/4B-Modellen wäre
  manuelles Parsing instabil — API-seitige Enforcement macht die Eval-Pipeline über
  alle Modellgrößen reproduzierbar.
- Antizipiert Reviewer-Frage: „Wie bekommt ihr konsistente strukturierte Ausgaben
  von kleinen Modellen?"

## Acceptance Criteria

- Satz exakt wie oben (oder inhaltlich äquivalent) im Paper-LaTeX vorhanden
- Satz steht in einem Kontext der die Layered-Determinism-Argumentation stützt
- Kein eigener Paragraph — eingebettet in bestehenden Implementierungstext

## References

- Geänderte Files: `aas-agent/src/aas_agent/agent_plan_nodes.py`,
  `aas-agent/src/aas_agent/reflexion_graph_nodes.py`
- Paper: `paper/etfa2026/`
- Verwandte Tasks: [[task-paper-pattern-modelsize-eval]], [[task-paper-layered-determinism-thesis]]
