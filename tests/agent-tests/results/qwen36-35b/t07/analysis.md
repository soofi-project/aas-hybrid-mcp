# Agent Evaluation: qwen36-35b · ReAct · T=0.7

**Date:** 2026-05-23 · 7 test suites · 230 runs · Judge: GPT-5.4 (Cortecs)
**Model:** Qwen 3.6 35B MoE — ~22B active parameters, FP8

---

## Overall Results

| Suite | N | Correct | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 100% | 45% | 65% | 20% |
| asset_specs | 20 | 100% | 45% | 45% | 35% |
| bench_b | 60 | 87% | 65% | 28% | 50% |
| containment_hall4 | 50 | 96% | 54% | 40% | 42% |
| srn_ablation_variant_a | 30 | 93% | 13% | 30% | 13% |
| srn_autonomous | 30 | 37% | 13% | 27% | 7% |
| srn_bypass | 20 | 75% | 15% | 50% | 5% |
| **Total** | **230** | **84%** | **41%** | **37%** | **30%** |

---

## What Worked Well

**Graph navigation and enumeration are solid.** B1 (Hall 3 devices), B2 (transport fleet), B3 (heavy
transport robot), and B6 (payload comparison) all hit 10/10. The agent reliably traverses
HierarchicalStructures submodels across both halls and reads TechnicalDataAGV fields without
confusion — including cross-hall queries where MiR100_001 is in Hall 4 and the MiR250s are in Hall 3.

**Anti-pattern and asset-spec queries are flawless at 100%.** Despite 65% antipattern trigger rate on
`anti_pattern` and 45% on `asset_specs`, the agent always recovers after validator rejection. The
validator fires on `idShort CONTAINS` or `toLower(...)` patterns, the agent re-issues the correct
exact-match Cypher, and proceeds to the correct answer. Recovery quality is perfect in these two suites.

**Containment Hall 4 is robust (96%).** Per-case breakdown: cobots (10/10), devices (10/10), identity
regression (10/10), ambiguous assets (9/10), transport (9/10). The two failures are isolated — one
from each of the ambiguous and transport cases — rather than systematic collapses.

**bench_b B5 (red status light) and B6 (payload comparison) perform well (80%, 100%).** B6 is the
highest `all_good` case in the entire eval at 90% — the model reads manuals first in every run and
produces clean, error-free answers. B5 is 80% with 70% manuals-first, showing the model does tend
to reach for documentation when troubleshooting device state.

---

## What Failed

### srn_from_fault_context — 10% (1/10)

The weakest individual case in the entire eval. Only one run produces a correct answer. This is a
sharp regression compared to qwen35-27b (67% adjusted) and qwen36-27b (~60% adjusted). The same
false-negative pattern documented for 27b models — judge penalising "Corrective Maintenance" in
the answer text vs. `"CorrectiveMaintenance"` in the tool call — may apply here too and inflate the
apparent failure rate. However, even accounting for false negatives, performance appears substantially
worse than the 27b models.

The most likely explanation: the 22B-active MoE routing may produce a different attention
distribution over the fault-context fields (spatial context + symptom description + implicit asset
type) compared to a dense 27B model of similar real capacity. This case requires simultaneous
disambiguation across three layers; the other SRN cases need only one or two.

### srn_autonomous — 37% overall (from_fault_context 10%, no_element_bypass 40%, routine_priority 60%)

SRN write-path from scratch remains the hardest task. `srn_routine_priority` at 60% is reasonable;
`srn_no_element_bypass` at 40% and `srn_from_fault_context` at 10% are systematic failures.
Only 13% of runs read manuals before writing — the model tends to attempt tool calls immediately
without consulting schema or template structure first.

The all_good rate for `srn_autonomous` is 7% — nearly every correct run still had at least one
tool error. The validator does not help here because failures are structural (wrong element path,
missing required fields) rather than Cypher anti-patterns.

### bench_b B4 — MiR250 emergency stop: 40% (4/10)

