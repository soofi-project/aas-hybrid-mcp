# Results Analysis: Qwen3-27b (Qwen3-30B-A3B) — Trial 07

**Model:** Qwen3-30B-A3B (27B dense, MoE routing) via vLLM
**Agent variant:** react
**Judge:** gpt-5.4 via Cortecs
**Date:** 2026-05-25
**5 test suites · 200 runs (50 SRN + 150 read-only)**

---

## 1. Paper Evaluation Table

| Suite | N | Correct | Manuals first | idShort violation | Bypass (pse) | Med. correct | Med. wrong |
|---|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 20 (100%) | 15 (75%) | 19 (95%) | — | 13.2s | — |
| asset_specs | 20 | 20 (100%) | 13 (65%) | 20 (100%) | — | 12.7s | — |
| bench_b | 60 | 51 (85%) | 50 (83%) | 23 (38%) | — | 33.0s | 18.8s |
| containment_hall4 | 50 | 50 (100%) | 43 (86%) | 10 (20%) | — | 29.0s | — |
| srn_autonomous | 50 | 13 (26%) | 39 (78%) | 23 (46%) | 46 (92%) | 69.1s | 98.5s |
| **Total** | **200** | **154 (77%)** | **160 (80%)** | **95 (48%)** | **46/50** | | |

**Bypass (pse)** = `put_submodel_element` called instead of atomic `put_submodel`. Only applicable to srn_autonomous (the only write suite).

### Key rates

| Metric | Value |
|---|---|
| Overall correctness | 77% (154/200) |
| Read-only correctness | 94% (141/150) |
| Write-path correctness | 26% (13/50) |
| Manuals read before first query | 80% (160/200) |
| idShort violation (runs affected) | 48% (95/200) |
| idShort self-correction rate | 98% (93/95) |

---

## 2. idShort Violation Self-Correction Rate

The Cypher anti-pattern validator rejected queries in 48% of all runs (95/200). 98% of violations were followed by a corrective action — the highest recovery rate observed across model sizes.

| Suite | Violation runs | Self-corrected | Rate |
|---|--:|--:|--:|
| anti_pattern | 19 | 19 | 100% |
| asset_specs | 20 | 20 | 100% |
| bench_b | 23 | 21 | 91% |
| containment_hall4 | 10 | 10 | 100% |
| srn_autonomous | 23 | 23 | 100% |
| **Total** | **95** | **93** | **98%** |

### Violation rule frequencies (all suites combined)

| Rule | Frequency |
|---|--:|
| `toLower_id_contains` | 110 |
| `idShort_contains_or_regex` | 54 |
| `id_contains_or_regex` | 13 |

The `toLower_id_contains` pattern dominates (63% of all violations), consistent with the model's tendency to write case-insensitive filters rather than exact idShort matches. The 2 uncorrected violations in `bench_b` are the only cases where the agent failed to self-correct — both involved the agent switching to a different tool instead of rewriting the Cypher query.

---

## 3. Write-Path Bypass Analysis

### 3.1 Bypass classification

| Bypass type | Count | Description |
|---|--:|---|
| `correct` | 2 (4%) | Used `put_submodel` only — no `put_submodel_element` |
| `direct` | 39 (78%) | Skipped `put_submodel` entirely, went straight to `put_submodel_element` |
| `surfaced` | 7 (14%) | Called `put_submodel` but then also called `put_submodel_element` |
| `none` | 2 (4%) | No write tool called at all |

**92% of SRN runs (46/50) used the bypass.** This is the highest bypass rate observed across any model. The dominant pattern is `direct` (78%) — the agent almost entirely skips `put_submodel` and goes straight to `put_submodel_element`, the most aggressive form of bypass.

### 3.2 Per-case bypass breakdown

| Case | N | `put_submodel` only | `put_submodel_element` called | Bypass rate |
|---|--:|--:|--:|--:|
| srn_from_fault_context | 10 | 0 | 10 | 100% |
| srn_routine_priority | 10 | 0 | 10 | 100% |
| srn_serial_number | 10 | 0 | 10 | 100% |
| srn_spatial_hall4 | 10 | 0 | 10 | 100% |
| srn_empty_submodel_bypass | 10 | 2 | 6 | 60% |
| **Total** | **50** | **2** | **46** | **92%** |

### 3.3 Root cause: Direct bypass as default strategy

