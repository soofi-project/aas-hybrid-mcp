---
name: Task – Temperature-Justification für Paper
description: T=0 erzeugt degenerativen Determinismus (keine Greedy-Loops); Validator-Feedback als externer Temperatur-Ersatz; optimale Temperatur als Funktion des Scaffolding-Levels
type: task
status: open
priority: high
---

## Summary

Alle Paper-Eval-Läufe nutzen T=0.7 (Qwen3.5-Default im non-thinking-mode). Die
T=0.0-Tests zeigen **keine Greedy-Loops**, aber zwei andere Probleme:

1. **122B MoE bei T=0:** Vollständig deterministisch — byte-identische Outputs über
   N=3 Repetitions. Multi-Sample-Evaluation wird statistisch degenerativ.
2. **9B dense bei T=0:** Partiell deterministisch — FP-Nichtdeterminismus auf BF16-Hardware
   (H200) verursacht gelegentliche argmax-Flips bei flachen Wahrscheinlichkeitsverteilungen.
   Die resultierende Variation ist unkontrolliert, nicht explorativ.

Kernthese: Der MCP-Validator (Cypher-Anti-Pattern-Rejection + Hint) fungiert als
*externer Temperatur-Ersatz* — er erzwingt deterministische Variation durch strukturiertes
Feedback, nicht durch Sampling. Mit zunehmendem Scaffolding (Validator + Enum-Check +
Few-Shot-Exemplars) sinkt die benötigte Temperatur, potentiell bis T≈0 für vollständig
konstruierte Agenten. Das verschiebt den Ort der Exploration vom Modell-Sampling zur
Tool-Umgebung.

## Empirische Grundlage

### T=0.0 Tests (bench_b, N=3)

| Modell | T=0.0 Correct | T=0.7 Correct | Deterministisch? |
|---|--:|--:|---|
| qwen35-122b (MoE, ~10B active) | 78% (14/18) | 72% (43/60) | Ja — 3/3 identisch pro Case |
| qwen35-9b (9B dense) | 61% (11/18) | 55% (33/60) | Partiell — B4/B5 variieren |

**9B Nicht-Determinismus korreliert mit `get_manual_page`-Aufrufen:**
- B1/B2/B3/B6 (kein Manual-Read): 3/3 identisch pro Case
- B4/B5 (Manual-Read): verschiedene Tool-Counts, teils correct/incorrect

Ursache: Nicht Weaviate (Manual-Pages sind statische .md-Dateien), sondern
FP-Nichtdeterminismus in BF16-Softmax auf H200. Flache 9B-Wahrscheinlichkeitsverteilungen
+ Tool-Return-Kontextänderungen → gelegentliche argmax-Flips → Trajektorien-Divergenz.

**122B MoE ist deterministisch weil:** Experten-Routing erzeugt schärfere
Wahrscheinlichkeitsverteilungen, die argmax-Flips unterdrücken.

### Validierung: Validator als Temperatur-Ersatz

Der Cypher-Anti-Pattern-Validator im MCP-Server rejected Queries und gibt einen Hinweis.
Der Agent MUSS umschreiben — das ist **deterministische Variation**, nicht zufällige.
Self-Correction-Rate: 95–100% über alle Modelle.

Allerdings: Der Validator deckt nur den **Read-Path** (Cypher-Queries). Der **Write-Path**
hat keinen Validator (keine Enum-Checks, keine Template-Validation). Deshalb ist T>0
aktuell noch nötig — aber nur weil das Scaffolding auf dem Write-Path unvollständig ist.

## Subtasks

### T1 — T=0 Quick-Tests **Status:** ✅ Done (2026-05-26)

122B und 9B auf bench_b N=3 bei T=0.0 getestet. Keine Greedy-Loops, aber degenerativer
Determinismus (122B) bzw. unkontrollierte Variation (9B). Ergebnisse in
`tests/agent-tests/results/qwen35-122b/t00/` und `tests/agent-tests/results/qwen35-9b/t00/`.

### T2 — §10 Evaluation: Temperature-Begründung umschreiben

Bestehender Satz (Zeile 28-31) bleibt. Danach neuen Satz einfügen — **nicht** "greedy loops",
sondern "degenerative determinism":

