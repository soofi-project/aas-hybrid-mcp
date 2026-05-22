# Results analysis: qwen35-397b

Generated: 2026-05-22 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 9 (45%) | 20 (100%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 15 (75%) | 19 (95%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 52 (87%) | 8 (13%) | 53 (88%) | 30 (50%) | 23 (38%) |
| containment_hall4_N10_T07 | 50 | 38 (76%) | 12 (24%) | 39 (78%) | 33 (66%) | 10 (20%) |
| srn_ablation_variant_a_N10_T07 | 30 | 28 (93%) | 2 (7%) | 18 (60%) | 17 (57%) | 3 (10%) |
| srn_autonomous_N10_T07 | 30 | 25 (83%) | 5 (17%) | 11 (37%) | 16 (53%) | 3 (10%) |
| srn_bypass_N10_T07 | 20 | 20 (100%) | 0 (0%) | 10 (50%) | 17 (85%) | 0 (0%) |
| **Total** | **230** | **203 (88%)** | **27 (12%)** | **155 (67%)** | **152 (66%)** | **39 (17%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 132 (65%) | 71 (35%) | 203 |
| **correct=False** | 23 (85%) | 4 (15%) | 27 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 137 (67%) | 66 (33%) | 203 |
| **correct=False** | 15 (56%) | 12 (44%) | 27 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 38.4s | 38.4s | – |
| asset_specs_N10_T07 | 20 | 37.7s | 37.7s | – |
| bench_b_N10_T07 | 60 | 61.1s | 59.1s | 78.6s |
| containment_hall4_N10_T07 | 50 | 93.9s | 94.4s | 92.5s |
| srn_ablation_variant_a_N10_T07 | 30 | 33.9s | 34.3s | 25.4s |
| srn_autonomous_N10_T07 | 30 | 43.5s | 31.8s | 65.4s |
| srn_bypass_N10_T07 | 20 | 37.0s | 37.0s | – |
