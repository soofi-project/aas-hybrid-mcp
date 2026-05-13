# Replace CRAG arXiv citation with MG-CRAG peer-reviewed journal paper

**Created:** 2026-05-13  
**Status:** open  
**Priority:** medium

## Motivation

`yan2024crag` (arXiv:2401.15884) is an arXiv-only preprint — no peer-reviewed venue. MG-CRAG (Masoumi et al., *Knowledge and Information Systems*, Springer 2026) directly extends and validates the CRAG corrective retrieval evaluator concept in a peer-reviewed journal. For ETFA, citing the peer-reviewed work is stronger.

## Subtasks

### T1: Beschaffe MG-CRAG Paper

- DOI + Springer Link für MG-CRAG finden
  - Masoumi, Davar, Eftekhari — "MG-CRAG: fusion of multi-granular retrieval evaluators in corrective RAG with weakly supervised fine-tuning"
  - *Knowledge and Information Systems* (Springer), 2026
- PDF herunterladen → `paper/papers_downloaded/mg_crag2026/mg_crag2026.pdf`
- `metadata.txt` anlegen (Titel, Autoren, Venue, DOI, Jahr)

### T2: BibTeX aktualisieren

- Neuen Eintrag `masoumi2026mgcrag` als `@article` in `paper/etfa2026/main.bib` hinzufügen:
  - Autoren: N. Masoumi, O. Davar, M. Eftekhari
  - Titel: MG-CRAG: Fusion of Multi-Granular Retrieval Evaluators in Corrective RAG with Weakly Supervised Fine-Tuning
  - Journal: Knowledge and Information Systems (Springer)
  - Jahr: 2026
  - DOI: (vom Springer Link)
- **`yan2024crag` Eintrag aus `main.bib` entfernen** — kein arXiv nötig, wenn peer-reviewed Reference verfügbar ist

### T3: Paper-Text anpassen

- In `content/06-architecture.tex` (Line ~57):
  ```
  \cite{yan2024crag} → \cite{masoumi2026mgcrag}
  ```
- Aktuelle Formulierung:
  > "Retrieval evaluator scores evidence quality on a 0.0–1.0 scale; below threshold the agent generates a refined query and retries, up to a configurable refinement limit~\cite{yan2024crag}."
- Prüfen ob MG-CRAG denselben Konzeptbeschrieb hat (retrieval evaluator → confidence score → corrective action) oder ob Anpassung nötig ist. Bei Bedarf Satz leicht anpassen.

### T4: Konsistenz-Check

- `grep -rn "yan2024crag" paper/etfa2026/` — keine Hits mehr
- Paper rebuilden, `.bbl` prüfen

## References

- MG-CRAG: Masoumi, N., Davar, O., Eftekhari, M. — *Knowledge and Information Systems* (Springer), 2026
- Original CRAG (arXiv, wird entfernt): Yan et al., arXiv:2401.15884
