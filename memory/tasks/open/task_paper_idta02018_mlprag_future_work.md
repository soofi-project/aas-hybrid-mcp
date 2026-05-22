---
name: Task – IDTA 02018 + MLP-RAG Future-Work-Bullet für §13
description: Future-Work-Bullet formulieren der IDTA 02018 als Zielformat für PDF-Extraktion und MLP-RAG als Skalierungspfad verbindet, als Pendant zum §12 Submodel Text Retrieval Limit.
type: task
status: open
priority: low
---

## Background

In §12 steht bereits: *"Text-bearing submodel fields such as `InstructionMaintenanceStep`
are not embedded and therefore not searchable via vector retrieval."*

Das ist die Limitation-Seite. Was fehlt, ist der korrespondierende Future-Work-Ausblick
der die konstruktive Richtung zeigt: wenn Maintenance-Inhalte strukturiert in
IDTA 02018-Feldern liegen statt in PDFs, löst sich die Limitation auf — und die
Architektur gewinnt mehrere Vorteile gleichzeitig.

**Kernargument (für den Bullet):**
1. **IDTA 02018 als Zielformat:** MaintenanceInstructions-Schablone deckt planmäßige
   + korrektive Wartungsschritte ab (`MaintenanceTask`, `InstructionMaintenanceStep`,
   Intervalle, Sicherheitshinweise). Realität: Felder oft leer, PDF fast immer vorhanden.
   Pfad: PDF-Ingest über Phase-10-Extraktions-Tools → strukturierte IDTA-02018-Felder
   füllen bevor die Schale registriert wird.
2. **MLP-RAG als Skalierungspfad:** Bei vielen Assets mit gepflegten Submodell-Feldern
   ist direktes Weaviate-Embedding über `MultiLanguageProperty`/`Property`-Werte
   dem PDF-RAG-Pfad überlegen: kein Extraktionsrauschen, direkte AAS-Graph-Verknüpfung,
   kein Chunking, XAI-traceable (idShortPath als Quellenangabe).
3. **Auflösung der Limitation:** Wenn Felder gepflegt → "Submodel Text Retrieval"-Limit
   aus §12 entfällt strukturell. Der §12-Bullet und dieser §13-Bullet bilden ein Paar.

**Vorhandene Bausteine (nicht neu erfinden):**
- Phase 10 "PDF-to-AAS Extraction" (`memory/future_phases.md`) — Extraktionsworkflow
- Phase 12 "MLP-RAG sibling axis" (`memory/future_phases.md`) — Weaviate-Collection
  über Submodell-Werte mit semanticId-Metadaten
- §12 "Submodel Text Retrieval" (`paper/etfa2026/content/12-limitations.tex`)

## Subtask

### T1 — Future-Work-Bullet für §13 schreiben

Bullet-Entwurf (Richtung, kein Wortlaut-Lock):

> *"AAS-Native Maintenance Content:* While the current pipeline embeds PDF attachments
> as the primary document source, IDTA 02020 (Handover Documentation) and IDTA 02018
> (Maintenance Instructions) define structured submodel fields such as
> `InstructionMaintenanceStep` that could carry equivalent content. Tooling that
> extracts PDF content into these fields before shell registration would shift the
> retrieval path from PDF-chunk search to direct submodel-field embedding — removing
> the chunking and extraction noise identified in Sec.~\ref{sec:limitations}.
> At scale, embedding `MultiLanguageProperty` and `Property` values directly into a
> dedicated Weaviate collection (keyed by `idShortPath`) would provide XAI-traceable
> retrieval without any PDF dependency — an open empirical question is at which
> asset-density this path outperforms document RAG."*

Länge und Platzierung in §13 gegen Page-Budget abwägen. Wenn knapp: auf 2-3 Sätze
kürzen und Phase-12-MLP-RAG-Aspekt in Klammersatz.

## Acceptance Criteria

- Future-Work-Bullet in §13 eingebaut
- Bullet referenziert §12 Submodel Text Retrieval Limitation explizit (`Sec.~\ref{sec:limitations}`)
- IDTA 02018 / 02020 namentlich genannt
- MLP-RAG / Submodell-Field-Embedding-Skalierungsargument enthalten
- Build grün

## References

- `paper/etfa2026/content/12-limitations.tex` — Submodel Text Retrieval Bullet (Pendant)
- `paper/etfa2026/content/13-future-work.tex` — Ziel-Section
- `memory/future_phases.md` — Phase 10 (PDF-to-AAS) + Phase 12 (MLP-RAG sibling axis)
- `C:\repo\submodel-templates\published\Maintenance Instructions\1\0\IDTA_02018_Template_MaintenanceInstructions.json`
- Verwandte Tasks: [[task-paper-layered-determinism-thesis]], [[task-paper-template-nodes-neo4j-ausblick]]
