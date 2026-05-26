---
name: Task – Qwen 3.5 vs 3.6 @ 27B Generation-Kontrollpunkt
description: Containment-Bench mit Qwen3.5-27B-FP8 wiederholen, Ergebnis als Generationsvergleich-Datenpunkt in Paper §Eval einbauen.
type: task
status: open
priority: medium
---

## Background

Die Containment-Bench-Baseline (N=3, 5 Cases × 4 Varianten) läuft bereits mit
`Qwen3.6-27B-FP8`. Ergebnis: `tests/agent-tests/results/containment_hall4_baseline_N3.json`.

Hypothese: Kleinere, neuere Modell-Generation (3.6-27B) übertrifft ältere,
gleich-große Generation (3.5-27B) — illustriert den "Better-at-smaller-size"-Trend
über Generationen hinweg. Relevant als Industrial-Deployment-Argument: neueres
Quantisierungs-Modell on-prem statt älteres, größeres Cloud-Modell.

**Scope-Entscheidung:** Kein eigener Hauptabschnitt — ein Kontrollpunkt in der
Eval-Tabelle + ein Satz in §Eval reicht. Keine zweite Generation-Achse aufmachen.

## Subtasks

### T1 — Qwen3.5-27B-FP8 im LiteLLM-Proxy verfügbar machen

Prüfen ob `Qwen/Qwen3.5-27B-FP8` bereits unter `http://10.2.10.33:4000/v1`
erreichbar ist. Falls nicht: Alias in LiteLLM-Config eintragen (analog `qwen36-27b`).
Ziel-Alias z. B. `qwen35-27b`.

### T2 — Bench-Run mit Qwen3.5-27B-FP8

Dieselbe Containment-Bench (5 Cases, 4 Varianten, N=3) gegen `qwen35-27b` fahren.
Ergebnis-JSON ablegen unter:
`tests/agent-tests/results/containment_hall4_qwen35_27b_N3.json`

### T3 — Ergebnisse vergleichen und Paper-Snippet schreiben

Per-Variante Pass-Rate aus beiden JSONs gegenüberstellen.
Satz für §Eval formulieren, z. B.:
> "Qwen 3.6-27B-FP8 outperforms Qwen 3.5-27B-FP8 at identical parameter count
> (Δ = X pp overall), consistent with reported generation improvements and
> supporting on-premises deployment of smaller, more recent models."

Tabelle in Paper um "Qwen 3.5-27B" Spalte/Zeile ergänzen (als Kontrollpunkt,
nicht als Hauptachse).

## Acceptance Criteria

- `containment_hall4_qwen35_27b_N3.json` existiert mit vollständigen Ergebnissen
- Zahlenwert-Vergleich (3.5 vs 3.6 @ 27B) ist reproduzierbar dokumentiert
- Paper §Eval enthält ≤ 2 Sätze + Tabellenzeile zu diesem Kontrollpunkt
- Kein eigener Unterabschnitt — bleibt Fußnote / Kontrollpunkt-Ebene

## References

- Baseline-Ergebnisse: `tests/agent-tests/results/containment_hall4_baseline_N3.json`
- Verwandte Tasks: [[task-paper-pattern-modelsize-eval]]
- Paper: `paper/etfa2026/conference_etfa_2026.tex`
- LiteLLM-Proxy: `http://10.2.10.33:4000/v1`
