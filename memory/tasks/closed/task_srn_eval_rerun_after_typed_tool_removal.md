---
name: Task – SRN eval re-run after create_service_request_notification removal
description: Re-run srn_autonomous suite for all models after typed SRN tool was removed; cases consolidated, new empty-submodel bypass added
type: task
status: open
priority: high
---

## Background

`create_service_request_notification` was removed from `write_tools.py` (2026-05-23).
All previous `srn_autonomous`, `srn_bypass`, and `srn_ablation_variant_a` eval results are now invalid:
every run used the typed tool, which no longer exists. Models must now use the generic
`put_submodel` + template validator path.

Old results to discard:
- `srn_autonomous` results in all model/t07 dirs (used typed tool)
- `srn_bypass` results in all model/t07 dirs (separate file, now merged)
- `srn_ablation_variant_a` results in all model/t07 dirs (was measuring the same as srn_autonomous anyway)

## What changed (2026-05-24)

- **Files deleted:** `srn_bypass.yaml`, `srn_ablation_variant_a.yaml`, `docker-compose.variant-a.yml`, `docker-compose.variant-b.yml`, `aas-agent/src/aas_agent/prompts/variant-a/`
- **`srn_autonomous.yaml` rewritten:** 5 consolidated cases (3 from old autonomous + 2 from old bypass) including new `srn_empty_submodel_bypass` case. All references to `create_service_request_notification` replaced with `put_submodel`.
- **`run_all.sh` / `judge.sh` updated:** removed srn_bypass and srn_ablation_variant_a blocks.
- **`WRITE_TOOLS_MODE` was never in Python code** — only in compose overlays (now deleted). No code change needed.

## Subtasks

### T1 — Re-run srn_autonomous for already-evaluated models

Models with existing results that need srn_autonomous re-run:
- `qwen35-27b` (T07)
- `qwen36-27b` (T07)
- `qwen36-35b` (T07)
- `qwen35-35b` (T07)
- `qwen35-122b` (T07)
- `qwen35-397b` (T07)

For each model: run only the srn_autonomous suite, judge, update analysis.md.

```bash
python3 run_tests.py \
  --cases cases/srn_autonomous.yaml \
  --variants aas-agent:react \
  --repetitions 10 \
  --temperature 0.7 \
  --export results/<model>/t07/<model>_srn_autonomous_N10_T07.json

./judge_single.sh <model> srn_autonomous T07   # or equivalent
```

Models qwen35-2b, qwen35-4b: user runs these directly as part of the
small-model sweep — no separate action needed here.

**Status:** Not done yet

### T2 — Update analysis.md files for re-run models

After new results are judged: update the `srn_autonomous` section and the comparison
tables in each affected `analysis.md`. Old `srn_bypass` and `srn_ablation_variant_a`
rows can be kept as historical data with a note that they measured the typed tool path.

**Status:** Not done yet

### T3 — Evaluate empty-submodel bypass results

After T1: check whether any model takes the empty-submodel + element-by-element
bypass path in the new `srn_empty_submodel_bypass` case. This is the key finding
for the paper: if the agent bypasses the template validator this way, it demonstrates
the Pragmatics-Validation-Gap.

**Status:** Not done yet — blocked by T1

## Acceptance Criteria

- `cases/srn_autonomous.yaml` has 6 cases, all using `put_submodel` (not `create_service_request_notification`)
- Fresh `srn_autonomous` results exist for all six models above
- `analysis.md` srn_autonomous rows updated for each model
- Empty-submodel bypass rate documented per model

## References

- Files: `tests/agent-tests/cases/srn_autonomous.yaml`
- Runner: `tests/agent-tests/run_all.sh`
- Judge: `tests/agent-tests/judge.sh`
- Write-Tools: `mcp-server/src/aas_hybrid_mcp/tools/write_tools.py`
- Related: `[[task-paper-ablation-sections]]`, `[[task-paper-eval-table-exporter]]`