Requires reading the MiR250 operator manual to cite stop category 0 / STO contactors / SS1 brake
or the release sequence. Only 20% of runs read a manual — a regression vs. qwen36-27b's 50%
manuals-first rate for this case. The 4 correct runs may have relied on partial context or generic
safety knowledge rather than citing the specific manual section. Zero all_good runs.

---

## Bench B Per-Case Summary

| Case | Correct | Manuals first | All good |
|---|--:|--:|--:|
| B1 — Hall 3 contents | 10/10 | 80% | 70% |
| B2 — Autonomous transport fleet | 10/10 | 50% | 30% |
| B3 — Heavy transport robot | 10/10 | 70% | 70% |
| B4 — MiR250 emergency stop | 4/10 | 20% | 0% |
| B5 — Hall 4 red status light | 8/10 | 70% | 40% |
| B6 — Heaviest payload comparison | 10/10 | 100% | 90% |

---

## Antipattern Behavior

37% of all runs trigger at least one validator rejection — comparable to qwen36-27b (40%) and much
lower than qwen35-35b (70%). The correlation between antipattern hits and incorrect answers is flat:

| | antipattern=True | antipattern=False |
|---|--:|--:|
| correct=True | 36% | 64% |
| correct=False | 44% | 56% |

The gap is small — antipattern occurrence is a weak predictor of failure. The model consistently
recovers after rejection and proceeds to correct answers, especially in the simpler graph-query suites.
The 30% all_good rate (no errors at all) is respectable: the model avoids the anti-pattern entirely
in 63% of runs.

---

## Duration Patterns

| Suite | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|
| anti_pattern | 5.1s | 5.1s | — |
| asset_specs | 5.1s | 5.1s | — |
| bench_b | 14.3s | 14.3s | 13.5s |
| containment_hall4 | 14.8s | 14.8s | 15.1s |
| srn_ablation_variant_a | 8.3s | 8.3s | 12.8s |
| srn_autonomous | 9.7s | 8.6s | 12.3s |
| srn_bypass | 7.0s | 7.6s | 6.5s |

Failure runs are not markedly longer in this model — the wrong/correct duration gap is narrower than
for the 27b models. `srn_bypass` failures are faster than successes, consistent with the serial-number
pattern: the SRN is created quickly but the answer text omits the required resolution confirmation.

---

## Comparison with Other Models

| Suite | qwen35-27b | qwen36-27b | qwen36-35b |
|---|--:|--:|--:|
| anti_pattern | 100% | 100% | **100%** |
| asset_specs | 95% | 100% | **100%** |
| bench_b | 70% | 80% | **87%** |
| containment_hall4 | 96% | 96% | **96%** |
| srn_ablation_variant_a | 97% | 90% | **93%** |
| srn_autonomous | 67% | 63% | **37%** |
| srn_bypass | 95% | 70% | **75%** |
| **Total** | **86%** | **85%** | **84%** |

qwen36-35b matches the 27b models on most suites and outperforms both on bench_b (+7% vs 36-27b,
+17% vs 35-27b). The major regression is `srn_autonomous` — the 27b models achieve 63–67% while
36-35b reaches only 37%. The cause is the dramatic collapse of `srn_from_fault_context` (10% vs
~60% adjusted for 27b). This is a MoE-specific or generation-specific effect worth investigating.

---

## Summary

qwen36-35b is a capable model for graph navigation, containment queries, and antipattern recovery.
Its overall score of 84% is on par with the 27b models. The two persistent failure modes are:

1. **srn_from_fault_context collapse (10%)** — multi-layer disambiguation (spatial + symptom +
   asset type simultaneously) appears to be the specific challenge. This case requires the model
   to synthesize all three signals at once; the 22B-active MoE routing produces systematically
   worse outputs here than dense 27b models of similar real parameter count.

2. **SRN write-path (srn_autonomous 37%)** — write-from-scratch tasks remain hard across all models.
   The model rarely consults schema or templates before attempting writes; failures are structural,
   not recoverable by the Cypher validator.
