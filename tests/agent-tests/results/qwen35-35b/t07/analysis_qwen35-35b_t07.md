# Results analysis: qwen35-35b

Generated: 2026-05-23 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 3 (15%) | 15 (75%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 6 (30%) | 17 (85%) | 2 (10%) |
| bench_b_N10_T07 | 60 | 43 (72%) | 17 (28%) | 37 (62%) | 38 (63%) | 15 (25%) |
| containment_hall4_N10_T07 | 50 | 41 (82%) | 9 (18%) | 35 (70%) | 33 (66%) | 2 (4%) |
| srn_ablation_variant_a_N10_T07 | 30 | 28 (93%) | 2 (7%) | 4 (13%) | 19 (63%) | 0 (0%) |
| srn_autonomous_N10_T07 | 30 | 10 (33%) | 20 (67%) | 5 (17%) | 20 (67%) | 0 (0%) |
| srn_bypass_N10_T07 | 20 | 15 (75%) | 5 (25%) | 1 (5%) | 18 (90%) | 0 (0%) |
| **Total** | **230** | **177 (77%)** | **53 (23%)** | **91 (40%)** | **160 (70%)** | **19 (8%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 74 (42%) | 103 (58%) | 177 |
| **correct=False** | 17 (32%) | 36 (68%) | 53 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 127 (72%) | 50 (28%) | 177 |
| **correct=False** | 33 (62%) | 20 (38%) | 53 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 9.1s | 9.1s | – |
| asset_specs_N10_T07 | 20 | 10.7s | 10.7s | – |
| bench_b_N10_T07 | 60 | 16.8s | 16.0s | 23.7s |
| containment_hall4_N10_T07 | 50 | 19.5s | 18.9s | 20.7s |
| srn_ablation_variant_a_N10_T07 | 30 | 11.0s | 9.9s | 21.6s |
| srn_autonomous_N10_T07 | 30 | 9.7s | 11.7s | 8.5s |
| srn_bypass_N10_T07 | 20 | 8.4s | 8.1s | 9.2s |
