"""MCP manual: index + sub-pages as tools.

The agent may pre-fetch the index at startup (controlled by the
``AGENT_INJECT_MANUAL`` flag in aas-agent) or call ``get_manual_index``
on demand. Sub-pages are loaded individually via ``get_manual_page``.
"""

from fastmcp import FastMCP

from aas_hybrid_mcp.tool_descriptions import load as load_description


_INDEX = """\
# AAS Hybrid MCP — Operator Manual

You are talking to a hybrid Neo4j + Weaviate MCP server that wraps a
BaSyx AAS environment. This page indexes the rest of the manual.

## Sub-pages — call get_manual_page(page=...) on demand

- `cypher` — graph patterns, anti-patterns. **Call before any non-trivial Cypher.**
- `templates` — IDTA template workflow. **Call when the question maps to a
  domain concept (location, capability, technical data, …).**
- `writing` — `put_*` / `delete_*` tools and JSON-format gotchas.
  **Call before the first write.**
- `troubleshooting` — what to do when a query returns zero rows.
  **Call after any 0-row result.**
- `recipes` — worked end-to-end examples (hall → assets, instance → type
  → docs, capability lookup, diagnostic listing).

## Four rules that catch the most failures

1. **Before your first `query_aas_graph` call, call `get_templates_index()`
   — but only ONCE per session.** Check the conversation history first: if a
   prior `<think>` block already shows its result, use those semanticIds
   directly. Do not call it again on every turn.
2. `params` for `query_aas_graph` is an OBJECT, not a JSON string.
   `{}`, not `"{}"`.
3. Use IDTA semanticIds VERBATIM from `get_templates_index()`. No `/Submodel`
   suffix, no version normalisation, no recall from training memory. The graph
   may also carry non-IDTA semanticIds (e.g. ZVEI Nameplate); discover them
   with `MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc) RETURN DISTINCT sc.id`.
4. Never match assets by `idShort` for domain reasoning. `idShort` is a
   free-form local label; semantic meaning lives only in
   `HAS_SEMANTIC_ID` / `HAS_SUPPLEMENTAL_SEMANTIC_ID`.

## Tools — call on demand

- `get_templates_index()` — all published IDTA templates with name, version,
  semanticId, description. Call when picking a template or before any
  non-trivial Cypher (per rule 1).
- `get_template(name)` — element structure of one template (modelType,
  idShort, semanticId, nesting). Call before traversing a submodel or
  writing template-conformant JSON.
"""


_CYPHER = """\
# Cypher patterns and anti-patterns

**Pre-condition.** Before composing your first `query_aas_graph` call
in a session, you must have read both `get_graph_schema()` (relation
labels, traversal tips) and `get_templates_index()` (verbatim
semanticIds). Do not skip this — invented relations and invented
semanticIds are the largest single source of zero-row results.

## Anti-patterns

**1. `Repository` is AAS-storage, not a physical location.**
The `(:AssetAdministrationShell)-[:DEPLOYED_IN]->(:Repository)` edge
points to the BaSyx server URL where the shell lives. It is not a hall,
room, or factory section. Locations live in submodels conforming to
`HierarchicalStructures` (or another location-bearing template),
discovered via `HAS_SEMANTIC_ID`.

**2. `semanticId` is a relation, not a property.**
```cypher
// WRONG — silently returns 0 rows
MATCH (sm:Submodel {semanticId: 'https://...'}) ...

// RIGHT
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: 'https://...'}) ...
```

**3. Use IDTA semanticIds verbatim — do not enrich them.**
For example, `HierarchicalStructures` is
`https://admin-shell.io/idta/HierarchicalStructures/1/1` — *not*
`.../1/1/Submodel`. The exact strings come from
`get_templates_index()`.

**4. `assetType` and `assetKind` are optional and often null.**
Use `(:AssetAdministrationShell)-[:DERIVED_FROM]->` for type vs.
instance distinction; use submodel semanticIds for domain
classification.

**5. Never match by `idShort` — always reason via `semanticId`.**
`idShort` is a free-form local label chosen by the shell author.
Domain classification (transport robot, welding cell, …) and template
conformance must be expressed via `HAS_SEMANTIC_ID` /
`HAS_SUPPLEMENTAL_SEMANTIC_ID`.

## Useful traversal recipes

List all submodels of a shell with their template's semanticId — the
fastest way to learn what kind of shell you are looking at:
```cypher
MATCH (aas:AssetAdministrationShell {id: $aasId})-[:HAS_SUBMODEL]->(sm:Submodel)
OPTIONAL MATCH (sm)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN sm.idShort, sm.id, sc.id AS templateSemanticId
```

Discover which semanticIds are actually present in the graph (use this
when the templates index ID does not match):
```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN DISTINCT sc.id ORDER BY sc.id
```

All submodels conforming to a given IDTA template across all shells:
```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $semanticId})
MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm)
RETURN aas.idShort, aas.id, sm.idShort, sm.id
```

Walk from an instance shell to its type shell (handover documentation
typically lives on the type per VDI 2770):
```cypher
MATCH (instance:AssetAdministrationShell {id: $instanceId})
      -[:DERIVED_FROM]->(type:AssetAdministrationShell)
RETURN type.id, type.idShort
```

Container traversal — a Hall AAS owns a HierarchicalStructures
submodel; contained assets appear as ReferenceElement values inside
its Entity tree:
```cypher
MATCH (container:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(ref:ReferenceElement)-[:HAS_VALUE]->(contained)
RETURN container.idShort, contained.idShort, labels(contained) AS containedType
```

For the full label/relation catalogue and 10+ further example queries,
read `get_graph_schema()`.

**Next:** if a query returned zero rows, read
`get_manual_page("troubleshooting")`. If you are about to write,
`get_manual_page("writing")`.
"""


