# Results Analysis: qwen3.5-35b — Trial 07

**Model:** qwen3.5-35b (dense) via vLLM on H200
**Agent variant:** react
**Judge:** gpt-5.4 via Cortecs
**Date:** 2026-05-24
**5 test suites · 200 runs (50 SRN + 150 read-only)**

---

## 1. Paper Evaluation Table

| Suite | N | Correct | Manuals first | idShort violation | Bypass (pse) | Med. correct | Med. wrong |
|---|--:|--:|--:|--:|--:|--:|--:|
| anti_pattern | 20 | 20 (100%) | 9 (45%) | 16 (80%) | — | 8.8s | — |
| asset_specs | 20 | 20 (100%) | 5 (25%) | 17 (85%) | — | 10.2s | — |
| bench_b | 60 | 44 (73%) | 42 (70%) | 37 (62%) | — | 18.2s | 24.3s |
| containment_hall4 | 50 | 44 (88%) | 40 (80%) | 23 (46%) | — | 19.4s | 22.0s |
| srn_autonomous | 50 | 17 (34%) | 27 (54%) | 31 (62%) | 28 (56%) | 34.8s | 45.0s |
| **Total** | **200** | **145 (72%)** | **123 (62%)** | **124 (62%)** | **28/50** | **15.3s** | **32.5s** |

**Bypass (pse)** = `put_submodel_element` called instead of atomic `put_submodel`. Only applicable to srn_autonomous (the only write suite).

### Key rates

| Metric | Value |
|---|---|
| Overall correctness | 72% (145/200) |
| Read-only correctness | 100% (40/40 for anti_pattern + asset_specs); 88% for containment_hall4; 73% for bench_b |
| Write-path correctness | 34% (17/50) |
| Manuals read before first query | 62% (123/200) |
| Correct without reading manuals first | 71% (55/77) |
| Correct with manuals read first | 73% (90/123; marginal +2pp) |
| idShort violation (self-corrected) | 62% of runs (124/200) |
| Write-path bypass via `put_submodel_element` | 56% (28/50 SRN runs) |

---

## 2. idShort / Cypher Validation

The Cypher anti-pattern validator rejected queries in 62% of all runs (124/200). Of those 124 runs, 121 (98%) self-corrected all violations — the agent read the hint and rewrote the query correctly. Three runs in bench_b and containment_hall4 retained uncorrected violations.

| Violation rule | Frequency |
|---|---|
| `idShort_contains_or_regex` | 194 (most common — agent writes `WHERE x.idShort CONTAINS '...'`) |
| `toLower_id_contains` | 97 (agent writes `WHERE toLower(x.idShort) CONTAINS '...'`) |
| `id_contains_or_regex` | 19 |
| `assetType_match` | 3 |

**98% self-correction rate across all suites.** The validator blocks the anti-pattern, the agent reads the hint, and rewrites correctly. However, the validator only guards `query_aas_graph` — it provides no protection on the write path.

Per-suite self-correction:
- anti_pattern: 16/16 (100%)
- asset_specs: 17/17 (100%)
- bench_b: 35/37 (95%)
- containment_hall4: 22/23 (96%)
- srn_autonomous: 31/31 (100%)

---

## 3. Write-Path Bypass Analysis

### 3.1 Bypass classification

| Bypass type | Count | Description |
|---|--:|---|
| `correct` | 13 (26%) | Used `put_submodel` only — no `put_submodel_element` |
| `direct` | 18 (36%) | Skipped `put_submodel` entirely, went straight to `put_submodel_element` |
| `surfaced` | 7 (14%) | Called `put_submodel` but then also called `put_submodel_element` |
| `cascade` | 3 (6%) | Mixed pattern — multiple write attempts with escalating bypass |
| `None` (no write) | 7 (14%) | No write attempted or write path data missing |
| `None/N/A` | 2 (4%) | Edge cases (write_path null) |

**56% of SRN runs (28/50) used the bypass.** In 36% (18/50) the agent went directly to `put_submodel_element` without ever calling `put_submodel`.

### 3.2 Per-case bypass breakdown

