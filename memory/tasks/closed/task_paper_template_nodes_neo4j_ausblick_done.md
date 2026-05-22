---
name: Task – Template-Nodes in Neo4j als Paper-Ausblick
description: IDTA-Template-Instanzen als :SubmodelTemplate-Knoten in Neo4j beschreiben und als Future-Work-Punkt im Paper §Ausblick verankern.
type: task
status: closed
priority: low
closed: 2026-05-22
---

## Background

IDTA-Templates liegen als JSON vor. Idee: Templates und/oder Beispiel-Instanzen
direkt in Neo4j laden — nicht als `:Submodel`, sondern mit eigenen Labels
`:SubmodelTemplate` / `:SubmodelExample`, verknüpft mit `:SemanticConcept`-Knoten.

**Hypothese:** Modelle — besonders kleinere — könnten davon profitieren, weil
die gleiche Query-Struktur und dieselben Rückgabefelder wie bei echten Daten
verwendet werden. Kein neues Tool-Interface nötig. Schema-Grounding ohne
externe Vektoren.

**Risiko:** Modell könnte Template-Knoten als echte Asset-Daten interpretieren
(Contamination). Absicherung über:
- Deterministischen Label-Filter in `query_aas_graph` (`WHERE NOT 'SubmodelTemplate' IN labels(n)`)
- Separates Tool `query_aas_templates` — Absicht im Tool-Call, nicht im Ergebnis
- Redundante Property `_is_template: true` auf allen Template-Knoten

**Entscheidung (2026-05-17):** Kein Implementierungs- oder Evaluations-Aufwand
bis zur Paper-Abgabe. Stattdessen als substanzieller Future-Work-Punkt ins Paper.
Keine generische "more domains"-Aussage, sondern technisch konkret mit
Layered-Determinism-Bezug (deterministischer Filter als Schutz vor Contamination).

## Subtasks

### T1 — Paper-Ausblick-Bullet formulieren ✅ (2026-05-22)

Bullet in `paper/etfa2026/content/13-future-work.tex` eingebaut (zusammen mit
dem neuen "Document Knowledge Graph"-Bullet, der `:SemanticConcept` als
gemeinsamen Anker für beide Future-Work-Ideen etabliert).

Finaler Text:

> *"Storing IDTA template instances as typed `:SubmodelTemplate` nodes
> co-located with `:SemanticConcept` nodes would give agents a schema-grounded
> retrieval path without additional tool learning — particularly relevant for
> smaller models that struggle with implicit structural priors. A deterministic
> label filter (`WHERE NOT 'SubmodelTemplate' IN labels(n)`) in all production
> queries mitigates template-contamination risk, exemplifying the
> layered-determinism pattern at the schema level. Measuring the grounding
> benefit against contamination risk across model sizes is left for future work."*

### T2 — (Optional, kein Abgabe-Druck) Konzept-Skizze für Implementierung

Falls Zeit bleibt: kurze Beschreibung des Ingest-Pfads (JSON → Neo4j, welche
Properties, welche Relationships zu `:SemanticConcept`) als Grundlage für
eine spätere Evaluation. Kein Code, nur Datenmodell-Skizze.

## Acceptance Criteria

- ✅ Future-Work-Bullet ist im Paper §Ausblick eingebaut
- ✅ Layered-Determinism-Bezug ist explizit (deterministischer Filter als Schutzmechanismus)
- ✅ Kein Implementierungs-Code committed (das ist Future Work)

## References

- Verwandte Tasks: [[task-paper-layered-determinism-thesis]]
- IDTA-Templates: liegen als JSON vor (Pfad im Repo klären)
- Paper: `paper/etfa2026/conference_etfa_2026.tex`