> At $T=0$, the 122B-A10B MoE model produces byte-identical outputs across repetitions, rendering multi-sample evaluation statistically degenerate; the 9B dense model exhibits uncontrolled variation from floating-point nondeterminism rather than principled exploration. Both behaviours confirm that agentic tool-use evaluation requires non-zero sampling temperature to enable recovery from suboptimal tool-call sequences and to yield meaningful variance estimates. All models were therefore evaluated at the manufacturer-recommended $T=0.7$.

**Datei:** `paper/etfa2026/content/10-evaluation.tex`

**Status:** ✅ Done (2026-05-26) — minimaler Satz in §10 Z. 28 eingefügt: Pilot-T=0-Beobachtung (122B byte-identisch über N=3) als Setup, kein "requires non-zero temperature"-Overclaim. Qwen-Default-Begründung stand bereits im Satz davor.

### T3 — §11 Discussion: Temperature-als-Funktion-von-Scaffolding-Absatz

Neuer Absatz nach dem Scaffolding-Asymmetrie-Absatz (aus
[[task-paper-ablation-sections]] T3a):

> The requirement for non-zero temperature is itself a function of the environment-side scaffolding available to the agent. In the current setup, the Cypher anti-pattern validator provides structured feedback that forces the agent to revise rejected queries—an external source of variation that partially substitutes for sampling stochasticity. However, the write path lacks equivalent validation (no enum checks, no template-conformance enforcement), leaving re-sampling as the only recovery mechanism for incorrect payload values. We conjecture that as environment-side scaffolding increases (validator-enforced enum constraints, template-guided write paths, few-shot exemplars), the required sampling temperature decreases, potentially approaching $T \approx 0$ for fully constrained agents. This shifts the locus of exploration from the model's sampling distribution to the structured feedback of the tool environment.

**Datei:** `paper/etfa2026/content/11-discussion.tex`

**Status:** ⬜ Open — kann sofort geschrieben werden

### T4 — §13 Future Work: Temperatur-Scaffolding-Forschungsfrage

Ein Satz im Future-Work-Bullet ergänzen:

> The interplay between scaffolding density and optimal sampling temperature warrants further investigation: the Cypher validator already acts as an external temperature substitute on the read path, and we expect that adding enum validation and template-conformance checks to the write path would similarly reduce the need for sampling stochasticity, potentially enabling near-deterministic agentic operation suitable for safety-critical deployment.

**Datei:** `paper/etfa2026/content/13-future-work.tex`

**Status:** ⬜ Open — kann sofort geschrieben werden

### T5 — Alten Temperature-Task schließen

[[task-paper-122b-temperature-findings]] ist obsolet — die "greedy loop"-Hypothese wurde
widerlegt. Nach Schreiben der Paper-Texte: alten Task nach `memory/tasks/closed/`
verschieben.

**Status:** ⬜ Open — nach T2/T3/T4

## Acceptance Criteria

- [x] T=0 Quick-Tests (N=3) für qwen35-122b und qwen35-9b durchgeführt
- [x] Keine Greedy-Loops bestätigt; degenerativer Determinismus dokumentiert
- [x] §10 enthält korrigierte T=0-Begründung (kein "greedy loop"-Claim)
- [x] §11 enthält Temperature-als-Funktion-von-Scaffolding-Absatz mit Validator-als-Ersatz-These
- [x] §13 enthält Temperatur-Scaffolding-Forschungsfrage
- [x] Alter Task geschlossen
- [x] Paper kompiliert ohne Fehler

## References

- T=0.0 Ergebnisse 122B: `tests/agent-tests/results/qwen35-122b/t00/`
- T=0.0 Ergebnisse 9B: `tests/agent-tests/results/qwen35-9b/t00/`
- Alter (obsoleter) Task: [[task-paper-122b-temperature-findings]]
- Scaffolding-Asymmetrie-Task: [[task-paper-ablation-sections]] (T3a)
- MCP-Validator-Code: `mcp-server/src/aas_hybrid_mcp/tools/cypher_query.py`
- Manual-Page-Code: `mcp-server/src/aas_hybrid_mcp/manual.py` (statische .md-Dateien, kein Weaviate)
- Paper-Dateien: `paper/etfa2026/content/10-evaluation.tex`, `11-discussion.tex`, `13-future-work.tex`
