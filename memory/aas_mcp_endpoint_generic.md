---
name: MCP endpoint is generic, not use-case-specific
description: Design principle — MCP documentation must be data-agnostic
type: project
---

## Principle

The MCP server (port 8110) provides a **reusable, generic endpoint** over BaSyx + Neo4j + Weaviate. Any AAS environment — not just our DFKI test deployment — may call these tools and read these manual pages.

**Manual pages, tool descriptions, and schema documentation must NEVER hardcode:**
- Specific AAS idShorts (`Hall4`, `MiR250_001`, `UR3e_001`)
- Specific graph IDs or `globalAssetId` values
- Specific AASX files or test assets (MiR100/250, UR3e/20, CRX10iA, Hall3/4)
- Specific containment structure assumptions (`EntryNode`, `Node` idShorts)
- Hall/factory-specific terminology as the domain ("halla" → use "container AAS")
- Concrete template semanticIds in examples (use `$templateId`, `$hierId`, etc.)

**They SHOULD:**
- Point out common AAS traversal patterns and anti-patterns in the abstract
- Teach the agent to discover its own data: `get_templates_index()`, `get_template(name)`, `MATCH ... RETURN DISTINCT sc.id`
- Show structural relationships: `Entity.statements → HAS_ELEMENT`, `Entity.globalAssetId → REPRESENTS_ASSET`
- Use parameterized variables (`$containerId`, `$templateSemanticId`) everywhere

## Why

The MCP tools are consumed by the aas-agent via tool calls, but could also be consumed by any agent or client against any BaSyx deployment. If the manual pages carry Hall-specific examples, they become misleading for other deployments and reinforce brittle idShort matching.

## What was done (2026-05-11)

- `manual_pages/mapping.md` (new) — generic mapping table derived from Kafka Connect plugin `*Node.java` classes
- `manual_pages/cypher.md` — container traversal example: `Hall` → generic `container AAS`
- `manual_pages/recipes.md` — Recipe A: two-step discover-then-traverse pattern with flat fallback
- `tools/manual.py` — `_CYPHER`, `_RECIPES`, `_MAPPING` all use parameterized Cypher
- `tools/schema.py` — entity tree example: `hall` → `container`, `entry` → `parent`
- `tool_descriptions/` — `mapping` page added to index

## Checklist for future manual-page edits

Before adding an example Cypher or prose reference, ask:
1. Would this query work against a BaSyx instance with completely different AASX files?
2. Does it hardcode an `idShort`, template URI, or asset ID that only exists in our test data?
3. Does it teach discovery (`get_templates_index()`, `get_template()`, `RETURN DISTINCT sc.id`) rather than prescribe a specific structure?

If any answer is "no" or "it hardcodes" or "it prescribes", rewrite to be generic.
