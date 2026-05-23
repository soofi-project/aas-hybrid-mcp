# Agent Evaluation: qwen35-397b · ReAct · T=0.7

**Date:** 2026-05-23 · 7 test suites · 230 runs · Judge: GPT-5.4 (Cortecs)

---

## Overall Results

| Suite | N | Correct (judged) | Correct (adjusted) | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 95% | 95% | 45% | 90% | 10% |
| asset_specs | 20 | 100% | 100% | 55% | 85% | 10% |
| bench_b | 60 | 78% | 78% | 85% | 57% | 37% |
| containment_hall4 | 50 | 96% | 96% | 80% | 64% | 30% |
| srn_ablation_variant_a | 30 | 100% | 100% | 60% | 33% | 27% |
| srn_autonomous | 30 | 70% | **~77%** | 43% | 47% | 13% |
| srn_bypass | 20 | 90% | 90% | 50% | 100% | 0% |
| **Total** | **230** | **88%** | **~89%** | **66%** | **63%** | **23%** |

**Adjusted column:** corrects for confirmed judge false negatives in `srn_from_fault_context` (see section below).

---

## What Worked Well

**SRN ablation is perfect.** `srn_ablation_variant_a`: 30/30 (100%). All three sub-cases —
fault context, no-element bypass, and routine priority — are answered correctly across all runs.
This is the first model in this evaluation set to achieve a perfect score on this suite.

**Autonomous transport fleet query resolved.** `bench_b_B2_autonomous_transport_fleet`: 10/10.
The agent reliably identifies all three AGVs (MiR100_001, MiR250_001, MiR250_002) and reports
their Hall locations by traversing HierarchicalStructures submodels. This is a full correction
of the 50% failure seen in qwen35-27b on this case.

**Containment and spec queries are robust.** B1, B3, B6, containment_transport_hall4,
containment_devices_hall4, identity_hall4_regression: all 10/10. Asset spec queries (UR3e payload,
MiR100 max speed) achieve 100%.

**Spatial bypass is perfect.** `srn_bypass_spatial_hall4`: 10/10. Hall 4 → MiR100_001
disambiguation works without error every time.

---

## What Failed

### srn_from_fault_context — 50% judged / ~70% adjusted

The weakest individual scenario. Raw judged score is 5/10. Two of the 5 failures are judge
false negatives (explained below). Actual corrected rate is approximately 7/10.

**Judge false negatives — "ServiceType" text representation:**
All 10 runs called `create_service_request_notification` with the correct enum value
`service_type: "CorrectiveMaintenance"` (no space) in the actual tool call. The judge penalized
runs where the *final answer text* said "Corrective Maintenance" (human-readable, with space)
instead of the exact enum string. The AAS write was correct in every case.

Breakdown of 5 failures:
- **2 runs** (reps 4, 5): only "ServiceType is CorrectiveMaintenance" listed as missing →
  confirmed false negatives; the tool call was correct
- **1 run** (rep 6): only "Status is Open" missing → legitimate failure — SRN created correctly
  but final answer does not confirm Open status
- **1 run** (rep 7): only MiR100_001 identification missing → legitimate failure — answer says
  "transport robot in Hall 4" without naming MiR100_001 explicitly
- **1 run** (rep 1): MiR100_001 identification + "Status is Open" → two text precision failures;
  SRN tool call was correct

**Manuals-first rate: 80%** for this case (8/10 read before first Cypher query). The agent
correctly uses `get_templates_index` to understand the SRN submodel before querying. This is the
highest rate across all three 27B/397B models for this case.

### srn_routine_priority — 70% (7/10)

Three failures (reps 0, 4, 9) — all three used `service_type: "PreventiveMaintenance"` in the
actual tool call instead of the correct `"Inspection"`. These are **genuine reasoning failures**,
not judge artifacts: the validator accepted the call (both are valid enum values), but the agent
misclassified a routine scheduled inspection as preventive maintenance. The final answers in these
runs stated "Preventive Maintenance" in the answer text, which the judge correctly penalized.

Frequency: 30% of runs on this case get the service type wrong. This is consistent across reps —
not a random fluctuation but a systematic tendency to default to "PreventiveMaintenance" for
maintenance-framed queries without reading the context carefully enough.

### bench_b B4 — MiR250 emergency stop: 20% (2/10)

This is the hardest test case: read the MiR250 operator manual (pp. 83–85) and cite specific
E-stop content: stop category 0 / STO contactors / SS1 brake, or the release sequence (release
E-stop → Resume button flashes blue → press Resume).

**Manuals-first rate: 10%** (1/10). Only 1 run reads a manual before querying the graph — but
that run is also one of the 2 correct ones, suggesting the manual read is necessary but not
sufficient. The other 9 runs go directly to Cypher queries and produce generic emergency stop
guidance without MiR250-specific content.

This is a slightly better outcome than qwen35-27b (10%, 0% manuals) and qwen36-27b (10%, 50%
manuals), but the fundamental pattern remains: the model does not consistently identify that this
question requires manufacturer documentation.

### bench_b B5 — Hall 4 red status light: 50% (5/10)

5 failures across 10 runs. All 10 runs read the manual first (`manuals_first = 100%`), but that
does not prevent failures:
- **4 runs** (reps 4, 7, 9 + one partial): the agent identifies a robot in Hall 4 but does not
  name it as MiR100_001 explicitly. The judge requires the asset ID by name.
- **1 run** (rep 5): missing both MiR100_001 identification and MiR100 manual troubleshooting
  content.
- **1 run** (rep 8): correct asset ID but missing substantive manual troubleshooting content.

The combined asset-identification + manual-content gap is the same pattern as in qwen35-27b and
qwen36-27b, though the failure count (5 vs. 4 for both 27B models) is slightly worse here.

