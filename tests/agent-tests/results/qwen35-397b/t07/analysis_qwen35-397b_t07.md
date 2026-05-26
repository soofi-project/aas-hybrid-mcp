# Results analysis: qwen35-397b

Generated: 2026-05-24 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 13 (65%) | 16 (80%) | 2 (10%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 15 (75%) | 20 (100%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 49 (82%) | 11 (18%) | 52 (87%) | 25 (42%) | 34 (57%) |
| containment_hall4_N10_T07 | 50 | 50 (100%) | 0 (0%) | 42 (84%) | 30 (60%) | 19 (38%) |
| srn_autonomous_N10_T07 | 50 | 13 (26%) | 37 (74%) | 45 (90%) | 32 (64%) | 1 (2%) |
| **Total** | **200** | **152 (76%)** | **48 (24%)** | **167 (84%)** | **123 (62%)** | **56 (28%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 131 (86%) | 21 (14%) | 152 |
| **correct=False** | 36 (75%) | 12 (25%) | 48 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 92 (61%) | 60 (39%) | 152 |
| **correct=False** | 31 (65%) | 17 (35%) | 48 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 18.1s | 18.1s | – |
| asset_specs_N10_T07 | 20 | 17.9s | 17.9s | – |
| bench_b_N10_T07 | 60 | 34.0s | 34.3s | 29.4s |
| containment_hall4_N10_T07 | 50 | 33.2s | 33.2s | – |
| srn_autonomous_N10_T07 | 50 | 89.8s | 94.3s | 65.5s |
