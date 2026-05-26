# Evaluation Analysis: Qwen3.5-4B — T07

Model: `qwen35-4b` · Trial: T07 · Suites: 5 · Total runs: 200

---

## 1. Paper-Evaluation Table per Suite

| Suite | N | Correct | Manuals first | idShort violation | Bypass (pse) | Median correct (s) | Median wrong (s) |
|---|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 16 (80%) | 16 (80%) | 18 (90%) | — | 7.6 | 12.3 |
| asset_specs | 20 | 17 (85%) | 19 (95%) | 18 (90%) | — | 9.4 | 11.2 |
| bench_b | 60 | 27 (45%) | 35 (58%) | 41 (68%) | — | 13.4 | 18.4 |
| containment_hall4 | 50 | 21 (42%) | 34 (68%) | 37 (74%) | — | 7.0 | 11.2 |
| srn_autonomous | 50 | 2 (4%) | 7 (14%) | 37 (74%) | 48% | 37.0 | 50.6 |
| **Total** | **200** | **83 (41.5%)** | **111 (55.5%)** | **151 (75.5%)** | — | — | — |

Only the two read-only suites with focused scope (anti_pattern 80%, asset_specs 85%) approach acceptable levels. The three broader suites collapse: bench_b at 45%, containment_hall4 at 42%, and SRN at a catastrophic 4%. The SRN suite is effectively at floor performance — 2 correct out of 50 runs. Compared to the 9B sibling (47% overall, 14% SRN), the 4B model loses another 5.5 pp overall and 10 pp on SRN, confirming a steep scaling cliff below ~9B parameters.

---

## 2. idShort Violation Self-Correction Rate

| Suite | Violations | Self-corrected | Rate |
|---|--:|--:|--:|
| anti_pattern | 18 | 17 | 94.4% |
| asset_specs | 18 | 17 | 94.4% |
| bench_b | 41 | 40 | 97.6% |
| containment_hall4 | 37 | 37 | 100% |
| srn_autonomous | 37 | 35 | 94.6% |
| **Total** | **151** | **146** | **96.7%** |

The 4B model violates the idShort anti-pattern in 75.5% of runs — comparable to the 9B model (76%). Self-correction is high at 96.7% (vs 95.4% for 9B), meaning the model almost always fixes the violation once it encounters an error. The pattern is consistent: the model generates non-conforming idShort values by default, then patches them reactively.

Violation occurrences by rule (merged across suites):

| Rule | Occurrences |
|---|--:|
| `idShort_contains_or_regex` | 322 |
| `id_contains_or_regex` | 73 |
| `toLower_id_contains` | 56 |
| `assetType_match` | 16 |

The `idShort_contains_or_regex` rule accounts for 69% of all occurrences (322/467), confirming the model systematically interpolates idShort values into natural-language output or query patterns rather than resolving semanticId. The total occurrence count (467) is lower than the 9B model (487), but the 4B model produces fewer total tool calls overall, so the per-attempt violation density is likely comparable or higher.

---

## 3. Write-Path Bypass (SRN Suite Only)

**Overall bypass rate: 48%**

| Bypass type | Count | Meaning |
|---|--:|---|
| none | 16 | No write attempted at all |
| cascade | 11 | Multi-step bypass via wrong intermediate steps |
| null | 8 | No submodel found / indeterminate path |
| direct | 7 | Called `put_submodel_element` without traversing structure |
| surfaced | 6 | Found existing submodel, stopped without writing |
| correct | 2 | Correct write path followed |

Per-case breakdown:

| Case | correct | surfaced | direct | cascade | none | null |
|---|--:|--:|--:|--:|--:|--:|
| srn_from_fault_context | 1 | 3 | — | 1 | — | 5 |
| srn_routine_priority | — | — | 3 | 4 | 2 | 1 |
| srn_serial_number | 1 | — | 2 | 1 | 5 | 1 |
| srn_spatial_hall4 | — | 2 | 2 | 2 | 4 | — |
| srn_empty_submodel_bypass | — | 1 | — | 3 | 5 | 1 |

The bypass profile is worse than the 9B model's (44% bypass rate). Key differences:

- **none (16/50):** The most common failure — the agent never attempts a write at all. This is the dominant failure in `srn_serial_number` (5/10), `srn_empty_submodel_bypass` (5/10), and `srn_spatial_hall4` (4/10). The model defers to the user or simply stops before reaching any write step.
- **cascade (11/50):** The agent chains wrong intermediate steps, compounding errors. Concentrated in `srn_routine_priority` (4/10) and `srn_empty_submodel_bypass` (3/10).
- **null (8/50):** The agent never finds the target submodel. Worst in `srn_from_fault_context` (5/10).
- **surfaced (6/50):** The agent finds the submodel but does not write to it. This is a smaller proportion than the 9B model, where "surfaced" was rarer — the 4B model actually locates submodels somewhat more often but then still fails to act.

