# Evaluation Analysis: Qwen3.5-2B — T07

Model: `qwen35-2b` · Trial: T07 · Suites: 5 · Total runs: 200

---

## 1. Paper-Evaluation Table per Suite

| Suite | N | Correct | Manuals first | idShort violation | Bypass (pse) | Median correct (s) | Median wrong (s) |
|---|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 2 (10%) | 0 (0%) | 1 (5%) | — | 17.2 | 16.0 |
| asset_specs | 20 | 4 (20%) | 0 (0%) | 1 (5%) | — | 15.1 | 22.8 |
| bench_b | 60 | 2 (3.3%) | 8 (13.3%) | 7 (11.7%) | — | 14.9 | 24.2 |
| containment_hall4 | 50 | 5 (10%) | 7 (14%) | 6 (12%) | — | 14.1 | 23.6 |
| srn_autonomous | 50 | 0 (0%) | 0 (0%) | 11 (22%) | 6% | — | 22.8 |
| **Total** | **200** | **13 (6.5%)** | **15 (7.5%)** | **26 (13%)** | — | — | — |

The 2B model is at floor performance across all suites. Even the focused read-only suites where the 4B model achieves 80–85% collapse to 10–20%. The three broader suites are catastrophic: bench_b at 3.3%, containment_hall4 at 10%, and SRN at 0%. Compared to the 4B model (41.5% overall, 4% SRN), the 2B loses another 35 pp overall and 4 pp on SRN — the latter an absolute floor that cannot go lower. The 2B model is qualitatively different from the 4B: where the 4B occasionally stumbles into correct answers, the 2B almost never does.

---

## 2. idShort Violation Self-Correction Rate

| Suite | Violations | Self-corrected | Rate |
|---|--:|--:|--:|
| anti_pattern | 1 | 1 | 100% |
| asset_specs | 1 | 1 | 100% |
| bench_b | 7 | 7 | 100% |
| containment_hall4 | 6 | 5 | 83.3% |
| srn_autonomous | 11 | 11 | 100% |
| **Total** | **26** | **25** | **96.2%** |

The 2B model violates idShort in only 13% of runs — far lower than the 4B model's 75.5%. This is not because the 2B model is better at compliance, but because it makes fewer tool calls overall: fewer attempts means fewer opportunities to produce non-conforming idShort values. Self-correction is high at 96.2%, with containment_hall4 the sole suite where it drops to 83.3% (5/6 corrected) — the only instance across all models where self-correction falls below 100% for any suite.

Violation occurrences by rule (merged across suites):

| Rule | Occurrences |
|---|--:|
| `idShort_contains_or_regex` | 26 |
| `assetType_match` | 8 |
| `id_contains_or_regex` | 2 |

The `idShort_contains_or_regex` rule accounts for 72% of all occurrences (26/36), consistent with the pattern seen at larger model sizes. The absolute counts are low (36 total vs 467 for the 4B model), again reflecting fewer tool interactions rather than better compliance.

---

## 3. Write-Path Bypass (SRN Suite Only)

**Overall bypass rate: 6%** (3 correct / 50 runs)

| Bypass type | Count | Meaning |
|---|--:|---|
| null | 41 | No submodel found / indeterminate path |
| correct | 3 | Correct write path followed |
| none | 3 | No write attempted at all |
| surfaced | 1 | Found existing submodel, stopped without writing |
| cascade | 2 | Multi-step bypass via wrong intermediate steps |

Per-case breakdown:

| Case | correct | surfaced | cascade | none | null |
|---|--:|--:|--:|--:|--:|
| srn_from_fault_context | 0 | 0 | 0 | 0 | 10 |
| srn_routine_priority | 1 | 0 | 0 | 1 | 8 |
| srn_serial_number | 0 | 1 | 1 | 0 | 8 |
| srn_spatial_hall4 | 0 | 0 | 0 | 0 | 10 |
| srn_empty_submodel_bypass | 2 | 0 | 1 | 2 | 5 |

The bypass profile is starkly different from the 4B model's. Where the 4B model's dominant failure was "none" (16/50 — never attempted a write), the 2B model's dominant failure is "null" (41/50 — never found the submodel). The 2B model fails at an earlier stage: it cannot navigate the AAS hierarchy to locate the target submodel at all. Two entire cases — `srn_from_fault_context` and `srn_spatial_hall4` — are pure "null" (10/10), meaning the model never reaches any part of the write path.

