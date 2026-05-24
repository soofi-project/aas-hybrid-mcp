---
name: Write-Tools Ablation Study Done
description: Ablation study (Variant A/B) obsoleted by typed-tool removal; all artifacts cleaned up and consolidated into srn_autonomous.yaml
type: task
status: done
---

## What was done

- **Variant B (typed-only) was already out of scope** — `create_service_request_notification` was never implemented.
- **Variant A (prompt-hint) overlays removed:** `docker-compose.variant-a.yml`, `docker-compose.variant-b.yml`, and `aas-agent/src/aas_agent/prompts/variant-a/` deleted. These set `WRITE_TOOLS_MODE` and a variant-specific system prompt that are no longer needed.
- **`WRITE_TOOLS_MODE` was never wired into Python code** — the env var existed only in compose overlays. No code changes required.
- **Test cases consolidated:** `srn_ablation_variant_a.yaml` and `srn_bypass.yaml` deleted. All SRN cases merged into `srn_autonomous.yaml` (5 cases: fault_context, routine_priority, serial_number, spatial_hall4, empty_submodel_bypass).
- **New case `srn_empty_submodel_bypass`** added: tests whether the agent pushes a minimal/empty submodel (passes template validator because `ServiceRequestNotification` has Cardinality ZeroToMany) and then builds it element-by-element via `put_submodel_element`.
- **`run_all.sh` and `judge.sh`** updated: removed `srn_bypass` and `srn_ablation_variant_a` blocks.
- **`README.md`** updated: suite count 7 → 5, removed obsolete suite entries.

## Why the approach changed

The original ablation design (Prompt-only vs. Typed tool) is obsolete because the typed tool was removed. The new story is: generic `put_submodel` + template validator can be bypassed via an empty submodel + element-by-element construction. This is what `srn_empty_submodel_bypass` tests.
