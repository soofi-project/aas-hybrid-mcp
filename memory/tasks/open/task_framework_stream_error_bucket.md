---
name: Task – Framework: Stream-Error als separater Failure-Bucket
description: Runner detektiert "[stream error" → markiert als infra-fail, nicht content-fail. Reporter zeigt 3 Buckets. Verhindert Infrastruktur-Rauschen in Compliance-Statistik.
type: task
status: open
priority: medium
---

## Background

Containment-Bench 2026-05-15 zeigte CRAG-Variant mit 40% Pass-Rate. Trace-
Analyse (`interaction-protocol/2026-05-15T19-24-21Z__0b18aa96ebde/turn-01__2026-05-15T19-25-28Z.md`)
zeigt: korrekte Antwort war im letzten Tool-Result bereits da, dann
`[stream error — see server logs]` vor Final-Output. Modell hat *nicht*
inhaltlich versagt, sondern Stream-Auslieferung ist gecrasht (vermutlich
CRAG `relevance`-Node oder LiteLLM-Hiccup).

Aktuell zählt das Framework solche Stream-Errors als „content fail"
(Score 0, Pass-Rate-Drop). Das verfälscht die Compliance-Statistik
gegen komplexere Variants (CRAG/Plan/Reflexion haben mehr LLM-Calls →
mehr Failure-Surface für Stream-Errors).

## Goal

Stream-Errors als separater Bucket tracken — bleibt für Variant-Reliability-
Statistik relevant, fällt aber aus der Modell-Compliance-Statistik raus.

## Subtasks

### T1 — Runner: Stream-Error-Detection

`tests/agent-tests/framework/runner.py`:

- Nach `_strip_think_blocks()`: check ob Response `[stream error` enthält.
- Wenn ja: `result.error = "agent stream error"` (bestehendes Feld nutzen,
  bisher nur für HTTP-Errors gesetzt).
- `result.response` so lassen wie sie ist (für Debugging).

### T2 — Evaluator: Infra-Fail-Bucket

`tests/agent-tests/framework/evaluator.py`:

- `Evaluation.notes` um `"stream_error"` ergänzen wenn
  `result.error == "agent stream error"`.
- Optional: neues `bool infra_failure` Feld am Evaluation-Objekt für
  saubere Reporter-Logik.

### T3 — Reporter: 3-Bucket-Anzeige

`tests/agent-tests/framework/reporter.py`:

- Pass-Spalte um Marker erweitern:
  - `ok` (grün)
  - `fail` (rot) — content-fail
  - `infra` (gelb) — stream-error / HTTP-Fehler
- Per-Variant-Summary um Spalte `Infra %` ergänzen.
- JSON-Export inkludiert `infra_failure: bool` pro Run.

### T4 — Bench-Run wiederholen oder Re-Analyse

Optionen:

- **(a)** Bench nicht neu fahren, sondern nur Re-Auswertung der
  bestehenden JSON-Daten — alle Stream-Errors aus den bestehenden
  Traces nachträglich als infra-fail klassifizieren.
- **(b)** Containment-Bench mit gefixtem Reporter neu fahren (zusätzlich
  30 min).

Vorschlag: (a) für Schnelligkeit, (b) wenn die Stream-Error-Häufigkeit
sich seit dem Test verändert (LiteLLM-Update etc.).

## Acceptance Criteria

- Runner setzt `result.error = "agent stream error"` bei
  `[stream error` im Response.
- Reporter zeigt 3 Buckets (ok / fail / infra) in Table + Summary.
- JSON-Export-Schema erweitert um `infra_failure`.
- CRAG-40%-Pass-Rate aus dem Baseline-Run re-klassifiziert: wieviele
  echte Compliance-Fails vs. Stream-Errors? Tabelle dokumentieren.
- Memory-Notiz in `bench_results.md` (oder ähnlich): „CRAG infra-fail
  rate war X% — nach Korrektur Compliance-Pass-Rate Y%".

## References

- Trace mit Stream-Error: `interaction-protocol/2026-05-15T19-24-21Z__0b18aa96ebde/turn-01__2026-05-15T19-25-28Z.md`
- Bench-Daten: `tests/agent-tests/results/containment_hall4_baseline_N3.json`
- Folge-Task: [[task-crag-failure-deep-dive]] — braucht das hier als Prereq.
