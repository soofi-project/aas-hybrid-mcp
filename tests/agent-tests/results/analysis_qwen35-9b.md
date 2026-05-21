# Results analysis: qwen35-9b

Generated: 2026-05-20 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 16 (80%) | 4 (20%) | 7 (35%) | 19 (95%) | 0 (0%) |
| asset_specs_N10 | 20 | 19 (95%) | 1 (5%) | 12 (60%) | 17 (85%) | 2 (10%) |
| bench_b_N10 | 60 | 31 (52%) | 29 (48%) | 22 (37%) | 47 (78%) | 5 (8%) |
| containment_hall4_N10 | 50 | 29 (58%) | 21 (42%) | 24 (48%) | 37 (74%) | 2 (4%) |
| srn_ablation_variant_a_N10 | 30 | 24 (80%) | 6 (20%) | 3 (10%) | 18 (60%) | 0 (0%) |
| srn_autonomous_N10 | 30 | 19 (63%) | 11 (37%) | 1 (3%) | 19 (63%) | 0 (0%) |
| srn_bypass_N10 | 20 | 14 (70%) | 6 (30%) | 1 (5%) | 15 (75%) | 1 (5%) |
| **Total** | **230** | **152 (66%)** | **78 (34%)** | **70 (30%)** | **172 (75%)** | **10 (4%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 46 (30%) | 106 (70%) | 152 |
| **correct=False** | 24 (31%) | 54 (69%) | 78 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 110 (72%) | 42 (28%) | 152 |
| **correct=False** | 62 (79%) | 16 (21%) | 78 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 11.9s | 10.6s | 23.0s |
| asset_specs_N10 | 20 | 12.2s | 10.8s | 98.2s |
| bench_b_N10 | 60 | 23.1s | 18.4s | 92.4s |
| containment_hall4_N10 | 50 | 14.5s | 16.6s | 13.5s |
| srn_ablation_variant_a_N10 | 30 | 12.5s | 12.7s | 10.6s |
| srn_autonomous_N10 | 30 | 12.2s | 12.5s | 12.0s |
| srn_bypass_N10 | 20 | 11.9s | 9.7s | 24.7s |
