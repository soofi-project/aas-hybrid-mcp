# Evaluation Analysis: Qwen3.5-27B — T07

Model: `qwen35-27b` · Trial: T07 · Suites: 5 · Total runs: 200

---

## 1. Paper-Evaluation Table per Suite

| Suite | N | Correct | Manuals first | idShort violation | Bypass (pse) | Median correct (s) | Median wrong (s) |
|---|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 20 (100%) | 0 (0%) | 20 (100%) | — | 13.4 | — |
| asset_specs | 20 | 20 (100%) | 0 (0%) | 20 (100%) | — | 11.4 | — |
| bench_b | 60 | 47 (78%) | 49 (82%) | 29 (48%) | — | 28.8 | 24.7 |
| containment_hall4 | 50 | 50 (100%) | 40 (80%) | 24 (48%) | — | 26.9 | — |
| srn_autonomous | 50 | 16 (32%) | 20 (40%) | 33 (66%) | 56% | 94.9 | 83.2 |
| **Total** | **200** | **153 (77%)** | **109 (55%)** | **126 (63%)** | — | — | — |

Three suites achieve perfect accuracy (anti_pattern, asset_specs, containment_hall4). The two remaining suites diverge sharply: bench_b lands at 78%, while srn_autonomous collapses to 32% — a 46-point gap that is entirely attributable to write-path failures (see §3).

---

## 2. idShort Violation Self-Correction Rate

| Suite | Violations | Self-corrected | Rate |
|---|--:|--:|--:|
| anti_pattern | 20 | 19 | 95.0% |
| asset_specs | 20 | 20 | 100% |
| bench_b | 29 | 29 | 100% |
| containment_hall4 | 24 | 24 | 100% |
| srn_autonomous | 33 | 31 | 93.9% |
| **Total** | **126** | **123** | **97.6%** |

The agent violates the idShort anti-pattern in 63% of all runs (126/200) but self-corrects in 97.6% of those cases. Violation rules merged across all suites:

| Rule | Occurrences | Interpretation |
|---|--:|---|
| `idShort_contains_or_regex` | 149 | Agent uses idShort in query/Cypher patterns |
| `toLower_id_contains` | 119 | Agent references elements by idShort value |
| `id_contains_or_regex` | 11 | Agent uses full identifier in regex |
| `assetType_match` | 1 | Agent matches by assetType (negligible) |

The dominant pattern is clear: the agent reaches for idShort as a shortcut in both queries and references. The near-perfect self-correction rate means this rarely affects the final answer, but it wastes turns and budget — particularly in the srn_autonomous suite where the agent already operates under time pressure.

---

## 3. Write-Path Bypass (SRN Suite Only)

The srn_autonomous suite is the only suite involving write operations. A "bypass" occurs when the agent fails to follow the correct write path — it either doesn't write at all, writes to the wrong location, or finds an existing structure and stops without creating the required element.

**Overall bypass rate: 56%** (28/50 runs with non-correct bypass)

| Bypass type | Count | Meaning |
|---|--:|---|
| correct | 17 | Wrote the right element via the right path |
| surfaced | 20 | Found existing submodel, stopped without writing |
| direct | 5 | Called `put_submodel_element` without traversing structure |
| cascade | 3 | Multi-step bypass (wrong intermediate step) |
| none | 4 | No write attempted at all |
| null | 1 | Indeterminate |

Per-case breakdown:

| Case | correct | surfaced | direct | cascade | none | null |
|---|--:|--:|--:|--:|--:|--:|
| srn_from_fault_context | 8 | 1 | — | — | 1 | — |
| srn_serial_number | 4 | 5 | — | 1 | — | — |
| srn_spatial_hall4 | 4 | 5 | — | 1 | — | — |
| srn_empty_submodel_bypass | 0 | 8 | 1 | 1 | — | — |
| srn_routine_priority | 1 | 1 | 4 | — | 3 | 1 |

The "surfaced" category is the dominant failure mode: 40% of all runs. The agent discovers an existing ServiceRequestNotification submodel on the target AAS, then treats its existence as task completion — a read-path/write-path confusion. This is most extreme in `srn_empty_submodel_bypass` (0% correct, 80% surfaced), where the submodel exists but is empty and needs a new element added.

Write-tool execution: `put_submodel_element` was called in only 12 of 45 write attempts (26.7%). In the remaining 73.3%, the agent either called `put_submodel` (creating a whole new submodel instead of an element within the existing one) or never reached a write-tool call at all.

---

## 4. Template Validation

All five suites report **zero write-tool rejections and zero validation errors**. The agent never sends malformed payloads — when it does call a write tool, the data passes schema validation. The problem is not validation quality but tool-selection accuracy: the agent picks the wrong tool or stops before issuing any write call.

---

## 5. Judge Failure Modes per SRN Case

| Case | n_incorrect | Top missing facts | Top wrong claims |
|---|--:|---|---|
| srn_from_fault_context | 10 | ServiceType=CorrectiveMaintenance (10/10), Status=Open (3/10) | Service Type: MAINTENANCE (2), Emergency Maintenance (1), TROUBLESHOOTING (1), Emergency Stop Reset (1) |
| srn_routine_priority | 10 | Priority=Low (10/10), ServiceType=Inspection (6/10) | Priority is NORMAL (4), Priority is Normal (2) |
| srn_empty_submodel_bypass | 10 | Payload contains SRN entry (9/10), Write was attempted (8/10) | — |
| srn_serial_number | 4 | Serial resolution errors (2), Write attempted (1) | Service Type: EMERGENCY_STOP instead of CorrectiveMaintenance (2) |