Unlike larger models that use a mix of bypass types (the 35b model uses `surfaced` 34% and `direct` 14%), the 27b model defaults almost exclusively to `direct` bypass (78%). Only `srn_empty_submodel_bypass` shows any resistance — 2 runs used `put_submodel` correctly and 2 made no write attempt. In every other case, the agent went straight to `put_submodel_element` without attempting the atomic write path.

This suggests the model has insufficiently internalized the instruction to use `put_submodel` as the primary write tool. The `put_submodel_element` tool is more granular and requires less structural understanding — the model takes the path of least resistance.

---

## 4. Template Validation

**No template validation rejection was observed on any write call across all 5 suites.** All `put_submodel` and `put_submodel_element` calls returned `{"status": "ok"}`.

This confirms the same architectural gap identified in other model evaluations:
1. The SRN template has `Cardinality ZeroToMany` — an empty submodel passes validation.
2. `put_submodel_element` has no template check at all.
3. The validator only checks structural conformance, not semantic correctness.

The 27b model writes invented ServiceType values ("Emergency", "repair", "Routine inspection") and Priority values ("Critical", "Normal") — none of which are rejected by the validator.

---

## 5. Judge Failure Modes per SRN Case

The judge (gpt-5.4) marked 37/50 SRN runs as incorrect. The dominant failure modes:

### srn_from_fault_context (0/10 correct)

| Mode | Freq | Example |
|---|--:|---|
| Missing: ServiceType CorrectiveMaintenance | 10/10 | Writes "emergency" or "repair" instead |
| Missing: Status Open | 10/10 | Writes "New" or "new" instead |
| Missing: Priority High | 5/10 | Writes "Critical" instead |
| Wrong: Status is new | 3/10 | |
| Wrong: Priority is critical | 2/10 | |

### srn_routine_priority (0/10 correct)

| Mode | Freq | Example |
|---|--:|---|
| Missing: Priority Low | 10/10 | Writes "Normal" instead |
| Missing: Status Open | 10/10 | Writes "New" instead |
| Missing: ServiceType Inspection | 7/10 | Writes "Routine inspection" instead |
| Wrong: Priority Normal | 6/10 | |
| Wrong: Status New | 6/10 | |

### srn_serial_number (1/10 correct)

| Mode | Freq | Example |
|---|--:|---|
| Missing: Priority High | 5/10 | Writes "Critical" instead |
| Missing: Serial resolution MIR100-2020-001 → MiR100_001 | 4/10 | Agent fails to resolve serial number |
| Wrong: Service Type repair instead of CorrectiveMaintenance | 2/10 | |
| Wrong: Priority Critical instead of High | 2/10 | |

### srn_spatial_hall4 (9/10 correct)

| Mode | Freq | Example |
|---|--:|---|
| Missing: Asset identification | 1/10 | Agent did not identify MiR100_001 |

### srn_empty_submodel_bypass (3/10 correct)

| Mode | Freq | Example |
|---|--:|---|
| Missing: ServiceRequestNotification entry in payload | 6/10 | Submodel created but empty |
| Missing: Write attempted or validation error reported | 4/10 | Agent did not attempt a write |

### Cross-case pattern

Two systemic failure modes account for the majority of wrong answers:
1. **Value invention** — the model invents ServiceType/Priority/Status values instead of using the template's controlled vocabulary. "New" instead of "Open", "Critical" instead of "High", "Emergency" instead of "CorrectiveMaintenance".
2. **Serial number resolution failure** — 4/10 `srn_serial_number` runs fail to map MIR100-2020-001 → MiR100_001.

The spatial case (`srn_spatial_hall4`) is the only one where the model performs well (9/10), because it requires only spatial resolution without value inference.

---

## 6. Duration: Median per Suite

| Suite | N | Median (correct) | Median (wrong) |
|---|--:|--:|--:|
| anti_pattern | 20 | 13.2s | — |
| asset_specs | 20 | 12.7s | — |
| bench_b | 60 | 33.0s | 18.8s |
| containment_hall4 | 50 | 29.0s | — |
| srn_autonomous | 50 | 69.1s | 98.5s |

