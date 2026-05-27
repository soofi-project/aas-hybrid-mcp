---
name: Fix Tool-Call Parser Result↔Call Misbinding Done
description: Write-path classification made fence-robust in the live evaluator (Option B); read-path parser + structured-log hardening (Option C) consciously deferred.
type: task
status: done
---

## What was done (commit 4be49ec)

The misbinding bug — a tool result containing an embedded code fence
(`get_graph_schema` / `get_manual_page` / `get_template`) shifts the result↔call
binding, so a foreign Cypher/JSON error could land on a successful `put_submodel`
call — was neutralized **on the write-path side**, which is what corrupted the
Bench-C numbers.

- **T2 (Option B):** `_analyse_write_path` (evaluator.py) now detects the BaSyx
  success signal across the joined result blob (same logic
  `reclassify_write_path.py` used offline), independent of the unreliable per-call
  binding. Added an auditable `wrote: bool` to `WritePathAnalysis` (serialized in
  `to_dict`).
- **T3:** Standalone regression `tests/agent-tests/test_write_path_classification.py`
  proves the old error-substring heuristic misfires as `surfaced` on misbound input
  while the new success-signal logic stays correct.
- **T4:** `reclassify_write_path.py` marked as an archive/verification tool.
- Paper numbers unchanged: live `wrote` aggregate matches reclassify's `NEW_wrote`
  exactly across all 9 models (450 runs / 77 % write success).

## Consciously deferred (out of scope for this task)

- The **parser itself** (`_TOOL_BLOCK_RE` / `_parse_tool_calls`) still misbinds —
  read-path result inspection remains fragile. Not paper-blocking; write-path is now
  binding-independent.
- **Option C** (have aas-agent emit a structured per-run tool-call JSONL the harness
  consumes instead of re-parsing rendered markdown) was the durable fix but is a
  larger aas-agent change. If read-path analysis ever needs reliable per-call
  results, open a fresh hardening task for it.

## References

- `tests/agent-tests/framework/evaluator.py` (`_analyse_write_path`)
- `tests/agent-tests/test_write_path_classification.py`
- `tests/agent-tests/reclassify_write_path.py` (archive tool)
- Related: `[[paper-bench-c-bypass-rewrite-done]]`, `[[write-tools-ablation-study-done]]`
