---
name: Task – Tool-Call-Analyse-Script für Eval-Ergebnisse
description: Script das aus den results/*.json-Dateien aggregiert welches Tool in welchem Turn wie oft aufgerufen wurde und mit welchen Argumenten — pro Case, Modell, und Suite.
type: task
status: open
priority: medium
---

## Ziel

Die Eval-Ergebnisse in `tests/agent-tests/results/` enthalten pro Record ein
`result.tool_calls`-Array mit `name`, `args`, `result_preview` sowie
`result.tool_call_count`. Ein Auswertungs-Script soll diese Daten aggregieren
und für die Paper-Analyse nutzbar machen.

## Kernfragen, die das Script beantworten soll

1. **Tool-Nutzungs-Profil pro Modell:** Welche Tools wurden im Schnitt wie oft
   aufgerufen? (z.B. `query_aas_graph` durchschnittlich 3× bei 27B, 0× bei 2B)
2. **Pro Case und Turn:** In welchem Turn (1. Aufruf, 2. Aufruf, …) wird welches
   Tool aufgerufen — Reihenfolge-Analyse (z.B. immer erst `get_templates_index`
   dann `query_aas_graph`?)
3. **Failure-Mode-Klassifikation:** Unterscheidung zwischen:
   - Kein Tool-Calling (tool_call_count == 0) → kompletter Ausfall
   - Tool-Calls mit Cypher-Violations → falsche Query-Generierung
   - Tool-Calls ohne Violations aber falsche Antwort → Reasoning-Fehler
4. **Argument-Analyse:** Bei `query_aas_graph` — welche Cypher-Queries wurden
   generiert? Gibt es wiederkehrende Muster oder Fehlertypen?
5. **Cross-Modell-Vergleich:** Gleiche Case × Modell-Matrix wie Bench-B-Tabelle,
   aber aufgeschlüsselt nach Tool-Nutzung statt nur Pass/Fail.

## Input / Output

**Input:** `tests/agent-tests/results/<slug>_<suite>_N<n>.json`
- Format: `{"records": [...], "summary_by_variant": {...}}`
- Pro Record: `result.tool_calls` (Liste mit `name`, `args`, `result_preview`),
  `result.tool_call_count`, `evaluation.cypher_violations`, `evaluation.tool_violations`

**Output:**
- Console-Tabelle (ASCII) oder CSV nach `results/analysis/`
- Pro Modell × Suite: Tool-Frequenz-Tabelle
- Pro Case: Failure-Mode-Verteilung
- Optional: Markdown-Snippet für Paper-Diskussion

## Implementierung

**Datei:** `tests/agent-tests/analyze_tool_calls.py`

**Aufruf-Varianten:**
```bash
# Einzelne Datei
python analyze_tool_calls.py results/qwen35-27b_bench_b_N10.json

# Alle Dateien eines Modells
python analyze_tool_calls.py results/qwen35-27b_*.json

# Vergleich mehrerer Modelle (Cross-Modell-Tabelle)
python analyze_tool_calls.py --compare results/qwen35-2b_bench_b_N10.json results/qwen35-27b_bench_b_N10.json

# Suite-Filter
python analyze_tool_calls.py results/qwen35-27b_bench_b_N10.json --suite bench_b
```

**Key-Metriken pro Ausgabe:**
```
Model: qwen35-27b | Suite: bench_b | N=10 | Cases: 6

Tool frequency (mean per run):
  get_templates_index      2.1  ████████████
  query_aas_graph          3.4  ████████████████████
  search_aas_documents     1.2  ███████
  get_graph_schema         1.0  ██████

Failure modes:
  No tool calls:           0/60  (0%)
  Cypher violations:       4/60  (7%)
  Tool calls, wrong answer: 8/60 (13%)
  Pass:                   48/60  (80%)
```

## Subtasks

### T1 — Basis-Script: Tool-Frequenz pro Datei

- Liest eine JSON-Datei
- Aggregiert `tool_call_count` und `tool_calls[].name` über alle Records
- Gibt ASCII-Tabelle aus (Tool → mean count, min, max, % Runs mit ≥1 Aufruf)
- Failure-Mode-Klassifikation (kein Tool / Violation / falsche Antwort / Pass)

### T2 — Turn-Reihenfolge-Analyse

- Pro Record: Liste der Tool-Namen in Aufruf-Reihenfolge
- Häufigste Sequenzen (z.B. `[get_templates_index, get_graph_schema, query_aas_graph]`)
- Visualisierung als Sankey oder einfache Transition-Matrix (ASCII reicht)

### T3 — Cross-Modell-Vergleich (`--compare`)

- Gleiche Metriken für mehrere Dateien nebeneinander
- Ausgabe als Markdown-Tabelle (copy-paste ins Paper möglich)

### T4 — Argument-Analyse für `query_aas_graph`

- Extrahiert alle generierten Cypher-Queries
- Klassifiziert Fehlertypen aus `cypher_violations` (LIKE, !=, Duplicate-Column, …)
- Listet Fehlerpattern mit Häufigkeit — Evidenz für §13 Future Work (JSON-zu-Cypher-Gap)

## Acceptance Criteria

- Script läuft auf allen vorhandenen `results/*.json`-Dateien ohne Fehler
- Tool-Frequenz-Tabelle korrekt (verifiziert gegen manuelles Zählen in einem Record)
- Failure-Mode-Klassifikation stimmt mit bekannten 2B-Ergebnissen überein
  (B4-B5: kein Tool-Calling, B1-B3: Cypher-Violations)
- `--compare`-Output als Markdown-Tabelle nutzbar für Paper-Diskussion

## Non-Goals

- Kein interaktives Dashboard / keine Visualisierungs-Library (matplotlib etc.)
- Kein automatischer Paper-Text-Generator
- Keine Veränderung des Eval-Frameworks (`run_tests.py`)

## References

- Ergebnis-Format: `tests/agent-tests/results/qwen36-27b_bench_b_N10.json`
- Record-Struktur: `records[].result.tool_calls`, `.tool_call_count`, `.evaluation.cypher_violations`
- Bench-B-Cases: `tests/agent-tests/cases/bench_b.yaml` (B1–B6)
- Verwandte Tasks:
  - [[task_paper_pattern_modelsize_eval]] — Eval-Läufe die dieses Script auswertet
  - [[task_paper_ablation_sections]] — Paper-Tabellen die auf Auswertungen basieren
