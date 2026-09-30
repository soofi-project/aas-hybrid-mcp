# Results analysis: nemotron3-nano-30b

Generated: 2026-08-25 · 10 test suites · 160 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N4_T07_THhigh | 8 | 0 (0%) | 8 (100%) | 6 (75%) | 4 (50%) | 0 (0%) |
| anti_pattern_N4_T07_THoff | 8 | 1 (12%) | 7 (88%) | 5 (62%) | 7 (88%) | 0 (0%) |
| asset_specs_N4_T07_THhigh | 8 | 0 (0%) | 8 (100%) | 6 (75%) | 5 (62%) | 0 (0%) |
| asset_specs_N4_T07_THoff | 8 | 0 (0%) | 8 (100%) | 8 (100%) | 5 (62%) | 0 (0%) |
| bench_b_N4_T07_THhigh | 24 | 0 (0%) | 24 (100%) | 22 (92%) | 8 (33%) | 0 (0%) |
| bench_b_N4_T07_THoff | 24 | 0 (0%) | 24 (100%) | 20 (83%) | 10 (42%) | 0 (0%) |
| containment_hall4_N4_T07_THhigh | 20 | 0 (0%) | 20 (100%) | 20 (100%) | 12 (60%) | 0 (0%) |
| containment_hall4_N4_T07_THoff | 20 | 0 (0%) | 20 (100%) | 19 (95%) | 9 (45%) | 0 (0%) |
| srn_autonomous_N4_T07_THhigh | 20 | 0 (0%) | 20 (100%) | 18 (90%) | 10 (50%) | 0 (0%) |
| srn_autonomous_N4_T07_THoff | 20 | 0 (0%) | 20 (100%) | 18 (90%) | 11 (55%) | 0 (0%) |
| **Total** | **160** | **1 (1%)** | **159 (99%)** | **142 (89%)** | **81 (51%)** | **0 (0%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 0 (0%) | 1 (100%) | 1 |
| **correct=False** | 142 (89%) | 17 (11%) | 159 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 1 (100%) | 0 (0%) | 1 |
| **correct=False** | 80 (50%) | 79 (50%) | 159 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N4_T07_THhigh | 8 | 223.3s | – | 223.3s |
| anti_pattern_N4_T07_THoff | 8 | 197.7s | 159.7s | 210.0s |
| asset_specs_N4_T07_THhigh | 8 | 331.8s | – | 331.8s |
| asset_specs_N4_T07_THoff | 8 | 156.1s | – | 156.1s |
| bench_b_N4_T07_THhigh | 24 | 282.4s | – | 282.4s |
| bench_b_N4_T07_THoff | 24 | 223.3s | – | 223.3s |
| containment_hall4_N4_T07_THhigh | 20 | 233.2s | – | 233.2s |
| containment_hall4_N4_T07_THoff | 20 | 182.5s | – | 182.5s |
| srn_autonomous_N4_T07_THhigh | 20 | 288.3s | – | 288.3s |
| srn_autonomous_N4_T07_THoff | 20 | 241.9s | – | 241.9s |
