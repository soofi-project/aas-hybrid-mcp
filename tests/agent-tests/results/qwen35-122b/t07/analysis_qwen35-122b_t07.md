# Results analysis: qwen35-122b

Generated: 2026-05-24 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 4 (20%) | 20 (100%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 7 (35%) | 20 (100%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 43 (72%) | 17 (28%) | 46 (77%) | 48 (80%) | 10 (17%) |
| containment_hall4_N10_T07 | 50 | 46 (92%) | 4 (8%) | 47 (94%) | 21 (42%) | 21 (42%) |
| srn_autonomous_N10_T07 | 50 | 11 (22%) | 39 (78%) | 26 (52%) | 41 (82%) | 0 (0%) |
| **Total** | **200** | **140 (70%)** | **60 (30%)** | **130 (65%)** | **150 (75%)** | **31 (16%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 96 (69%) | 44 (31%) | 140 |
| **correct=False** | 34 (57%) | 26 (43%) | 60 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 99 (71%) | 41 (29%) | 140 |
| **correct=False** | 51 (85%) | 9 (15%) | 60 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 19.0s | 19.0s | – |
| asset_specs_N10_T07 | 20 | 18.1s | 18.1s | – |
| bench_b_N10_T07 | 60 | 30.0s | 29.3s | 34.3s |
| containment_hall4_N10_T07 | 50 | 24.2s | 24.2s | 23.6s |
| srn_autonomous_N10_T07 | 50 | 67.5s | 63.7s | 68.6s |
