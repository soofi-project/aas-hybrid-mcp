# Agent Evaluation: qwen35-27b · ReAct · T=0.7

**Date:** 2026-05-23 · 7 test suites · 230 runs · Judge: GPT-5.4 (Cortecs)

---

## Overall Results

| Suite | N | Correct (judged) | Correct (adjusted) | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 100% | 100% | 0% | 100% | 0% |
| asset_specs | 20 | 95% | 95% | 0% | 100% | 0% |
| bench_b | 60 | 70% | 70% | 78% | 60% | 32% |
| containment_hall4 | 50 | 96% | 96% | 80% | 40% | 54% |
| srn_ablation_variant_a | 30 | 97% | 97% | 10% | 63% | 0% |
| srn_autonomous | 30 | 67% | **~77%** | 20% | 63% | 0% |
| srn_bypass | 20 | 95% | 95% | 15% | 75% | 5% |
| **Total** | **230** | **86%** | **~87%** | **43%** | **65%** | **20%** |

**Adjusted column:** corrects for confirmed judge false negatives in `srn_from_fault_context` (see section below).

---

## What Worked Well

**Anti-pattern recovery is reliable.** Every single run in the `anti_pattern` and `asset_specs` suites
(100%) triggers a validator rejection — the agent starts with a Cypher query containing
`idShort CONTAINS` or `toLower(sm.idShort) CONTAINS` and gets rejected. However, it recovers
after rejection and produces the correct answer every time. The antipattern hit rate (65%) is
notably higher than for qwen36-27b (40%), but this does not translate into lower correctness
because recovery quality is high.

**Containment and spec queries are robust.** B1 (Hall 3 devices), B3 (payload filter), B6
(cross-asset comparison): all 10/10. The agent navigates HierarchicalStructures submodels and reads
TechnicalDataAGV fields reliably. `all_good` for containment_hall4 is 54% — runs that are correct
AND tool-error-free.

**Serial number bypass is perfect.** `srn_bypass_serial_number`: 10/10. The agent resolves
"MIR100-2020-001" to MiR100_001, creates the SRN, and explicitly confirms the resolution in every
run. This is a key differentiator versus qwen36-27b, which succeeds only 40% of the time on the
same case.

**SRN ablation robustness.** `srn_ablation_variant_a`: 29/30 (97%). Only 1 failure, caused by the
agent not identifying MiR100_001 as the transport robot in Hall 4.

---

## What Failed

### srn_from_fault_context — 10% judged / ~40% adjusted

The weakest individual scenario. Raw judged score is 1/10, but 3 of the 9 failures are judge
false negatives (explained below). Actual corrected rate is approximately 4/10.

**Judge false negatives — "ServiceType" text representation:**
All 10 runs called `create_service_request_notification` with the correct enum value
`service_type: "CorrectiveMaintenance"` (no space) in the actual tool call. The judge penalized
runs where the *final answer text* said "Corrective Maintenance" (human-readable, with space)
instead of the exact enum string. The AAS write was correct in every case.

Breakdown of 9 failures:
- **3 runs** (reps 2, 4, 6): only "ServiceType is CorrectiveMaintenance" listed as missing →
  confirmed false negatives; the tool call was correct
- **4 runs** (reps 0, 5, 9 — missing only "Status is Open"; rep 7 — missing MiR100_001 +
  "Status is Open"): legitimate failures — the SRN was created but the final answer did not
  confirm the new request has Status Open
- **1 run** (rep 1): missing MiR100_001 identification + "Status is Open" → two text precision
  failures; SRN call was correct
- **1 run** (rep 3): missing MiR100_001 + "ServiceType is CorrectiveMaintenance" → ServiceType
  part is a false negative; the asset identity part is a real text failure

**Remaining real failure pattern — "Status is Open" not stated:**
When the SRN is created and the judge requires `keywords: ["Open"]` in the answer text, some runs
return troubleshooting guidance without explicitly stating the new SRN has Status Open. The tool
call was correct, but the confirmatory summary omits this field. Frequency: 4 runs.

**Manuals-first: 60% for this case** (6/10 reads before first Cypher). Every run starts with a
spatial disambiguation query using substring matching (`idShort CONTAINS 'hall4'`) and gets a
validator rejection before recovering. This is consistent across both qwen35-27b and qwen36-27b.

### bench_b B4 — MiR250 emergency stop: 10% (1/10)

This is the test case that requires reading the MiR250 operator manual (pp. 83–85) to cite specific
E-stop content: stop category 0 / STO contactors / SS1 brake, or the release sequence (release
E-stop → Resume button flashes blue → press Resume).

**Manuals-first rate: 0%** — the agent never reads a manual before querying the graph for this
case. Every run issues a `query_aas_graph` first. The single correct run (rep 5) presumably found
the content through graph metadata; 9 failures provide generic emergency stop guidance without any
MiR250-specific details.

This is a **trigger failure**, not just a content extraction problem: the agent does not recognize
that a manufacturer-specific emergency stop procedure requires consulting the operator manual. By
contrast, qwen36-27b reads the manual in 50% of runs — but even then, content extraction fails
because the agent retrieves general sections rather than pp. 83–85.

### bench_b B2 — autonomous transport fleet: 50% (5/10)