Write-tool execution: `put_submodel_element` was called in 34 out of 35 attempts, confirming the model does invoke the write tool when it reaches that point. The failure is upstream — the model cannot navigate the AAS structure or construct the correct payload.

---

## 4. Template Validation

All five suites report **zero write-tool rejections and zero validation errors**. When the 4B model does issue a write call, the payload passes schema validation — identical to the 9B and 27B models. The constraint is never payload correctness per se but tool-selection, path-finding, and domain knowledge: the model either never reaches a write call, or calls it with the wrong structural context (wrong submodel, wrong element path).

---

## 5. Judge Failure Modes per SRN Case

| Case | n_incorrect | Top missing facts | Top wrong claims |
|---|--:|---|---|
| srn_from_fault_context | 10 | ServiceType=CorrectiveMaintenance (10/10), Request created for MiR100_001 (8/10), Status=Open (7/10), Priority=High (5/10) | Wrong asset UR3e_002/CRX10iA (3), User must provide info (1), Emergency Stop (2) |
| srn_routine_priority | 10 | ServiceType=Inspection (10/10), Priority=Low (10/10), Request created for UR3e_002 (9/10), Status=Open (9/10) | User must provide info (1), Priority: Normal (1), Service Type: Routine Inspection (1) |
| srn_empty_submodel_bypass | 8 | Payload contains SRN entry (8/8), Write attempted (7/8), Asset=CRX10iA_001 (3/8) | — |
| srn_serial_number | 10 | Write attempted (6/10), Serial resolved MIR100-2020-001→MiR100_001 (5/10), Priority=High (5/10) | User must provide info (1) |
| srn_spatial_hall4 | 10 | Asset=MiR100_001 identified (7/10), Write attempted (2/10) | — |

Three root causes emerge:

1. **Complete vocabulary failure:** In `srn_from_fault_context`, the agent fails to map "emergency stop" to ServiceType=CorrectiveMaintenance in 10/10 incorrect runs. In `srn_routine_priority`, it never assigns Priority=Low (10/10 miss) or ServiceType=Inspection (10/10 miss). The 4B model lacks the inferential capacity to map natural-language descriptions to the SRN schema's controlled vocabulary. It substitutes colloquial terms ("Routine Inspection" instead of "Inspection", "Normal" instead of "Low") rather than reading the schema enums.

2. **Asset confusion and spatial reasoning failure:** In `srn_from_fault_context`, the agent misidentifies the Hall 4 transport robot as UR3e_002 or CRX10iA in 3/10 runs. In `srn_spatial_hall4`, it fails to identify MiR100_001 as the Hall 4 transport robot in 7/10 runs. The model cannot reliably resolve spatial references to specific asset identifiers.

3. **Autonomy refusal:** The recurring "user must provide info" wrong claim across multiple scenarios indicates the model actively refuses to act autonomously, requesting human input for fields that are derivable from context. This is a temperament problem — the model does not behave as an autonomous agent.

---

## 6. Duration: Median per Suite

| Suite | Median correct (s) | Median wrong (s) |
|---|--:|--:|
| anti_pattern | 7.6 | 12.3 |
| asset_specs | 9.4 | 11.2 |
| bench_b | 13.4 | 18.4 |
| containment_hall4 | 7.0 | 11.2 |
| srn_autonomous | 37.0 | 50.6 |

Wrong runs are consistently slower across all suites (1.8s–13.6s gap), indicating the model wastes time on unproductive exploration before failing. The gap is largest in srn_autonomous (13.6s) and bench_b (5.0s).

SRN per-case durations:

| Case | n | Median all (s) | Median correct (s) | Median wrong (s) |
|---|--:|--:|--:|--:|
| srn_from_fault_context | 10 | 42.9 | — | 42.9 |
| srn_routine_priority | 10 | 44.5 | — | 44.5 |
| srn_serial_number | 10 | 55.1 | — | 55.1 |
| srn_spatial_hall4 | 10 | 56.3 | — | 56.3 |
| srn_empty_submodel_bypass | 10 | 52.2 | 37.0 | 53.3 |

Four of five SRN cases have `median_correct = null` because they produced 0 correct runs. Only `srn_empty_submodel_bypass` has a single correct run (37.0s), which is 16s faster than the median wrong time (53.3s). The spatial reasoning cases (`srn_spatial_hall4`, `srn_serial_number`) are the slowest at 55–56s, reflecting the model's inability to resolve the asset identification step. Compared to the 9B model (40–64s per SRN case), the 4B is in a similar range but with fewer correct outcomes per unit time.

