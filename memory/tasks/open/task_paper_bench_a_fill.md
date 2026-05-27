---
name: Task — Paper Bench A: Fill [EVAL] Placeholders
description: Run Benchmark A (ingestion plugin v1 vs v2) and fill all [EVAL] placeholder cells in §10; required to demonstrate R6 (50k-shell validated ingestion).
type: task
status: open
priority: high
---

## Summary

§10 Benchmark A contains 10 unfilled `[EVAL: ...]` placeholders — the entire v1/v2
comparison table plus the 50k-shell scale result. Until these are filled, R6 from §05
("Validated ingestion and query performance for a reference dataset of 50,000 shells")
is not demonstrated by the paper. The conclusion's "50×" and "Bench A micro-benchmark
causally attributes the speed-up" also depend on these numbers.

`[EVAL: S]` (scale multiplier) = 50 (50,000 / 1,000 from ETFA 2025) and can be
hardcoded without a new measurement.

## Source of ground truth

`paper/etfa2026/claim_audit.md` rows E1–E2 document which cells are missing.

## Subtasks

### T1 — Run v1 vs v2 micro-benchmark (1,000-shell workload)

Measure the following for both ingestion plugin versions on a fresh stack:

- **a1 / b1:** Mean ingest latency per event (ms)
- **a2 / b2:** Full-load wall-clock time (s or min)
- **a3 / b3:** Cypher p95 latency, 2-hop query (ms)
- **a4 / b4:** Cypher p95 latency, 4-hop with semID resolution (ms)

Speed-up column = a1/b1, a2/b2 (latency ratio).

Protocol: use the load-injector replaying a canonical CREATE sequence (same as Bench A
description in §10). Run on the same commodity hardware used in the paper.

### T2 — Run 50k-shell ingestion (v2 only)

Ingest 50,000 synthetic AAS instances using v2. Record:

- **T_50k:** Total wall-clock time for full 50k ingestion

Synthetic shells derived from the same five IDTA templates listed in §10.

### T3 — Fill cells in `10-evaluation.tex`

Replace all `[EVAL: ...]` tokens with measured values:

```latex
% Table cells
[EVAL: a1] → measured v1 mean latency
[EVAL: b1] → measured v2 mean latency
[EVAL: a2] → v1 full-load time
[EVAL: b2] → v2 full-load time
[EVAL: a3] → v1 Cypher p95 2-hop
[EVAL: b3] → v2 Cypher p95 2-hop
[EVAL: a4] → v1 Cypher p95 4-hop+semID
[EVAL: b4] → v2 Cypher p95 4-hop+semID
[EVAL]× (speed-up col) → compute from a/b ratios

% Scale result line
[EVAL: T\_50k] → 50k wall-clock time
[EVAL: S] → 50  (hardcode: 50k/1k)
```

### T4 — Verify conclusion is consistent

After T3, check §14 that "50×" refers to the *scale ratio* (repository size 50k vs 1k),
not the ingestion speed-up — these are different metrics. Adjust §14 wording if it
conflates the two.

## Acceptance Criteria

- All `[EVAL: ...]` tokens removed from `10-evaluation.tex`
- `[EVAL: S]` = 50 hardcoded
- Speed-up column values computed from measured a/b pairs
- Paper builds without errors
- §14 conclusion is consistent with the filled numbers

## References

- claim_audit.md rows E1, E2, Z5
- §05 R6 requirement: "Validated ingestion and query performance for 50,000 shells"
- §14 conclusion "50× jump in repository scale"