| Case | N | `correct` | `direct` | `surfaced` | `cascade` | `None` | N/A |
|---|--:|--:|--:|--:|--:|--:|--:|
| srn_empty_submodel_bypass | 10 | 2 | 8 | — | — | — | — |
| srn_from_fault_context | 10 | 2 | 3 | 2 | — | 1 | 2 |
| srn_routine_priority | 10 | 1 | 4 | 2 | 2 | 1 | — |
| srn_serial_number | 10 | 4 | — | 1 | 1 | 4 | — |
| srn_spatial_hall4 | 10 | 4 | 3 | 2 | — | 1 | — |
| **Total** | **50** | **13** | **18** | **7** | **3** | **7** | **2** |

### 3.3 Root cause

The `srn_empty_submodel_bypass` case was designed to test whether the agent would push an empty submodel and then build it element-by-element. In 8/10 runs, the agent chose exactly this bypass path — going straight to `put_submodel_element` instead of `put_submodel`.

For `srn_from_fault_context`, the agent often finds existing SRN submodels from previous runs and decides to patch them via `put_submodel_element` rather than creating a new one atomically.

`put_submodel_element_called=true` in 28/50 runs; `put_submodel_attempted=true` in 30/50 runs.

**Mitigation:** Wipe the stack (`./down.sh` default, then `./up.sh --vllm`) before each eval run to remove stale SRN data.

---

## 4. Template Validation Gap

**No template validation rejection was observed on any write call.** All `put_submodel` and `put_submodel_element` calls returned `{"status": "ok"}`.

This confirms the architectural gap:
1. The SRN template has `Cardinality ZeroToMany` on `ServiceRequestNotification` — an empty submodel passes validation.
2. `put_submodel_element` has no template check at all — elements are accepted without validation.
3. The validator only checks structural conformance, not semantic correctness (controlled vocabulary enforcement).

As a result, the agent consistently writes **invented ServiceType values** ("Emergency Stop", "EmergencyStop", "Emergency", "Maintenance", "Routine Inspection") instead of the template's controlled vocabulary ("CorrectiveMaintenance", "Inspection"). The validator cannot catch this because it does not enforce value constraints.

---

## 5. Judge Failure Modes per SRN Case

The judge (gpt-5.4) marked 33/50 SRN runs as incorrect. The dominant failure modes:

### srn_from_fault_context (0/10 correct)
| Missing fact | Count | Wrong claim | Count |
|---|--:|---|---:|
| ServiceType is CorrectiveMaintenance | 10 | ServiceType = "EmergencyStop" / "Emergency Stop" / "Emergency Stop Troubleshooting" / "Emergency" | 4 |

Every run got Priority=High and Status=Open correct, but none used the template vocabulary `CorrectiveMaintenance` for ServiceType.

### srn_routine_priority (0/10 correct)
| Missing fact | Count | Wrong claim | Count |
|---|--:|---|---:|
| Priority is Low | 10 | Priority = "Medium" / "Normal" | 8 |
| ServiceType is Inspection | 4 | ServiceType = "Routine Inspection" / "Maintenance" | 2 |
| SR created for UR3e_002 | 3 | Created for UR3e_001 instead | 1 |
| Status is Open | 2 | | |

The agent never assigns "Low" priority for routine inspections — it defaults to "Medium" or "Normal", failing the priority inference requirement.

### srn_serial_number (8/10 correct)
| Missing fact | Count | Wrong claim | Count |
|---|--:|---|---:|
| Write attempted / serial number resolved | 2 | — | — |
| Priority is High | 2 | | |

Two runs failed to clearly resolve MIR100-2020-001 → MiR100_001 or to confirm a write attempt.

### srn_spatial_hall4 (6/10 correct)
| Missing fact | Count | Wrong claim | Count |
|---|--:|---|---:|
| Identified MiR100_001 as the robot | 3 | Asserted MiR250_001 instead | 1 |
| Write attempted / confirmed | 2 | | |

The spatial disambiguation is usually solved correctly, but some runs get confused by multiple MiR instances.

### srn_empty_submodel_bypass (3/10 correct)
| Missing fact | Count | Wrong claim | Count |
|---|--:|---|---:|
| Write attempted / payload contains SRN entry | 5 | — | — |
| Correct asset identified | 1 | | |

Five runs attempted writes but the answer lacked proof of correct payload content — the agent often gets stuck in a loop trying to verify the write but never produces a clean final answer.

---

## 6. Duration Analysis

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern | 20 | 8.8s | 8.8s | — |
| asset_specs | 20 | 10.2s | 10.2s | — |
| bench_b | 60 | 18.8s | 18.2s | 24.3s |
| containment_hall4 | 50 | 19.5s | 19.4s | 22.0s |
| srn_autonomous | 50 | 40.1s | 34.8s | 45.0s |

