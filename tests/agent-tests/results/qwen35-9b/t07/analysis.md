# Evaluation Analysis: Qwen3.5-9B — T07

Model: `qwen35-9b` · Trial: T07 · Suites: 5 · Total runs: 200

---

## 1. Paper-Evaluation Table per Suite

| Suite | N | Correct | Manuals first | idShort violation | Bypass (pse) | Median correct (s) | Median wrong (s) |
|---|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 18 (90%) | 15 (75%) | 20 (100%) | — | 6.7 | 7.9 |
| asset_specs | 20 | 14 (70%) | 17 (85%) | 19 (95%) | — | 8.9 | 12.2 |
| bench_b | 60 | 33 (55%) | 42 (70%) | 37 (62%) | — | 10.5 | 18.5 |
| containment_hall4 | 50 | 22 (44%) | 31 (62%) | 35 (70%) | — | 6.6 | 11.7 |
| srn_autonomous | 50 | 7 (14%) | 1 (2%) | 41 (82%) | 44% | 38.3 | 47.7 |
| **Total** | **200** | **94 (47%)** | **106 (53%)** | **152 (76%)** | — | — | — |

Only anti_pattern approaches acceptable accuracy (90%). The remaining four suites form a descending staircase: 70% → 55% → 44% → 14%. The SRN suite collapses to near-floor performance. Compared to the 27B sibling (77% overall, 100% on containment_hall4 and asset_specs), the 9B model loses 30 percentage points overall — with the steepest drop on containment_hall4 (−56 pp) and asset_specs (−30 pp), suites the 27B model aces perfectly.

---

## 2. idShort Violation Self-Correction Rate

| Suite | Violations | Self-corrected | Rate |
|---|--:|--:|--:|
| anti_pattern | 20 | 19 | 95.0% |
| asset_specs | 19 | 17 | 89.5% |
| bench_b | 37 | 37 | 100% |
| containment_hall4 | 35 | 33 | 94.3% |
| srn_autonomous | 41 | 39 | 95.1% |
| **Total** | **152** | **145** | **95.4%** |

The 9B model violates the idShort anti-pattern even more aggressively than the 27B (76% vs 63% of runs), but self-corrects at a comparable rate (95.4% vs 97.6%). The absolute number of violation occurrences is telling:

| Rule | Occurrences |
|---|--:|
| `idShort_contains_or_regex` | 348 |
| `id_contains_or_regex` | 66 |
| `toLower_id_contains` | 59 |
| `assetType_match` | 14 |

The dominant pattern (`idShort_contains_or_regex` = 348 occurrences, vs 149 for the 27B) shows the 9B model is over 2× more prone to using idShort as a shortcut. While self-correction eventually fixes the query, the wasted turns are proportionally more damaging for a smaller model that already struggles with budget and task completion.

---

## 3. Write-Path Bypass (SRN Suite Only)

**Overall bypass rate: 44%**

| Bypass type | Count | Meaning |
|---|--:|---|
| null | 16 | No submodel found / indeterminate path |
| cascade | 14 | Multi-step bypass via wrong intermediate steps |
| none | 10 | No write attempted at all |
| direct | 7 | Called `put_submodel_element` without traversing structure |
| correct | 2 | Correct write path followed |
| surfaced | 1 | Found existing submodel, stopped without writing |

Per-case breakdown:

| Case | correct | surfaced | direct | cascade | none | null |
|---|--:|--:|--:|--:|--:|--:|
| srn_from_fault_context | 1 | — | — | 1 | — | 8 |
| srn_routine_priority | — | — | 4 | 3 | — | 3 |
| srn_serial_number | — | — | 1 | 1 | 6 | 2 |
| srn_spatial_hall4 | — | — | 2 | 1 | 4 | 3 |
| srn_empty_submodel_bypass | 1 | 1 | — | 8 | — | — |

The bypass profile is fundamentally different from the 27B model. Where the 27B's dominant failure was "surfaced" (finding the submodel but not writing to it), the 9B model rarely even discovers the target submodel. The dominant failure modes are:

