---
name: Task – CRAG Failure-Mode Deep-Dive (40% Pass-Rate Diagnose)
description: CRAG fiel im Containment-Bench 2026-05-15 auf 40% Pass-Rate (vs ReAct 100%). Aufgliedern: Infra-Errors vs echte Compliance-Fails. Server-Logs ziehen + möglicher Bug-Fix in crag_nodes.py.
type: task
status: open
priority: medium
---

## Background

Containment-Bench 2026-05-15 Ergebnisse (N=3 × 4 Variants × 5 Cases = 60 Runs):

| Variant | Pass-Rate | Avg-Dur | Avg-Tools |
|---|---|---|---|
| react | 100% (15/15) | 22s | 14 |
| reflexion | 93% (14/15) | 51s | 23 |
| plan | 73% (11/15) | 60s | 21 |
| **crag** | **40% (6/15)** | 41s | 23 |

CRAG fällt deutlich raus. Mindestens einer der Fails ist nachgewiesener
Stream-Error (siehe [[task-framework-stream-error-bucket]]). Frage: wieviele
sind Stream-Error, wieviele echte Compliance-Versagen?

## Voraussetzung (Hard-Block)

- [[task-framework-stream-error-bucket]] fertig — sonst kann man Infra-
  vs Content-Fails nicht trennen.

## Subtasks

### T1 — Re-Klassifikation der CRAG-Fails

Mit gefixter Stream-Error-Detection:

- Alle 9 CRAG-Fails aus `containment_hall4_baseline_N3.json` durchgehen.
- Pro Fail: ist es Stream-Error (infra) oder content-fail?
- Bei Content-Fails: war es ein Anti-Pattern-Hit, eine falsche Antwort,
  oder Pipeline-Crash?

### T2 — Server-Logs ziehen

`docker logs aas-agent` für Zeitraum 2026-05-15T19:24-19:55 archivieren.
Suchen nach Exceptions / Stack-Traces im CRAG-Pipeline-Code (`crag.py`,
`crag_nodes.py`, `crag_graph.py`).

### T3 — Bug-Hypothese verifizieren

Falls Server-Logs systematischen Crash zeigen (z.B. der bekannte
`int('E0')` Parser-Bug von 2026-05-14, siehe
[[task-container-location-traversal-prompt-fix]] „Out of Scope"):

- Reproduzierbarer Test-Case formulieren
- Fix in `crag_nodes.py` planen
- Eigener Task wenn nicht-trivial

### T4 — Paper-Implikation

Je nach Ergebnis:

- **Wenn meisten CRAG-Fails Infra:** Variant-Reliability-Punkt fürs Paper
  (komplexere Pipeline = mehr Failure-Surface). Compliance-Pass-Rate nach
  Korrektur in der Tabelle nachziehen.
- **Wenn meisten CRAG-Fails echte Compliance:** starker Layered-
  Determinism-Punkt — die *komplexere* Variante macht es schlechter,
  nicht besser. Counter-intuitiv zur Agent-Literatur, paper-würdig.

## Acceptance Criteria

- Tabelle CRAG-Failures × Kategorie (infra-fail / anti-pattern / wrong
  answer / pipeline-crash) erzeugt.
- Server-Logs für den Bench-Zeitraum archiviert.
- Wenn Bug identifiziert: Fix-Task angelegt oder direkt gefixt.
- Paper-Implikation dokumentiert: welcher der zwei Szenarien zutrifft.

## References

- Bench-Daten: `tests/agent-tests/results/containment_hall4_baseline_N3.json`
- Stream-Error-Trace: `interaction-protocol/2026-05-15T19-24-21Z__0b18aa96ebde/turn-01__2026-05-15T19-25-28Z.md`
- Bekannter CRAG-Bug (Out-of-Scope-Notiz): [[task-container-location-traversal-prompt-fix]]
- Prereq: [[task-framework-stream-error-bucket]]