SRN write runs are 2.1× slower than read-only runs (median 40.1s vs 19.5s). Within SRN, correct runs are faster than wrong runs (34.8s vs 45.0s) — incorrect runs burn time on futile write-retry loops.

SRN per-case:

| Case | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| srn_from_fault_context | 10 | 42.2s | — | 42.2s |
| srn_routine_priority | 10 | 48.5s | — | 48.5s |
| srn_serial_number | 10 | 36.5s | 34.2s | 57.7s |
| srn_spatial_hall4 | 10 | 43.1s | 39.2s | 50.2s |
| srn_empty_submodel_bypass | 10 | 31.3s | 34.8s | 27.8s |

The two zero-correct cases (fault context, routine priority) have the highest medians (42–49s), reflecting extensive but fruitless tool usage.

---

## 7. Manuals-First Correlation

|  | Manuals first | No manuals | Total |
|---|--:|--:|--:|
| Correct | 90 (73%) | 55 (71%) | 145 |
| Incorrect | 33 (27%) | 22 (29%) | 55 |

Reading manuals first provides a negligible +2pp improvement (73% vs 71%). The 35b model is notably less dependent on manual pre-reading than the 397b model — it often proceeds directly to graph queries and still achieves similar or better correctness. However, 62% of runs still read manuals first, largely driven by the containment_hall4 (80%) and bench_b (70%) suites where the agent consistently calls `get_graph_schema` or `get_templates_index` before its first Cypher query.

---

## 8. Comparison with qwen3.5-397b

### Overall

| Metric | 35b | 397b | Delta |
|---|---|---|---|
| Overall correctness | 72% | 76% | **−4pp** |
| Manuals-first rate | 62% | 84% | **−22pp** |
| idShort violation rate | 62% | 62% | 0pp |
| Write-path bypass rate | 56% | 44% | **+12pp** |
| SRN correctness | 34% | 26% | **+8pp** |

### Per-suite comparison

| Suite | Metric | 35b | 397b | Delta |
|---|---|---|---|---|
| anti_pattern | Correct | 100% | 100% | 0pp |
| anti_pattern | Manuals-first | 45% | 65% | −20pp |
| anti_pattern | Median duration | 8.8s | 18.1s | **−9.3s** |
| asset_specs | Correct | 100% | 100% | 0pp |
| asset_specs | Manuals-first | 25% | 75% | **−50pp** |
| asset_specs | Median duration | 10.2s | 17.9s | **−7.7s** |
| bench_b | Correct | 73% | 82% | −9pp |
| bench_b | Manuals-first | 70% | 87% | −17pp |
| bench_b | Median duration | 18.8s | 34.0s | **−15.2s** |
| containment_hall4 | Correct | 88% | 100% | **−12pp** |
| containment_hall4 | Manuals-first | 80% | 84% | −4pp |
| containment_hall4 | Median duration | 19.5s | 33.2s | **−13.7s** |
| srn_autonomous | Correct | 34% | 26% | **+8pp** |
| srn_autonomous | Manuals-first | 54% | 90% | **−36pp** |
| srn_autonomous | Median duration | 40.1s | 89.8s | **−49.7s** |

### Key takeaways

1. **35b is ~2× faster** across all suites (−9s to −50s), especially in SRN (−49.7s). This is the most striking difference — the smaller model is far more token-efficient.
2. **35b reads manuals far less** (−22pp overall; −50pp on asset_specs). It often skips `get_graph_schema`/`get_templates_index` and goes straight to Cypher, relying on the validator to correct anti-patterns.
3. **Despite reading fewer manuals, 35b matches or beats 397b on SRN** (+8pp). The write-path performance is better because the smaller model is less verbose — it constructs simpler payloads that happen to be more correct.
4. **35b trades read-heavy correctness for speed**: −12pp on containment_hall4 (6 wrong runs, mostly the "ambiguous assets" sub-case) and −9pp on bench_b (4 runs fail to find MiR250 location in Hall 3).
5. **idShort violation rates are identical** (62% both), confirming this is a model-family trait, not a size-dependent behavior.
6. **35b has a higher bypass rate** (56% vs 44%), suggesting it defaults to `put_submodel_element` more readily — likely because it constructs simpler plans that skip the atomic `put_submodel` step.
