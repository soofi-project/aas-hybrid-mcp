# Results analysis: qwen36-27b

Generated: 2026-05-20 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 20 (100%) | 0 (0%) | 13 (65%) | 17 (85%) | 3 (15%) |
| asset_specs_N10 | 20 | 20 (100%) | 0 (0%) | 16 (80%) | 17 (85%) | 3 (15%) |
| bench_b_N10 | 60 | 43 (72%) | 17 (28%) | 53 (88%) | 31 (52%) | 26 (43%) |
| containment_hall4_N10 | 50 | 46 (92%) | 4 (8%) | 40 (80%) | 19 (38%) | 26 (52%) |
| srn_ablation_variant_a_N10 | 30 | 27 (90%) | 3 (10%) | 14 (47%) | 10 (33%) | 8 (27%) |
| srn_autonomous_N10 | 30 | 21 (70%) | 9 (30%) | 17 (57%) | 10 (33%) | 6 (20%) |
| srn_bypass_N10 | 20 | 14 (70%) | 6 (30%) | 10 (50%) | 8 (40%) | 9 (45%) |
| **Total** | **230** | **191 (83%)** | **39 (17%)** | **163 (71%)** | **112 (49%)** | **81 (35%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 139 (73%) | 52 (27%) | 191 |
| **correct=False** | 24 (62%) | 15 (38%) | 39 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 86 (45%) | 105 (55%) | 191 |
| **correct=False** | 26 (67%) | 13 (33%) | 39 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 9.0s | 9.0s | – |
| asset_specs_N10 | 20 | 9.1s | 9.1s | – |
| bench_b_N10 | 60 | 30.1s | 24.5s | 58.0s |
| containment_hall4_N10 | 50 | 20.7s | 20.7s | 23.0s |
| srn_ablation_variant_a_N10 | 30 | 10.9s | 10.2s | 40.2s |
| srn_autonomous_N10 | 30 | 10.7s | 8.3s | 15.1s |
| srn_bypass_N10 | 20 | 11.4s | 12.3s | 10.2s |
