# Results analysis: qwen36-35b

Generated: 2026-05-21 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 20 (100%) | 0 (0%) | 6 (30%) | 13 (65%) | 2 (10%) |
| asset_specs_N10 | 20 | 19 (95%) | 1 (5%) | 8 (40%) | 11 (55%) | 3 (15%) |
| bench_b_N10 | 60 | 46 (77%) | 14 (23%) | 53 (88%) | 29 (48%) | 28 (47%) |
| containment_hall4_N10 | 50 | 44 (88%) | 6 (12%) | 29 (58%) | 29 (58%) | 13 (26%) |
| srn_ablation_variant_a_N10 | 30 | 25 (83%) | 5 (17%) | 8 (27%) | 14 (47%) | 6 (20%) |
| srn_autonomous_N10 | 30 | 25 (83%) | 5 (17%) | 4 (13%) | 14 (47%) | 3 (10%) |
| srn_bypass_N10 | 20 | 14 (70%) | 6 (30%) | 3 (15%) | 14 (70%) | 2 (10%) |
| **Total** | **230** | **193 (84%)** | **37 (16%)** | **111 (48%)** | **124 (54%)** | **57 (25%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 95 (49%) | 98 (51%) | 193 |
| **correct=False** | 16 (43%) | 21 (57%) | 37 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 96 (50%) | 97 (50%) | 193 |
| **correct=False** | 28 (76%) | 9 (24%) | 37 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 4.7s | 4.7s | – |
| asset_specs_N10 | 20 | 4.4s | 4.5s | 3.8s |
| bench_b_N10 | 60 | 18.3s | 12.7s | 53.1s |
| containment_hall4_N10 | 50 | 14.9s | 16.0s | 11.6s |
| srn_ablation_variant_a_N10 | 30 | 8.7s | 8.4s | 26.8s |
| srn_autonomous_N10 | 30 | 9.4s | 10.8s | 7.3s |
| srn_bypass_N10 | 20 | 7.0s | 7.7s | 6.7s |
