# Results analysis: qwen35-4b

Generated: 2026-05-22 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 16 (80%) | 4 (20%) | 7 (35%) | 14 (70%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 14 (70%) | 6 (30%) | 5 (25%) | 18 (90%) | 1 (5%) |
| bench_b_N10_T07 | 60 | 28 (47%) | 32 (53%) | 35 (58%) | 40 (67%) | 5 (8%) |
| containment_hall4_N10_T07 | 50 | 19 (38%) | 31 (62%) | 21 (42%) | 34 (68%) | 3 (6%) |
| srn_ablation_variant_a_N10_T07 | 30 | 15 (50%) | 15 (50%) | 4 (13%) | 20 (67%) | 1 (3%) |
| srn_autonomous_N10_T07 | 30 | 8 (27%) | 22 (73%) | 1 (3%) | 21 (70%) | 0 (0%) |
| srn_bypass_N10_T07 | 20 | 13 (65%) | 7 (35%) | 2 (10%) | 17 (85%) | 1 (5%) |
| **Total** | **230** | **113 (49%)** | **117 (51%)** | **75 (33%)** | **164 (71%)** | **11 (5%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 41 (36%) | 72 (64%) | 113 |
| **correct=False** | 34 (29%) | 83 (71%) | 117 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 74 (65%) | 39 (35%) | 113 |
| **correct=False** | 90 (77%) | 27 (23%) | 117 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 38.6s | 34.0s | 39.8s |
| asset_specs_N10_T07 | 20 | 28.2s | 28.2s | 28.3s |
| bench_b_N10_T07 | 60 | 60.5s | 16.3s | 95.8s |
| containment_hall4_N10_T07 | 50 | 11.3s | 9.2s | 12.5s |
| srn_ablation_variant_a_N10_T07 | 30 | 22.2s | 5.8s | 61.9s |
| srn_autonomous_N10_T07 | 30 | 13.2s | 4.9s | 29.3s |
| srn_bypass_N10_T07 | 20 | 8.0s | 7.0s | 12.4s |