The agent must identify all three AGVs (MiR100_001, MiR250_001, MiR250_002) and state their
locations. 5 failures:
- **3 runs** (reps 0, 1, 8): the agent identifies all three AGVs but claims location data is "not
  available," failing to query the HierarchicalStructures submodels of Hall 3 and Hall 4
- **2 runs** (reps 2, 4): different failure pattern (likely CRX10iA misclassification as AGV, or
  incomplete fleet enumeration — missing_facts field was empty in judged output)

All 10 runs do read manuals first (`manuals_first = 100%`), so this is a graph navigation gap,
not a retrieval trigger problem. qwen36-27b achieves 90% on this case.

### bench_b B5 — Hall 4 red status light: 60% (6/10)

4 failures. Common pattern: the agent identifies a robot in Hall 4 but does not name it as
MiR100_001 explicitly (3 of 4 failures). Two failures also lack MiR100 manual content (emergency
stop procedure, protective stop, or diagnostic steps). The agent provides general troubleshooting
guidance but misses asset identification and manual citation together.

---

## Did the Agent Read Manuals Before Cypher Queries?

Overall manuals-first rate: **43%** — lower than qwen36-27b (70%). The flag counts any
`get_templates_index`, `get_template`, or `get_manual_page` call before the first `query_aas_graph`.
In most cases this is `get_templates_index` — a schema lookup to understand submodel structure,
not actual device documentation.

| Suite | Manuals first |
|---|--:|
| bench_b B1–B3, B6 | 100% |
| bench_b B5 (red status light) | 70% |
| **bench_b B4 (MiR250 manual required)** | **0%** |
| srn_from_fault_context | 60% |
| srn_routine_priority | 0% |
| srn_no_element_bypass | 0% |
| anti_pattern, asset_specs | 0% |

Key observation: for anti_pattern and asset_specs (100% antipattern hit rate), the agent jumps
directly to Cypher queries. qwen36-27b runs `get_templates_index` first in 55% of these cases.
For B4, qwen35-27b reads nothing — the agent shows no awareness that this is a manual-dependent
question. This is the primary driver of the 0% B4 manual read rate.

---

## Antipattern Behavior

65% of qwen35-27b runs trigger a validator rejection (`idShort CONTAINS` or `toLower(...)`) —
the highest antipattern rate across all tested models. The pattern:

| | antipattern=True | antipattern=False |
|---|--:|--:|
| correct=True | 63% | 37% |
| correct=False | 76% | 24% |

Unlike qwen36-27b, where antipattern and correctness are essentially uncorrelated, here there is
a modest negative signal: failures are somewhat more likely to have had an antipattern (76% vs 63%).
This likely reflects that harder queries — where the agent struggles to formulate the right Cypher
— also tend to start with substring lookups. Recovery quality determines the outcome, not the
antipattern itself.

---

## Duration Patterns

Failed runs consume significantly more time in the write-path and complex reasoning suites,
indicating exhaustion of the recursion limit rather than early termination.

| Suite | Median (correct) | Median (wrong) |
|---|--:|--:|
| srn_autonomous | 9.4s | 30.9s |
| srn_ablation_variant_a | 16.8s | 31.0s |
| containment_hall4 | 24.3s | 36.0s |
| srn_bypass | 15.1s | 31.9s† |
| bench_b | 24.8s | 25.4s‡ |

†`srn_bypass` has only 1 failure — the long duration is consistent with a full-effort attempt that
still missed the explicit asset identification in the answer.

‡`bench_b` correct/wrong durations are nearly equal because both B4 failures (short: quick generic
answer) and B2 failures (long: multiple graph queries before giving up) average out.

---

## Comparison with qwen36-27b (same temperature, same suites)

| Suite | qwen35-27b | qwen36-27b | Delta |
|---|--:|--:|--:|
| anti_pattern | 100% | 100% | = |
| asset_specs | 95% | 100% | -5% |
| bench_b | 70% | 80% | **-10%** |
| containment_hall4 | 96% | 96% | = |
| srn_ablation_variant_a | 97% | 90% | **+7%** |
| srn_autonomous | 67% | 63% | +4% |
| srn_bypass | 95% | 70% | **+25%** |
| **Total** | **86%** | **85%** | +1% |

qwen35-27b is stronger on srn_bypass (serial number resolution is perfect vs 40%) and
srn_ablation, but weaker on bench_b (B2 transport fleet: 50% vs 90%). The overall score is
essentially identical. The most striking contrast is the antipattern rate (65% vs 40%) combined
with an identical anti_pattern suite correctness (100%): qwen35-27b hits the validator more often
but recovers just as reliably.

---

## Summary

The agent handles graph navigation, containment queries, anti-pattern recovery, and serial number
resolution reliably. The three persistent failure modes are:

1. **Manual trigger absence for device-specific questions** — B4 (MiR250 E-stop): the agent never
   reaches for the operator manual, provides generic guidance, and fails 90% of the time. No
   awareness that manufacturer-specific procedure content lives in documentation, not the graph.

2. **Write-path answer precision** — SRNs are written correctly (tool args verified), but the
   final answer text omits required confirmatory fields (Status Open, explicit asset ID).
   Not a validator gap; a natural language output gap.

3. **Transport fleet location queries (B2)** — the agent identifies the AGVs but fails to traverse
   the HierarchicalStructures submodels of both halls to retrieve location data, claiming it is
   "not available." This navigation pattern is fully solved in qwen36-27b (90%).
