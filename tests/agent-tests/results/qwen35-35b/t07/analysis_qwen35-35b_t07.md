# Results analysis: qwen35-35b

Generated: 2026-05-22 · 7 test suites · 230 runs

## Per test suite

| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |
|---|--:|--:|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 20 (100%) | 0 (0%) | 4 (20%) | 9 (45%) | 2 (10%) |
| asset_specs_N10_T07 | 20 | 20 (100%) | 0 (0%) | 4 (20%) | 18 (90%) | 0 (0%) |
| bench_b_N10_T07 | 60 | 48 (80%) | 12 (20%) | 41 (68%) | 35 (58%) | 18 (30%) |
| containment_hall4_N10_T07 | 50 | 43 (86%) | 7 (14%) | 37 (74%) | 23 (46%) | 15 (30%) |
| srn_ablation_variant_a_N10_T07 | 30 | 29 (97%) | 1 (3%) | 4 (13%) | 21 (70%) | 0 (0%) |
| srn_autonomous_N10_T07 | 30 | 9 (30%) | 21 (70%) | 4 (13%) | 21 (70%) | 0 (0%) |
| srn_bypass_N10_T07 | 20 | 17 (85%) | 3 (15%) | 0 (0%) | 18 (90%) | 0 (0%) |
| **Total** | **230** | **186 (81%)** | **44 (19%)** | **94 (41%)** | **145 (63%)** | **35 (15%)** |

## Correct × Manuals first

Did reading the agent manuals before the first graph query correlate with a correct answer?

| | **read_manuals_first=True** | **read_manuals_first=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 84 (45%) | 102 (55%) | 186 |
| **correct=False** | 10 (23%) | 34 (77%) | 44 |

## Correct × Antipattern hit

Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?

| | **had_antipattern=True** | **had_antipattern=False** | Total |
|---|--:|--:|--:|
| **correct=True** | 117 (63%) | 69 (37%) | 186 |
| **correct=False** | 28 (64%) | 16 (36%) | 44 |

## Duration (median seconds per suite)

Fairest cross-model comparison: **Median (all)** — same suite = same questions, so question difficulty is controlled. Correct-only median is confounded: smaller models only solve easier (faster) questions while larger models also solve harder (slower) ones. Failed runs are disproportionately long because models exhaust the recursion limit rather than giving up quickly.

| Suite | N | Median (all) | Median (correct) | Median (wrong) |
|---|--:|--:|--:|--:|
| anti_pattern_N10_T07 | 20 | 18.1s | 18.1s | – |
| asset_specs_N10_T07 | 20 | 13.3s | 13.3s | – |
| bench_b_N10_T07 | 60 | 19.2s | 16.8s | 64.9s |
| containment_hall4_N10_T07 | 50 | 14.9s | 13.8s | 15.3s |
| srn_ablation_variant_a_N10_T07 | 30 | 8.9s | 9.2s | 5.8s |
| srn_autonomous_N10_T07 | 30 | 7.5s | 7.9s | 7.3s |
| srn_bypass_N10_T07 | 20 | 7.9s | 7.9s | 7.4s |
