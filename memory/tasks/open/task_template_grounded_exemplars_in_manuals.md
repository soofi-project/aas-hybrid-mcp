---
name: Task – Template-Grounded Exemplars in Manual Pages
description: >
  Hypothesis: injecting concrete end-to-end walkthroughs derived from IDTA
  template artifacts into the manual pages improves accuracy of smaller models
  (≤27B) on read-path and write-path tasks. Documents the observation, the
  hypothesis, and the planned intervention for future evaluation.
type: task
status: open
priority: medium
---

## Summary

Commit 66289b3 generalized `cypher.md` and `recipes.md` from
HierarchicalStructures-specific to generic container traversal patterns.
Concrete URIs (e.g. `https://admin-shell.io/idta/HierarchicalStructures/1/1`)
were replaced with `$containerTemplateSemanticId` placeholders. This change
improved generality but removed the "pattern-match scaffolding" that smaller
models rely on.

The 9B eval (T07) shows the consequences: 44% on containment_hall4 (read-only),
14% on SRN (write), and a +36.5pp manuals-first correlation — the model
depends on the manual but the manual gives it no concrete anchors.

The IDTA template artifacts already contain the raw material:
- `_Template_*.json` files define structure with semanticIds, idShorts,
  modelTypes, Cardinality qualifiers, and `ExampleValue` qualifiers
- Only 1 of ~40+ templates ships an `_Example_*.json` (HandoverDocumentation)
- But the Template files themselves are nearly sufficient: they contain
  `ExampleValue` qualifiers with sample values and the full nesting structure

**Hypothesis:** If concrete end-to-end walkthroughs (with real semanticIds,
real idShorts, real Cypher queries, and real write payloads) were injected
into the manual pages, smaller models would pattern-match instead of
reasoning from scratch, improving both read-path accuracy and write-path
completion rate.

## Current State

### Manuals (as of 2026-05-25)

| File | Content | Problem for small models |
|---|---|---|
| `cypher.md` | Anti-patterns + traversal recipes | Uses `$semanticId` placeholders; no real URIs |
| `recipes.md` | 4 worked recipes (A–D) | All Cypher uses `$variable` syntax; no concrete example |
| `mapping.md` | AAS→Graph field mapping | Complete but abstract; no per-template walkthrough |
| `writing.md` | Write-tool API + JSON gotchas | No example `put_submodel` call with a real payload |
| `templates.md` | 3-step lookup workflow | No concrete template→instance→query chain |

### IDTA Template Artifacts

| Template | Has Example? | Has ExampleValue qualifiers? | Relevant for |
|---|---|---|---|
| HandoverDocumentation (02004) | ✅ `_Example_*.json` | ✅ | Read-path: document metadata |
| HierarchicalStructures (02011) | ❌ | ✅ (Cardinality) | Read-path: container traversal |
| TechnicalData (02003) | ❌ | ✅ | Read-path: spec lookup |
| ServiceRequestNotification (02010) | ❌ | ✅ | Write-path: SRN creation |
| DigitalNameplate (02006) | ❌ | ✅ | Read-path: asset identification |

### Eval Evidence (T07, 9B vs 27B)

| Suite | 9B | 27B | Gap |
|---|---|---|---|
| anti_pattern | 90% | 100% | −10pp |
| asset_specs | 70% | 100% | −30pp |
| bench_b | 55% | 78% | −23pp |
| containment_hall4 | 44% | 100% | −56pp |
| srn_autonomous | 14% | 32% | −18pp |

The +36.5pp manuals-first correlation (9B) vs +11.4pp (27B) suggests
the 9B model is *willing* to use the manual but *cannot extract actionable
queries* from the abstract recipes.

## Planned Intervention (not yet implemented)

### Step 1: Generate template-grounded exemplars

For each template used in the eval suites, produce a concrete walkthrough:

1. **Templates with `_Example_*.json`** — extract directly, no LLM needed.
   Verify the example payload passes the MCP write-tool validator.

2. **Templates without `_Example_*.json`** — use a large LLM (≥70B or API
   model) to generate a complete instance JSON from the template structure.
   The template provides: semanticIds, idShorts, modelTypes, Cardinality
   constraints, ExampleValue qualifiers. The LLM fills in plausible values
   that satisfy all constraints. Human review before inclusion.

Each walkthrough contains:
- Natural-language question (matching eval-suite patterns)
- Concrete Cypher query with real semanticIds from the graph
- Expected result structure
- (For write-path:) Complete `put_submodel` / `put_submodel_element` call
  with a validated JSON payload

### Step 2: Add `walkthroughs.md` manual page

