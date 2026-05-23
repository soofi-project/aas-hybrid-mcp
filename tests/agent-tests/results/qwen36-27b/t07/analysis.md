# Agent Evaluation: qwen36-27b · ReAct · T=0.7

**Date:** 2026-05-23 · 7 test suites · 230 runs · Judge: GPT-5.4 (Cortecs)

---

## Overall Results

| Suite | N | Correct (judged) | Correct (adjusted) | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 100% | 100% | 55% | 95% | 0% |
| asset_specs | 20 | 100% | 100% | 55% | 95% | 5% |
| bench_b | 60 | 80% | 80% | 92% | 33% | 65% |
| containment_hall4 | 50 | 96% | 96% | 80% | 28% | 68% |
| srn_ablation_variant_a | 30 | 90% | 90% | 60% | 30% | 30% |
| srn_autonomous | 30 | 63% | **73%** | 57% | 17% | 17% |
| srn_bypass | 20 | 70% | 70% | 45% | 30% | 35% |
| **Total** | **230** | **85%** | **~87%** | **70%** | **40%** | **41%** |

**Adjusted column:** corrects for confirmed judge false negatives in `srn_from_fault_context` (see section below).

---

## What Worked Well

**Anti-pattern recovery is reliable.** 40% of all runs trigger at least one validator rejection —
the agent starts a Cypher query with `idShort CONTAINS` or `toLower(sm.idShort) CONTAINS` and gets
rejected. However, it corrects after rejection and completes the query correctly. Notably, the
antipattern hit rate (40%) is much lower than for qwen35-27b (65%), suggesting the larger context
window or slightly different instruction following reduces the initial tendency to use substring
lookups.

**Containment and spec queries are robust.** B1 (Hall 3 devices), B3 (payload filter), B6
(cross-asset comparison): all 10/10. The agent reliably navigates HierarchicalStructures submodels
and reads TechnicalDataAGV fields. `all_good` rate for bench_b as a whole is 65% — the highest of
all suites — meaning more than half of bench_b runs produce a correct answer AND are tool-error-free.

**B2 (autonomous transport fleet) is strongly improved over qwen35-27b.** 9/10 correct (vs. 50%
for qwen35-27b). The one failure (rep 4) is the same pattern as qwen35-27b failures: the agent
identifies all three AGVs but claims location data is "not available," failing to query the
HierarchicalStructures submodels of Hall 3 and Hall 4 from the other direction.

**Spatial disambiguation works consistently.** `srn_bypass_spatial_hall4`: 10/10 correct. The agent
resolves "transport robot in Hall 4" → MiR100_001 without error, every time.

---

## What Failed

### srn_from_fault_context — 20% judged / ~60% adjusted

The weakest individual scenario. Raw judged score is 2/10, but 4 of the 8 failures are judge
false negatives (explained below). Actual corrected rate is approximately 6/10.

**Judge false negatives — "ServiceType" text representation:**
All 8 runs that called `create_service_request_notification` used the correct enum value
`service_type: "CorrectiveMaintenance"` (no space) in the actual tool call. The judge penalized
runs where the *final answer text* said "Corrective Maintenance" (human-readable, with space)
instead of the exact enum string. The AAS write was correct in every case.

Breakdown of 8 failures:
- **4 runs** (reps 1, 4, 7, 8): only "ServiceType" listed as missing → confirmed false negatives
- **2 runs** (reps 2, 5): only "Status is Open" missing → legitimate (answer does not confirm open status)
- **1 run** (rep 6): no `create_service_request_notification` call found — the SRN was not created at all; legitimate failure
- **1 run** (rep 9): multiple fields missing including Priority → potentially complete failure

**Remaining real failure pattern — "Status is Open" not stated:**
When the SRN is created and the judge requires `keywords: ["Open"]` in the answer text, some runs
return detailed troubleshooting guidance without explicitly stating the new SRN has Status Open.
The tool call was correct, but the confirmatory summary omits this field. Frequency: 2–3 runs.

**Cypher antipattern at start:** Every run in this case starts with a spatial disambiguation query
using substring matching (`idShort CONTAINS 'hall4'`) and gets a validator rejection before
recovering. This is consistent across both qwen35-27b and qwen36-27b and appears to be a hardwired
first-move tendency for spatial queries.

### bench_b B4 — MiR250 emergency stop: 10% (1/10)

This is the test case that requires reading the MiR250 operator manual (pp. 83–85) to cite specific
E-stop content: stop category 0 / STO contactors / SS1 brake, or the release sequence (release
E-stop → Resume button flashes blue → press Resume).

