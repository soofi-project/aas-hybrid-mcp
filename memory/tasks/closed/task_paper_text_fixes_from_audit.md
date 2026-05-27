---
name: Task — Paper Text Fixes from Claim Audit
description: Fix all text-only blockers and soften-candidates found in the claim audit (B5, B6, B7, B8, S1–S5, V1, V2, V4) — no new measurements required.
type: task
status: closed
priority: high
---

## Resolution (2026-05-26)

All subtasks done. T1 verified counts against live Neo4j + MCP code: tools = 15 (paper said 16, fixed); node-label/rel-type counts unverifiable as a precise figure (schema doc 27/33, live graph 23/14, divergent), so V1 softened to a qualitative metamodel-coverage claim instead of a number. T2–T9 applied as text edits. Also fixed an undefined `\ref{sec:evaluation}`→`sec:eval` in §13 caught during the build. Paper builds clean (no undefined refs/errors). Per-row detail in `paper/etfa2026/claim_audit.md` → Resolution Log. V3 needed no action (already `wu2023autogen`). Still open as separate tasks: B1 (Docker Hub TODO), B2 (GPU placeholder), B3/B4 (Bench A fill).

## Summary

The claim audit (`paper/etfa2026/claim_audit.md`) identified several factual errors,
internal contradictions, and unattributed qualitative claims that require text-only fixes.
No new benchmark data is needed for any of these items.

## Subtasks

### T1 — Verify node/label/tool counts (pre-condition for B6/V1/V2)

Before editing, confirm ground truth:

- **V1:** Count actual node labels and relationship types exposed by the MCP server's
  `aas://schema/graph` resource (claim: "exactly 27 node labels and 34 relationship types"
  in §06 line 15).
- **V2:** Count MCP tools currently registered in the MCP server
  (claim: "exposing 16 tools" in §06 line 27).

If counts differ from paper claims, fix them in T2.

### T2 — Fix §06 model-list inconsistency (B6)

**File:** `06-architecture.tex` line 63.

Current: `"For evaluation we use the Qwen3.5 family (9B, 35B-A3B, 122B-A10B)"`

Fix to match §10 Table 1 which evaluates: Qwen3.5-2B, 4B, 9B, 27B-FP8, 35B-A3B-FP8,
122B-A10B-FP8, 397B-A17B plus Qwen3.6-27B-FP8 and Qwen3.6-35B-A3B-FP8.

Suggested replacement:
```
For evaluation we use the Qwen3.5 and Qwen3.6 open-weight families spanning two orders
of magnitude in total parameter count (2B to 397B), detailed in Section~\ref{sec:bench-b}.
```

### T3 — Fix §10 Bench C "eight" vs "nine" contradiction (B5)

**File:** `10-evaluation.tex`.

- Line 66: "We evaluate **eight** models" (Bench C)
- Line 72: "Across all 1,750 runs and **nine** models"

Bench C table has 8 rows. Bench B table has 9 rows (includes Qwen3.6-27B which is
excluded from Bench C). Fix both the model count and run total in line 72.

Run total for Bench C: 8 models × 5 cases × 10 reps = **400 runs**
(The 1,750 figure appears to conflate Bench B and C — verify and correct.)

### T4 — Fix §14 false claims about evaluation scope (B7, B8)

**File:** `14-conclusion.tex` line 6.

Two false claims:
- **B7:** "Our evaluation compares agent orchestration variants" — false, §10 uses only ReAct.
- **B8:** "isolates the contribution of template awareness" — false, no ablation benchmark.

Suggested replacement for the affected sentence:
```latex
Our evaluation uses the ReAct variant as a representative baseline across all model sizes,
while a direct v1-versus-v2 micro-benchmark causally attributes the ingestion speed-up
to the architectural changes.
```

### T5 — Fix §03 unattributed manufacturer claim (S1)

**File:** `03-introduction.tex` line 4.

Current: `"manufacturers frequently prefer to link a PDF operator manual rather than
populate individual maintenance steps, leaving the template fields empty"`

Fix: scope to own observation:
```
as observed across our test fixture set, manufacturers frequently link a PDF operator
manual rather than populate individual maintenance steps, leaving the template fields empty
```

Or if a citation can be found: add it. If not, the scoped wording is acceptable.

### T6 — Fix §09 "many AAS servers" claim (S2)

**File:** `09-write-loop.tex` line 11.

Current: `"Since many AAS servers do not strictly enforce IDTA templates"`

Fix: scope to the specific implementation under test:
```
Since Eclipse BaSyx does not enforce IDTA template conformance at the server level
```

Note: BaSyx version should ideally be pinned here (see paper skill constraint on BaSyx version pinning). If version is available from the running stack, add it.

### T7 — Soften §08 "dramatically" (S3)

**File:** `08-retrieval-pipeline.tex` line 18.

Current: `"This dramatically reduces noise"`
Fix: `"This substantially reduces noise"`

### T8 — Soften §11 latency/cost claim (S4)

**File:** `11-discussion.tex` line 6.

Current: `"This directly lowers end-to-end latency and inference costs"`
Fix: `"This reduces step count and thus turn budget"` (or reference Bench B turn-count data if available)

### T9 — Soften abstract "autonomously resolve" (S5) — optional

**File:** `02-abstract-keywords.tex`.

Current: `"enable agents to autonomously resolve complex maintenance scenarios"`

This is defensible as a capability claim. Only fix if §02 review deems it overclaims
given the Bench C max 34% write success rate. Suggested softening if needed:
`"enable agents to navigate and address complex maintenance scenarios"`

## Acceptance Criteria

- No "exactly N node labels and M relationship types" claim without verification
- §06 model list matches §10 table
- §10 Bench C has consistent model count and run total
- §14 does not claim variant comparison or template-awareness ablation
- §03 manufacturer claim is scoped or cited
- §09 "many AAS servers" scoped to BaSyx
- §08 "dramatically" removed
- §11 latency claim softened or backed by turn data
- Paper builds without errors after all edits

## References

- `paper/etfa2026/claim_audit.md` rows B5, B6, B7, B8, S1, S2, S3, S4, S5, V1, V2, V4
