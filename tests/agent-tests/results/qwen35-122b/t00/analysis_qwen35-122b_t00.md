# Results analysis: qwen35-122b

Generated: 2026-05-22 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T00 | 20 | 0 (0%) | 20 (100%) | 0 (0%) | 0 (0%) | 0 (0%) |
| asset_specs_N10_T00 | 20 | 0 (0%) | 20 (100%) | 0 (0%) | 0 (0%) | 0 (0%) |
| bench_b_N10_T00 | 60 | 34 (57%) | 26 (43%) | 59 (98%) | 30 (50%) | 20 (33%) |
| containment_hall4_N10_T00 | 50 | 31 (62%) | 19 (38%) | 41 (82%) | 31 (62%) | 0 (0%) |
| srn_ablation_variant_a_N10_T00 | 30 | 0 (0%) | 30 (100%) | 0 (0%) | 0 (0%) | 0 (0%) |
| srn_autonomous_N10_T00 | 30 | 0 (0%) | 30 (100%) | 0 (0%) | 0 (0%) | 0 (0%) |
| srn_bypass_N10_T00 | 20 | 0 (0%) | 20 (100%) | 0 (0%) | 0 (0%) | 0 (0%) |
| **Total** | **230** | **65 (28%)** | **165 (72%)** | **100 (43%)** | **61 (27%)** | **20 (9%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 65 (100%) | 0 (0%) | 65 |
| **correct=False** | 35 (21%) | 130 (79%) | 165 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 45 (69%) | 20 (31%) | 65 |
| **correct=False** | 16 (10%) | 149 (90%) | 165 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T00 | 20 | 1.8s | – | 1.8s |
| asset_specs_N10_T00 | 20 | 42.2s | – | 42.2s |
| bench_b_N10_T00 | 60 | 28.1s | 20.8s | 90.0s |
| containment_hall4_N10_T00 | 50 | 30.2s | 30.2s | 52.5s |
| srn_ablation_variant_a_N10_T00 | 30 | 1.3s | – | 1.3s |
| srn_autonomous_N10_T00 | 30 | 1.3s | – | 1.3s |
| srn_bypass_N10_T00 | 20 | 41.3s | – | 41.3s |
