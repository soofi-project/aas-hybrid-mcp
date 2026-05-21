# Results analysis: qwen35-4b

Generated: 2026-05-20 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 16 (80%) | 4 (20%) | 7 (35%) | 14 (70%) | 0 (0%) |
| asset_specs_N10 | 20 | 17 (85%) | 3 (15%) | 5 (25%) | 18 (90%) | 1 (5%) |
| bench_b_N10 | 60 | 27 (45%) | 33 (55%) | 35 (58%) | 40 (67%) | 5 (8%) |
| containment_hall4_N10 | 50 | 14 (28%) | 36 (72%) | 21 (42%) | 34 (68%) | 2 (4%) |
| srn_ablation_variant_a_N10 | 30 | 11 (37%) | 19 (63%) | 4 (13%) | 20 (67%) | 0 (0%) |
| srn_autonomous_N10 | 30 | 16 (53%) | 14 (47%) | 1 (3%) | 21 (70%) | 0 (0%) |
| srn_bypass_N10 | 20 | 13 (65%) | 7 (35%) | 2 (10%) | 17 (85%) | 1 (5%) |
| **Total** | **230** | **114 (50%)** | **116 (50%)** | **75 (33%)** | **164 (71%)** | **9 (4%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 38 (33%) | 76 (67%) | 114 |
| **correct=False** | 37 (32%) | 79 (68%) | 116 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 77 (68%) | 37 (32%) | 114 |
| **correct=False** | 87 (75%) | 29 (25%) | 116 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 38.6s | 34.0s | 39.8s |
| asset_specs_N10 | 20 | 28.2s | 22.7s | 39.4s |
| bench_b_N10 | 60 | 60.5s | 16.6s | 96.7s |
| containment_hall4_N10 | 50 | 11.3s | 8.7s | 12.1s |
| srn_ablation_variant_a_N10 | 30 | 22.2s | 4.2s | 44.8s |
| srn_autonomous_N10 | 30 | 13.2s | 7.8s | 29.3s |
| srn_bypass_N10 | 20 | 8.0s | 6.3s | 12.4s |
