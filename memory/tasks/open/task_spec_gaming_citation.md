---
name: Task – Specification Gaming Citation Audit
description: Prüfen ob park2024aideception die beste Referenz für "specification gaming" in §11 Discussion ist, oder eine präzisere existiert.
type: task
status: open
priority: medium
---

## Summary

In §11 Discussion (Layered Determinism, Write-Anekdote) wird der Begriff *specification gaming* mit `park2024aideception` (Park et al. 2024, "AI deception: A survey of examples, risks, and potential solutions", *Patterns*) referenziert. Der Kontext: Ein goal-directed Agent umgeht den Template-Validator, indem er Strukturen elementweise über `put_submodel_element` aufbaut.

**Problem:** Park et al. ist ein Survey über AI-Deception im allgemeinen Sinn (Lügen, Tarnung, Manipulation). "Specification gaming" im engeren Sinne — ein Agent exploitet Lücken in der Zielspezifikation, ohne zu "lügen" — könnte treffender belegt sein.

## Subtasks

### T1 — Spezifikation-Gaming-Begriff klären
- Ist "specification gaming" der richtige Terminus, oder wäre "reward hacking", "objective mis-specification", oder einfach "unintended execution path" treffender?
- Der Agent "lügt" nicht — er findet einen ungesicherten Pfad. Das ist ein wichtiges Argument.

### T2 — Alternative Referenzen prüfen
Kandidaten für präzisere Referenzierung:
- **Krakovna et al. 2020** — "Specification gaming: the flip side of AI ingenuity" (DeepMind Blog, ggf. nicht peer-reviewed → arXiv-Check)
- **Amodei et al. 2016** — "Concrete Problems in AI Safety" (specification gaming als eine der 5 Kategorien)
- **Lehman et al. 2020** — "The Surprising Creativity of Digital Evolution" (evolutionäre specification gaming Beispiele)
- Ggf. gibt es ein passenderes Zitat **in** Park et al. selbst (Secondary Citation)

### T3 — Entscheidung und Edit
- Wenn eine präzisere Referenz existiert: Austauschen in `11-discussion.tex` und `main.bib` (Citation-Workflow: erst WebFetch-Bestätigung, dann BibTeX-Eintrag).
- Wenn Park et al. passen sollte: Begründung dokumentieren und Task schließen.
- Ggf. den Terminus anpassen (z.B. von "specification gaming" zu "specification gaming~\cite{krakovna2020spec Gaming}" oder den Begriff umformulieren).

## Acceptance Criteria
- Referenz ist entweder bestätigt (mit Begründung) oder durch präzisere ersetzt
- BibTeX-Eintrag verifiziert (DOI, Venue, Autoren) falls neu
- Build bestanden

## References
- Files: `paper/etfa2026/content/11-discussion.tex` (Zeile 8), `paper/etfa2026/main.bib` (Zeile 115)
