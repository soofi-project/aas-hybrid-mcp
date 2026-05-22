# Results analysis: qwen35-397b

Generated: 2026-05-22 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T00 | 20 | 20 (100%) | 0 (0%) | 12 (60%) | 19 (95%) | 1 (5%) |
| asset_specs_N10_T00 | 20 | 20 (100%) | 0 (0%) | 12 (60%) | 19 (95%) | 0 (0%) |
| bench_b_N10_T00 | 60 | 48 (80%) | 12 (20%) | 52 (87%) | 37 (62%) | 20 (33%) |
| containment_hall4_N10_T00 | 50 | 43 (86%) | 7 (14%) | 41 (82%) | 24 (48%) | 21 (42%) |
| srn_ablation_variant_a_N10_T00 | 30 | 29 (97%) | 1 (3%) | 14 (47%) | 14 (47%) | 4 (13%) |
| srn_autonomous_N10_T00 | 30 | 26 (87%) | 4 (13%) | 14 (47%) | 15 (50%) | 3 (10%) |
| srn_bypass_N10_T00 | 20 | 19 (95%) | 1 (5%) | 5 (25%) | 17 (85%) | 0 (0%) |
| **Total** | **230** | **205 (89%)** | **25 (11%)** | **150 (65%)** | **145 (63%)** | **49 (21%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 133 (65%) | 72 (35%) | 205 |
| **correct=False** | 17 (68%) | 8 (32%) | 25 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 127 (62%) | 78 (38%) | 205 |
| **correct=False** | 18 (72%) | 7 (28%) | 25 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T00 | 20 | 19.1s | 19.1s | – |
| asset_specs_N10_T00 | 20 | 19.1s | 19.1s | – |
| bench_b_N10_T00 | 60 | 28.3s | 33.2s | 22.9s |
| containment_hall4_N10_T00 | 50 | 37.7s | 37.7s | 39.2s |
| srn_ablation_variant_a_N10_T00 | 30 | 26.4s | 26.4s | 9.6s |
| srn_autonomous_N10_T00 | 30 | 24.6s | 20.3s | 43.2s |
| srn_bypass_N10_T00 | 20 | 25.2s | 25.1s | 30.8s |