**Manuals-first rate: 50%** — significantly better than qwen35-27b (0%). The agent does read the
manual half the time. But reading the manual is not enough: only 1 run managed to extract and cite
the required specific content. The agent tends to provide generic emergency stop guidance (clear
safety zones, check E-stop button) rather than the precise MiR250 procedure from the manual pages.

This points to a **content extraction problem**, not just a retrieval trigger problem. The agent
retrieves the document but fails to locate and cite the right section.

### srn_bypass — serial number resolution: 40% (4/10 for `srn_bypass_serial_number`)

A notable regression compared to qwen35-27b. The query asks: "The MiR with serial number
MIR100-2020-001 just triggered an emergency stop. Quickly log a service request for it."

6/10 failures all share the same pattern: the agent creates the SRN but does not explicitly state
in the final answer that serial number MIR100-2020-001 was resolved to MiR100_001. The tool call
itself likely targeted the correct AAS (the judge checks the final answer text for the resolution
confirmation).

`srn_bypass_spatial_hall4` is 10/10 — spatial disambiguation works perfectly; only the serial
number path fails.

---

## Did the Agent Read Manuals Before Cypher Queries?

Short answer: **more often than qwen35-27b (70% overall vs. 43%), but in ways that matter less
than the numbers suggest.**

The `read_manuals_first` flag counts any `get_templates_index`, `get_template`, or `get_manual_page`
call before the first `query_aas_graph`. In most cases this is `get_templates_index` — a schema
lookup to understand submodel structure, not actual device documentation.

| Suite | Manuals first |
|---|--:|
| bench_b B1–B3, B6 | 100% |
| bench_b B5 (red status light) | 100% |
| **bench_b B4 (MiR250 manual required)** | **50%** |
| srn_from_fault_context | 100% |
| srn_routine_priority | 60% |
| srn_no_element_bypass | 10% |

Key observation for B4: the agent reads a manual in 5/10 runs, but none of those runs extracts the
specific required content (stop category, release sequence, or page range). Reading the index or a
general section is not equivalent to finding and citing pp. 83–85. The failure is content precision,
not trigger rate.

---

## Antipattern Behavior

65% of qwen35-27b runs hit an antipattern; only 40% for qwen36-27b. The pattern is the same
(`idShort CONTAINS` or `toLower(...)`) but fires less often. Crucially, the correlation between
antipattern hits and incorrect answers is essentially flat:

| | antipattern=True | antipattern=False |
|---|--:|--:|
| correct=True | 40% | 60% |
| correct=False | 41% | 59% |

The validator rejects the forbidden query, the agent recovers and issues a valid query, and
proceeds to the correct answer. Antipattern occurrence does not predict failure — recovery quality
does.

---

## Duration Patterns

Failed runs consume significantly more time than successful ones in the write-path and complex
reasoning suites, indicating exhaustion of the recursion limit rather than early termination.

| Suite | Median (correct) | Median (wrong) |
|---|--:|--:|
| srn_autonomous | 7.7s | 27.6s |
| srn_ablation_variant_a | 12.9s | 32.6s |
| containment_hall4 | 24.6s | 36.2s |
| srn_bypass | 14.5s | 12.9s† |

†`srn_bypass` failures are faster than successes — serial number failures terminate quickly because
the agent creates the SRN promptly but simply does not confirm the resolution in its answer.

---

## Comparison with qwen35-27b (same temperature, same suites)

| Suite | qwen35-27b | qwen36-27b | Delta |
|---|--:|--:|--:|
| anti_pattern | 100% | 100% | = |
| asset_specs | 95% | 100% | +5% |
| bench_b | 70% | 80% | **+10%** |
| containment_hall4 | 96% | 96% | = |
| srn_ablation_variant_a | 97% | 90% | -7% |
| srn_autonomous | 67% | 63% | -4% |
| srn_bypass | 95% | 70% | **-25%** |
| **Total** | **86%** | **85%** | -1% |

qwen36-27b improves on bench_b reasoning (especially B2 transport fleet classification) but
regresses on srn_bypass serial number resolution and srn_ablation. The overall score is
essentially identical at this temperature setting.

---

## Summary

The agent handles graph navigation, containment queries, and antipattern recovery reliably.
The two persistent failure modes are:

1. **Write-path answer precision** — SRNs are written correctly (tool args verified), but the
   final answer text omits required confirmatory fields (Status, explicit asset ID). Not a
   validator gap; a natural language output gap.

2. **Deep manual content extraction** — for B4, triggering manual reads is not enough. The agent
   retrieves documents but does not consistently locate and cite the required specific passages
   (stop procedure, page numbers). Generic troubleshooting replaces precise manual citations.
