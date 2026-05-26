# Results analysis: qwen35-4b

Generated: 2026-05-26 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 16 (80%) | 4 (20%) | 16 (80%) | 18 (90%) | 1 (5%) |
| asset_specs_N10_T07 | 20 | 17 (85%) | 3 (15%) | 19 (95%) | 18 (90%) | 2 (10%) |
| bench_b_N10_T07 | 60 | 27 (45%) | 33 (55%) | 35 (58%) | 41 (68%) | 4 (7%) |
| containment_hall4_N10_T07 | 50 | 21 (42%) | 29 (58%) | 34 (68%) | 37 (74%) | 4 (8%) |
| srn_autonomous_N10_T07 | 50 | 2 (4%) | 48 (96%) | 7 (14%) | 39 (78%) | 0 (0%) |
| **Total** | **200** | **83 (42%)** | **117 (58%)** | **111 (56%)** | **153 (76%)** | **11 (6%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 60 (72%) | 23 (28%) | 83 |
| **correct=False** | 51 (44%) | 66 (56%) | 117 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 66 (80%) | 17 (20%) | 83 |
| **correct=False** | 87 (74%) | 30 (26%) | 117 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 7.8s | 7.6s | 12.3s |
| asset_specs_N10_T07 | 20 | 9.5s | 9.4s | 11.2s |
| bench_b_N10_T07 | 60 | 15.9s | 13.4s | 18.4s |
| containment_hall4_N10_T07 | 50 | 9.6s | 7.0s | 11.2s |
| srn_autonomous_N10_T07 | 50 | 49.4s | 37.0s | 50.6s |
