---
name: Multi-Granular Eval (MG-CRAG) Done — Out of Paper Scope nach Pivot 2026-05-16
description: MG-CRAG-Multigranular-Evaluator nicht implementiert; CRAG-Variante komplett aus Paper raus, MG-CRAG-Zitation wird ebenfalls entfernt.
type: task
status: done
---

## Outcome

Der Task stand bereits seit 2026-05-13 auf „decision pending — default if
undecided: stays in Future Work". Mit dem Paper-Pivot 2026-05-16 ist auch
diese Future-Work-Erwähnung überholt — MG-CRAG wird im Paper gar nicht mehr
zitiert (siehe `task_paper_crag_removal_and_reframe.md` T4).

## Was nicht passiert ist

- Kein PDF-Studium der MG-CRAG-Patterns (T1)
- Keine `RelevanceScore`-Schema-Erweiterung für sentence-level scores (T2)
- Keine `crag_multigranular.py`-Implementierung (T3)
- Keine Graph-Integration mit `CRAG_EVALUATOR_MODE`-Switch (T4)
- Keine §08-Paper-Erweiterung (T5)

## Status der Zitation

`masoumi2026mgcrag` wird in `task_paper_crag_removal_and_reframe.md` T4
aus `main.bib` und allen `.tex`-Files entfernt. PDF unter
`paper/papers_downloaded/masoumi2026mgcrag/paper_davar_masoumi.pdf` bleibt
archiviert für mögliches Follow-up.

## Reaktivierung möglich, wenn

- ein Follow-up-Paper Multi-Granular-Evaluation auf hybridem AAS-Backend
  tatsächlich untersucht (Backend-Mismatch wäre erst zu lösen — siehe
  Node-Decomposed-CRAG-Future-Work)
- ODER ein anderer Industrial-Anwendungsfall mit reinem Document-RAG
  konkret nach MG-CRAG verlangt

## References

- Pivot-Kontext: `task_paper_crag_removal_and_reframe.md`, `paper_etfa2026.md` Pivot-Sektion
- Originalpaper: Masoumi et al. 2026, *Knowledge and Information Systems* 68(1):149
