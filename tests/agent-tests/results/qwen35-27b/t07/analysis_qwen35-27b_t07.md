# Results analysis: qwen35-27b

Generated: 2026-05-25 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 0 (0%) | 20 (100%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 0 (0%) | 20 (100%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 47 (78%) | 13 (22%) | 49 (82%) | 29 (48%) | 28 (47%) |
| containment_hall4_N10_T07 | 50 | 50 (100%) | 0 (0%) | 40 (80%) | 24 (48%) | 26 (52%) |
| srn_autonomous_N10_T07 | 50 | 16 (32%) | 34 (68%) | 20 (40%) | 33 (66%) | 0 (0%) |
| **Total** | **200** | **153 (76%)** | **47 (24%)** | **109 (54%)** | **126 (63%)** | **54 (27%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 89 (58%) | 64 (42%) | 153 |
| **correct=False** | 20 (43%) | 27 (57%) | 47 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 95 (62%) | 58 (38%) | 153 |
| **correct=False** | 31 (66%) | 16 (34%) | 47 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 13.4s | 13.4s | – |
| asset_specs_N10_T07 | 20 | 11.4s | 11.4s | – |
| bench_b_N10_T07 | 60 | 28.5s | 28.8s | 24.7s |
| containment_hall4_N10_T07 | 50 | 26.9s | 26.9s | – |
| srn_autonomous_N10_T07 | 50 | 85.0s | 94.9s | 83.2s |