---

## 7. Manuals-First Correlation

| | Manuals first | No manuals | Total |
|---|--:|--:|--:|
| **Correct** | 60 | 23 | 83 |
| **Wrong** | 51 | 66 | 117 |

- Manuals-first correct rate: 60/111 = **54.1%**
- No-manuals correct rate: 23/89 = **25.8%**
- Difference: **+28.3 percentage points**

The manuals-first effect is strong (+28.3 pp), though slightly weaker than the 9B model (+36.5 pp). The smaller gap may reflect the 4B model's weaker ability to act on documentation even when it does consult it — reading the manual helps but does not fully compensate for the model's reasoning limitations. The SRN suite's 14% manuals-first rate pulls down the "no manuals" cell heavily: most SRN runs fall into the "no manuals + wrong" quadrant.

The causal direction in the SRN suite remains ambiguous: the low manuals-first rate may reflect the model's tendency to jump to tool calls without reading documentation (a cause of failure), or it may reflect that the model gives up quickly and never reaches the documentation step (a symptom of broader inability).

---

## 8. Key Takeaways / Action Items

### T1 — The 4B model is below the viability threshold for all multi-step tasks

At 4% SRN accuracy (vs 14% for 9B, 32% for 27B), the 4B model is effectively non-functional on write-path tasks. Even the read-only suites that the 9B model handles moderately well (bench_b 55%, containment_hall4 44%) drop to 45% and 42% respectively. Only the focused read-only suites (anti_pattern, asset_specs) remain above 80%. **Action:** The 4B model should not be deployed for any AAS agent task requiring multi-step reasoning or write-path execution. Use this result as the absolute floor data point for the scaling analysis.

### T2 — Vocabulary mapping is the primary SRN bottleneck

In `srn_from_fault_context` and `srn_routine_priority`, the model fails to map natural-language descriptions to SRN schema enums in 100% of incorrect runs (CorrectiveMaintenance, Inspection, Low, Open). This is not an orchestration problem — the model literally does not know the correct enum values. **Action:** For models below ~9B, inject the SRN schema enum table directly into the system prompt or tool description, so the model does not need to infer vocabulary from context.

### T3 — Autonomy refusal blocks write-path completion

The "user must provide info" wrong claim appears across multiple SRN scenarios. The 4B model defaults to asking the user instead of acting autonomously, even when all required information is available in the conversation context. This is a temperament failure that compounds the vocabulary and navigation problems. **Action:** Strengthen the "Act, don't ask permission" directive in the system prompt for smaller models, or add an explicit pre-check step that verifies all required fields are available before allowing the agent to defer to the user.

### T4 — Navigation failure precedes write failure

The "none" bypass category (16/50 SRN runs) dominates over "surfaced" (6/50), meaning the 4B model's primary failure mode is never reaching the write step at all — it cannot navigate the AAS structure to locate the target submodel. This is an earlier-stage failure than the 9B model's, which more often finds the submodel but then fails to write. **Action:** Add a `find_submodel_by_semantic_type` tool that accepts an AAS ID and a submodel semantic ID, returning the matching submodel's idShort and path — bypassing the need for the model to construct multi-hop graph traversals.

### T5 — idShort violations are a budget drain on smaller models

At 75.5% violation rate with 96.7% self-correction, the idShort pattern wastes 1–2 turns per violation without affecting the final answer. For the 4B model with its already-constrained recursion budget, these wasted turns are proportionally more costly than for larger models. **Action:** Add pre-flight idShort validation or a few-shot idShort warning in the system prompt. The ROI is highest for the smallest models because saved turns represent a larger fraction of the total budget.

### T6 — Manuals-first helps but cannot close the gap

The +28.3 pp manuals-first correlation shows documentation consultation is beneficial, but even with manuals the 4B model only reaches 54.1% correctness — barely above chance for many suites. The model cannot fully act on the information it reads. **Action:** For models below ~9B, consider auto-injecting relevant manual excerpts into the context rather than relying on the model to fetch and interpret them, reducing the cognitive load of the retrieval step.

### T7 — The scaling cliff is between 9B and 27B, not 4B and 9B

The 4B → 9B jump yields only +5.5 pp overall (41.5% → 47%) and +10 pp on SRN (4% → 14%), while the 9B → 27B jump yields +29.5 pp overall and +18 pp on SRN. The 4B model's failure modes (vocabulary, navigation, autonomy) are largely the same as the 9B's, just more severe. The qualitative shift occurs at ~27B parameters. **Action:** Present this as a scaling-cliff finding in the paper: models below ~9B are uniformly inadequate, and the minimum viable model size for the current tool set and prompt design is ~27B parameters.
