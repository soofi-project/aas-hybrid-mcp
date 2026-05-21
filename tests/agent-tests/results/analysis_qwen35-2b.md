# Results analysis: qwen35-2b

Generated: 2026-05-20 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 0 (0%) | 20 (100%) | 3 (15%) | 5 (25%) | 0 (0%) |
| asset_specs_N10 | 20 | 0 (0%) | 20 (100%) | 5 (25%) | 2 (10%) | 0 (0%) |
| bench_b_N10 | 60 | 0 (0%) | 60 (100%) | 14 (23%) | 11 (18%) | 0 (0%) |
| containment_hall4_N10 | 50 | 0 (0%) | 50 (100%) | 9 (18%) | 7 (14%) | 0 (0%) |
| srn_ablation_variant_a_N10 | 30 | 3 (10%) | 27 (90%) | 2 (7%) | 7 (23%) | 0 (0%) |
| srn_autonomous_N10 | 30 | 2 (7%) | 28 (93%) | 2 (7%) | 4 (13%) | 0 (0%) |
| srn_bypass_N10 | 20 | 0 (0%) | 20 (100%) | 1 (5%) | 1 (5%) | 0 (0%) |
| **Total** | **230** | **5 (2%)** | **225 (98%)** | **36 (16%)** | **37 (16%)** | **0 (0%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 0 (0%) | 5 (100%) | 5 |
| **correct=False** | 36 (16%) | 189 (84%) | 225 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 0 (0%) | 5 (100%) | 5 |
| **correct=False** | 37 (16%) | 188 (84%) | 225 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 22.7s | – | 22.7s |
| asset_specs_N10 | 20 | 22.2s | – | 22.2s |
| bench_b_N10 | 60 | 22.3s | – | 22.3s |
| containment_hall4_N10 | 50 | 21.7s | – | 21.7s |
| srn_ablation_variant_a_N10 | 30 | 21.5s | 19.0s | 21.5s |
| srn_autonomous_N10 | 30 | 20.5s | 19.7s | 20.5s |
| srn_bypass_N10 | 20 | 20.2s | – | 20.2s |