New bind-mounted manual page with 3–5 concrete end-to-end walkthroughs:

| # | Walkthrough | Template | Covers |
|---|---|---|---|
| W1 | Container traversal ("Was ist in Halle 4?") | HierarchicalStructures | Entity→REPRESENTS_ASSET, concrete semanticId |
| W2 | Spec lookup ("Wie schnell ist der MiR100?") | TechnicalData | Instance→DERIVED_FROM→Type, Property read |
| W3 | SRN creation ("Erstelle Service Request") | ServiceRequestNotification | Full `put_submodel` payload, enum values |
| W4 | Handover Documentation lesen | HandoverDocumentation | Documents→DocumentVersions→Title |
| W5 | Nameplate auslesen | DigitalNameplate | ManufacturerName, SerialNumber |

### Step 3: Re-run T07 eval on 9B (and optionally 27B)

Same suites, same model, same trial configuration — only difference is
the new `walkthroughs.md` in the bind-mounted manual pages.

**Success criterion:** read-path accuracy on containment_hall4 improves
by ≥15pp (from 44% to ≥59%). Write-path improvement is desirable but
not required for the hypothesis to hold.

## Paper Integration

### As controlled-variable observation in Discussion:

The read and write paths differ not only in task structure but in the
prompt-side scaffolding available to the agent. The read-path manual
pages include concrete Cypher traversal recipes, anti-pattern
comparisons, and worked question-to-query walkthroughs. The write-path
provides no analogous scaffolding — no payload examples, no field-value
enumerations, no end-to-end write sequence. This difference was held
constant across all evaluated model sizes, allowing us to isolate the
effect of parametric knowledge from prompt-side scaffolding. The result
is a measurable scaling threshold: on the scaffolded read path, a 4B
model achieves 80% on focused tasks; on the unscaffolded write path, the
same model collapses to 4%, and only the 27B model reaches 32%.

### As future-work hypothesis:

We hypothesise that template-grounded exemplars — derived mechanically
from IDTA template artefacts rather than deployment-specific fixtures —
would shift this threshold downward, just as read-path exemplars do for
retrieval tasks. The exemplars must be template-grounded (derived from
IDTA semanticIds and ExampleValue qualifiers) rather than
fixture-specific (tied to particular asset names or factory layouts),
ensuring transferability across deployments that share the same template
catalogue. Verifying this is left as future work.

This intervention is a **Layer-2 prompt-side refinement** within the
4-layer model (see [[task-paper-outlook-trained-in-manuals]]). If
exemplars in the prompt prove effective, they simultaneously serve as
high-quality candidates for Layer-1 fine-tuning, making the prompt
injection itself a temporary bridge toward weight-based internalization.

### Why not Fine-Tune directly?

Fine-tuning is a separate experiment with different scope (GPU hours,
corpus curation, SOOFI dependency). It is already tracked in
[[task-paper-outlook-trained-in-manuals]]. The exemplar injection is the
minimal intervention that tests the hypothesis without changing model
weights — keeping the variable isolation clean.

## Acceptance Criteria

- [ ] `walkthroughs.md` created in `mcp-server/src/aas_hybrid_mcp/manual_pages/`
- [ ] Contains ≥3 concrete end-to-end walkthroughs with real semanticIds
- [ ] Write-path walkthrough includes a `put_submodel` JSON payload validated
      against the MCP write tool
- [ ] T07 eval re-run on 9B shows improvement on containment_hall4
- [ ] Paper Discussion section contains the hypothesis paragraph
- [ ] Paper Future Work references the 4-layer connection

## Open Questions

- **Which LLM generates the missing examples?** Current candidate: the 27B
  or 122B model via the agent API, or an API model (Claude/GPT). The template
  JSON is the prompt; the output is a valid instance JSON. Human review
  before committing to `walkthroughs.md`.
- **Token budget:** 3–5 walkthroughs add ~2–4k tokens to the manual. Is this
  acceptable given the bind-mount auto-injection? Or should walkthroughs be
  on-demand only (`get_manual_page("walkthroughs")`)?
- **Staleness:** If AASX files change, the concrete URIs in walkthroughs may
  break. Mitigation: walkthroughs reference template semanticIds (stable)
  not instance-specific IDs where possible.

## References

- Eval analysis: `tests/agent-tests/results/qwen35-9b/t07/analysis.md`
- Generalization commit: `66289b3` ("Generalize cypher.md and recipes.md")
- 4-Layer outlook: [[task-paper-outlook-trained-in-manuals]]
- Container traversal fix: [[task-container-location-traversal-prompt-fix]]
- Prompt quality: [[task-prompt-quality]]
- Template artifacts: `idta_templates/published/`