- **null (16/50):** The agent never finds the relevant submodel — it gets lost in the graph traversal or fails to issue the right queries. Most acute in `srn_from_fault_context` (8/10).
- **cascade (14/50):** The agent takes a wrong intermediate step and never recovers. Dominates `srn_empty_submodel_bypass` (8/10), where the agent appears to chase a multi-step write path that doesn't lead to a valid `put_submodel` call.
- **none (10/50):** The agent never attempts a write at all. Concentrated in `srn_serial_number` (6/10) and `srn_spatial_hall4` (4/10).

Write-tool execution: `put_submodel_element` was called in 31 runs, while `put_submodel` was attempted in 27. Only 2 runs achieved the correct write path. The 9B model is effectively unable to complete the SRN write task.

---

## 4. Template Validation

All five suites report **zero write-tool rejections and zero validation errors**. When the 9B model does issue a write call, the payload passes schema validation — identical to the 27B model. The constraint is never payload correctness but tool-selection and path-finding: the model either never reaches a write call, or calls the wrong tool for the structural context.

---

## 5. Judge Failure Modes per SRN Case

| Case | n_incorrect | Top missing facts | Top wrong claims |
|---|--:|---|---|
| srn_from_fault_context | 10 | ServiceType=CorrectiveMaintenance (10/10), Status=Open (9/10), Priority=High (9/10), Asset=MiR100_001 (9/10) | Service Type: Emergency Stop (1) |
| srn_routine_priority | 10 | Priority=Low (10/10), Asset=UR3e_002 (10/10), ServiceType=Inspection (9/10), Status=Open (6/10) | Priority is Medium (3), Asset=UR3e_001 (3), Priority is Normal (1) |
| srn_empty_submodel_bypass | 9 | Payload contains SRN entry (9/9), Write was attempted (3/9), Asset=CRX10iA_001 (2/9) | User must provide info (1) |
| srn_serial_number | 9 | Write was attempted (6/9), Serial resolved to MiR100_001 (4/9), Priority=High (3/9) | User must provide info (1) |
| srn_spatial_hall4 | 5 | Write was attempted (4/5), Asset=MiR100_001 identified (3/5) | User must provide info (1) |

Two root causes — mirroring the 27B analysis but more severe:

1. **Complete vocabulary failure:** In `srn_from_fault_context`, the agent fails to map "emergency stop" to CorrectiveMaintenance in 10/10 incorrect runs. In `srn_routine_priority`, it never assigns the correct Priority=Low (10/10 miss). The 9B model lacks the inferential capacity to map natural-language descriptions to the SRN schema's controlled vocabulary.

2. **Write-path non-arrival:** Unlike the 27B, where "surfaced" (finding the submodel but not writing) was the dominant failure, the 9B model mostly never arrives at the write step at all. Missing facts like "Write was attempted" (6/9 in `srn_serial_number`, 4/5 in `srn_spatial_hall4`) indicate the agent never reaches the point of issuing a write call.

3. **Asset confusion:** In `srn_routine_priority`, the agent targets UR3e_001 instead of UR3e_002 in 3/10 wrong claims — a spatial disambiguation failure absent in the 27B model.

---

## 6. Duration: Median per Suite

| Suite | Median correct (s) | Median wrong (s) |
|---|--:|--:|
| anti_pattern | 6.7 | 7.9 |
| asset_specs | 8.9 | 12.2 |
| bench_b | 10.5 | 18.5 |
| containment_hall4 | 6.6 | 11.7 |
| srn_autonomous | 38.3 | 47.7 |

Wrong runs are consistently slower than correct runs across all suites (1.2s–7.9s gap), indicating the model wastes time on unproductive exploration before failing. The gap is largest in bench_b (8.0s) and asset_specs (3.3s).

SRN per-case durations:

| Case | n | Median all (s) | Median correct (s) | Median wrong (s) |
|---|--:|--:|--:|--:|
| srn_empty_submodel_bypass | 10 | 63.6 | 27.1 | 64.9 |
| srn_serial_number | 10 | 53.5 | 49.5 | 57.5 |
| srn_from_fault_context | 10 | 48.3 | — | 48.3 |
| srn_spatial_hall4 | 10 | 41.8 | 38.3 | 45.3 |
| srn_routine_priority | 10 | 40.5 | — | 40.5 |

Three SRN cases have `median_correct = null` because they produced 0 correct runs. `srn_empty_submodel_bypass` is the longest case at 63.6s median — the agent spends the most time on the case it can never solve. The single correct run in that case (27.1s) is less than half the median wrong time, suggesting the correct path is significantly shorter but the model almost never finds it.

