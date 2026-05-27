---
name: Testfall-Übersicht (alle Cases) Done
description: Verified inventory of all test cases against the live YAMLs; reconciled paper §10 case/run references and fixed two inconsistencies found in the process.
type: task
status: done
---

## Result

Authoritative inventory of `tests/agent-tests/cases/`, verified against the live
YAML files (not the prior stale notes). **6 YAML files, 23 cases, 20 runnable.**
The old frontmatter claim "26 cases / 8 YAMLs" was outdated.

| File | Cases | Runnable | Used in paper |
|---|---|---|---|
| `bench_b.yaml` | 6 (B1–B6) | ✅ | Bench B suite `bench_b` |
| `containment_hall4.yaml` | 5 | ✅ | Bench B suite `containment_hall4` |
| `asset_specs.yaml` | 2 | ✅ | Bench B suite `asset_specs` |
| `anti_pattern_idShort_lookup.yaml` | 2 | ✅ | Bench B suite `anti_pattern` |
| `srn_autonomous.yaml` | 5 | ✅ | Bench C (write-path) |
| `naming_stress.yaml` | 3 | ❌ requires_fixture | — (out of scope, not needed) |
| **Total** | **23** | **20** | |

`naming_stress` is a stub (needs `MiR100_Type_stressed.aasx`); decided we don't need
it — not referenced anywhere in the paper.

## Coverage framing (added to paper §10)

Added one sentence to the Bench B setup: suites cover the target use case across
difficulty levels, from single-step spec lookups (`asset_specs`) to multi-step
queries requiring spatial disambiguation, manual grounding, and cross-asset
comparison (`bench_b`, `containment_hall4`). Matches the real complexity gradient
of the cases.

## Paper consistency — verified

- Bench B read-path: anti_pattern(2) + asset_specs(2) + bench_b(6) + containment(5)
  = 15 cases × N=10 = **150 runs/model** — matches §10 caption.
- Bench C write-path: srn_autonomous(5) × N=10 × 9 models = **450 runs** — matches §10/§11.
- Same 9 models in both Bench B and Bench C tables; all 9 have read- *and* write-path
  result files.

## Bugs found and fixed in the process

1. **B1 query blanked.** `bench_b.yaml` B1 (`bench_b_B1_hall3_contents`) had its
   `query` emptied to `""` in the working tree (uncommitted). Restored to
   "Which devices are located in Hall 3?" — the judged results were produced with
   the real query; an empty query would break any rerun.
2. **False Bench-B footnote.** The §10 caption claimed Qwen3.6-27B was
   "read-path suites only (no SRN suite)". Untrue: `qwen36-27b_srn_autonomous_N10_T07_judged.json`
   exists with n=50, all_good_rate=0.14 (= the 14% SRN value in the Bench C table,
   discussed in §11). Removed the `*` marker and the footnote line.

## Still open (not part of this task)

- Bench C table (`tab:bench_c`) has 9 `\todo{define}` cells in the "Primary
  limitation" column — unfilled. Needs per-model limitation labels derived from the
  judge failure modes.

## References

- `tests/agent-tests/cases/*.yaml` (6 files)
- `paper/etfa2026/content/10-evaluation.tex` (§10), `11-discussion.tex` (§11)
- Related: `[[task-paper-pattern-modelsize-eval]]`, `[[task-paper-modeling-vs-pragmatics-anecdote]]`
