---
name: Task — Paper §06 GPU Speedup: Measure or Remove
description: Resolve the [X]/[Y] placeholder for H200 GPU PDF-conversion speedup in §06 Architecture — either run the measurement or remove the sentence.
type: task
status: open
priority: medium
---

## Summary

§06 Architecture contains an unfilled claim:

> "Routing the same workload to a dedicated GPU microservice on an NVIDIA H200 reduces
> this to **[X] s**, a **[Y]×** speedup at no quality cost (chunk count ±5%)."

This requires either (a) running the actual measurement on the H200 and filling the values,
or (b) removing or qualifying the sentence if the measurement is out of scope for this paper.

The claim is a concrete quantitative assertion with placeholders — it cannot remain as-is
in the submission.

## Decision Gate (must choose before implementing)

**Option A — Measure:** Run the docling GPU benchmark on the NVIDIA H200 (Triton endpoint),
measure wall-clock time for the same 5 fixture manuals, fill `[X]` and `[Y]`.
Verify "chunk count ±5%" claim holds.

**Option B — Remove:** Remove the H200 sentence entirely. The commodity CPU figure (165 s)
stands alone. The GPU path becomes a one-line Future Work mention or is dropped.

**Option C — Qualify:** Replace with a forward-looking statement that doesn't claim a
measured speedup: "A GPU-accelerated deployment path exists via the H200 microservice;
quantifying the speedup is left for future work."

Recommendation: **Option B or C** if H200 measurement is not already available.
The 165 s CPU figure is already measured; the GPU claim adds little to the paper's argument
if it has no number behind it.

## Subtasks (if Option A)

### T1 — Run H200 docling benchmark

- Same 5 fixture manuals as the CPU benchmark
- Record: wall-clock time per document (mean), total time for all 5
- Verify chunk count is within ±5% of CPU-based output

### T2 — Fill §06 cells

Replace `[X]` and `[Y]` in `06-architecture.tex` with measured values.

## Subtasks (if Option B or C)

### T1 — Remove or replace sentence in §06

Remove the H200 sentence from `06-architecture.tex` line 18, or replace with the
Option C forward-looking statement.

Update `claim_audit.md` row B2 to ✅.

## Acceptance Criteria

- `[X]` and `[Y]` tokens removed from `06-architecture.tex`
- If Option A: measured values backed by H200 benchmark run
- If Option B/C: no quantitative GPU claim without measurement
- Paper builds without errors

## References

- `paper/etfa2026/claim_audit.md` row B2
- §06 `06-architecture.tex` line 18
- H200 Triton endpoint: described in MEMORY.md (NVIDIA H200 available with Triton Inference Server)
