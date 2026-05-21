# Results analysis: qwen35-27b

Generated: 2026-05-21 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 20 (100%) | 0 (0%) | 1 (5%) | 17 (85%) | 0 (0%) |
| asset_specs_N10 | 20 | 20 (100%) | 0 (0%) | 1 (5%) | 18 (90%) | 0 (0%) |
| bench_b_N10 | 60 | 46 (77%) | 14 (23%) | 44 (73%) | 39 (65%) | 18 (30%) |
| containment_hall4_N10 | 50 | 42 (84%) | 8 (16%) | 33 (66%) | 26 (52%) | 17 (34%) |
| srn_ablation_variant_a_N10 | 30 | 26 (87%) | 4 (13%) | 5 (17%) | 21 (70%) | 0 (0%) |
| srn_autonomous_N10 | 30 | 22 (73%) | 8 (27%) | 2 (7%) | 21 (70%) | 1 (3%) |
| srn_bypass_N10 | 20 | 17 (85%) | 3 (15%) | 0 (0%) | 18 (90%) | 0 (0%) |
| **Total** | **230** | **193 (84%)** | **37 (16%)** | **86 (37%)** | **160 (70%)** | **36 (16%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 76 (39%) | 117 (61%) | 193 |
| **correct=False** | 10 (27%) | 27 (73%) | 37 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 132 (68%) | 61 (32%) | 193 |
| **correct=False** | 28 (76%) | 9 (24%) | 37 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10 | 20 | 10.6s | 10.6s | – |
| asset_specs_N10 | 20 | 8.2s | 8.2s | – |
| bench_b_N10 | 60 | 26.3s | 19.9s | 60.1s |
| containment_hall4_N10 | 50 | 17.1s | 17.8s | 11.8s |
| srn_ablation_variant_a_N10 | 30 | 11.2s | 11.2s | 22.3s |
| srn_autonomous_N10 | 30 | 10.5s | 10.1s | 53.6s |
| srn_bypass_N10 | 20 | 8.9s | 10.2s | 5.4s |
