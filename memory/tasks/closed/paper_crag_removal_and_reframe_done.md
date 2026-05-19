---
name: Paper CRAG Removal and Reframe Done
description: CRAG aus Eval entfernt; §08 + §13 mit architektonisch korrekter Einordnung; masoumi2026mgcrag aus Bib.
type: task
status: done
---

## Was umgesetzt

**§06 Architecture** — CRAG-Bullet (Corrective RAG) vollständig entfernt. Zähler von „four" auf „three" korrigiert.

**§08 Retrieval Pipeline** — Zwei Sätze am Ende von „Retrieval Enhancements" ergänzt: CRAG-Relevance-Gate ist auf diesem Hybrid-Backend nur auf dem Vector-Pfad sinnvoll (Graph-Ergebnisse sind deterministisch); ob ein solches Gate über den Reranker hinaus hilft, bleibt Future Work mit `\cite{yan2024crag}`.

**§13 Future Work** — „Multi-Granular Relevance Evaluation"-Item (das fälschlicherweise `masoumi2026mgcrag` zitierte) ersetzt durch knappen „Corrective Retrieval"-Eintrag: path-aware CRAG-Variante als Komplement zum Reranker, cite `yan2024crag`.

**main.bib** — `masoumi2026mgcrag` entfernt (war nur in dem ersetzten Item referenziert). `yan2024crag` bleibt für §08 + §13.

**Build:** grün, keine broken references.

## Entscheidungen on the way

- CRAG nicht in Related Work: kein direkter Beitrag zur Hauptthese (Layered Determinism / Pattern×Modellgröße), daher nur in §08 und §13.
- Implementierung eines CRAG-Gates vor Submission abgelehnt (Advisor-Empfehlung): Aufwand 4–6 Tage, orthogonal zur These, Reviewer-Concern mit §08-Prosa abgedeckt.
- `masoumi2026mgcrag` raus: der zugehörige Multi-Granular-Item fiel weg; kein anderer Verwendungsort.
