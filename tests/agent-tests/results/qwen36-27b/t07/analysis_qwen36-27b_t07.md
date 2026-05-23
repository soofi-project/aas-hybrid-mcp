# Results analysis: qwen36-27b

Generated: 2026-05-23 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 11 (55%) | 19 (95%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 11 (55%) | 19 (95%) | 1 (5%) |
| bench_b_N10_T07 | 60 | 48 (80%) | 12 (20%) | 55 (92%) | 20 (33%) | 39 (65%) |
| containment_hall4_N10_T07 | 50 | 48 (96%) | 2 (4%) | 40 (80%) | 14 (28%) | 34 (68%) |
| srn_ablation_variant_a_N10_T07 | 30 | 27 (90%) | 3 (10%) | 18 (60%) | 9 (30%) | 9 (30%) |
| srn_autonomous_N10_T07 | 30 | 19 (63%) | 11 (37%) | 17 (57%) | 5 (17%) | 5 (17%) |
| srn_bypass_N10_T07 | 20 | 14 (70%) | 6 (30%) | 9 (45%) | 6 (30%) | 7 (35%) |
| **Total** | **230** | **196 (85%)** | **34 (15%)** | **161 (70%)** | **92 (40%)** | **95 (41%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 138 (70%) | 58 (30%) | 196 |
| **correct=False** | 23 (68%) | 11 (32%) | 34 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 78 (40%) | 118 (60%) | 196 |
| **correct=False** | 14 (41%) | 20 (59%) | 34 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 12.2s | 12.2s | – |
| asset_specs_N10_T07 | 20 | 12.3s | 12.3s | – |
| bench_b_N10_T07 | 60 | 24.7s | 26.5s | 21.2s |
| containment_hall4_N10_T07 | 50 | 25.3s | 24.6s | 36.2s |
| srn_ablation_variant_a_N10_T07 | 30 | 14.0s | 12.9s | 32.6s |
| srn_autonomous_N10_T07 | 30 | 13.3s | 7.7s | 27.6s |
| srn_bypass_N10_T07 | 20 | 13.5s | 14.5s | 12.9s |
