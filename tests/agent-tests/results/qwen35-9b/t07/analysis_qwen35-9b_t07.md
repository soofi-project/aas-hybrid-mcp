# Results analysis: qwen35-9b

Generated: 2026-05-25 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 18 (90%) | 2 (10%) | 15 (75%) | 20 (100%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 14 (70%) | 6 (30%) | 17 (85%) | 19 (95%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 33 (55%) | 27 (45%) | 42 (70%) | 37 (62%) | 9 (15%) |
| containment_hall4_N10_T07 | 50 | 22 (44%) | 28 (56%) | 31 (62%) | 35 (70%) | 6 (12%) |
| srn_autonomous_N10_T07 | 50 | 7 (14%) | 43 (86%) | 1 (2%) | 41 (82%) | 0 (0%) |
| **Total** | **200** | **94 (47%)** | **106 (53%)** | **106 (53%)** | **152 (76%)** | **15 (8%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 68 (72%) | 26 (28%) | 94 |
| **correct=False** | 38 (36%) | 68 (64%) | 106 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 72 (77%) | 22 (23%) | 94 |
| **correct=False** | 80 (75%) | 26 (25%) | 106 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 7.1s | 6.7s | 7.9s |
| asset_specs_N10_T07 | 20 | 10.3s | 8.9s | 12.2s |
| bench_b_N10_T07 | 60 | 14.1s | 10.5s | 18.5s |
| containment_hall4_N10_T07 | 50 | 8.2s | 6.6s | 11.7s |
| srn_autonomous_N10_T07 | 50 | 47.6s | 38.3s | 47.7s |