SRN write runs are 2.4× slower than read-only runs (median 69.1s vs 29.0s). Within SRN, **wrong runs are slower than correct runs** (98.5s vs 69.1s) — the opposite pattern from `bench_b` where wrong runs are faster (18.8s vs 33.0s). This indicates that SRN wrong answers are not quick guesses but rather the result of lengthy, unsuccessful write attempts. The agent spends more time constructing incorrect submodel payloads.

### SRN per-case duration (median, wrong only — no correct runs in most cases)

| Case | N correct | Median wrong |
|---|--:|--:|
| srn_from_fault_context | 0 | 137.3s |
| srn_empty_submodel_bypass | 0* | 97.1s |
| srn_routine_priority | 0 | 86.7s |
| srn_serial_number | 1 | 72.5s |
| srn_spatial_hall4 | 9 | 69.5s |

`srn_from_fault_context` is the slowest case (137.3s median) — the agent makes extensive tool calls attempting to construct the correct ServiceRequestNotification, but consistently arrives at the wrong values.

---

## 7. Manuals-First Correlation

| | Manuals first | No manuals | Total |
|---|--:|--:|--:|
| Correct | 131 | 23 | 154 |
| Incorrect | 29 | 17 | 46 |
| **Total** | **160** | **40** | **200** |

| Metric | Manuals first | No manuals |
|---|--:|--:|
| Correctness rate | 82% (131/160) | 58% (23/40) |
| Difference | **+24pp** | |

Reading manuals first correlates with a **+24pp** correctness improvement (82% vs 58%). This is a strong positive correlation, unlike the 35b model which showed a negative correlation (−11pp). The 27b model appears to benefit consistently from reading manuals — particularly on read-only suites where it has a 99% correct rate when manuals are read first (120/121 in non-SRN suites) vs 72% when they are not (21/29).

The correlation is partly confounded by difficulty: SRN runs (where correctness is low) have a 78% manuals-first rate, while easy suites like `anti_pattern` have 75% and still achieve 100% correctness. However, even within SRN, the manuals-first group outperforms the no-manuals group (28% vs 18% correct).

---

## 8. Key Takeaways / Action Items

### T1: Write-path bypass is the dominant failure mode

92% bypass rate (46/50 SRN runs) with 78% `direct` bypass is the worst observed across all model sizes. The 27b model almost never uses `put_submodel` — it defaults to `put_submodel_element` as its primary write strategy. **Action:** Consider requiring `put_submodel` as a prerequisite before `put_submodel_element` can be called (server-side gate), or demoting `put_submodel_element` in the tool description to discourage direct use.

### T2: Value invention is systematic, not random

The model consistently invents ServiceType/Priority/Status values from its training distribution rather than the template's controlled vocabulary. "New" for Status (instead of "Open"), "Critical" for Priority (instead of "High"), and "Emergency"/"repair" for ServiceType (instead of "CorrectiveMaintenance") are the three most frequent invention patterns, appearing in 100% of `srn_from_fault_context` and `srn_routine_priority` runs. **Action:** Add value-level validation to the write tools (enum check against template vocabulary), and include the SRN vocabulary in the writing manual or system prompt.

### T3: idShort recovery is excellent but violations are frequent

48% of runs trigger at least one idShort violation, but 98% self-correct. The model reliably reads the cypher manual and rewrites the query. The remaining 2% (2 runs in `bench_b`) are cases where the agent abandons the graph query path entirely. **No immediate action needed** — the validator + manual feedback loop is working as designed.

### T4: Manuals-first reading provides a strong correctness signal

The +24pp correlation is the strongest positive signal across all evaluated models. This suggests the 27b model is more dependent on manual context for correct behavior — it lacks the internalized knowledge that larger models use as a fallback. **Action:** Consider making manuals-first the default agent behavior (inject `get_manual_page` as the first tool call in the system prompt) rather than relying on the model to choose it.

### T5: Read-only performance is strong; write-path is the bottleneck

94% read-only correctness (141/150) matches or exceeds larger models on the same suites. The 26% write-path correctness (13/50) is the primary drag on overall performance. The model can query and reason effectively but cannot construct semantically correct submodel payloads. **Action:** Focus evaluation improvements on the write path — either through better tool design (see T1), better value validation (see T2), or a dedicated write-planning step in the agent pipeline.

### T6: No template validation rejections

Zero rejections across 200 runs confirms the template validation gap is architectural, not model-specific. **Action:** Implement server-side vocabulary validation for `put_submodel` and `put_submodel_element` (see T2).
