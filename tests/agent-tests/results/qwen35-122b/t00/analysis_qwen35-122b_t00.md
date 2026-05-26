# Results analysis: qwen35-122b

Generated: 2026-05-26 · 1 test suites · 18 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| bench_b_N3_T00 | 18 | 14 (78%) | 4 (22%) | 12 (67%) | 18 (100%) | 0 (0%) |
| **Total** | **18** | **14 (78%)** | **4 (22%)** | **12 (67%)** | **18 (100%)** | **0 (0%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 12 (86%) | 2 (14%) | 14 |
| **correct=False** | 0 (0%) | 4 (100%) | 4 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 14 (100%) | 0 (0%) | 14 |
| **correct=False** | 4 (100%) | 0 (0%) | 4 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| bench_b_N3_T00 | 18 | 25.3s | 27.8s | 19.0s |