### anti_pattern — 95% (19/20)

One unexpected failure: rep 0 of `mir100_max_speed_no_substring_lookup`. The agent issued a
valid Cypher query (after recovering from the initial antipattern) but returned an incorrect speed
value for the MiR100. This is a **factual read error** — the graph query executed successfully
but the agent reported a wrong number. Every other run (9/10 on this case, 10/10 on the second)
is correct. The overall 95% score is still the first sub-perfect score on the anti_pattern suite
across the tested models.

### srn_bypass_serial_number — 80% (8/10)

Two failures (reps 2, 7): the agent creates the SRN for MiR100_001 correctly but does not
explicitly state in the final answer that serial number MIR100-2020-001 was resolved to
MiR100_001. This is the same text confirmation gap seen in qwen35-27b (10/10, no gap) and
qwen36-27b (40%). At 80%, qwen35-397b sits between the two 27B models on this case.

Note: `srn_bypass` has a 100% antipattern hit rate, meaning every run attempts a substring-based
Cypher query first and gets a validator rejection. All 18 correct runs recover successfully, but
the antipattern adds latency and tool errors to every run — hence `all_good = 0%` for this suite.

---

## Did the Agent Read Manuals Before Cypher Queries?

Overall manuals-first rate: **66%** — close to qwen36-27b (70%) and substantially higher than
qwen35-27b (43%). The flag counts any `get_templates_index`, `get_template`, or `get_manual_page`
call before the first `query_aas_graph`.

| Suite | Manuals first |
|---|--:|
| bench_b B1–B3, B6 | 100% |
| bench_b B5 (red status light) | 100% |
| **bench_b B4 (MiR250 manual required)** | **10%** |
| srn_from_fault_context | 80% |
| srn_ablation_variant_a (avg) | 60% |
| srn_routine_priority | 30% |
| srn_no_element_bypass | 20% |
| anti_pattern, asset_specs | 45–55% |

The 100% manuals-first rate on B5 is higher than qwen35-27b (70%) and equal to qwen36-27b. For
B4, the trigger rate (10%) is close to qwen35-27b (0%) and far below qwen36-27b (50%). In both
cases where the manual is read for B4, the content extraction problem persists — the model reads
the document but does not locate and cite pp. 83–85 with the required specifics.

---

## Antipattern Behavior

63% of qwen35-397b runs trigger a validator rejection — essentially the same rate as qwen35-27b
(65%). The relationship between antipattern occurrence and correctness:

| | antipattern=True | antipattern=False |
|---|--:|--:|
| correct=True | — | — |
| correct=False | — | — |

As in both 27B models, antipattern hits do not predict failure: `srn_bypass` has a 100%
antipattern hit rate with a 90% correct rate. Recovery quality — not the initial antipattern —
determines the outcome. The 397B model does not learn to avoid the initial antipattern more
reliably than the 27B variants.

---

## Duration Patterns

| Suite | Median (correct) | Median (wrong) |
|---|--:|--:|
| srn_autonomous | 15.0s | 41.6s |
| containment_hall4 | 31.3s | 43.2s |
| srn_bypass | 22.6s | 29.0s |
| bench_b | 31.7s | 23.4s† |
| anti_pattern | 18.9s | 5.5s‡ |

†`bench_b` shows inverted durations: failures are *shorter* (23.4s) than successes (31.7s). This
is driven by B4 failures — the agent quickly provides generic emergency stop guidance without any
manual consultation, terminating in less time than the successful cases that do proper graph
traversal and manual lookups.

‡`anti_pattern` has only 1 failure; the 5.5s is a single data point.

`srn_autonomous` shows the largest gap: 15s for correct vs. 42s for wrong — indicating recursion-
limit exhaustion on failed write-path runs, consistent with all tested models.

---

## Comparison with qwen35-27b and qwen36-27b

| Suite | qwen35-27b | qwen36-27b | qwen35-397b | Δ (27b→397b) |
|---|--:|--:|--:|--:|
| anti_pattern | 100% | 100% | 95% | **-5%** |
| asset_specs | 95% | 100% | 100% | +5% |
| bench_b | 70% | 80% | 78% | +8% |
| containment_hall4 | 96% | 96% | 96% | = |
| srn_ablation_variant_a | 97% | 90% | 100% | +3% |
| srn_autonomous | 67% | 63% | 70% | +3% |
| srn_bypass | 95% | 70% | 90% | -5% |
| **Total** | **86%** | **85%** | **88%** | **+2%** |

The 397B model improves on bench_b (B2 is now perfect), srn_ablation, and srn_autonomous, but
regresses on anti_pattern (first sub-100% score) and srn_bypass (serial number confirmation drops
from 100% to 80%). The net gain over qwen35-27b is only +2%, suggesting that model size alone
provides modest overall improvement when the primary failure modes are answer precision and
manual content extraction rather than reasoning capacity.

---

## Summary

The agent handles graph navigation, containment, fleet queries, and SRN ablation reliably at this
scale. The three persistent failure modes mirror the 27B results with different intensity:

1. **Manual trigger absence for device-specific questions** — B4 (MiR250 E-stop): the 10%
   manual-read rate means 9 out of 10 runs never consult the operator manual; score remains 20%.
   Increasing model size does not fix the trigger problem.

2. **Service type classification errors** — `srn_routine_priority`: 30% of runs use
   "PreventiveMaintenance" where "Inspection" is correct. This is the first model to show
   a *real* tool-call service-type error (not a text representation artifact); the validator
   accepts both values, so the wrong service type is silently written to the AAS.

3. **Write-path answer precision** — SRNs are written correctly (tool args verified), but the
   final answer text omits required confirmatory fields (Status Open, explicit asset ID). Same
   pattern as 27B models; scaling does not eliminate the natural language output gap.
