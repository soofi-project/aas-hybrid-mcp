# Results Analysis: qwen3.5-122b — Trial 07

**Model:** qwen3.5-122b (MoE, ~10B active) via vLLM on H200
**Agent variant:** react
**Judge:** gpt-5.4 via Cortecs
**Date:** 2026-05-24
**5 test suites · 200 runs (50 SRN + 150 read-only)**

---

## 1. Paper Evaluation Table

| Suite | N | Correct | Manuals first | idShort violation | Bypass (pse) | Med. correct | Med. wrong |
|---|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 20 (100%) | 4 (20%) | 20 (100%) | — | 19.0s | — |
| asset_specs | 20 | 20 (100%) | 7 (35%) | 20 (100%) | — | 18.1s | — |
| bench_b | 60 | 43 (72%) | 46 (77%) | 49 (82%) | — | 29.3s | 34.3s |
| containment_hall4 | 50 | 46 (92%) | 47 (94%) | 24 (48%) | — | 24.2s | 23.6s |
| srn_autonomous | 50 | 11 (22%) | 26 (52%) | 45 (90%) | 2 (4%) | 63.7s | 68.6s |
| **Total** | **200** | **140 (70%)** | **130 (65%)** | **158/200 (79%)** | **2/50** | **23.7s** | **58.1s** |

**Bypass (pse)** = `put_submodel_element` called instead of atomic `put_submodel`. Only applicable to srn_autonomous.

### Key rates

| Metric | Value |
|---|---|
| Overall correctness | 70% (140/200) |
| Read-only correctness (anti+asset+containment) | 98% (86/90) |
| Write-path correctness | 22% (11/50) |
| Manuals read before first query | 65% (130/200) |
| Correct without reading manuals first | 63% (44/70) |
| Correct with manuals read first | 74% (96/130; marginal +11pp) |
| idShort violation rate | 79% of runs (158/200) |
| idShort self-correction rate | 98% (177/181) |
| Write-path bypass via `put_submodel_element` | 4% (2/50 SRN runs) |

---

## 2. idShort / Cypher Validation

The Cypher anti-pattern validator rejected queries in 79% of all runs (158/200) — higher than the 397b model (62%). This model triggers more violations per run, especially in the SRN suite (90% of runs).

| Violation rule | Frequency |
|---|---|
| `idShort_contains_or_regex` | 100 |
| `toLower_id_contains` | 50 |
| `id_contains_or_regex` | 27 |
| `assetType_match` | 9 |

**Self-correction rate: 98% (177/181).** The `self_corrected` field was not populated in the judged JSON for this model, but tracing the tool-call sequence shows the agent successfully rewrites the query after rejection in 98% of cases. The 3 uncorrected violations occurred in `containment_hall4` where the agent abandoned the query path.

The 122b model triggers more violations than the 397b (79% vs 62%) and reads manuals far less often before querying (65% vs 84%). These are correlated: the 122b model is more likely to attempt a query without reading the cypher manual first, trigger the validator, and then self-correct.

---

## 3. Write-Path Bypass Analysis

### 3.1 Bypass classification

| Bypass type | Count | Description |
|---|--:|---|
| `correct` | 29 (58%) | Used `put_submodel` only — no `put_submodel_element` |
| `surfaced` | 17 (34%) | Called `put_submodel` but then also called `put_submodel_element` |
| `direct` | 2 (4%) | Skipped `put_submodel`, went straight to `put_submodel_element` |
| `N/A` | 2 (4%) | Edge cases |

**Only 4% of SRN runs (2/50) used the direct bypass** — dramatically lower than the 397b model's 44%. The 122b model strongly prefers `put_submodel` as the primary write tool. However, 34% of runs are classified as `surfaced` — the agent calls `put_submodel` first, then supplements with `put_submodel_element` to add missing fields.

### 3.2 Per-case bypass breakdown

| Case | N | `put_submodel` only | `put_submodel_element` called | Bypass rate |
|---|--:|--:|--:|--:|
| srn_from_fault_context | 10 | 9 | 0 | **0%** |
| srn_routine_priority | 10 | 5 | 0 | 0% |
| srn_serial_number | 10 | 5 | 0 | 0% |
| srn_spatial_hall4 | 10 | 6 | 1 | 10% |
| srn_empty_submodel_bypass | 10 | 4 | 1 | 10% |
| **Total** | **50** | **29** | **2** | **4%** |

### 3.3 Comparison: 122b vs 397b bypass behavior

| Metric | 122b | 397b |
|---|--:|--:|
| Direct bypass (`put_submodel_element` only) | 4% (2/50) | 36% (18/50) |
| Any `put_submodel_element` called | 4% (2/50) | 44% (22/50) |
| `put_submodel` attempted | 92% (46/50) | 62% (31/50) |
| `put_submodel` only (correct) | 58% (29/50) | 40% (20/50) |

The 122b model is significantly more compliant with the write protocol. The 397b model was heavily influenced by SRN pollution in the graph (seeing existing submodels and patching them). The 122b model consistently creates new submodels via `put_submodel` even when existing ones are present.

### 3.4 SRN pollution impact

Despite the low bypass rate, the 122b model still suffers from stale SRN data. The `surfaced` category (34%) shows the agent creating a submodel via `put_submodel` and then patching it with `put_submodel_element` — likely because the initial `put_submodel` payload was incomplete (missing mandatory fields).

---

## 4. Template Validation Gap

