# Results analysis: qwen35-2b

Generated: 2026-05-22 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 0 (0%) | 20 (100%) | 0 (0%) | 5 (25%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 0 (0%) | 20 (100%) | 3 (15%) | 2 (10%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 1 (2%) | 59 (98%) | 11 (18%) | 11 (18%) | 0 (0%) |
| containment_hall4_N10_T07 | 50 | 2 (4%) | 48 (96%) | 7 (14%) | 7 (14%) | 0 (0%) |
| srn_ablation_variant_a_N10_T07 | 30 | 5 (17%) | 25 (83%) | 1 (3%) | 7 (23%) | 0 (0%) |
| srn_autonomous_N10_T07 | 30 | 2 (7%) | 28 (93%) | 0 (0%) | 4 (13%) | 0 (0%) |
| srn_bypass_N10_T07 | 20 | 0 (0%) | 20 (100%) | 0 (0%) | 1 (5%) | 0 (0%) |
| **Total** | **230** | **10 (4%)** | **220 (96%)** | **22 (10%)** | **37 (16%)** | **0 (0%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 0 (0%) | 10 (100%) | 10 |
| **correct=False** | 22 (10%) | 198 (90%) | 220 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 1 (10%) | 9 (90%) | 10 |
| **correct=False** | 36 (16%) | 184 (84%) | 220 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 22.7s | – | 22.7s |
| asset_specs_N10_T07 | 20 | 22.2s | – | 22.2s |
| bench_b_N10_T07 | 60 | 22.3s | 20.3s | 22.3s |
| containment_hall4_N10_T07 | 50 | 21.7s | 14.0s | 21.7s |
| srn_ablation_variant_a_N10_T07 | 30 | 21.5s | 19.0s | 21.6s |
| srn_autonomous_N10_T07 | 30 | 20.5s | 19.7s | 20.5s |
| srn_bypass_N10_T07 | 20 | 20.2s | – | 20.2s |
