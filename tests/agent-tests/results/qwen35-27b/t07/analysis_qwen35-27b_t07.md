# Results analysis: qwen35-27b

Generated: 2026-05-22 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 1 (5%) | 17 (85%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 1 (5%) | 18 (90%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 47 (78%) | 13 (22%) | 44 (73%) | 39 (65%) | 17 (28%) |
| containment_hall4_N10_T07 | 50 | 47 (94%) | 3 (6%) | 33 (66%) | 26 (52%) | 20 (40%) |
| srn_ablation_variant_a_N10_T07 | 30 | 25 (83%) | 5 (17%) | 5 (17%) | 21 (70%) | 1 (3%) |
| srn_autonomous_N10_T07 | 30 | 18 (60%) | 12 (40%) | 2 (7%) | 21 (70%) | 0 (0%) |
| srn_bypass_N10_T07 | 20 | 17 (85%) | 3 (15%) | 0 (0%) | 18 (90%) | 0 (0%) |
| **Total** | **230** | **194 (84%)** | **36 (16%)** | **86 (37%)** | **160 (70%)** | **38 (17%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 82 (42%) | 112 (58%) | 194 |
| **correct=False** | 4 (11%) | 32 (89%) | 36 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 131 (68%) | 63 (32%) | 194 |
| **correct=False** | 29 (81%) | 7 (19%) | 36 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 10.6s | 10.6s | – |
| asset_specs_N10_T07 | 20 | 8.2s | 8.2s | – |
| bench_b_N10_T07 | 60 | 26.3s | 21.1s | 59.7s |
| containment_hall4_N10_T07 | 50 | 17.1s | 17.2s | 5.9s |
| srn_ablation_variant_a_N10_T07 | 30 | 11.2s | 10.6s | 39.0s |
| srn_autonomous_N10_T07 | 30 | 10.5s | 9.7s | 53.3s |
| srn_bypass_N10_T07 | 20 | 8.9s | 10.2s | 5.4s |
