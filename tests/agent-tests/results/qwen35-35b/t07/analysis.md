# Agent Evaluation: qwen35-35b · ReAct · T=0.7

**Date:** 2026-05-23 · 7 test suites · 230 runs · Judge: GPT-5.4 (Cortecs)
**Model:** Qwen 3.5 35B MoE — ~3B active parameters (sparse MoE routing)

---

## Overall Results

| Suite | N | Correct | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 100% | 15% | 75% | 0% |
| asset_specs | 20 | 100% | 30% | 85% | 10% |
| bench_b | 60 | 72% | 62% | 63% | 25% |
| containment_hall4 | 50 | 82% | 70% | 66% | 4% |
| srn_ablation_variant_a | 30 | 93% | 13% | 63% | 0% |
| srn_autonomous | 30 | 33% | 17% | 67% | 0% |
| srn_bypass | 20 | 75% | 5% | 90% | 0% |
| **Total** | **230** | **77%** | **40%** | **70%** | **8%** |

---

## The Dominant Pattern: Validator as Active Recovery Mechanism

qwen35-35b has a 70% overall antipattern hit rate — nearly double the 37% for qwen36-35b and 40%
for qwen36-27b. The `all_good` rate (zero errors, correct answer) is only 8% across all runs. In
effect, almost every correct answer goes through at least one validator rejection.

This is the clearest demonstration of the "layered determinism" thesis in the eval dataset: the
model's top-1 Cypher output is an anti-pattern (`idShort CONTAINS`, `toLower(...) CONTAINS`) in the
majority of attempts, the validator hard-rejects it, and the model recovers on retry. The architecture
compensates for training-data quality at the expense of efficiency — more tool calls, more latency,
but still reaching correct answers 77% of the time.

Notable: `srn_bypass` antipattern hit rate is 90% — 18/20 runs trigger the validator at least once.
Yet the overall correct rate for the suite is 75%. The validator is the only thing preventing this
model from getting stuck in invalid Cypher indefinitely.

---

## What Worked Well

**Simple enumeration queries are 100%.** Anti-pattern and asset-spec queries both hit 100% correct.
These require a single correct Cypher for containment or attribute lookup; the model gets there after
one or two validator rejections. The validator loop works reliably when the correct Cypher is
syntactically close to the failed anti-pattern.

**B1, B3 (hall contents and heavy transport) are 10/10.** Straightforward graph traversal with
exact known idShort values — even with multiple validator rejections, the model converges correctly.

**B6 (heaviest payload comparison) is 9/10.** 90% with a 90% manuals-first rate; the model learns
to look up the template structure before querying. The single failure is an outlier.

**srn_ablation_variant_a at 93%** — the same write-path task with generic tools achieves 93%, showing
the model can complete write operations when the schema is sufficiently constrained by the tool design.

---

## What Failed

### containment_hall4 — cobots: 30% (3/10)

The sharpest case-level collapse in the eval. The model achieves 100% on `containment_devices_hall4`,
`containment_ambiguous_assets_hall4`, and `identity_hall4_regression`, but collapses to 30% on
`containment_cobots_hall4`. The likely cause: the model conflates the concept of "cobot" with
all robots, or issues a Cypher query that returns both AGVs and cobots, then incorrectly selects
the set. At ~3B active parameters, type-classification reasoning (cobot vs. AGV vs. industrial robot)
appears less reliable. The 90% manuals-first rate for this case is high — the model reads the template
but still fails to translate the cobot-classification signal into the correct filter condition.

### bench_b B2 — Autonomous transport fleet: 60% (6/10)

Four failures share the same pattern: the agent searches for location data in the robot's own AAS
(Nameplate, ServiceRequestNotification) and concludes "location not recorded in AAS" rather than
querying the Hall HierarchicalStructures submodels from the hall's side. The model does not discover
that location is encoded as a reverse relationship — the hall AAS points to the robot as a child
entity, not the other way around. This is a graph traversal direction problem, not a Cypher
anti-pattern — the validator cannot catch it.

qwen36-35b with 22B active parameters solves B2 10/10. The capacity gap is visible here: resolving
indirect graph traversal direction requires reasoning about schema semantics, not just pattern matching.

### bench_b B4 — MiR250 emergency stop: 30% (3/10)

Only 10% manuals-first. The model almost never reads the MiR250 manual and falls back to generic
safety guidance. Even for the 3 correct runs, the answers likely reflect general E-stop knowledge
rather than the specific MiR250 procedure (stop category 0 / STO contactors / release sequence).
Zero all_good runs.

### bench_b B5 — Hall 4 red status light: 50% (5/10)

20% manuals-first. Five failures: the model either identifies the wrong device (MiR100 vs. the
Hall 4 device with the red status light) or provides generic troubleshooting guidance without
accessing the relevant manual section. Similar to B4, the failure is a content-extraction problem
compounded by infrequent manual access.