The exception is `srn_empty_submodel_bypass`, which has the most non-null outcomes (correct=2, none=2, cascade=1) — the absence of prior content makes the submodel slightly more discoverable. But even here, all 10 runs are judged incorrect because the ServiceRequestNotification payload is never populated.

Write-tool execution: `put_submodel_element` was called in only 5 out of 50 runs (10%), with 9 total attempts. The 4B model called it in 34/35 attempts — the 2B model barely reaches the write step at all.

---

## 4. Template Validation

All five suites report **zero write-tool rejections and zero validation errors**. This is consistent with all other model sizes: when the 2B model does issue a write call, the payload passes schema validation. The constraint is never payload correctness but the upstream failure to navigate the AAS structure and construct the correct write context.

---

## 5. Judge Failure Modes per SRN Case

| Case | n_incorrect | Top missing facts | Top wrong claims |
|---|--:|---|---|
| srn_from_fault_context | 10 | ServiceType=CorrectiveMaintenance (10/10), Request for MiR100_001 (10/10), Priority=High (10/10), Status=Open (10/10) | — |
| srn_routine_priority | 10 | ServiceType=Inspection (10/10), Priority=Low (10/10), Request for UR3e_002 (10/10), Status=Open (10/10) | — |
| srn_empty_submodel_bypass | 10 | Payload contains SRN entry (10/10), Write attempted (8/10), Asset=CRX10iA_001 (8/10) | User must provide info (1) |
| srn_serial_number | 10 | Serial resolved (7/10 positive, 2/10 negative), Priority=High (4/10), Write attempted (4/10) | — |
| srn_spatial_hall4 | 10 | Asset=MiR100_001 identified (9/10 negative), Write attempted (8/10 negative) | — |

Three root causes emerge:

1. **Complete vocabulary failure:** In `srn_from_fault_context` and `srn_routine_priority`, the agent fails to map natural-language descriptions to SRN schema enums in 100% of incorrect runs (10/10 miss on ServiceType, Priority, Status). This is identical to the 4B model's pattern but with zero exceptions — the 2B model never produces a correct enum value. It lacks the parametric capacity to map task context onto the SRN submodel's controlled vocabulary.

2. **Asset identification failure:** In `srn_spatial_hall4`, the agent fails to identify MiR100_001 as the Hall 4 transport robot in 9/10 runs. In `srn_empty_submodel_bypass`, it fails to identify CRX10iA_001 in 8/10. The 2B model cannot reliably resolve spatial or contextual references to specific asset identifiers.

3. **Navigation failure precedes vocabulary failure:** The "null" bypass dominance means most runs never reach the point where vocabulary matters. The 2B model fails at structural navigation first; vocabulary failure is a second-order problem that would only appear if the model could locate the target submodel.

---

## 6. Duration: Median per Suite

| Suite | Median correct (s) | Median wrong (s) |
|---|--:|--:|
| anti_pattern | 17.2 | 16.0 |
| asset_specs | 15.1 | 22.8 |
| bench_b | 14.9 | 24.2 |
| containment_hall4 | 14.1 | 23.6 |
| srn_autonomous | — | 22.8 |

A notable inversion: in anti_pattern, wrong runs are *faster* than correct runs (16.0s vs 17.2s). This likely reflects the 2B model's tendency to guess quickly and incorrectly, while the rare correct answer requires a slightly longer reasoning chain. In all other suites, wrong runs are slower (7.7–9.3s gap), consistent with unproductive exploration.

SRN per-case durations:

| Case | n | Median all (s) | Median correct (s) | Median wrong (s) |
|---|--:|--:|--:|--:|
| srn_from_fault_context | 10 | 22.8 | — | 22.8 |
| srn_routine_priority | 10 | 24.3 | — | 24.3 |
| srn_serial_number | 10 | 21.4 | — | 21.4 |
| srn_spatial_hall4 | 10 | 22.1 | — | 22.1 |
| srn_empty_submodel_bypass | 10 | 26.7 | — | 26.7 |

All median_correct values are null because no SRN case produced a correct run. The 2B model is consistently faster than the 4B model (21–27s vs 42–56s), but this is not efficiency — it is early exhaustion. The model fails quickly because it cannot sustain the multi-step reasoning chain (identify asset → locate submodel → populate fields → write) that SRN requires. It terminates after shallow exploration, having never engaged deeply enough to be slow.