Same as the 397b model: **no template validation rejection was observed on any write call.** All `put_submodel` and `put_submodel_element` calls returned `{"status": "ok"}`.

The 122b model writes incorrect ServiceType values even more consistently than the 397b:

| Case | Wrong ServiceType | Count |
|---|---|---|
| srn_from_fault_context | "Emergency" instead of "CorrectiveMaintenance" | 7/10 |
| srn_from_fault_context | "Maintenance" instead of "CorrectiveMaintenance" | 1/10 |
| srn_routine_priority | "Normal" instead of "Low" priority | 7/10 |

The validator cannot catch these because it only checks structural conformance, not value constraints.

---

## 5. Judge Assessment

The judge marked 39/50 SRN runs as incorrect (78% failure rate). The dominant failure modes:

| Failure mode | Cases affected | Example |
|---|---|---|
| Wrong ServiceType | srn_from_fault_context (10/10) | "Emergency" instead of "CorrectiveMaintenance" |
| Wrong Priority | srn_routine_priority (10/10) | "Normal" instead of "Low" |
| Serial number not resolved | srn_serial_number (10/10) | Agent cannot map MIR100-2020-001 → MiR100_001 |
| Missing write confirmation | srn_empty_submodel_bypass (6/10) | Agent claims success but judge requires payload proof |
| Robot not identified | srn_spatial_hall4 (3/10) | Agent fails to identify MiR100_001 |

**Notable:** `srn_from_fault_context` and `srn_routine_priority` both scored 0/10 — worse than the 397b model (2/10 and 0/10). The 122b model never writes "CorrectiveMaintenance" as a ServiceType, always preferring "Emergency" or "Maintenance".

The `srn_serial_number` case also scored 0/10 — the 122b model consistently fails to resolve serial numbers to AAS IDs.

---

## 6. Duration Analysis

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern | 20 | 19.0s | 19.0s | — |
| asset_specs | 20 | 18.1s | 18.1s | — |
| bench_b | 60 | 31.0s | 29.3s | 34.3s |
| containment_hall4 | 50 | 24.2s | 24.2s | 23.6s |
| srn_autonomous | 50 | 67.5s | 63.7s | 68.6s |

The 122b model is faster than the 397b across all suites (23.7s vs 29.1s overall median). This is expected: the 122b has ~10B active parameters vs ~17B for the 397b. Within SRN, correct and wrong runs have similar latency (~65s), unlike the 397b where correct runs were slower (94s vs 66s).

### Comparison: 122b vs 397b median duration

| Suite | 122b | 397b | Delta |
|---|--:|--:|--:|
| anti_pattern | 19.0s | 18.1s | +0.9s |
| asset_specs | 18.1s | 17.9s | +0.2s |
| bench_b | 31.0s | 34.0s | −3.0s |
| containment_hall4 | 24.2s | 33.2s | −9.0s |
| srn_autonomous | 67.5s | 89.8s | −22.3s |

The 122b is significantly faster on write tasks (−22s) and containment queries (−9s).

---

## 7. Manuals-First Correlation

| | Manuals first | No manuals | Total |
|---|--:|--:|--:|
| Correct | 96 (74%) | 44 (63%) | 140 |
| Incorrect | 34 (49%) | 26 (37%) | 60 |

Reading manuals first correlates with a +11pp correctness improvement (74% vs 63%). The 122b model reads manuals far less often than the 397b (65% vs 84%), particularly in the simpler suites (anti_pattern: 20% vs 65%, asset_specs: 35% vs 75%). This suggests the smaller model relies more on pattern-matching from training data than on reading the manual.

In the SRN suite specifically, manuals-first has negligible impact (23% vs 21% correctness) — the write-path failures are dominated by wrong ServiceType values, which the manuals do not address (the cypher manual teaches query patterns, not vocabulary constraints).

---

## 8. Model Comparison Summary: 122b vs 397b

| Metric | 122b | 397b | Winner |
|---|--:|--:|---|
| Overall correctness | 70% | 76% | 397b (+6pp) |
| Read-only correctness | 98% | 100% | 397b |
| Write-path correctness | 22% | 26% | 397b (+4pp) |
| Manuals-first rate | 65% | 84% | 397b |
| idShort violation rate | 79% | 62% | 397b (fewer violations) |
| idShort self-correction | 98% | 100% | 397b |
| Bypass rate (pse) | 4% | 44% | **122b** (far more compliant) |
| Median latency | 23.7s | 29.1s | **122b** (faster) |
| SRN median latency | 67.5s | 89.8s | **122b** (−22s) |

**Key finding:** The 122b model is substantially more compliant with the write protocol (4% bypass vs 44%) but less correct overall (22% vs 26% on SRN). The lower bypass rate likely reflects less sophisticated reasoning — the 122b follows the `put_submodel` pattern more rigidly rather than adapting to existing graph state. The 397b model "notices" existing SRN submodels and patches them (bypass), while the 122b model consistently creates new ones regardless.

---

## 9. Action Items

1. **Wipe the stack before eval runs** — same recommendation as for 397b.
2. **Add ServiceType vocabulary to the writing manual** — both models invent ServiceType values because the template does not enumerate allowed values and the manual does not specify them.
3. **Consider adding value-level validation** — same as 397b recommendation.
4. **Serial number resolution** — the 122b model fails 100% on `srn_serial_number`. The agent needs a lookup path (Nameplate → SerialNumber → match) that neither model discovers reliably.