_TEMPLATES = """\
# IDTA template workflow

User questions almost always map to a domain concept — location,
containment, capability, contact information, maintenance schedule,
certificates, technical data, … The answer lives in a submodel that
conforms to a specific IDTA template. Your job is to translate user
intent → template → semanticId → graph traversal. Don't invent ad-hoc
Cypher patterns and don't recall semanticIds from training memory.

## Three-step lookup

1. **Skim `get_templates_index()`** for templates whose description
   matches the user's concept. The index is the ground truth for which
   templates exist and what their `semanticId` is.
2. **Confirm against the graph.** Submodels are not labelled by their
   template — only the relation
   `-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: ...})` proves
   conformance. List the actual semanticIds with the discovery query in
   `get_manual_page("cypher")` if the index ID does not match anything.
3. **Read `get_template(name)`** when you need the field-level
   structure (which child idShorts to expect, their nesting) before
   composing the traversal into the submodel's elements.

## ZVEI vs IDTA — the graph may not use IDTA's IDs

Several legacy templates use ZVEI URIs even when IDTA has published an
equivalent template. The most common case is Nameplate: the IDTA
templates index lists
`https://admin-shell.io/idta/nameplate/3/0/Nameplate`, but a graph
populated from older AASX files may carry
`https://admin-shell.io/zvei/nameplate/2/0/Nameplate` instead. Filtering
on the IDTA-3.0 ID returns zero rows.

When this happens, do NOT conclude the data is absent. Run the
discovery query and use whatever semanticId the graph actually carries:
```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN DISTINCT sc.id ORDER BY sc.id
```

## When no template matches

A custom `semanticId` in the data is the AAS ecosystem's escape hatch
for concepts not yet standardised — finding one confirms the data is
correctly modelled, not that data is missing. State the gap explicitly:
name which template domains *do* exist, name which template you looked
for, and offer the closest matches.

**Next:** `get_manual_page("cypher")` for the actual traversal patterns;
`get_manual_page("recipes")` for end-to-end worked examples.
"""


_WRITING = """\
# Write tools — `put_*` / `delete_*`

Six generic, symmetric tools cover the full mutation surface:

- `put_aas(aas_json)` — idempotent create-or-replace shell
- `delete_aas(aas_id)`
- `put_submodel(aas_id, submodel_json)` — idempotent
  create-or-replace submodel under a shell
- `delete_submodel(aas_id, submodel_id)`
- `put_submodel_element(submodel_id, id_short_path, element_json)` —
  covers ALL SubmodelElement subtypes (Property, File, SMC, SML,
  MultiLanguageProperty, Range, ReferenceElement, RelationshipElement,
  Entity, Operation, …) via a single tool
- `delete_submodel_element(submodel_id, id_short_path)`

Writes go through BaSyx; client-side validation runs first against the
basyx-python-sdk, so constraint violations (missing `semanticId`,
wrong nesting, wrong `modelType`) come back as a Python error you can
react to without ever touching the server.

## JSON-format gotchas

All `*_json` parameters are JSON STRINGS, not dicts. Pass the
serialised JSON of the AAS / Submodel / SubmodelElement object:
```
put_submodel(
  aas_id="https://example.com/aas/MyAsset",
  submodel_json='{"modelType":"Submodel","id":"https://...","idShort":"Nameplate", ...}'
)
```

`id_short_path` is a dot-separated path from the submodel root, e.g.
`MarkingsObject.0.MarkingFile` for the first MarkingFile in a
SubmodelElementList.

## Read template structure first

Before writing a submodel that should conform to a published IDTA
template:

1. Find the template name from `get_templates_index()`.
2. Read `get_template(name)` — gives you the modelType, idShort,
   semanticId, and full nesting structure.
3. Build your JSON from that skeleton. Set `semanticId` verbatim from
   the template; use the same idShorts.

Skipping this step is the most common cause of validation failures
on write.

## After writing

Kafka events from BaSyx auto-sync the change to Neo4j and Weaviate.
You can immediately observe your write through `query_aas_graph` and
`search_aas_documents` — but allow a second or two for the event to
propagate.

## Attachments

Binary `File` / `Blob` upload (the actual bytes) is NOT yet implemented
as an MCP tool — that is Phase 10. For now, write the `File` element
metadata (contentType, empty value) via `put_submodel_element`; the
binary itself must be uploaded out-of-band.

**Next:** `get_manual_page("cypher")` to verify what you wrote;
`get_manual_page("troubleshooting")` if a write fails.
"""


