---
name: Task – Bench B Hall 3 Followup
description: Qwen35-2b Bench-B Hall-3-Läufe auswerten und als offenen Paper-Fund dokumentieren
type: task
status: open
priority: medium
---

## Summary
- Bench-B N=20 mit Qwen35-2b zeigt bei `bench_b_B1_hall3_contents` ausschließlich Fehlversuche.
- Ursache: syntaktisch fehlerhafte Cypher (z. B. `LIKE`, `!=`, Inline-`WHERE`), nicht leere Graphdaten.
- Für das Workshop-Paper bleibt das als dokumentierter Fund; Korrekturen der Queries wandern in spätere Arbeiten.

## Subtasks
### T1 — Ergebnisse konsolidieren
- `tests/agent-tests/results/qwen35-2b_bench_b_N20_judged.json` auswerten.
- Kernaussagen (0 % Passrate, Judge-Begründungen → „Geräte nicht gefunden“) in einer Notiz oder Paper-Sektion festhalten.

### T2 — Paper-Notiz vorbereiten
- Formulierung für „Known Limitations / Future Work“: aktueller Stand dokumentiert, Query-Rezepte als Folgearbeit.
- Abstimmen, ob Abschnitt im Workshop-Paper oder in separatem Log landet.

### T3 — Folgearbeit definieren (optional)
- Wenn beschlossen: Draft für zukünftigen Task zur Query-Rezept-Überarbeitung anlegen (z. B. `task_query_recipe_refactor`).
- Sonst als Hinweis in Acceptance Criteria markieren.

## Acceptance Criteria
- Fund in zentraler Quelle (Paper-Abschnitt oder Meeting-Notiz) dokumentiert und auf JSON-Ergebnis verwiesen.
- Klarer Vermerk: Keine kurzfristige Fix-Umsetzung, sondern späteres Paper-Ziel.
- Entscheidung zu optionaler Folgearbeit protokolliert (Task angelegt oder als Hinweis notiert).

## References
- Ergebnisse: `tests/agent-tests/results/qwen35-2b_bench_b_N20_judged.json`
- verwandter Task: `[[task_paper_bench_b_cases]]`
