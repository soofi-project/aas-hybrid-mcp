---
name: Task – GraphRAG / Unified Neo4j Knowledge Graph — Paper-Ausblick
description: Bestehenden "Document Knowledge Graph"-Bullet in §13 um HNSW/GraphRAG und
  "Unified Cypher Surface" ergänzen (Chunks + Templates + ConceptDescriptions in Neo4j).
type: task
status: open
priority: low
---

## Background

Bestehender "Document Knowledge Graph"-Bullet in `paper/etfa2026/content/13-future-work.tex`
(Zeile 13–21) beschreibt LLM-extrahierte KG-Knoten aus Manuals, erwähnt aber nicht:

- HNSW-Chunk-Vektoren direkt in Neo4j (Weaviate-Ablösung)
- `NEXT_CHUNK`-Sequenzierung für Kontext-Expansion nach Vektor-Hit
- `MENTIONS`-Edges von Chunks zu AAS-Knoten für scoped Retrieval
- ConceptDescription-Bibliothek (eCLASS / IDTA) als semantische Suchbasis für
  SemanticId-Zuweisung und Shell-Autoring

Das übergreifende Konzept: `:SemanticConcept` als gemeinsamer Anker für alle drei
Ideen → operationelle Vereinheitlichung (eine DB, ein Betriebspfad) für
Graph-Traversal, Schema-Lookup und Vektor-Ähnlichkeitssuche in einem Cypher-Statement.
Der Agent-Interface bleibt unverändert — er ruft weiterhin Tools, sieht kein Cypher.

### Die drei Dimensionen

**Dimension 1 — DocumentChunk-Knoten mit HNSW-Index:**
`(File)-[:HAS_CHUNK]->(DocumentChunk)` mit Embedding-Property + HNSW-Index;
`NEXT_CHUNK` für sequentielle Kontext-Expansion; `MENTIONS` → `:Submodel`
(submodel-level coarse anchor — kein feingranulares NER/Entity-Linking)
für asset-scoped Retrieval ohne Metadaten-Replikation in die Vektordatenbank.
Echte Entity-Extraktion (NER + LLM-basiertes Linking zu spezifischen Knoten)
ist Phase 2 und separat zu behandeln.
Ob Weaviate entfällt, ist eine empirische Frage (BM25-hybrid recall vs. Neo4j
dense-only HNSW bei Sparse-Identifiern wie Part-Nummern und Fault-Codes).

**Dimension 2 — Template-Nodes (schon im Paper):**
`:SubmodelTemplate`-Knoten verknüpft mit `:SemanticConcept`; deterministischer
Label-Filter als Contamination-Schutz. Synergie: zusammen mit Dimension 1 und 3
bildet `:SemanticConcept` den gemeinsamen Anker.

**Dimension 3 — ConceptDescription-Bibliothek:**
eCLASS / IDTA-CDs als `:ConceptDescription`-Knoten in Neo4j ermöglichen semantische
Suche ("Welche CD passt zu 'Maximaldrehzahl'?") und SemanticId-Zuweisung für bare
Properties. Freiheitsgrad-Kontrolle: dediziertes Tool `find_matching_semanticid()`
statt freiem Cypher-Zugriff — dieselbe Containment-Logik wie Write-Path-Validator.

## Subtasks

### T1 — §13-Bullet um ~3 Sätze ergänzen

Bestehenden "Document Knowledge Graph"-Bullet erweitern (nicht ersetzen).
Datei: `paper/etfa2026/content/13-future-work.tex`, Zeile 13–21.

Entwurf-Ausgangspunkt:

> *An intermediate step would store document chunks as `DocumentChunk` nodes with
> HNSW-indexed embedding properties, linked to `File` nodes via `HAS\_CHUNK` and
> sequenced via `NEXT\_CHUNK`, enabling combined graph-filter and vector queries in
> a single Cypher statement. Whether Neo4j's dense-only HNSW index matches Weaviate's
> BM25-hybrid recall for sparse identifiers such as part numbers and fault codes is
> an open empirical question; the existing cross-encoder reranker partially compensates
> but does not substitute. Combined with template nodes and internalised concept
> descriptions, `:SemanticConcept` would become a shared anchor for retrieval, schema
> grounding, and semantic-ID suggestion~--- consolidating three currently separate
> subsystems into one operational surface without changing the agent's tool interface.*

Länge gegen Page-Budget abwägen; ggf. auf 2 Sätze kürzen.

### T2 — (Optional) Memory-Sketch: Post-Paper-Implementierungs-Skizze

Kurze Beschreibung des Ingest-Pfads für alle drei Dimensionen als Memory-Dokument
`memory/graphrag_neo4j_design.md` (kein Code, nur Datenmodell-Skizze).
Kein Abgabe-Druck — nur wenn Zeit nach ETFA-Submission verfügbar.

## Acceptance Criteria

- T1: Bestehender Bullet in §13 erweitert, Build grün
- Bestehender Bullet-Text bleibt erhalten (nur Ergänzung)
- `:SemanticConcept` als Anker für alle drei Dimensionen explizit erwähnt
- Weaviate-Ablösung als empirische offene Frage formuliert (nicht als Tatsache), BM25-Hedge explizit
- Kein Impl-Code committed

## References

- `paper/etfa2026/content/13-future-work.tex` Zeile 13–21 (bestehender Bullet)
- `memory/tasks/closed/task_paper_template_nodes_neo4j_ausblick_done.md` — Synergie Dim 2
- `memory/tasks/closed/task_paper_future_work_template_cypher_done.md` — "eine Sprache" Cypher
- `memory/tasks/open/task_paper_idta02018_mlprag_future_work.md` — **konkurrierende** Richtung: GraphRAG verbessert den PDF-Chunk-Pfad; IDTA-02018-Felder umgehen ihn. Wenn beide Bullets im Paper landen: eine Cross-Reference-Zeile nötig.
- `memory/future_phases.md` — Phase 12 "MLP-RAG sibling axis" als verwandter Ansatz
- Verwandte Tasks: [[task-paper-layered-determinism-thesis]], [[task-paper-claim-audit]]