Two distinct root causes emerge:

1. **Vocabulary gap** — In `srn_from_fault_context` and `srn_routine_priority`, the agent cannot map the natural-language task description to the correct SRN enum values. It invents service types (MAINTENANCE, ROUTINE_INSPECTION, Emergency Maintenance) and defaults priority to "Normal" instead of "Low". The agent has no internal lookup table for the SRN submodel's controlled vocabulary.

2. **Write-path paralysis** — In `srn_empty_submodel_bypass`, the agent finds the empty container but never creates an element inside it. Missing facts are entirely structural: the payload should contain an SRN entry (9/10) and a write should have been attempted (8/10). The agent doesn't understand that discovering a container ≠ completing the task.

---

## 6. Duration: Median per Suite

| Suite | Median correct (s) | Median wrong (s) |
|---|--:|--:|
| asset_specs | 11.4 | — |
| anti_pattern | 13.4 | — |
| containment_hall4 | 26.9 | — |
| bench_b | 28.8 | 24.7 |
| srn_autonomous | 94.9 | 83.2 |

SRN per-case durations:

| Case | n | Median all (s) | Median correct (s) | Median wrong (s) |
|---|--:|--:|--:|--:|
| srn_spatial_hall4 | 10 | 96.7 | 96.7 | — |
| srn_from_fault_context | 10 | 95.1 | — | 95.1 |
| srn_empty_submodel_bypass | 10 | 82.7 | — | 82.7 |
| srn_serial_number | 10 | 80.4 | 85.7 | 79.2 |
| srn_routine_priority | 10 | 77.4 | — | 77.4 |

Three SRN cases have `median_correct = null` because they produced 0 or 1 correct runs — insufficient for a reliable median. Correct SRN runs are ~12s slower than wrong runs, consistent with the extra tool-call round-trips needed for a successful write. All SRN cases exceed 77s, reflecting the multi-step nature of submodel traversal → element creation.

In bench_b, correct answers are slower (28.8s vs 24.7s), suggesting the agent invests more exploration effort in successful runs.

---

## 7. Manuals-First Correlation

| | Manuals first | No manuals | Total |
|---|--:|--:|--:|
| **Correct** | 89 | 64 | 153 |
| **Wrong** | 20 | 27 | 47 |

- Manuals-first correct rate: 89/109 = **81.7%**
- No-manuals correct rate: 64/91 = **70.3%**
- Difference: +11.4 percentage points

Consulting manuals before the first graph query correlates with a higher success rate. The effect is moderate but consistent: agents that read the manual first are ~11 pp more likely to produce a correct answer. However, causation is not established — the 40% manuals-first rate in the srn_autonomous suite (where most failures are write-path, not knowledge-gap) depresses the overall correlation.

---

## 8. Key Takeaways / Action Items

### T1 — Fix the SRN vocabulary gap
The agent invents enum values (MAINTENANCE, ROUTINE_INSPECTION, Emergency Maintenance) instead of using the correct ones (CorrectiveMaintenance, Inspection). **Action:** Inject the SRN submodel template's controlled vocabulary into the system prompt or add a dedicated `get_srn_enum_values` tool that returns valid ServiceType and Priority values before the agent attempts a write.

### T2 — Address write-path paralysis
40% of SRN runs "surface" — the agent finds the submodel and stops without creating the required element. The `srn_empty_submodel_bypass` case scores 0% correct. **Action:** Add an explicit instruction to the system prompt: "If a submodel exists but contains no elements matching the task, you must create a new SubmodelElement inside it." Alternatively, detect empty submodels in the write-tool logic and auto-suggest element creation.

### T3 — Improve tool-selection clarity
Only 26.7% of write attempts reach `put_submodel_element`; the rest either call `put_submodel` (wrong scope) or never issue a write call. **Action:** Rename or re-describe the write tools to make the distinction between "create a submodel" and "add an element inside an existing submodel" more prominent. Consider a unified upsert tool that handles both cases based on context.

### T4 — Reduce idShort violation waste
The agent violates the idShort anti-pattern in 63% of runs, then self-corrects in 97.6% of cases — wasting 1–2 turns per violation. In the SRN suite, these wasted turns consume budget before the write attempt. **Action:** Strengthen the idShort warning in the system prompt with a few-shot example, or add a pre-flight validation step that rejects idShort-based queries before they execute.

### T5 — Investigate manuals-first as a causal factor
The +11 pp correlation between manuals-first and correctness is promising but not proven causal. The srn_autonomous suite's low manuals-first rate (40%) may reflect the agent's tendency to jump directly to tool calls for write tasks. **Action:** Run an ablation where the system prompt mandates manual consultation before any write operation, and measure whether SRN correctness improves.

### T6 — The 32% SRN floor is the binding constraint
All read-only suites score 78–100%. The overall 77% accuracy is dragged down entirely by the SRN write path. Until the agent can reliably create SubmodelElements inside existing submodels, improving read-path accuracy yields diminishing returns. **Priority: T2 and T3 are the highest-impact fixes.**
