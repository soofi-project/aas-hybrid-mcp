# Results analysis: qwen35-122b

Generated: 2026-05-21 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 1 (5%) | 19 (95%) | 0 (0%) | 1 (5%) | 0 (0%) |
| asset_specs_N10 | 20 | 1 (5%) | 19 (95%) | 0 (0%) | 0 (0%) | 0 (0%) |
| bench_b_N10 | 60 | 1 (2%) | 59 (98%) | 1 (2%) | 0 (0%) | 1 (2%) |
| containment_hall4_N10 | 50 | 0 (0%) | 50 (100%) | 0 (0%) | 0 (0%) | 0 (0%) |
| srn_ablation_variant_a_N10 | 30 | 0 (0%) | 30 (100%) | 0 (0%) | 0 (0%) | 0 (0%) |
| srn_autonomous_N10 | 30 | 0 (0%) | 30 (100%) | 0 (0%) | 0 (0%) | 0 (0%) |
| srn_bypass_N10 | 20 | 0 (0%) | 20 (100%) | 0 (0%) | 0 (0%) | 0 (0%) |
| **Total** | **230** | **3 (1%)** | **227 (99%)** | **1 (0%)** | **1 (0%)** | **1 (0%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 1 (33%) | 2 (67%) | 3 |
| **correct=False** | 0 (0%) | 227 (100%) | 227 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 1 (33%) | 2 (67%) | 3 |
| **correct=False** | 0 (0%) | 227 (100%) | 227 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 1.3s | 35.5s | 1.2s |
| asset_specs_N10 | 20 | 1.2s | 24.8s | 1.2s |
| bench_b_N10 | 60 | 2.1s | 19.4s | 2.0s |
| containment_hall4_N10 | 50 | 2.8s | – | 2.8s |
| srn_ablation_variant_a_N10 | 30 | 1.5s | – | 1.5s |
| srn_autonomous_N10 | 30 | 2.0s | – | 2.0s |
| srn_bypass_N10 | 20 | 1.7s | – | 1.7s |
