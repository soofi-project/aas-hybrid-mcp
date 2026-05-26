# Results analysis: qwen35-35b

Generated: 2026-05-25 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 9 (45%) | 16 (80%) | 2 (10%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 5 (25%) | 17 (85%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 44 (73%) | 16 (27%) | 42 (70%) | 37 (62%) | 17 (28%) |
| containment_hall4_N10_T07 | 50 | 44 (88%) | 6 (12%) | 40 (80%) | 23 (46%) | 11 (22%) |
| srn_autonomous_N10_T07 | 50 | 17 (34%) | 33 (66%) | 27 (54%) | 31 (62%) | 2 (4%) |
| **Total** | **200** | **145 (72%)** | **55 (28%)** | **123 (62%)** | **124 (62%)** | **32 (16%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 90 (62%) | 55 (38%) | 145 |
| **correct=False** | 33 (60%) | 22 (40%) | 55 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 83 (57%) | 62 (43%) | 145 |
| **correct=False** | 41 (75%) | 14 (25%) | 55 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 8.8s | 8.8s | – |
| asset_specs_N10_T07 | 20 | 10.2s | 10.2s | – |
| bench_b_N10_T07 | 60 | 18.8s | 18.2s | 24.3s |
| containment_hall4_N10_T07 | 50 | 19.5s | 19.4s | 22.0s |
| srn_autonomous_N10_T07 | 50 | 40.1s | 34.8s | 45.0s |
