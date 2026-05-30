---
name: Eval Tool-Call Analysis Done
description: Tool-call analysis script built and run across 9 models (1800 records). Key findings integrated into paper §10 and §11.
type: task
status: done
---

## Was umgesetzt

**Script:** `tests/agent-tests/analyze_tool_calls.py` (~570 Zeilen, Stdlib-only)

- Lädt beide Formate: per-Model-Dateien (`results/<model>/t07/`) und neue Run-Dateien (`run_*.json`), filtert auf ReAct-only
- Pro-Record-Analyse: Prerequisite-Timeline (welche Tools vor erster `query_aas_graph`), Violation-Timeline (Manual vor erster Violation?), Failure-Mode-Klassifikation, Self-Correction-Rate
- `--compare`-Modus: Paper-ready Markdown-Tabelle über alle Modelle
- Output geschrieben nach `tests/agent-tests/results/tool_call_analysis_t07.md`

**Lauf über 9 Modelle, 1800 Records (200 pro Modell, 5 Suites):**

| Modell | Pass% | AP-hit% | Self-corr% | Manual-1st | All-3-1st | Manual>AP |
|---|---|---|---|---|---|---|
| qwen35-2b | 38% | 13% | 96% | 4% | 0% | 12% |
| qwen35-4b | 50% | 76% | 97% | 2% | 1% | 1% |
| qwen35-9b | 50% | 76% | 95% | 4% | 0% | 3% |
| qwen35-27b | 71% | 63% | 98% | 15% | 1% | 12% |
| qwen35-35b | 64% | 62% | 98% | 3% | 0% | 5% |
| qwen35-122b | 68% | 74% | 97% | 16% | 2% | 10% |
| qwen35-397b | 70% | 62% | 95% | 44% | 4% | 50% |
| qwen36-27b | 64% | 48% | 97% | 49% | 21% | 32% |
| qwen36-35b | 64% | 39% | 97% | 39% | 5% | 22% |

**Paper-Integration (3 Stellen):**

- **§10 `10-evaluation.tex`:** Neuer Absatz "Anti-pattern compliance" — AP-hit nicht monoton mit Modellgröße, Self-Correction 95-98%, qwen36-27b beste Prerequisite-Compliance aber 48% AP-hit
- **§11 `11-discussion.tex` "Necessity of Enforcement":** Manual>AP-Befund als empirischer Beleg — 397b liest Manual in 44%, verletzt trotzdem in 50%; qwen36-27b 32% Manual>AP
- **§11 `11-discussion.tex` "Reads vs Writes":** qwen36-27b Scaffolding-Asymmetrie — 94% read-path, 14% SRN, kein write-path-scaffolding

**Key-Befunde:**

- AP-hit korreliert nicht monoton mit Modellgröße (4b/9b: 76%, 397b: 62%)
- Manual>AP > 0 bei ALLEN Modellen — konsultiertes Wissen reicht nicht
- qwen35-397b: stärkster "Prompt is Hint"-Beleg (44% Manual-1st, 50% Manual>AP)
- qwen36-27b: höchste Prerequisite-Compliance, aber write-path bricht ein
- Self-Correction hoch (95-98%), aber teuer in Tool-Calls

## Akzeptanzkriterien erfüllt

- Script läuft auf allen vorhandenen `results/*.json`-Dateien ohne Fehler
- Failure-Mode-Klassifikation plausibel (2b: 52% Clean Fail, 9b: 40% Viol+Fail)
- `--compare`-Output als Markdown-Tabelle in Paper-Diskussion eingearbeitet
- Violation-Rule-Breakdown zeigt idShort_contains dominiert (348 von ~500 bei 9b)

## Nicht umgesetzt (bewusst)

- T2 (Turn-Sequenz / Transition-Matrix) — diagnostisch, nicht Paper-relevant
- T4 (Argument-Analyse / Cypher-Pattern-Mining) — interessant aber separater Scope

## References

- Script: `tests/agent-tests/analyze_tool_calls.py`
- Output: `tests/agent-tests/results/tool_call_analysis_t07.md`
- Paper-Edits: `paper/etfa2026/content/10-evaluation.tex`, `11-discussion.tex`
