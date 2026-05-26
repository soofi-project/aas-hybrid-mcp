# Results analysis: qwen35-2b

Generated: 2026-05-26 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 2 (10%) | 18 (90%) | 0 (0%) | 1 (5%) | 0 (0%) |
| asset_specs_N10_T07 | 20 | 4 (20%) | 16 (80%) | 0 (0%) | 1 (5%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 2 (3%) | 58 (97%) | 8 (13%) | 7 (12%) | 0 (0%) |
| containment_hall4_N10_T07 | 50 | 5 (10%) | 45 (90%) | 7 (14%) | 6 (12%) | 0 (0%) |
| srn_autonomous_N10_T07 | 50 | 0 (0%) | 50 (100%) | 0 (0%) | 11 (22%) | 0 (0%) |
| **Total** | **200** | **13 (6%)** | **187 (94%)** | **15 (8%)** | **26 (13%)** | **0 (0%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 0 (0%) | 13 (100%) | 13 |
| **correct=False** | 15 (8%) | 172 (92%) | 187 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 0 (0%) | 13 (100%) | 13 |
| **correct=False** | 26 (14%) | 161 (86%) | 187 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 16.0s | 17.2s | 16.0s |
| asset_specs_N10_T07 | 20 | 22.3s | 15.1s | 22.8s |
| bench_b_N10_T07 | 60 | 23.9s | 14.9s | 24.2s |
| containment_hall4_N10_T07 | 50 | 22.7s | 14.1s | 23.6s |
| srn_autonomous_N10_T07 | 50 | 22.8s | – | 22.8s |
