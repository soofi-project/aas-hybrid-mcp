# Results analysis: qwen35-35b

Generated: 2026-05-22 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T00 | 20 | 20 (100%) | 0 (0%) | 0 (0%) | 19 (95%) | 0 (0%) |
| asset_specs_N10_T00 | 20 | 20 (100%) | 0 (0%) | 0 (0%) | 10 (50%) | 0 (0%) |
| bench_b_N10_T00 | 60 | 48 (80%) | 12 (20%) | 40 (67%) | 36 (60%) | 16 (27%) |
| containment_hall4_N10_T00 | 50 | 50 (100%) | 0 (0%) | 40 (80%) | 30 (60%) | 12 (24%) |
| srn_ablation_variant_a_N10_T00 | 30 | 29 (97%) | 1 (3%) | 0 (0%) | 20 (67%) | 0 (0%) |
| srn_autonomous_N10_T00 | 30 | 4 (13%) | 26 (87%) | 0 (0%) | 20 (67%) | 0 (0%) |
| srn_bypass_N10_T00 | 20 | 19 (95%) | 1 (5%) | 0 (0%) | 20 (100%) | 0 (0%) |
| **Total** | **230** | **190 (83%)** | **40 (17%)** | **80 (35%)** | **155 (67%)** | **28 (12%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 80 (42%) | 110 (58%) | 190 |
| **correct=False** | 0 (0%) | 40 (100%) | 40 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 125 (66%) | 65 (34%) | 190 |
| **correct=False** | 30 (75%) | 10 (25%) | 40 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T00 | 20 | 26.6s | 26.6s | – |
| asset_specs_N10_T00 | 20 | 7.5s | 7.5s | – |
| bench_b_N10_T00 | 60 | 18.3s | 17.0s | 58.9s |
| containment_hall4_N10_T00 | 50 | 18.6s | 18.6s | – |
| srn_ablation_variant_a_N10_T00 | 30 | 6.2s | 6.2s | 7.0s |
| srn_autonomous_N10_T00 | 30 | 6.1s | 7.8s | 6.1s |
| srn_bypass_N10_T00 | 20 | 8.8s | 9.1s | 7.1s |
