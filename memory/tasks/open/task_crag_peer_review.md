# Replace CRAG arXiv citation with MG-CRAG peer-reviewed journal paper

**Created:** 2026-05-13
**Status:** open (PDF pending)
**Priority:** medium

## Done ✓

- **BibTeX:** `yan2024crag` → `masoumi2026mgcrag` in `main.bib` (✅)
- **Paper text:** `\cite{yan2024crag}` → `\cite{masoumi2026mgcrag}` in `06-architecture.tex:57` (✅)
- **Metadaten:** DOI `10.1007/s10115-026-02778-2`, `metadata.txt` created (✅)

## Still Open

### T1: PDF beschaffen

- Springer blockt direkten Download (HTML statt PDF)
- E-Mail an Autoren (Dr. Masoumi + co-authors) ist unterwegs
- PDF nach Erhalt: `paper/papers_downloaded/masoumi2026mgcrag/masoumi2026mgcrag.pdf`
- Optional: markdown extrahieren

### T2: Stale LaTeX files + memory doc

- `.aux` und `.bbl` содержат noch `yan2024crag` — werden beim nächsten rebuild automatisch sauber
- `memory/agent_variants.md:129` hat noch "Based on CRAG (yan2024crag)" → auf `masoumi2026mgcrag` aktualisieren

## References

- MG-CRAG: Masoumi, N., Davar, O., Eftekhari, M. — *Knowledge and Information Systems* 68(1):149, 2026. Springer. DOI: 10.1007/s10115-026-02778-2
- Original CRAG (arXiv, wird nicht mehr zitiert): Yan et al., arXiv:2401.15884