---

## 7. Manuals-First Correlation

| | Manuals first | No manuals | Total |
|---|--:|--:|--:|
| **Correct** | 0 | 13 | 13 |
| **Wrong** | 15 | 172 | 187 |

- Manuals-first correct rate: 0/15 = **0.0%**
- No-manuals correct rate: 13/185 = **7.0%**
- Difference: **−7.0 percentage points**

The manuals-first effect is not merely absent — it is negative. Zero out of 15 runs where the model consulted manuals first produced a correct answer, while 7% of runs without manuals-first were correct. This is an artifact of selection bias: the model only consults manuals when it is already struggling, and those harder runs are less likely to succeed regardless. The 2B model cannot act on documentation even when it does retrieve it — unlike the 4B model (+28.3 pp manuals-first benefit), the 2B's reading comprehension is too weak to extract actionable guidance from manual text.

The near-total absence of manuals-first behavior (7.5% vs 55.5% for 4B) also indicates the model defaults to generating from parametric knowledge rather than retrieving structured guidance, which contributes to the low overall accuracy.

---

## 8. Key Takeaways / Action Items

### T1 — The 2B model is below any viability threshold

At 6.5% overall (vs 41.5% for 4B) and 0% SRN, the 2B model is non-functional for AAS agent tasks. Even the simplest read-only suite (asset_specs) achieves only 20%. The model lacks the parametric capacity for multi-step tool orchestration, spatial reasoning, and controlled-vocabulary mapping. **Action:** Do not deploy the 2B model for any AAS agent task. Use this as the absolute floor data point for the scaling analysis — below 4B, performance does not degrade gracefully, it collapses.

### T2 — Navigation failure is the primary bottleneck, not vocabulary

The "null" bypass dominance (41/50 SRN runs) shows the 2B model fails at structural navigation before it even reaches the point where enum vocabulary matters. This is an earlier-stage failure than the 4B model, which more often finds the submodel but then fails on content. **Action:** Any intervention targeting smaller models must address AAS hierarchy navigation first — inject a `find_submodel_by_semantic_type` tool or provide explicit path instructions before tackling vocabulary gaps.

### T3 — Manuals are useless at 2B scale

The manuals-first correct rate is 0% — reading documentation provides no benefit. The model lacks the comprehension capacity to extract structured guidance from manual text and apply it to tool calls. **Action:** For models below ~4B, auto-injecting relevant manual excerpts is insufficient; the model needs pre-computed action templates (step-by-step tool-call sequences) rather than documentation to read.

### T4 — The scaling cliff extends below 4B

The 4B → 2B jump yields a −35 pp overall drop (41.5% → 6.5%) and −4 pp on SRN (4% → 0%). Combined with the 4B → 9B jump of only +5.5 pp, this confirms two regimes: below ~9B, models are uniformly inadequate (2B and 4B are both on the floor), while the qualitative shift occurs at ~27B. The 2B and 4B are not meaningfully different in kind — both fail on SRN and struggle on broader read-only suites — only in degree. **Action:** In the paper, present the 2B/4B results as a "below-threshold" cluster distinct from the 9B and 27B tiers.

### T5 — The "null" bypass pattern is a diagnostic for minimum model size

The shift from "none" dominance (4B: agent finds submodel but doesn't write) to "null" dominance (2B: agent never finds submodel) marks a qualitative breakdown in structural reasoning. If a model's bypass profile is dominated by "null," it is below the threshold for AAS navigation tasks. **Action:** Use the "null"-dominance threshold as a diagnostic criterion for model selection — if null > 50% of SRN bypasses, the model is not viable.

### T6 — Self-correction holds but is irrelevant at this scale

At 96.2% self-correction, the 2B model matches the 4B's 96.7%. But with only 13% violation rate (vs 75.5% for 4B), there are fewer violations to correct, and the model's overall success is so low that self-correction never translates into task completion. Self-correction is a necessary but insufficient capability. **Action:** Do not use self-correction rate as a standalone quality metric — it must be interpreted alongside correct rate and bypass profile.

### T7 — Duration is not a proxy for effort at floor performance

The 2B model is faster than the 4B on SRN (21–27s vs 42–56s), not because it is more efficient but because it fails earlier. At floor performance, duration reflects exhaustion depth rather than reasoning quality. **Action:** Do not use duration as a positive quality signal for models below ~9B — shorter times indicate shallower engagement, not faster success.
