---
name: Task – N=30 Evaluation Run (Containment-Family + Paper-Zahlen)
description: CRAG-Bug fixen, dann seriellen N=30-Durchlauf für alle 4 Varianten fahren. Ergibt echte statistische Grundlage (95%-KI, Fisher-Test) für ETFA-Paper-Tabelle.
type: task
status: open
priority: high
depends_on: task_variant_faithfulness_audit (T1 – CRAG-Parser-Bug)
---

## Motivation

N=3 (Baseline 2026-05-15) reicht für Existence-Claims, nicht für präzise Frequenz-
Aussagen oder Varianten-Vergleiche mit engen Abständen (Plan 73% vs. Reflexion 93%).
Qwen3.6-27B-FP8 läuft lokal auf H200 → Kosten ≈ 0. N=30 seriell = ~7h Overnight-
Run. Ergibt Paper-fähige 95%-KIs und ermöglicht Fisher-Exact-Tests zwischen Varianten.

## Voraussetzungen (müssen davor erledigt sein)

1. **CRAG-Parser-Bug (`int('E0')`) gefixed** — `task_variant_faithfulness_audit T1`.
   Ohne Fix sind N=30 CRAG-Runs durch einen bekannten Crash kontaminiert; der Bug
   sorgt für systematisch leere Antworten, keine inhaltlichen CRAG-Failures.
2. **Varianten-Fidelity-Audit abgeschlossen** — zumindest für CRAG (T1) und
   optional Plan (T2). Reflexion und ReAct können parallel laufen.

## Framework-Limitation (dokumentiert, kein Blocker)

`runner.py:136` evaluiert `_strip_think_blocks(raw_stream)` als response-Text.
In verbose-Modus steht der gesamte Reasoning-Text **außerhalb** der `<think>`-Blöcke
→ Keyword-Suche läuft über Reasoning + Schlussantwort, nicht nur über die finale
Antwort.

**Konsequenz:** Ein Agent der das Keyword im Reasoning nennt, dann in der
Schlussantwort kapituliert, würde als *pass* gezählt (false positive).

**Warum bei den N=3-Daten kein Problem:** Alle CRAG-Failures zeigen `miss=[]`
(kein Keyword anywhere) → die Failures sind genuine Crashes, keine Evaluator-
Artefakte. Für N=30 trotzdem spot-checken (T3 unten).

**Mittel- bis langfristiger Fix:** LLM-Judge evaluiert nur die Schlussantwort durch
Prompt-Design → umgeht den Reasoning-Text-Bias automatisch.

## Subtasks

### T1 — Seriellen N=30-Run für ReAct + Reflexion + Plan starten

Kann sofort ohne CRAG-Bug-Fix laufen. Eine Variante nach der anderen:

```
python run_tests.py \
  --cases cases/containment_hall4.yaml \
  --variants aas-agent:react aas-agent:reflexion aas-agent:plan \
  --repetitions 30 \
  --export results/containment_hall4_N30_react_reflexion_plan.json
```

Laufzeit: ~5h (3 Varianten × ~1.75h seriell).

### T2 — CRAG-Run nach Bug-Fix

Nach `task_variant_faithfulness_audit T1`:

```
python run_tests.py \
  --cases cases/containment_hall4.yaml \
  --variants aas-agent:crag \
  --repetitions 30 \
  --export results/containment_hall4_N30_crag_postfix.json
```

Laufzeit: ~1.75h.

### T3 — Spot-Check: Reasoning-Text-Bias

Aus den N=30-Ergebnissen 5–10 *pass*-Records für CRAG und Plan manuell lesen:
Nennt die Schlussantwort das Keyword, oder nur das Reasoning?

Falls systematische false positives gefunden werden:
- Im Paper die Evaluator-Limitation als Fußnote dokumentieren
- Optional: LLM-Judge-Run als Gegenprobe (T5)

### T4 — Statistische Auswertung

Per-Variante aus den kombinierten JSON-Exports:

```python
# pro Variante: passes / total → binomial CI (Wilson-Intervall)
# paarweise: Fisher-Exact-Test (scipy.stats.fisher_exact)
```

