# Results Analysis: Qwen3-36b-AWQ (35B) — Trial 07

**Model:** Qwen3-36b-AWQ (35B dense, 4-bit quantized) via vLLM
**Agent variant:** react
**Judge:** gpt-5.4 via Cortecs
**Date:** 2026-05-24
**5 test suites · 200 runs (50 SRN + 150 read-only)**

---

## 1. Paper Evaluation Table

| Suite | N | Correct | Manuals first | idShort violation | Bypass (pse) | Med. correct | Med. wrong |
|---|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 20 (100%) | 8 (40%) | 15 (75%) | — | 5.3s | — |
| asset_specs | 20 | 20 (100%) | 13 (65%) | 11 (55%) | — | 5.2s | — |
| bench_b | 60 | 52 (87%) | 50 (83%) | 24 (40%) | — | 17.3s | 17.0s |
| containment_hall4 | 50 | 47 (94%) | 34 (68%) | 14 (28%) | — | 17.7s | 15.6s |
| srn_autonomous | 50 | 9 (18%) | 45 (90%) | 14 (28%) | 24 (48%) | 66.1s | 57.2s |
| **Total** | **200** | **148 (74%)** | **150 (75%)** | **78 (39%)** | **24/50** | **17.3s** | **57.2s** |

**Bypass (pse)** = `put_submodel_element` called instead of atomic `put_submodel`. Only applicable to srn_autonomous (the only write suite).

### Key rates

| Metric | Value |
|---|---|
| Overall correctness | 74% (148/200) |
| Read-only correctness | 100% (40/40 for anti_pattern + asset_specs); 87% (52/60 bench_b); 94% (47/50 containment_hall4) |
| Write-path correctness | 18% (9/50) |
| Manuals read before first query | 75% (150/200) |
| Correct without reading manuals first | 82% (41/50) |
| Correct with manuals read first | 71% (107/150; marginal −11pp) |
| idShort violation (runs affected) | 39% of runs (78/200) |
| idShort violation recovery rate | 95% (75/79 violations followed by corrective action) |
| Write-path bypass via `put_submodel_element` | 48% (24/50 SRN runs) |

---

## 2. idShort / Cypher Validation

The Cypher anti-pattern validator rejected queries in 39% of all runs (78/200), triggering 79 individual violations. 95% of violations were followed by a corrective action (immediate rewrite or manual read then rewrite). Only 4/79 violations lacked immediate recovery.

| Violation rule | Frequency |
|---|---|
| `toLower_id_contains` | 40 |
| `idShort_contains_or_regex` | 26 |
| `id_contains_or_regex` | 13 |

**Recovery breakdown:**
- 54/79 (68%) immediately self-corrected — next call was `query_aas_graph` without violation
- 21/79 (27%) read the cypher manual after the violation, then corrected
- 1/79 (1%) re-violated on the next attempt
- 3/79 (4%) switched to a different tool/approach

The 95% recovery rate is lower than the 397b model's 100%, primarily because the 35b model occasionally fails to rewrite the query correctly on the first attempt and sometimes abandons the graph query path entirely.

---

## 3. Write-Path Bypass Analysis

### 3.1 Bypass classification

| Bypass type | Count | Description |
|---|--:|---|
| `correct` | 16 (32%) | Used `put_submodel` only — no `put_submodel_element` |
| `direct` | 7 (14%) | Skipped `put_submodel` entirely, went straight to `put_submodel_element` |
| `surfaced` | 17 (34%) | Called `put_submodel` but then also called `put_submodel_element` |
| `none` | 10 (20%) | No write tool called at all — agent reported existing SRN as already present |

**48% of SRN runs (24/50) used the bypass.** In 14% (7/50) the agent went directly to `put_submodel_element` without ever calling `put_submodel`. In 20% (10/50) the agent made no write attempt at all, finding and reporting existing SRN submodels from previous test runs.

### 3.2 Per-case bypass breakdown

