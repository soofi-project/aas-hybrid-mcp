---
name: Task – Paper Data Quality Assumption
description: Dokumentiert für das Paper, dass die Agenten-Resultate saubere, template-konforme AAS voraussetzen; der Vergleich mit unsauberen Modellen bleibt Future Work.
type: task
status: open
priority: medium
---

## Summary

- Aktuelle Experimente und Evaluationen setzen voraus, dass die bereitgestellten AAS-Templates semantisch sauber und template-konform modelliert sind (vgl. `aasx-dev-templates/`).
- Diese Annahme soll im Paper (Outlook/Discussion) transparent gemacht werden.
- Ein strukturierter Vergleich mit "messy, aber syntaktisch validen" AAS wird als Future Work markiert und nicht vor der Submission umgesetzt.

## Subtasks

### T1: Annahme im Paper verankern

- Stellen im Paper identifizieren (z. B. `Discussion` oder `Outlook`), an denen die Datenqualitäts-Annahme klar ausgesprochen wird.
- Formulierung ergänzen, die auf die sauberen Templates verweist und transparent macht, dass das Agentenverhalten damit korreliert.

### T2: Future-Work-Punkt formulieren

- Im selben Abschnitt einen klaren Hinweis setzen, dass Experimente mit strukturell korrekten, aber semantisch unsauberen AAS noch ausstehen.
- Optional: kurz schildern, welche Fragestellungen (z. B. Einheitensalat, fehlende ConceptDescriptions) als Naechstes untersucht werden sollen.

**Outlook-Text (fertig formuliert, direkt ins Paper uebertragbar):**

> Real-world AAS deployments frequently contain schema violations, incomplete
> submodels, and inconsistent idShort assignments. Rather than building
> fault-tolerance into the query agent -- which would hide data-quality problems
> behind increasingly complex reasoning heuristics -- a dedicated agentic
> preprocessing stage could validate and complete shells against IDTA templates
> before indexing. Such a pipeline would run template-conformance checks
> deterministically and invoke an LLM only for ambiguous repair decisions,
> keeping the query agent's input clean by construction. This separation aligns
> with the layered-determinism principle introduced in \S\,\ref{sec:discussion}:
> deterministic guarantees at each layer reduce the reasoning burden on the
> model above, and a data-quality layer is the natural foundation of that stack.

Platzierung: Paragraph in §Future Work, nach dem Abschnitt zu SOOFI/Modell-Austausch.
Verbindung zu §Discussion herstellen wo Layered Determinism definiert wird.

### T3: Kontext weitergeben

- Im internen Wissensspeicher verlinken, dass `aasx-dev-templates/` den "clean baseline"-Status hat.
- Hinweis, dass spaetere Tasks den Vergleich liefern sollen, sobald Ressourcen verfuegbar sind (z. B. Follow-up Task `task_data_quality_eval`).

## Acceptance Criteria

- Paper enthaelt einen expliziten Satz/Abschnitt zur Annahme "Agenten laufen auf sauber modellierten AAS".
- Paper verweist darauf, dass Evaluation mit "messy but valid" AAS Teil der Future Work ist.
- Outlook-Text aus T2 ist im Paper eingearbeitet (§Future Work).
- Referenz auf die sauberen Templates (`aasx-dev-templates/*.json`) ist im Paper oder in den Begleitmaterialien dokumentiert.
- Task bleibt offen, bis Paper-Pass erfolgt ist; Abschluss erst nach Submission-Review der entsprechenden Textstellen.

## References

- `aasx-dev-templates/`
- `paper/etfa2026/conference_etfa_2026.tex`
- `memory/tasks/open/task_paper_*`
- [[task_paper_layered_determinism_thesis]] -- Layered Determinism ist die uebergeordnete These; Data-Quality-Layer ist deren logische Grundlage
