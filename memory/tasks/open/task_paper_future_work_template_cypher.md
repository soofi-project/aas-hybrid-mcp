---
name: Task - Future Work — Pre-compile IDTA Templates to Cypher at Ingest
description: Add a future-work paragraph hypothesising that smaller LLMs may fail at JSON-template→Cypher translation, and that pre-compiling templates into Cypher fragments/examples per field at ingest could close that gap
type: task
status: open
priority: medium
---

## Summary

Eine Future-Work-Hypothese, die in §13 (`13-future-work.tex`) verankert werden soll —
und parallel als Forschungsfrage notiert wird, falls Bench-B / die geplante
Multi-Modell-Auswertung tatsächlich zeigt, dass kleinere LLMs schwächeln.

**Hypothese:** Wenn kleinere LLMs (z. B. < 30B Parameter) die Bench-B-Queries
schlechter lösen als Qwen3.5-120B, ist eine plausible Ursache nicht die
Reasoning-Tiefe, sondern der **Übertrag zwischen Repräsentationen**: die IDTA-Templates
liegen als JSON im MCP-Server, die Daten liegen aber im Neo4j-Graph und müssen per
Cypher abgefragt werden. Das LLM muss diesen Sprung selbst leisten — JSON-Template-
Pfad → Cypher-Pattern.

**Lösungsidee:** Schon **beim Einlesen** der Templates (oder beim Bauen des
`get_templates_index()`-Outputs) die Template-Felder auf Cypher-Snippets / Cypher-
Beispiele mappen. Das LLM sieht dann nicht „SubmodelElement `MaxRotationSpeed` in
Template `AGV-TechnicalData`" sondern direkt das passende Cypher-Pattern, das den
Wert holt — Beispiel inklusive.

Das verschiebt Komplexität von Inference-Time zu Index-Build-Time und sollte
kleinere LLMs entlasten.

## Was im Paper landet (§13)

Ein Absatz, knapp, klar als Hypothese formuliert — kein „we will do X", sondern
„a plausible direction is X, motivated by Y". Beispiel-Struktur:

> *Our evaluation uses a 120B-parameter model. Preliminary observation suggests that
> smaller models may struggle not with reasoning depth but with the implicit
> translation between the JSON template representation and the Cypher query layer.
> A future direction is to pre-compile IDTA templates into Cypher fragments at
> ingest time, exposing per-field query examples to the agent. This shifts the
> JSON→Cypher mapping from inference-time inference to index-build-time compilation
> and may close the gap for self-hostable open-weight models in the 7B–30B range.*

Formulierung muss durch [[task_paper_claim_audit]] (kein Overclaim) und
[[task_paper_style_review]] (keine Marketing-Sprache) durchkommen.

## Subtasks

### T1: §13-Absatz formulieren und einfügen

- Datei: `paper/etfa2026/content/13-future-work.tex`
- Eine Subsection oder ein klarer Absatz, max. ~10 Zeilen
- Als **Hypothese** kennzeichnen (nicht als Plan / Zusage)
- Konkret machen: welche Templates, welche Cypher-Beispiele, was der Index ändert

### T2: Eigenes Memo zur Hypothese (separat von Paper)

- Memory-Doc: `memory/research_idea_template_cypher_compile.md` (oder als Eintrag in
  `memory/future_phases.md`)
- Skizziert: Was wir technisch ändern müssten (`get_templates_index()`,
  Ingest-Pipeline, Schema des Index), grobe Aufwandsschätzung, was wir vorher
  empirisch brauchen würden (Bench mit kleinerem Modell)

### T3: Trigger-Bedingung für „aus Future Work nach oben holen"

Wann lohnt es sich, das Thema in einem Follow-up-Paper voll auszuarbeiten?
- Bench-B mit einem 7B–30B-Modell zeigt deutlich schlechtere Performance als 120B
- Fehler-Klassen lassen sich kausal auf JSON↔Cypher-Übertrag zurückführen
  (nicht: generelles Halluzinieren, nicht: tool-call-Reihenfolge)
- Verfügbare Zeit / freier Slot in der Pipeline

Dokumentation der Bedingung im Memo (T2), damit eine spätere Entscheidung nicht
„weil ich Lust habe" ist.

### T4 (optional, nur falls Bench das nahelegt): Quick Probe

Eine **kleine** Validierung *bevor* der Future-Work-Absatz konkreter wird:
- Eine handgepflegte Cypher-Übersetzung für 1–2 Templates (z. B. AGV-TechnicalData,
  HierarchicalStructures) in `get_templates_index()` mit aufnehmen
- Mit einem kleineren Modell laufen lassen, Diff zur JSON-only-Variante messen
- Wenn sichtbarer Lift: Future-Work-Absatz konkreter formulieren. Wenn nicht:
  Hypothese im Paper trotzdem behalten, aber klarer als „open question" kennzeichnen.

T4 ist explizit **optional** und nur sinnvoll, wenn Zeit + Modell-Zugriff da sind.

## Acceptance Criteria

- `13-future-work.tex` enthält einen Absatz/Subsection zur Pre-Compile-Hypothese
- Formulierung passt durch Claim-Audit ([[task_paper_claim_audit]]) und Style-Review
  ([[task_paper_style_review]])
- Eigenes Memo existiert (T2) mit konkretem Trigger für Follow-up
- Falls T4 gemacht: Ergebnis im Memo dokumentiert (Lift / kein Lift / unklar)

## Non-Goals

- **Keine** Implementierung im aktuellen Paper-Scope — bleibt Future Work
- **Keine** vollständige Multi-Modell-Auswertung — wäre ein eigenes Paper
- **Kein** Refactoring der Template-Pipeline „auf Verdacht"

## References

- IDTA-Templates: `mcp-server/src/aas_hybrid_mcp/idta_templates/` (?)
- Templates-Index: `mcp-server/src/aas_hybrid_mcp/tools/template_search.py`,
  `get_templates_index()`
- Bench-B-Protokoll: `memory/bench_b_evaluation.md`
- Modellverfügbarkeit (H200): `memory/llm_deployment.md` (auto-memory)
- Schwester-Tasks: [[task_paper_claim_audit]], [[task_paper_style_review]]
