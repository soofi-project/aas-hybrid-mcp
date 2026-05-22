---
name: Task – Optimizer's Bias Citation für §12/§13
description: Paper finden das Optimizer's Bias / Prompt-Overfitting in LLM-Evaluierungen belegt, als Cite für Single-Model-Family-Limitation.
type: task
status: open
priority: medium
---

## Background

In §12 (Limitations) und §13 (Future Work) wurde die Single-Model-Family-Einschränkung
ergänzt. Der Begriff „optimizer bias" (Prompt-Schicht wurde nur gegen Qwen beobachtet)
braucht einen Peer-Review-Beleg.

Gesucht: Paper das zeigt, dass Prompts / Benchmarks / Toolbeschreibungen auf die
Modellfamilie overfittet werden können — auch bekannt als:
- „optimizer's bias" in LLM eval
- „prompt overfitting" to a model family
- „evaluation contamination" durch iteratives Tuning gegen eine Familie
- Benchmark-Design-Diskussion zu single-model-family-Evaluierungen

## Subtasks

### T1 — Paper suchen
`/paper-search` mit Queries wie:
- „optimizer bias prompt tuning LLM evaluation"
- „prompt overfitting model family benchmark"
- „evaluation bias single model family LLM"

Kandidaten prüfen: Autoren, Venue, Jahr, DOI verifizieren bevor Bib-Eintrag.

### T2 — Bib-Eintrag in main.bib
Key-Konvention: `<erstautor><jahr><slug>` (z.B. `mizrahi2024state`).
Pflichtfelder: author, title, year, booktitle/journal, pages/volume, doi.
Erst greppen ob Variante schon existiert.

### T3 — Cite in §12 einbauen
Stelle in `12-limitations.tex`: nach „introducing a potential optimizer bias toward that family"
→ `\cite{<key>}` anhängen.

## Acceptance Criteria

- Peer-reviewtes Paper (IEEE/ACM/Springer/EMNLP/ICLR/NeurIPS o.ä.) gefunden und verifiziert
- Bib-Eintrag in `main.bib` ohne Duplikat
- `\cite{}` in §12 Limitations eingebaut
- Build grün

## References

- `paper/etfa2026/content/12-limitations.tex` — Single-Model-Family-Bullet
- `paper/etfa2026/content/13-future-work.tex` — Cross-Family-Validation-Bullet
- `paper/etfa2026/main.bib`
