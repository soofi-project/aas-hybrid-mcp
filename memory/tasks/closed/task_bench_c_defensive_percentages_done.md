---
name: Task – Bench C Defensive Percentage Framing
description: Bench-C-Prozentzahlen bei N=10 defensiver rahmen; Existenz-Claims statt präziser Raten
type: task
status: open
priority: medium
status_note: done 2026-05-31 — §10 reframed to "no model exceeds roughly one third (34% at best)" + N=10 caveat once + "indicative not precise, no model ranking"; §11 point estimates (77%/34%) replaced with "roughly three quarters" / "never exceeds about a third". Build green.
---

## Summary

Benchmark C (SRN write-path, §10) basiert auf N=10 pro Case bei 5 Cases = 50 Runs/Modell. Die aktuellen Prozentzahlen (34%, 14%, 32% etc.) suggerieren eine Präzision, die bei N=10 nicht gegeben ist. Die Existenz-Claims sind legitim ("the agent CAN fail on vocabulary"), aber die prozentualen Raten sollten defensiver gerahmt werden.

## Problemstellen

### §10 Benchmark C (10-evaluation.tex)

- **"Maximum correct rate is 34%"** — bei N=10 ist die 95%-CI für p=0.34 etwa [0.17, 0.55]. Die 34% sind ein Punktschätzer, kein stabiler Wert.
- **Tabelle 3:** Alle Prozentzahlen suggerieren Stabilität. Option: auf 10er-Schritte runden oder als Bereiche angeben.
- **"13--79% of runs trigger at least one idShort anti-pattern violation"** — Existenz-Claim ist OK, aber der Range suggeriert einen systematischen Zusammenhang.

### §11 Discussion (11-discussion.tex)

- **"structural writes succeed in ~77% of runs"** — "~" ist schon besser, aber die Quelle ist N=10.
- **"SRN semantic correctness peaks at 34%"** — dieselbe Punktschätzung wie oben.
- **"self-correction reliable (95--100%)"** — bei N=10 bedeutet 100% nur "in allen 10 Runs", nicht "immer".

## Subtasks

### T1 — §10 Bench C Text defensiver rahmen

- Prozentzahlen in "~35%" statt "34%" oder als Bereiche formulieren
- Explizit N=10 als Caveat nennen (einmalig, nicht bei jeder Zahl)
- Existenz-Claims beibehalten, Frequenz-Claims abschwächen

### T2 — §11 Discussion konsistent anpassen

- Zahlen aus §10 übernehmen, nicht präziser wiederholen
- "~77%" → beibehalten oder zu "roughly three quarters" umformulieren

## Acceptance Criteria

- Keine Bench-C-Zahl suggeriert mehr Präzision als bei N=10 gerechtfertigt
- Existenz-Claims ("models fail on vocabulary") bleiben stark
- Frequenz-Claims ("34%") werden als Beobachtung, nicht als echte Rate gerahmt
- N=10-Caveat wird mindestens einmal im Text explizit erwähnt

## References

- `paper/etfa2026/content/10-evaluation.tex` (Zeilen 82–108)
- `paper/etfa2026/content/11-discussion.tex` (Zeilen 8, 10)