Compared to the 27B model (77–97s per SRN case), the 9B is faster (40–64s), but this reflects earlier termination due to failure rather than efficiency — the 9B exhausts its budget or gives up before completing the write path.

---

## 7. Manuals-First Correlation

| | Manuals first | No manuals | Total |
|---|--:|--:|--:|
| **Correct** | 68 | 26 | 94 |
| **Wrong** | 38 | 68 | 106 |

- Manuals-first correct rate: 68/106 = **64.2%**
- No-manuals correct rate: 26/94 = **27.7%**
- Difference: **+36.5 percentage points**

The manuals-first effect is dramatically stronger than in the 27B model (+36.5 pp vs +11.4 pp). This is driven by two factors:

1. The SRN suite's near-zero manuals-first rate (1/50, 2%) almost entirely falls into the "no manuals + wrong" cell, inflating the contrast.
2. For read-only suites, the 9B model is far more dependent on manual consultation to compensate for its weaker graph-traversal ability — without the manual, it lacks the contextual anchors that the 27B model can infer.

However, the causal direction is ambiguous for the SRN suite: the 2% manuals-first rate may reflect the model's tendency to jump to tool calls without reading documentation, which is both a cause and a symptom of its inability to complete the write task.

---

## 8. Key Takeaways / Action Items

### T1 — The 9B model is below the viability threshold for write-path tasks

At 14% SRN accuracy (vs 32% for 27B), the 9B model cannot reliably perform autonomous service-request creation. The failure is not primarily about vocabulary or tool selection — it's about basic task completion: the model rarely reaches the point of issuing any write call. **Action:** For models below ~27B, consider a guided write-path where the system prompt explicitly enumerates the step sequence (traverse → identify submodel → call `put_submodel` with full payload), rather than relying on the model to discover it autonomously.

### T2 — Read-path accuracy collapses without manual consultation

The containment_hall4 suite drops from 100% (27B) to 44% (9B), and asset_specs from 100% to 70%. The +36.5 pp manuals-first correlation shows the 9B model depends heavily on documentation to anchor its graph traversal. Without manuals, the model's weaker reasoning leads to wrong submodel lookups and misidentified assets. **Action:** Enforce manuals-first as a hard constraint in the system prompt for smaller models, or auto-inject relevant manual excerpts when a graph query returns empty results.

### T3 — Asset confusion compounds SRN failures

In `srn_routine_priority`, the 9B model confuses UR3e_001 and UR3e_002 in 3/10 runs. This spatial disambiguation failure is absent in the 27B model. The 9B model cannot reliably distinguish between same-type assets in the same location. **Action:** Strengthen the asset-identification step in the system prompt, or add a disambiguation tool that returns all assets matching a type + location filter.

### T4 — The "null" bypass category reveals a navigation gap

16/50 SRN runs end in "null" — the agent never finds the target submodel. This contrasts with the 27B model's "surfaced" dominance (20/50), where the submodel is found but the write is skipped. The 9B model's failure is earlier in the pipeline: it cannot navigate the AAS structure to locate the relevant submodel. **Action:** Add a `find_submodel_by_semantic_type` tool that accepts an AAS ID and a submodel semantic ID, returning the matching submodel's idShort and path — bypassing the need for the model to construct multi-hop graph traversals.

### T5 — idShort violations are a budget drain, not a correctness issue

At 76% violation rate with 95.4% self-correction, the idShort pattern wastes 1–2 turns per violation without affecting the final answer. For the 9B model, these wasted turns are proportionally more costly given its lower recursion budget and slower convergence. **Action:** Same as 27B recommendation — add pre-flight validation or a few-shot idShort warning. The ROI is higher for smaller models because the saved turns represent a larger fraction of the total budget.

### T6 — The 47% overall accuracy sets a floor for model-size requirements

No read-only suite exceeds 90% (anti_pattern) and the write-path suite is at 14%. If the production requirement is ≥80% on read-only tasks and ≥50% on write tasks, the 9B model does not meet either threshold. **Action:** Use this result as the lower-bound data point for the model-size scaling analysis in the paper. The 9B → 27B jump (+30 pp overall, +18 pp SRN) suggests that ~27B parameters is the minimum viable size for the current tool set and prompt design.
