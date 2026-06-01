---
name: Task – Paper Style Fixes (Future Work Compression + Minor Issues)
description: §13 Future Work komprimieren, Architecture-Caption, Conclusion-These, Bench B Regime-Definition, und weitere Minor Fixes
type: task
status: open
priority: medium
---

## Summary

Aus dem Review ergeben sich ein Major Fix (§13 Future Work zu lang/wiederholt Limitations) und mehrere Minor Issues, die in einem Pass behoben werden.

## Major Fix

### T1 — §13 Future Work komprimieren (13-future-work.tex)

**Problem:** §13 wiederholt §12 Limitations mit Lösungsideen. Drei Bullets, jeder ein Absatz — zu viel für ein 8-Seiten-Paper.

**Lösung:** Jeder Bullet auf 1–2 Sätze komprimieren. Keine Wiederholung der Limitations-Diagnose, nur die geplante Lösung. Ziel: ~50% Platzersparnis.

## Minor Fixes

### T2 — §06 Architecture Figure Caption (06-architecture.tex) — MOVED TO COMPRESSION

`"System Overview."` ist schwach, aber der Body erklärt die Pfeile direkt davor
("Solid arrows ... synchronous; dashed arrows ... event-driven"). Längere Caption
würde das duplizieren + Platz kosten. **Lösung: den Body-Satz IN die Caption
verschieben** → bessere Caption *und* eine Body-Zeile gespart. Gehört damit in den
8-Seiten-Kompressions-Pass, nicht als eigenständiger Minor-Fix.

### T3 — §14 Conclusion: Layered-Determinism-These erwähnen (14-conclusion.tex)

Die stärkste Aussage des Papers fehlt in der Conclusion. Mindestens ein Satz der "prompts are hints; validators are guarantees" oder "Layered Determinism" referenziert.

### T4 — §10 Bench B: "run-weighted averages" erklären (10-evaluation.tex) — DROPPED

Bereits durch die Tabellen-Caption abgedeckt: "Avg: run-weighted over 150
runs/model (20 anti-pat. + 20 specs + 60 bench_b + 50 contain.)". Kein Handlungsbedarf.

### T5 — §10 Bench B: Regime-Grenzen quantitativ definieren (10-evaluation.tex)

"Floor / Sub-viable / Viable" Currently implizit. Explizit machen: z.B. <20% floor, 20–70% sub-viable, >70% viable.

### T6 — §08 Retrieval: Überleitung vor ECLASS-Satz (08-retrieval-pipeline.tex)

Der letzte Satz vor §08.D springt plötzlich zu ECLASS IRDIs. Kurze Überleitung einfügen.

### T7 — §06 "15 tools across six categories" (06-architecture.tex)

Entweder die sechs Kategorien benennen oder "15 tools" ohne Kategorien-Zahl schreiben.

### T8 — §10 Bench B: self-correction 95–100% Zuordnung klären (10-evaluation.tex)

§11 Discussion zitiert "95–100% self-correction" im Write-Kontext, aber der Satz im Discussion-Section mischt Read und Write. Sicherstellen dass klar ist welches Benchmark gemeint ist.

## Acceptance Criteria

- §13 Future Work um mindestens 40% gekürzt
- Architecture-Figure hat aussagekräftige Caption
- Conclusion erwähnt Layered-Determinism-These
- Alle Minor Fixes angewendet
- Paper baut ohne Fehler

## References

- `paper/etfa2026/content/13-future-work.tex`
- `paper/etfa2026/content/06-architecture.tex`
- `paper/etfa2026/content/14-conclusion.tex`
- `paper/etfa2026/content/10-evaluation.tex`
- `paper/etfa2026/content/08-retrieval-pipeline.tex`
- `paper/etfa2026/content/11-discussion.tex`