_TROUBLESHOOTING = """\
# When retrieval is empty

A zero-row Cypher result or empty document-search result means your
query was wrong, NOT that the data is missing. Stopping early —
"there's no such data" — after a single failed query is a failure
mode. Before concluding the data is absent, exhaust all of these moves:

1. **Sanity-check against the schema.** If you filtered on a property
   like `semanticId`, you almost certainly meant the
   `HAS_SEMANTIC_ID` relation. See `get_graph_schema()` anti-patterns.
2. **Open the search.** Drop the most restrictive clause (a hard `=`
   filter, an exact-string match) and re-run with `CONTAINS` /
   case-insensitive comparison or no filter at all to see what is
   actually in the graph.
3. **List the actual semanticIds.** If you assumed an IDTA-3.0 ID
   (e.g. `nameplate/3/0/Nameplate`) and got nothing, the graph may
   carry a ZVEI / older variant
   (`zvei/nameplate/2/0/Nameplate`). Run the
   `RETURN DISTINCT sc.id` discovery query from
   `get_manual_page("cypher")`.
4. **Re-skim the templates index.** If you assumed a specific template
   carries the answer and the submodel isn't there, a sibling template
   may. The index is at `get_templates_index()`.
5. **Walk type ↔ instance.** If the question is about an instance and
   you came up empty, the answer probably lives on its type AAS via
   `DERIVED_FROM` (and vice-versa for instance-specific records like
   serial number, calibration certificates, delivery protocols — those
   live on the *instance*, not the type).
5a. **`value: null` on a Nameplate element means MultiLanguageProperty.**
   Read the text via `(el)-[:HAS_VALUE]->(ls:LangString)` instead —
   see Recipe E in `get_manual_page("recipes")`.
6. **List what *is* on the shell.** Run the
   "submodels of a shell with their templates" recipe from
   `get_manual_page("cypher")`; the actual contents will usually point you
   at the right path.

Only after all moves have been tried may you state the gap. State it
specifically — name the templates you checked, the semanticIds you
searched for, and what the graph actually contains:

> *"No AAS in the graph carries a submodel for X (template Y). The
> closest matches I see are A, B, C — let me know if one of those is
> what you mean."*

Do not say "you would need to add this data" after a single failed
query. Do not silently substitute generic advice for missing data.

**Next:** `get_manual_page("recipes")` for end-to-end worked examples that
exercise these moves.
"""


