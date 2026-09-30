# Results analysis: qwen38-27b-coding

Generated: 2026-08-20 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 20 (100%) | 18 (90%) | 2 (10%) |
| asset_specs_N10_T07 | 20 | 19 (95%) | 1 (5%) | 20 (100%) | 16 (80%) | 4 (20%) |
| bench_b_N10_T07 | 60 | 49 (82%) | 11 (18%) | 60 (100%) | 25 (42%) | 32 (53%) |
| containment_hall4_N10_T07 | 50 | 41 (82%) | 9 (18%) | 46 (92%) | 29 (58%) | 16 (32%) |
| srn_autonomous_N10_T07 | 50 | 13 (26%) | 37 (74%) | 50 (100%) | 20 (40%) | 9 (18%) |
| **Total** | **200** | **142 (71%)** | **58 (29%)** | **196 (98%)** | **108 (54%)** | **63 (32%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 138 (97%) | 4 (3%) | 142 |
| **correct=False** | 58 (100%) | 0 (0%) | 58 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 78 (55%) | 64 (45%) | 142 |
| **correct=False** | 30 (52%) | 28 (48%) | 58 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 8.1s | 8.1s | – |
| asset_specs_N10_T07 | 20 | 7.7s | 7.6s | 63.6s |
| bench_b_N10_T07 | 60 | 14.2s | 12.5s | 52.9s |
| containment_hall4_N10_T07 | 50 | 11.5s | 11.0s | 52.8s |
| srn_autonomous_N10_T07 | 50 | 58.4s | 45.3s | 68.4s |