Erwartete Paper-Tabelle:

| Variant   | Pass-Rate | 95% CI        | Avg Dur (s) | Avg Tools |
|-----------|-----------|---------------|-------------|-----------|
| ReAct     | ?/150     | [?, ?]        | ~22s        | ~14       |
| Reflexion | ?/150     | [?, ?]        | ~51s        | ~23       |
| Plan      | ?/150     | [?, ?]        | ~60s        | ~21       |
| CRAG*     | ?/150     | [?, ?]        | ~41s        | ~23       |

*CRAG: mit Fußnote zu Post-Fix-Status + ggf. Deviations aus Fidelity-Audit.

Wichtige Fisher-Tests:
- ReAct vs. CRAG: bei N=3 schon klar (100% vs 40%) → bei N=30 p-Wert für Paper
- Plan vs. Reflexion: bei N=3 nicht signifikant → bei N=30 evtl. p≈0.03

### T5 — Optional: LLM-Judge-Run für finale Paper-Tabelle

LLM-Judge sieht nur `{query} + {llm_criteria} + {final_answer}` → kein
Reasoning-Text-Bias. Gibt qualitative Score-Dimension zusätzlich zu pass/fail.

```
python run_tests.py \
  --cases cases/containment_hall4.yaml \
  --repetitions 5 \
  --llm-judge \
  --export results/containment_hall4_N5_llm_judge.json
```

N=5 reicht für LLM-Judge (teurer in Laufzeit wegen zweitem LLM-Call pro Run).
Vergleich LLM-Score vs. Regex-Score zeigt ob Reasoning-Text-Bias messbar ist.

## Timing-Richtlinie (keine Parallelisierung)

Seriell laufen lassen — parallele Requests konkurrieren um KV-Cache-Slots auf
dem H200 und verzerren die Latenz-Messungen. Pass-Rate ist timing-agnostisch,
aber die Duration-Zahlen gehen ins Paper.

Empfohlene Reihenfolge:
1. T1 sofort starten (overnight)
2. T2 nach CRAG-Bug-Fix (folgetag)
3. T3 manueller Spot-Check (~1h)
4. T4 Auswertung + Tabelle (~2h)
5. T5 optional

## Acceptance Criteria

- N=30-Ergebnisse für alle 4 Varianten als JSON in `results/`
- 95%-KI pro Variante berechnet (Wilson-Intervall)
- Fisher-Exact-Test ReAct vs. CRAG + Plan vs. Reflexion dokumentiert
- Paper-Tabelle (Eval-Sektion) aktualisiert mit N=30-Zahlen + CI-Spalte
- Reasoning-Text-Bias-Check durchgeführt (T3), Ergebnis dokumentiert
- CRAG-Ergebnisse mit Hinweis auf Post-Fix-Status + Fidelity-Audit versehen

## Statistische Erwartung (aus N=3 extrapoliert)

Bei N=150 (5 Cases × 30 Reps) mit aktuellen Raten:
- ReAct 100%: 95%-KI ≈ [97.6%, 100%] — paper-fest
- Reflexion 93%: 95%-KI ≈ [88%, 97%] — paper-fest
- Plan 73%: 95%-KI ≈ [66%, 80%]
- CRAG 40% (pre-fix): 95%-KI ≈ [32%, 48%] — Fußnote obligatorisch

ReAct vs. CRAG Fisher-Test: p < 0.0001 auch bei N=30 → sehr klare Aussage.
Plan vs. Reflexion bei N=30 pro Variante: p ≈ 0.03 → Grenzbereich, aber publizierfähig
als "statistically significant trend".

## References

- Baseline N=3: `tests/agent-tests/results/containment_hall4_baseline_N3.json`
- Framework: `tests/agent-tests/framework/`
- CRAG-Bug: [[task_variant_faithfulness_audit]] T1 + [[task_crag_parser_int_e0_bug]]
- Stream-Error-Kontamination: [[task_framework_stream_error_bucket]]
- Paper-Eval-Sektion: `paper/etfa2026/` (Abschnitt §Evaluation)
