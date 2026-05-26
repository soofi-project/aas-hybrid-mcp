# Results analysis: qwen36-35b

Generated: 2026-05-24 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 8 (40%) | 15 (75%) | 3 (15%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 13 (65%) | 11 (55%) | 6 (30%) |
| bench_b_N10_T07 | 60 | 52 (87%) | 8 (13%) | 50 (83%) | 24 (40%) | 32 (53%) |
| containment_hall4_N10_T07 | 50 | 47 (94%) | 3 (6%) | 34 (68%) | 14 (28%) | 25 (50%) |
| srn_autonomous_N10_T07 | 50 | 9 (18%) | 41 (82%) | 45 (90%) | 14 (28%) | 5 (10%) |
| **Total** | **200** | **148 (74%)** | **52 (26%)** | **150 (75%)** | **78 (39%)** | **71 (36%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 107 (72%) | 41 (28%) | 148 |
| **correct=False** | 43 (83%) | 9 (17%) | 52 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 62 (42%) | 86 (58%) | 148 |
| **correct=False** | 16 (31%) | 36 (69%) | 52 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 5.3s | 5.3s | – |
| asset_specs_N10_T07 | 20 | 5.2s | 5.2s | – |
| bench_b_N10_T07 | 60 | 17.3s | 17.3s | 17.0s |
| containment_hall4_N10_T07 | 50 | 17.5s | 17.7s | 15.6s |
| srn_autonomous_N10_T07 | 50 | 62.7s | 66.1s | 57.2s |
