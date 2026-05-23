# Results analysis: qwen35-397b

Generated: 2026-05-23 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 19 (95%) | 1 (5%) | 9 (45%) | 18 (90%) | 2 (10%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 11 (55%) | 17 (85%) | 2 (10%) |
| bench_b_N10_T07 | 60 | 47 (78%) | 13 (22%) | 51 (85%) | 34 (57%) | 22 (37%) |
| containment_hall4_N10_T07 | 50 | 48 (96%) | 2 (4%) | 40 (80%) | 32 (64%) | 15 (30%) |
| srn_ablation_variant_a_N10_T07 | 30 | 30 (100%) | 0 (0%) | 18 (60%) | 10 (33%) | 8 (27%) |
| srn_autonomous_N10_T07 | 30 | 21 (70%) | 9 (30%) | 13 (43%) | 14 (47%) | 4 (13%) |
| srn_bypass_N10_T07 | 20 | 18 (90%) | 2 (10%) | 10 (50%) | 20 (100%) | 0 (0%) |
| **Total** | **230** | **203 (88%)** | **27 (12%)** | **152 (66%)** | **145 (63%)** | **53 (23%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 138 (68%) | 65 (32%) | 203 |
| **correct=False** | 14 (52%) | 13 (48%) | 27 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 125 (62%) | 78 (38%) | 203 |
| **correct=False** | 20 (74%) | 7 (26%) | 27 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 18.6s | 18.9s | 5.5s |
| asset_specs_N10_T07 | 20 | 18.3s | 18.3s | – |
| bench_b_N10_T07 | 60 | 30.3s | 31.7s | 23.4s |
| containment_hall4_N10_T07 | 50 | 31.3s | 31.3s | 43.2s |
| srn_ablation_variant_a_N10_T07 | 30 | 24.7s | 24.7s | – |
| srn_autonomous_N10_T07 | 30 | 19.6s | 15.0s | 41.6s |
| srn_bypass_N10_T07 | 20 | 22.6s | 22.6s | 29.0s |
