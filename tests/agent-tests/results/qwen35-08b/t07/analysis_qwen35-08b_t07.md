# Results analysis: qwen35-08b

Generated: 2026-05-20 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 0 (0%) | 20 (100%) | 13 (65%) | 0 (0%) | 0 (0%) |
| asset_specs_N10 | 20 | 0 (0%) | 20 (100%) | 9 (45%) | 0 (0%) | 0 (0%) |
| bench_b_N10 | 60 | 0 (0%) | 60 (100%) | 44 (73%) | 1 (2%) | 0 (0%) |
| containment_hall4_N10 | 50 | 0 (0%) | 50 (100%) | 31 (62%) | 1 (2%) | 0 (0%) |
| srn_ablation_variant_a_N10 | 30 | 0 (0%) | 30 (100%) | 5 (17%) | 1 (3%) | 0 (0%) |
| srn_autonomous_N10 | 30 | 0 (0%) | 30 (100%) | 10 (33%) | 2 (7%) | 0 (0%) |
| srn_bypass_N10 | 20 | 0 (0%) | 20 (100%) | 5 (25%) | 1 (5%) | 0 (0%) |
| **Total** | **230** | **0 (0%)** | **230 (100%)** | **117 (51%)** | **6 (3%)** | **0 (0%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 0 (–) | 0 (–) | 0 |
| **correct=False** | 117 (51%) | 113 (49%) | 230 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 0 (–) | 0 (–) | 0 |
| **correct=False** | 6 (3%) | 224 (97%) | 230 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 5.1s | – | 5.1s |
| asset_specs_N10 | 20 | 2.1s | – | 2.1s |
| bench_b_N10 | 60 | 4.2s | – | 4.2s |
| containment_hall4_N10 | 50 | 4.7s | – | 4.7s |
| srn_ablation_variant_a_N10 | 30 | 10.6s | – | 10.6s |
| srn_autonomous_N10 | 30 | 14.7s | – | 14.7s |
| srn_bypass_N10 | 20 | 12.2s | – | 12.2s |
