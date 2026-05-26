# Results analysis: qwen36-27b

Generated: 2026-05-25 · 5 test suites · 200 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 15 (75%) | 19 (95%) | 1 (5%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 13 (65%) | 20 (100%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 51 (85%) | 9 (15%) | 50 (83%) | 23 (38%) | 37 (62%) |
| containment_hall4_N10_T07 | 50 | 50 (100%) | 0 (0%) | 43 (86%) | 10 (20%) | 39 (78%) |
| srn_autonomous_N10_T07 | 50 | 13 (26%) | 37 (74%) | 39 (78%) | 23 (46%) | 7 (14%) |
| **Total** | **200** | **154 (77%)** | **46 (23%)** | **160 (80%)** | **95 (48%)** | **84 (42%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 131 (85%) | 23 (15%) | 154 |
| **correct=False** | 29 (63%) | 17 (37%) | 46 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 67 (44%) | 87 (56%) | 154 |
| **correct=False** | 28 (61%) | 18 (39%) | 46 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 13.2s | 13.2s | – |
| asset_specs_N10_T07 | 20 | 12.7s | 12.7s | – |
| bench_b_N10_T07 | 60 | 27.1s | 32.6s | 18.8s |
| containment_hall4_N10_T07 | 50 | 29.0s | 29.0s | – |
| srn_autonomous_N10_T07 | 50 | 90.2s | 69.1s | 98.5s |