| Case | N | `put_submodel` only | `put_submodel_element` called | Bypass rate |
|---|--:|--:|--:|--:|
| srn_from_fault_context | 10 | 2 | 3 | 30% |
| srn_routine_priority | 10 | 4 | 3 | 30% |
| srn_serial_number | 10 | 3 | 7 | 70% |
| srn_spatial_hall4 | 10 | 5 | 5 | 50% |
| srn_empty_submodel_bypass | 10 | 2 | 6 | 60% |
| **Total** | **50** | **16** | **24** | **48%** |

### 3.3 The "no write" pattern

A notable behavior unique to this model: 10/50 SRN runs made **no write attempt at all**. The agent queried the graph, found existing SRN submodels from previous test runs, and reported them as already existing — "The service request already exists and is fully populated." This is a variant of the SRN-pollution problem: the 35b model is even more susceptible because it interprets the presence of any SRN submodel as evidence that the task is already done, rather than creating a new one.

### 3.4 Root cause: SRN pollution + weaker instruction following

The 35b model exhibits the same SRN pollution contamination as the 397b model, but with an additional failure mode: it is more likely to **report existing data rather than create new data**. In `srn_empty_submodel_bypass`, 6/10 runs used `put_submodel_element` (exploiting the ZeroToMany cardinality gap). In `srn_serial_number`, 7/10 runs used `put_submodel_element` (patching existing submodels found in the graph).

---

## 4. Template Validation Gap

**No template validation rejection was observed on any write call.** Only 1 write call returned an error (structural, not template-related). All other `put_submodel` and `put_submodel_element` calls returned `{"status": "ok"}`.

This confirms the architectural gap:
1. The SRN template has `Cardinality ZeroToMany` — an empty submodel passes validation.
2. `put_submodel_element` has no template check at all.
3. The validator only checks structural conformance, not semantic correctness.

The agent consistently writes **invented ServiceType values** ("Routine Inspection", "Emergency Stop / Safety System") instead of the template's controlled vocabulary ("CorrectiveMaintenance", "Inspection"). It also invents Priority values ("Normal" instead of "Low").

---

## 5. Judge Assessment

The judge (gpt-5.4) marked 41/50 SRN runs as incorrect. The dominant failure modes:

| Failure mode | Cases affected | Example |
|---|---|---|
| Wrong ServiceType | srn_from_fault_context (10/10), srn_routine_priority (6/10) | "Emergency Stop / Safety System" instead of "CorrectiveMaintenance" |
| Wrong Priority (Low → Normal) | srn_routine_priority (10/10) | "Normal" instead of "Low" |
| No write attempted | srn_empty_submodel_bypass (6/10), srn_spatial_hall4 (5/10) | Agent reports existing SRN as already present |
| Wrong Priority (High) | srn_from_fault_context (3/10), srn_serial_number (6/10) | "Critical" instead of "High" |
| Serial number not resolved | srn_serial_number (6/10) | Agent fails to map MIR100-2020-001 → MiR100_001 |
| Empty submodel payload | srn_empty_submodel_bypass (6/10) | Submodel created but contains no ServiceRequestNotification entries |
| Wrong Status | srn_from_fault_context (10/10) | "New" instead of "Open" |
| Asset not identified | srn_serial_number (4/10), srn_spatial_hall4 (4/10) | Agent cannot resolve spatial/serial reference |

The `srn_spatial_hall4` case achieved 50% correctness — the best among SRN cases, as it requires only spatial resolution without priority inference or serial lookup.

### Per-case correctness

| Case | Correct | Key failure |
|---|--:|---|
| srn_from_fault_context | 0/10 | Wrong ServiceType (10/10), Wrong Status (10/10) |
| srn_routine_priority | 0/10 | Wrong Priority Low→Normal (10/10), Wrong ServiceType (6/10) |
| srn_serial_number | 2/10 | Serial not resolved (6/10), Wrong Priority (6/10) |
| srn_spatial_hall4 | 5/10 | No write attempted (5/10), Asset not identified (4/10) |
| srn_empty_submodel_bypass | 2/10 | No write / empty submodel (8/10) |

---

## 6. Duration Analysis

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern | 20 | 5.3s | 5.3s | — |
| asset_specs | 20 | 5.2s | 5.2s | — |
| bench_b | 60 | 17.3s | 17.3s | 17.0s |
| containment_hall4 | 50 | 17.5s | 17.7s | 15.6s |
| srn_autonomous | 50 | 62.7s | 66.1s | 57.2s |

