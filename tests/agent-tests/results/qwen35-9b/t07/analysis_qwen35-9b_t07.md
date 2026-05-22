# Results analysis: qwen35-9b

Generated: 2026-05-22 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 15 (75%) | 5 (25%) | 7 (35%) | 19 (95%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 16 (80%) | 4 (20%) | 12 (60%) | 17 (85%) | 2 (10%) |
| bench_b_N10_T07 | 60 | 37 (62%) | 23 (38%) | 22 (37%) | 47 (78%) | 6 (10%) |
| containment_hall4_N10_T07 | 50 | 32 (64%) | 18 (36%) | 24 (48%) | 37 (74%) | 3 (6%) |
| srn_ablation_variant_a_N10_T07 | 30 | 23 (77%) | 7 (23%) | 3 (10%) | 18 (60%) | 0 (0%) |
| srn_autonomous_N10_T07 | 30 | 12 (40%) | 18 (60%) | 1 (3%) | 19 (63%) | 0 (0%) |
| srn_bypass_N10_T07 | 20 | 15 (75%) | 5 (25%) | 1 (5%) | 15 (75%) | 1 (5%) |
| **Total** | **230** | **150 (65%)** | **80 (35%)** | **70 (30%)** | **172 (75%)** | **12 (5%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 49 (33%) | 101 (67%) | 150 |
| **correct=False** | 21 (26%) | 59 (74%) | 80 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 109 (73%) | 41 (27%) | 150 |
| **correct=False** | 63 (79%) | 17 (21%) | 80 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 11.9s | 11.8s | 15.4s |
| asset_specs_N10_T07 | 20 | 12.2s | 10.0s | 23.5s |
| bench_b_N10_T07 | 60 | 23.1s | 19.3s | 92.4s |
| containment_hall4_N10_T07 | 50 | 14.5s | 14.5s | 15.8s |
| srn_ablation_variant_a_N10_T07 | 30 | 12.5s | 12.6s | 11.3s |
| srn_autonomous_N10_T07 | 30 | 12.2s | 6.2s | 13.5s |
| srn_bypass_N10_T07 | 20 | 11.9s | 10.4s | 25.6s |
