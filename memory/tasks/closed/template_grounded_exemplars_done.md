---
name: Template-Grounded Exemplars Done
description: Observation + hypothesis documented and integrated into paper §11 Discussion (scaffolding asymmetry, qwen36-27b example). Actual intervention (walkthroughs.md + re-eval) is Future Work.
type: task
status: done
---

## Was umgesetzt (Paper-Ebene)

Die Beobachtung und Hypothese sind in §11 Discussion eingearbeitet:

- **Scaffolding-Asymmetrie** in §11 "Reads vs Writes": read-path hat concrete Cypher-Exemplars, write-path hat keine. qwen36-27b als Beleg: 94% read-path, 14% SRN.
- **Future-Work-Hypothese** in §11: "template-grounded exemplars would shift this threshold downward" — wird als Future Work formuliert, nicht als erbrachter Beweis.
- Die Tool-Call-Analyse liefert die empirische Basis: Manual>AP > 0 bei allen Modellen, Manual-1st korreliert positiv aber reicht nicht.

## Nicht umgesetzt (bewusst — Future Work)

Die eigentliche Intervention:
- `walkthroughs.md` nicht gebaut
- Kein 9B re-eval mit neuen Walkthroughs
- Kein A/B-Vergleich vor/nach

Begründung: Scope des Workshop-Papers (8 Seiten). Die Intervention ist ein separates Experiment (variablenisolierter Test, braucht Re-Eval über alle Modelle).

## Referenzen

- Paper: `paper/etfa2026/content/11-discussion.tex` "Reads vs Writes"
- Eval-Daten: `memory/tasks/closed/eval_tool_call_analysis_done.md`
- IDTA-Templates: `idta_templates/published/`