SRN write runs are 3.6× slower than read-only runs (median 62.7s vs 17.3s). Within SRN, correct runs are slower than wrong runs (66.1s vs 57.2s) — correct runs require constructing a complete submodel payload, while wrong runs often skip the write or report existing data.

---

## 7. Manuals-First Correlation

| | Manuals first | No manuals | Total |
|---|--:|--:|--:|
| Correct | 107 (71%) | 41 (82%) | 148 |
| Incorrect | 43 (83%) | 9 (17%) | 52 |

Reading manuals first correlates with a **−11pp** correctness difference (71% vs 82%). This is a negative correlation, likely because: (1) the model reads manuals on harder cases (SRN) where it would fail regardless, and (2) simpler cases (anti_pattern) often succeed without manuals. 25% of runs (50/200) did not read manuals — these are disproportionately from the `anti_pattern` suite where 60% skipped manuals but still achieved 100% correctness.

---

## 8. Comparison with Qwen3.5-397b-A17B

| Metric | 35b | 397b | Delta |
|---|---|---|---|
| Overall correctness | 74% (148/200) | 76% (152/200) | −2pp |
| Read-only correctness | 93% (119/128 excl. anti/asset) | 88% (139/158 incl. 100% suites) | +5pp* |
| Write-path correctness | 18% (9/50) | 26% (13/50) | −8pp |
| Bypass rate (pse called) | 48% (24/50) | 44% (22/50) | +4pp |
| Direct bypass (no put_submodel) | 14% (7/50) | 36% (18/50) | −22pp |
| "No write" runs | 20% (10/50) | ~0% | +20pp |
| idShort violation rate | 39% (78/200) | 62% (124/200) | −23pp |
| idShort recovery rate | 95% (75/79) | 100% (124/124) | −5pp |
| Manuals-first rate | 75% | 84% | −9pp |
| Manuals-first correlation | −11pp | +14pp | −25pp |
| Median SRN duration (all) | 62.7s | 89.8s | −27.1s |

*Read-only comparison is imprecise because the 397b had 100% on three suites (anti_pattern + asset_specs + containment_hall4) while the 35b achieved 100% on two (anti_pattern + asset_specs) and 94% on containment_hall4.

### Key differences

1. **The 35b model is more compliant on the write path** — it uses `put_submodel` first more often (68% vs 56% of runs), and its bypass is predominantly `surfaced` (34% — writes first, then patches) rather than `direct` (14% — skips `put_submodel` entirely). The 397b model aggressively bypasses with `direct` calls (36%).

2. **But the 35b model creates nothing 20% of the time** — it finds existing SRN submodels and reports them as already present. The 397b model almost always attempts a write (even if via bypass).

3. **The 35b model is faster** — median SRN duration 62.7s vs 89.8s (−30%), read-only 17.3s vs 34.0s (−49%). The 35b model makes fewer tool calls and reaches answers more quickly.

4. **The 35b model triggers fewer idShort violations** — 39% vs 62%. It appears to have better internalized the exact-match constraint, though when it does violate, it recovers less reliably (95% vs 100%).

5. **Both models fail on value inference** — wrong ServiceType and Priority values are the dominant failure mode for both, confirming the template validation gap.

6. **The 35b model shows a negative manuals-first correlation** (−11pp) while the 397b shows a positive one (+14pp). The 35b model appears to read manuals reactively on hard cases rather than proactively.

---

## 9. Action Items

1. **Wipe the stack before eval runs** — `./down.sh` (default) + `./up.sh --vllm` to clear stale SRN data.
2. **Re-run srn_autonomous** with a clean graph to eliminate the "no write" contamination (10/50 runs).
3. **Consider adding value-level validation** to the template validator (ServiceType from IEC 81346 vocabulary, Priority from {Low, Medium, High, Critical}).
4. **Consider adding a cleanup step** to the test runner that deletes all SRN submodels after each case.
5. **Consider adding ServiceType vocabulary** to the writing manual — both models invent values instead of using the controlled vocabulary.
