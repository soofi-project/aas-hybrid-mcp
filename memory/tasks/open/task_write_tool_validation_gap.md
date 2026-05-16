---
name: Task – Write Tool Validation Gap Analysis
description: Quantify and mitigate the ability of agents to bypass Maintenance Instructions template checks by using put_submodel_element, and capture the finding for the paper
type: task
status: open
priority: high
---

## Background

Die Interaktion `interaction-protocol/2026-05-15T17-32-26Z__5ca5b397266a` zeigte, dass `put_submodel` korrekt an der BaSyx-SDK-Validierung scheitert (falsches `semanticId`-Format, Typ-Mismatches), der Agent jedoch durch sequentielle `put_submodel_element`-Schreibungen ein inkonsistentes, nur teilweise semantisch annotiertes „Maintenance Instructions“-Submodell anlegen konnte. Damit umgeht er faktisch jede Template-Vollständigkeitsprüfung.

## Goals

- Belastbar belegen, wie häufig Varianten den Validator mit Einzel-Element-Schreibungen umgehen.
- Dokumentieren, welche Validierungen aktuell in `put_submodel` vs. `put_submodel_element` greifen und wo Lücken bestehen.
- Evaluieren und empfehlen, wie Write-Rechte künftig gestaltet werden sollen (Slot-Filling, Usecase-spezifische Tools, Entfernung der Element-Write-Tools) und wie die Erkenntnis ins Paper fließt.

## Subtasks

### T1 – Mess-Infrastruktur nutzen
- `tests/agent-tests` um Write-Cases erweitern, die das Anlegen eines Maintenance-Instructions-Submodells verlangen (mit/ohne fehlende Felder).
- Testläufe über alle Varianten fahren und `results/run_*.json` archivieren.
- Auswerten, wie oft `put_submodel` fehlschlägt und anschließend `put_submodel_element`-Calls dieselbe Struktur erzeugen.

### T2 – Validator-Coverage dokumentieren
- Prüfen, welche Checks BaSyx-SDK bei `put_submodel` vs. `put_submodel_element` auslöst (z.B. verpflichtende `semanticId`, Typen, Kardinalitäten).
- Festhalten, welche Template-Validierungen NICHT greifen (Cardinality, Pflichtfelder, MultiLanguageProperty-Sprachen etc.).

### T3 – Mitigations & Paper-Einbindung
- Optionen bewerten: (a) Slot-Filling-Tool in LangGraph (erst sammeln, dann `put_submodel`), (b) Usecase-spezifisches Write-Tool mit deterministischer Template-Füllung, (c) Entzug von `put_submodel_element` für Produktionsläufe.
- Für jede Option Aufwand, Risiken und Auswirkungen auf Werker-Interaktion skizzieren.
- Entscheidungsvorschlag formulieren und festhalten, wie der Befund im Paper genutzt wird (Lessons Learned / Evaluation).

## Acceptance Criteria

- Messdaten existieren, die zeigen, in wie vielen Runs der Validator via Element-Schreibungen umgangen wurde.
- Tabelle oder Abschnitt dokumentiert die aktuelle Validator-Abdeckung je Write-Tool.
- Vergleich der Mitigationsoptionen mit Empfehlung und Paper-Platzierung liegt vor.
- Ergebnis als Input für Paper-Abschnitt referenzierbar (z.B. Ablage im Paper-Todo oder Memory-Eintrag).

## References

- interaction-protocol/2026-05-15T17-32-26Z__5ca5b397266a
- tests/agent-tests (Runner, Evaluator, Cases)
- memory/tasks/open/task_container_location_traversal_prompt_fix.md
