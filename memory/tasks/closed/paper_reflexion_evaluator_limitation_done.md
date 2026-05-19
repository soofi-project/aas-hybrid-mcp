---
name: Reflexion Evaluator Limitation Done
description: §12 neuer Bullet — same-model self-eval als Ausschlussgrund für Reflexion-Eval. T2 (§13) durch §12-Formulierung abgedeckt.
type: task
status: done
---

## Was umgesetzt

**T1 — §12 Limitations: neuer Bullet** — erledigt.

Neuer Bullet "Same-Model Self-Evaluation" am Ende von `12-limitations.tex` eingefügt:
- Benennt same-model actor+evaluator als bewussten Ausschlussgrund für die quantitative Evaluation der Reflexion-Variante
- Verweist auf Reflexion-Originaldesign (separater Evaluator / Heuristik per `shinn2023reflexion`)
- Framt das als Setup-Entscheidung, nicht als fundamentales Versagen
- Schließt mit "heterogeneous model pairing remains future work" — T2 (§13-Satz) damit abgedeckt, separater §13-Edit nicht mehr nötig

**T2 — §13 Future-Work-Satz** — entfällt.

Der §12-Bullet nennt "heterogeneous model pairing as a resource-constrained deployment strategy remains future work" bereits explizit. Ein separater Satz im Corrective-Retrieval-Bullet wäre redundant.

## Kontext-Entscheidung

Im Zuge der Entscheidung für ReAct-only-Evaluation (kein Variant-Vergleich im Paper) wird Reflexion in §06 nur noch als "die Architektur unterstützt auch dieses Pattern" erwähnt, ohne Evaluation. Der §12-Bullet ist die defensive Begründung dafür, warum wir Reflexion nicht evaluiert haben — nicht nur ein Caveat.