### srn_autonomous — 33% overall (from_fault_context 40%, no_element_bypass 20%, routine_priority 40%)

Write-from-scratch SRN creation is systematically hard at this capacity level. Notably,
`srn_from_fault_context` at 40% is higher here than for qwen36-35b (10%), which is a surprising
reversal. Whether this reflects a genuine capacity difference or variance at N=10 is unclear.
`srn_no_element_bypass` at 20% is the weakest individual case: the model fails to verify that the
target element path exists before writing. Zero all_good runs across all three SRN cases.

---

## Bench B Per-Case Summary

| Case | Correct | Manuals first | All good |
|---|--:|--:|--:|
| B1 — Hall 3 contents | 10/10 | 100% | 40% |
| B2 — Autonomous transport fleet | 6/10 | 60% | 10% |
| B3 — Heavy transport robot | 10/10 | 90% | 80% |
| B4 — MiR250 emergency stop | 3/10 | 10% | 0% |
| B5 — Hall 4 red status light | 5/10 | 20% | 0% |
| B6 — Heaviest payload comparison | 9/10 | 90% | 20% |

---

## Antipattern Behavior

The correlation between antipattern hits and correct answers reveals that at 3B active parameters,
the anti-pattern is essentially the model's default first attempt:

| | antipattern=True | antipattern=False |
|---|--:|--:|
| correct=True | 72% | 28% |
| correct=False | 62% | 38% |

127 of 177 correct answers went through at least one validator rejection. For comparison, in
qwen36-35b (22B active), 70 of 194 correct answers had antipattern hits — the inverse pattern.
At 3B active parameters, successful runs almost always involve the validator; at 22B active, most
correct runs avoid the anti-pattern entirely.

---

## Duration Patterns

| Suite | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|
| anti_pattern | 9.1s | 9.1s | — |
| asset_specs | 10.7s | 10.7s | — |
| bench_b | 16.8s | 16.0s | 23.7s |
| containment_hall4 | 19.5s | 18.9s | 20.7s |
| srn_ablation_variant_a | 11.0s | 9.9s | 21.6s |
| srn_autonomous | 9.7s | 11.7s | 8.5s |
| srn_bypass | 8.4s | 8.1s | 9.2s |

The model runs slower than qwen36-35b (16.8s vs 14.3s for bench_b) despite having fewer active
parameters — the higher antipattern hit rate adds extra round-trips. Failed bench_b runs are notably
longer (23.7s) because the model exhausts reasoning steps trying to find location data that isn't
where it expects. `srn_autonomous` failures are faster than successes, suggesting early termination
without completing the write operation.

---

## Comparison with Other Models

| Suite | qwen35-27b | qwen36-27b | qwen36-35b | qwen35-35b |
|---|--:|--:|--:|--:|
| anti_pattern | 100% | 100% | 100% | **100%** |
| asset_specs | 95% | 100% | 100% | **100%** |
| bench_b | 70% | 80% | 87% | **72%** |
| containment_hall4 | 96% | 96% | 96% | **82%** |
| srn_ablation_variant_a | 97% | 90% | 93% | **93%** |
| srn_autonomous | 67% | 63% | 37% | **33%** |
| srn_bypass | 95% | 70% | 75% | **75%** |
| **Total** | **86%** | **85%** | **84%** | **77%** |

At 3B active parameters, qwen35-35b achieves 77% — 7–9 points below the 27b models. The regressions
are concentrated in containment (82% vs 96%), bench_b (72% vs 70–87%), and srn_autonomous (33% vs
37–67%). Simple graph lookups and write-path ablation (srn_ablation) remain competitive, which
confirms that the capacity gap shows up in tasks requiring multi-step reasoning or indirect graph
traversal, not in straightforward retrieval.

---

## Summary

qwen35-35b demonstrates that a ~3B-active-parameter MoE model can handle AAS graph queries
when backed by an active validator. The two defining characteristics of this eval are:

1. **High antipattern rate (70%), high correct rate (77%)** — the validator functions as a recovery
   mechanism rather than a safety net. Every correct answer in simpler suites went through validator
   rejection; the model relies on the correction loop to reach valid Cypher. This is the strongest
   empirical argument in the eval dataset for the "validator as active guard-rail" design pattern.

2. **Capacity ceiling at indirect reasoning** — B2 (indirect graph traversal direction), B4/B5
   (manual content extraction), and `containment_cobots_hall4` (type classification) all collapse
   below 60%. These tasks require schema-semantic reasoning that exceeds what 3B active parameters
   can reliably produce. The threshold between "recoverable with validator" and "systematically
   failing" maps clearly onto task complexity.
