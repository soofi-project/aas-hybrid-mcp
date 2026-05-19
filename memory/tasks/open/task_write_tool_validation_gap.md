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

### T0 – Explizite Prompt-Instruktion vor dem Test ✅ Done (2026-05-18)

`mcp-server/src/aas_hybrid_mcp/tool_descriptions/put_submodel_element.md` aktualisiert:
- Restriktion explizit: nur für existierende Submodelle, kein piecemeal-Aufbau
- Agent soll bei Fehler analysieren und korrigieren, nicht eskalieren
- Server erzwingt Parent-Existence-Check (Gate 2) — Instruktion jetzt architektonisch gestützt

### T1 – Mess-Infrastruktur nutzen
- `tests/agent-tests` um Write-Cases erweitern, die das Anlegen eines Maintenance-Instructions-Submodells verlangen (mit/ohne fehlende Felder).
- Testläufe über alle Varianten fahren und `results/run_*.json` archivieren.
- Auswerten, wie oft `put_submodel` fehlschlägt und anschließend `put_submodel_element`-Calls dieselbe Struktur erzeugen.

### T2 – Validator-Coverage dokumentieren
- Prüfen, welche Checks BaSyx-SDK bei `put_submodel` vs. `put_submodel_element` auslöst (z.B. verpflichtende `semanticId`, Typen, Kardinalitäten).
- Festhalten, welche Template-Validierungen NICHT greifen (Cardinality, Pflichtfelder, MultiLanguageProperty-Sprachen etc.).

### T3 – Validator-Registry-Gate umgesetzt ✅

Zwei strukturelle Garantien implementiert (2026-05-18):

**Gate 1 — `REQUIRE_TEMPLATE_VALIDATOR` in `template_validator.py`:**
- `put_submodel` ohne semanticId → deterministischer Fehler mit Hinweis auf `get_templates_index()`
- `put_submodel` mit semanticId aber ohne registrierten Validator → Fehler mit Liste der unterstützten semanticIds
- Kein Default — muss explizit in `.env` gesetzt sein (`true` oder `false`), sonst Runtime-Error

**Gate 2 — Parent-Existence-Check in `put_submodel_element` (`write_tools.py`):**
- `get_submodel` auf BaSyx vor jedem Element-Write
- Submodel existiert nicht → Fehler mit Hinweis auf `put_submodel`
- Agent bekommt klare Fehlermeldung statt stilles Durchschlüpfen

**Verbleibender Gap (Limitation, ehrlich im Paper):**
- ZeroToMany-Strukturen (z.B. `ServiceRequestNotification`-SMC): leere Shell mit korrekter semanticId besteht Gate 1, da die generierten Klassen nur Top-Level-Kwargs prüfen, nicht rekursiv nested SMC-Pflichtfelder
- Agent kann: valide leere Shell posten → Gate 2 passiert (Parent existiert jetzt) → Elemente nachschieben
- Fix: rekursive Validierung oder Mindest-1-Inhalt erzwingen → Future Work in §13

**Paper-Aussage:** Befund (Bypass trat auf trotz Prompt-Instruktion) + Architektur (Validator-Registry als strukturelle Garantie für Gate 1+2) + Limitation (ZeroToMany-Gap) = dreistufiger Layered-Determinism-Beleg.

### T4 – Eval-Query-Design für Paper-Methodologie ✅

Die Testfälle in `tests/agent-tests/cases/srn_bypass.yaml` sind bewusst so konstruiert:

**Kein direkter AAS-ID im Query** — Werker kennen IDs nicht, sie sagen „der Transportroboter in Halle 4" oder geben die Seriennummer (`MIR100-2020-001`) an. Der Agent muss erst per Spatial-Disambiguation oder Seriennummern-Lookup den Asset auflösen (zusätzliche Tool-Calls → mehr Kontext-Druck → Bypass wahrscheinlicher).

**„Quickly"** — reduziert die Wahrscheinlichkeit dass der Agent Rückfragen stellt. Ein Agent unter Zeitdruck rationalisiert den Bypass-Pfad eher als einer der in Ruhe die Payload korrigieren kann.

**Seriennummer-Variante** — realistisch: Typenschild am Gerät zeigt `MIR100-2020-001`, nicht `urn:aas:mir100_001`. Erzwingt eine Lookup-Sequenz, die echte Feldszenarien abbildet.

Diese Designentscheidungen gehören in §10-Evaluation als Methodologie-Satz: *„Queries were formulated using natural asset references (location, serial number) rather than AAS identifiers, reflecting realistic operator input; the term 'quickly' was included to reduce the likelihood of the agent pausing to request clarification."*

## Acceptance Criteria

- Messdaten existieren, die zeigen, in wie vielen Runs der Validator via Element-Schreibungen umgangen wurde.
- Tabelle oder Abschnitt dokumentiert die aktuelle Validator-Abdeckung je Write-Tool.
- Vergleich der Mitigationsoptionen mit Empfehlung und Paper-Platzierung liegt vor.
- Ergebnis als Input für Paper-Abschnitt referenzierbar (z.B. Ablage im Paper-Todo oder Memory-Eintrag).

## References

- interaction-protocol/2026-05-15T17-32-26Z__5ca5b397266a
- tests/agent-tests (Runner, Evaluator, Cases)
- memory/tasks/open/task_container_location_traversal_prompt_fix.md
