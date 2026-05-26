---
name: Task – Paper-Tabellen aus Eval-Ergebnissen
description: Nach Abschluss aller Modell-Runs analyze_results.py pro Modell ausführen, analysis.md finalisieren, Ergebnistabellen in paper/etfa2026 einpflegen
type: task
status: open
priority: high
---

## Background

Die Skalierungsstudie (Pattern × Modellgröße) läuft noch. Bisher abgeschlossen:
2B / 4B / 9B / 27B (qwen36). Noch ausstehend: qwen35-27b, qwen35-122b,
qwen35-397b (Cortecs), qwen36-35b. Wenn alle Runs + Judgings da sind, kommen die
Ergebnisse als Tabellen ins Paper.

Analyse-Tooling ist fertig: `tests/agent-tests/analyze_results.py <slug>` erzeugt
`results/analysis_<slug>.md` mit Per-Suite-Stats, Cross-Tabs und Dauer-Block.
Zwischenstand-Befunde in `tests/agent-tests/results/analysis.md`.

## Subtasks

### T1 — Fehlende Modell-Runs abschließen

Pro Modell: `./eval-model.sh <slug>` (repo root) + `./run_all.sh <slug>`
(tests/agent-tests/). Reihenfolge laut README: qwen35-27b → qwen35-122b →
qwen36-35b → qwen35-397b (Cortecs zuletzt).

### T2 — analyze_results.py für alle Modelle ausführen

```bash
cd tests/agent-tests
for slug in qwen35-27b qwen35-122b qwen36-35b qwen35-397b; do
    python analyze_results.py $slug
done
```

Ergibt `results/analysis_<slug>.md` pro Modell.

### T3 — analysis.md finalisieren

Übersichtstabelle in `tests/agent-tests/results/analysis.md` mit allen Modellen
vervollständigen. Befund-Sektion prüfen — insbesondere ob der Phasenübergang bei 4B
und der qualitative Sprung bei 27B stabil bleiben wenn 122B/397B dazukommen.

### T4 — Tabellen ins Paper übertragen

In `paper/etfa2026/conference_etfa_2026.tex` (§Evaluation):

- **Haupt-Ergebnistabelle:** Correct-Rate pro Modell × Suite als LaTeX-Tabelle.
  Kernsuites: bench_b, containment_hall4, anti_pattern, srn_bypass.
- **Dauer-Tabelle (optional):** Median (all) pro Modell × Suite —
  bench_b + containment als repräsentative Suites.
- **Befund-Text anpassen:** Phasenübergang 4B, Validator-Scaffolding bei 4–9B,
  qualitativer Sprung 27B (All-good), Recursion-Exhaustion-Muster bei failed runs.

## Acceptance Criteria

- `results/analysis_<slug>.md` für alle 9 Modelle vorhanden
- `analysis.md` enthält vollständige Übersichtstabelle (alle Modelle, alle Metriken)
- Paper §Evaluation enthält mind. eine LaTeX-Tabelle mit Correct-Rate nach Modellgröße
- Paper kompiliert ohne Fehler

## References

- `tests/agent-tests/analyze_results.py`
- `tests/agent-tests/results/analysis.md`
- `tests/agent-tests/README.md` (Modell-Run-Workflow unter "Paper eval")
- `paper/etfa2026/conference_etfa_2026.tex`
- Verwandte Tasks: `[[task-paper-pattern-modelsize-eval]]`
