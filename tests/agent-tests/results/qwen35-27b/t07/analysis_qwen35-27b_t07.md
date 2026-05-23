# Results analysis: qwen35-27b

Generated: 2026-05-23 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 0 (0%) | 20 (100%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 19 (95%) | 1 (5%) | 0 (0%) | 20 (100%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 42 (70%) | 18 (30%) | 47 (78%) | 36 (60%) | 19 (32%) |
| containment_hall4_N10_T07 | 50 | 48 (96%) | 2 (4%) | 40 (80%) | 20 (40%) | 27 (54%) |
| srn_ablation_variant_a_N10_T07 | 30 | 29 (97%) | 1 (3%) | 3 (10%) | 19 (63%) | 0 (0%) |
| srn_autonomous_N10_T07 | 30 | 20 (67%) | 10 (33%) | 6 (20%) | 19 (63%) | 0 (0%) |
| srn_bypass_N10_T07 | 20 | 19 (95%) | 1 (5%) | 3 (15%) | 15 (75%) | 1 (5%) |
| **Total** | **230** | **197 (86%)** | **33 (14%)** | **99 (43%)** | **149 (65%)** | **47 (20%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 83 (42%) | 114 (58%) | 197 |
| **correct=False** | 16 (48%) | 17 (52%) | 33 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 124 (63%) | 73 (37%) | 197 |
| **correct=False** | 25 (76%) | 8 (24%) | 33 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 11.3s | 11.3s | – |
| asset_specs_N10_T07 | 20 | 9.8s | 9.8s | 9.4s |
| bench_b_N10_T07 | 60 | 25.2s | 24.8s | 25.4s |
| containment_hall4_N10_T07 | 50 | 24.8s | 24.3s | 36.0s |
| srn_ablation_variant_a_N10_T07 | 30 | 17.1s | 16.8s | 31.0s |
| srn_autonomous_N10_T07 | 30 | 15.4s | 9.4s | 30.9s |
| srn_bypass_N10_T07 | 20 | 15.4s | 15.1s | 31.9s |
