---
name: Modeling-vs-Pragmatics Anecdote Done
description: MANAGES_ASSET self-reference + idShort/CONTAINS anti-pattern as domain pragmatics subsection in §11 Discussion.
type: task
status: done
---

## Umgesetzt

Neuer Subsection §11 "Domain Pragmatics and the Limits of Formal Correctness" in `11-discussion.tex`:

1. MANAGES_ASSET-Anecdote: "Was ist in Halle 4?" → formale Korrektheit (Selbstreferenz) vs. pragmatische Erwartung (enthaltenene Geräte). Lösung: Pragmatik-Regel im Manual.
2. idShort/CONTAINS als häufigstes Anti-Pattern: syntaktisch gültig, metamodel-semantisch falsch. 397B produziert es trotz Manual-Lektüre in 50% der Fälle.
3. Schluss: Manuals (operationales Wissen) + Validatoren (Determinismus) — beides nötig, keines allein reicht.

## Nicht umgesetzt

- Kein Pre/Post-Bench-Vergleich (Pre-Fix-Daten fehlen)
- Keine harten Eval-Zahlen für die MANAGES_ASSET-Anecdote (nur Beobachtung aus Bench B)

## Referenz

- `paper/etfa2026/content/11-discussion.tex` Zeile ~15