_RECIPES = """\
# Worked recipes

End-to-end examples for the most common question shapes. Each recipe
assumes you have already read `get_manual_page("cypher")` and (for steps
involving templates) `get_templates_index()`.

## Recipe A — "What's in hall 4?" (container traversal)

The Hall AAS is the container. It owns a `HierarchicalStructures`
submodel that lists contained assets as `ReferenceElement` nodes.
Traverse from the Hall outward — assets do NOT reference back to their
hall.

```cypher
// 1. Find Hall AAS by name (idShort acceptable here — purely identification)
MATCH (hall:AssetAdministrationShell)
WHERE hall.idShort CONTAINS 'Hall'
RETURN hall.idShort, hall.id

// 2. From the Hall's HierarchicalStructures submodel, walk to contained assets
MATCH (hall:AssetAdministrationShell {idShort: 'Hall4'})-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept
        {id: 'https://admin-shell.io/idta/HierarchicalStructures/1/1'})
MATCH (sm)-[:HAS_ELEMENT*]->(ref:ReferenceElement)-[:HAS_VALUE]->(contained)
RETURN contained.idShort, labels(contained)
```

If the second query returns zero rows, list which semanticIds Hall4's
submodels actually carry — the HierarchicalStructures URI in this graph
may differ.

## Recipe B — "Where's the manual for this MiR100?" (instance → type → docs)

Per VDI 2770, product-level documentation lives on the *type* AAS, not
the instance. Walk `DERIVED_FROM`, then call `search_aas_documents`
scoped by the type's HandoverDocumentation submodel.

```cypher
// 1. instance → type
MATCH (instance:AssetAdministrationShell {id: $instanceId})
      -[:DERIVED_FROM]->(type:AssetAdministrationShell)
RETURN type.id

// 2. type → HandoverDocumentation submodel
MATCH (type:AssetAdministrationShell {id: $typeId})-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $handoverDocSemanticId})
RETURN sm.id
```

Then: `search_aas_documents(query=..., submodel_id=<sm.id from step 2>)`.

The `$handoverDocSemanticId` comes verbatim from
`get_templates_index()` — do not type it from memory.

## Recipe E — Reading name / designation fields (MultiLanguageProperty)

Nameplate fields like `ManufacturerName`, `ManufacturerProductDesignation`,
`ManufacturerProductFamily` are `MultiLanguageProperty` — they have **no
`.value` property**. Their text lives in `(:LangString)` nodes:

```cypher
MATCH (aas:AssetAdministrationShell {id: $aasId})-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $nameplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(el)
MATCH (el)-[:HAS_VALUE]->(ls:LangString)
RETURN el.idShort AS field, ls.language AS lang, ls.text AS value
```

If you see `value: null` on a Nameplate element, it is almost certainly
a MultiLanguageProperty — traverse `HAS_VALUE` instead of reading `.value`.

## Recipe F — Serial number (instance-specific, not on type)

`SerialNumber` is an instance-specific field. It lives on the **instance
AAS** Nameplate, not the type AAS. Searching the type shell for a serial
number will always return zero rows — the type represents the product
class, not a physical unit.

```cypher
// WRONG — searching type shell
MATCH (type:AssetAdministrationShell {id: 'urn:aas:mir100:type'})
      -[:HAS_SUBMODEL]->(sm)-[:HAS_ELEMENT*]->(el)
WHERE el.idShort = 'SerialNumber'   // will always be empty

// RIGHT — search instance shell
MATCH (instance:AssetAdministrationShell {id: $instanceId})
      -[:HAS_SUBMODEL]->(sm)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $nameplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(el {idShort: 'SerialNumber'})
RETURN el.value
```

## Recipe C — "Which asset is the transport robot in hall 4?"
(domain classification via capability)

User vocabulary ("transport robot") never matches `idShort`. Functional
categories live on `Capability` elements with a project- or
IDTA-supplied semanticId.

1. From recipe A, get the assets in hall 4.
2. For each, list capabilities:
   ```cypher
   MATCH (aas:AssetAdministrationShell {id: $assetAasId})
         -[:HAS_SUBMODEL]->(:Submodel)-[:HAS_ELEMENT*]->(c:Capability)
   OPTIONAL MATCH (c)-[:HAS_SUPPLEMENTAL_SEMANTIC_ID]->(sup:SemanticConcept)
   OPTIONAL MATCH (c)-[:HAS_SEMANTIC_ID]->(sem:SemanticConcept)
   RETURN aas.idShort, c.idShort, sem.id, collect(sup.id)
   ```
3. Match capabilities whose semanticId carries `Transport`
   (project namespace
   `https://aas-hybrid-mcp.dfki.de/capability/Transport`) — these are
   the transport robots.

## Recipe D — "I have no idea what's on this shell"
(diagnostic listing)

When a user gives an asset reference but you have nothing else to go
on, list its submodels with their templates first — almost every
follow-up question becomes obvious from the result.

```cypher
MATCH (aas:AssetAdministrationShell {id: $aasId})-[:HAS_SUBMODEL]->(sm:Submodel)
OPTIONAL MATCH (sm)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN sm.idShort, sm.id, sc.id AS templateSemanticId
```

For each `templateSemanticId` in the result, look it up in
`get_templates_index()` to learn what kind of submodel it is. If a
semanticId is not in the index, the shell uses a custom one — query
its elements directly to see what's there.

**Next:** `get_manual_page("troubleshooting")` if any step in a recipe
returned zero rows.
"""


_PAGES = {
    "cypher": _CYPHER,
    "templates": _TEMPLATES,
    "writing": _WRITING,
    "troubleshooting": _TROUBLESHOOTING,
    "recipes": _RECIPES,
}


def register(mcp: FastMCP) -> None:
    """Register operator-manual tools."""

    @mcp.tool(description=load_description("get_manual_index"))
    def get_manual_index() -> str:
        """Operator manual index. Cheap to call repeatedly; static content."""
        return _INDEX

    @mcp.tool(description=load_description("get_manual_page"))
    def get_manual_page(page: str) -> str:
        """Return one sub-page of the operator manual."""
        content = _PAGES.get(page.lower())
        if content is None:
            return (
                f"Unknown page '{page}'. Valid pages: "
                + ", ".join(_PAGES)
            )
        return content
