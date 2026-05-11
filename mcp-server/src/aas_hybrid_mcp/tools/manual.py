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
- `recipes` — worked end-to-end examples (container traversal, instance → type
   → docs, capability lookup, diagnostic listing).
- `mapping` — AASX field → Neo4j graph mapping. **Call when you need to know
   how an AAS type (Entity, SMC, etc.) maps to Neo4j relationships.**

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
4. Never use `idShort` for **domain reasoning** or **capability matching**.
   `idShort` is a free-form local label. Using it to identify a shell the
   user named (e.g. "Hall 4") is acceptable as a starting point — but
   always verify what the shell actually contains by listing its submodels
   and their template semanticIds. Semantic meaning lives only in
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
room, or factory section. Physical location and containment hierarchy
live in submodels whose template describes such concepts (discovered
via `HAS_SEMANTIC_ID`). Check `get_templates_index()` for templates
whose description mentions location, hierarchy, or containment.

**2. `semanticId` is a relation, not a property.**
```cypher
// WRONG — silently returns 0 rows
MATCH (sm:Submodel {semanticId: 'https://...'}) ...

// RIGHT
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: 'https://...'}) ...
```

**3. Use semanticIds verbatim — do not enrich them.**
The exact strings come from `get_templates_index()` or the graph's
discovery query. Do not append `/Submodel`, change version numbers,
or recall URIs from training memory. For example, if the index says
`https://example.com/template/1/0`, match that exact string — not
`.../1/0/Submodel` or `.../2/0`.

**4. `assetType` and `assetKind` are optional and often null.**
Use `(:AssetAdministrationShell)-[:DERIVED_FROM]->` for type vs.
instance distinction; use submodel semanticIds for domain
classification.

**5. Never use `idShort` for domain reasoning.**
`idShort` is a free-form local label chosen by the shell author.
Using it to locate a shell the user explicitly named is acceptable as an
entry point — but do not derive its purpose, capabilities, or containment
structure from `idShort` alone. Verify by listing the shell's submodels
and their template semanticIds. Domain classification, capability matching,
and template conformance must be expressed via `HAS_SEMANTIC_ID` /
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

Container traversal — a container AAS (hall, cell, ...) owns a submodel
whose template carries an Entity tree for contained assets:
```cypher
MATCH (container:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(parent:Entity)-[:HAS_ELEMENT]->(child:Entity)
MATCH (child)-[:REPRESENTS_ASSET]->(asset:Asset)
RETURN container.idShort, parent.idShort, child.idShort, asset.globalAssetId
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
conforms to a template. Your job is to translate user intent → template
→ semanticId → graph traversal. Don't invent ad-hoc Cypher patterns and
don't recall semanticIds from training memory.

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
templates index lists one version, but a graph populated from older AASX
files may carry a ZVEI or older variant instead. Filtering on the
current IDTA ID returns zero rows.

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

## Recipe A — "What's in X?" (container traversal)

A container AAS (hall, cell, production line, …) typically has a submodel
whose template describes a containment hierarchy of `Entity` nodes, each
linked to `:Asset` via `REPRESENTS_ASSET`.

1. Find the container AAS — identify it from the user's question.
2. Discover which of its submodels carry containment data:
   ```cypher
   MATCH (aas:AssetAdministrationShell {idShort: $containerIdShort})-[:HAS_SUBMODEL]->(sm:Submodel)
   OPTIONAL MATCH (sm)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
   RETURN sm.idShort, sc.id AS templateSemanticId
   ```
3. Pick the submodel whose template describes containment (check
   `get_templates_index()` or `get_template(name)`), then traverse:
   ```cypher
   MATCH (container:AssetAdministrationShell {idShort: $containerIdShort})
         -[:HAS_SUBMODEL]->(sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept {id: $templateId})
   MATCH (sm)-[:HAS_ELEMENT*]->(parent:Entity)-[:HAS_ELEMENT]->(child:Entity)
   MATCH (child)-[:REPRESENTS_ASSET]->(asset:Asset)
   RETURN parent.idShort, child.idShort, asset.globalAssetId
   ```

If step 3 returns zero rows, the nesting may be flat (no parent/child
Entity tree). Try:
```cypher
MATCH (sm)-[:HAS_ELEMENT*]->(e:Entity)-[:REPRESENTS_ASSET]->(a:Asset)
RETURN e.idShort, a.globalAssetId
```

## Recipe B — "Where's the documentation for this asset?" (instance → type → docs)

In many deployments, product-level documentation lives on the *type*
AAS while instance-specific data lives on the *instance*. Walk
`DERIVED_FROM`, then call `search_aas_documents` scoped by the relevant
type submodel.

```cypher
// 1. instance → type
MATCH (instance:AssetAdministrationShell {id: $instanceId})
      -[:DERIVED_FROM]->(type:AssetAdministrationShell)
RETURN type.id

// 2. type → relevant documentation submodel
MATCH (type:AssetAdministrationShell {id: $typeId})-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $docSemanticId})
RETURN sm.id
```

Then: `search_aas_documents(query=..., submodel_id=<sm.id from step 2>)`.

The `$docSemanticId` comes verbatim from `get_templates_index()` — do not
type it from memory.

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
MATCH (type:AssetAdministrationShell {id: 'urn:example:aas:MyProduct:type'})
      -[:HAS_SUBMODEL]->(sm)-[:HAS_ELEMENT*]->(el)
WHERE el.idShort = 'SerialNumber'   // will always be empty

// RIGHT — search instance shell
MATCH (instance:AssetAdministrationShell {id: $instanceId})
      -[:HAS_SUBMODEL]->(sm)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $nameplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(el {idShort: 'SerialNumber'})
RETURN el.value
```

## Recipe C — Category classification via capability

User vocabulary (e.g. "transport robot", "welding station") never matches `idShort`. Functional
categories live on `Capability` elements with a project- or
IDTA-supplied semanticId.

1. From recipe A, get the contained assets.
2. For each, list capabilities:
   ```cypher
   MATCH (aas:AssetAdministrationShell {id: $assetAasId})
         -[:HAS_SUBMODEL]->(:Submodel)-[:HAS_ELEMENT*]->(c:Capability)
   OPTIONAL MATCH (c)-[:HAS_SUPPLEMENTAL_SEMANTIC_ID]->(sup:SemanticConcept)
   OPTIONAL MATCH (c)-[:HAS_SEMANTIC_ID]->(sem:SemanticConcept)
   RETURN aas.idShort, c.idShort, sem.id, collect(sup.id)
   ```
3. Match capabilities whose semanticId or the SemanticConcept's
   preferredName (via `lookup_semantic_id`) contains the domain term
   the user mentioned. The exact URI prefix is project-specific —
   discover it from the graph, don't assume it.

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


_MAPPING = """\
# AASX field → Neo4j graph mapping

Shows how the Kafka Connect plugin (aas-repository-neo4j-kafka-plugin)
maps each AAS4J type's fields to Neo4j node labels and relationship types.
Derived from the `*Node` mapping classes in the plugin's source code.

## Common labels

Every node carries `:GraphNode`. Referable nodes add `:Referable`,
`:Referenceable`. Identifiable nodes add `:Identifiable` on top.

Every SubmodelElement gets `:SubmodelElement` plus its concrete type label
(e.g. `:Property`, `:Entity`, `:Operation`).

## Top-level nodes

| AAS Type | JSON/Java field | Neo4j relationship | Target |
|---|---|---|---|
| AssetAdministrationShell | `assetInformation` | `MANAGES_ASSET` | `:Asset` |
| | `submodels` | `HAS_SUBMODEL` | `:Submodel` |
| | `derivedFrom` | `DERIVED_FROM` | `:AssetAdministrationShell` |
| | `administration` | `HAS_ADMIN_INFO` | `:AdminInfo` |

## SubmodelElements — containment slots

These are the source of the most traversal bugs. Read the **Key insight**
below carefully.

| AAS Type | JSON/Java field | Neo4j relationship | Notes |
|---|---|---|---|
| Submodel | `submodelElements` | `HAS_ELEMENT` | Direct children only |
| SubmodelElementCollection | `value` | `HAS_ELEMENT` | Nested child elements |
| SubmodelElementList | `value` | `HAS_ELEMENT` | List items |
| SubmodelElementList | `semanticIdListElement` | `HAS_SEMANTIC_ID_LIST_ELEMENT` | Per-item semantic ref |
| **Entity** | **`statements`** | **`HAS_ELEMENT`** | **Child entities — see Key insight** |
| Entity | `globalAssetId` | `REPRESENTS_ASSET` | `:Asset` (from the ID string) |
| Entity | `specificAssetIds` | `HAS_SPECIFIC_ASSET_ID` | `:SpecificAssetId` |
| ReferenceElement | `value` | `HAS_VALUE` | Cross-reference to target node |

### Key insight — Entity.statements is HAS_ELEMENT

Entity.statements is mapped to the **same relationship label** as
SubmodelElementCollection children and SubmodelElementList items:
`HAS_ELEMENT`. This means that `[:HAS_ELEMENT*]` descends through
nested Entity trees seamlessly. There is no separate relationship for
Entity containment.

**Example — container AAS with an Entity tree (generic):**

Any container-style submodel that contains entities for contained assets.
First, discover which submodel template carries the containment structure
via `get_templates_index()` and `get_template(name)`, then determine the
Entity idShorts from `get_template(name)` — they vary by template:

```cypher
// Identify the container template semanticId via get_templates_index()
// Determine entity nesting from get_template(name)
MATCH (container:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(parent:Entity)
MATCH (parent)-[:HAS_ELEMENT]->(child:Entity)
MATCH (child)-[:REPRESENTS_ASSET]->(asset:Asset)
RETURN container.idShort, parent.idShort, child.idShort, asset.globalAssetId
```

If the submodel contains only top-level entities (no parent/child nesting),
skip the intermediate `parent:Entity` step:

```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(e:Entity)
MATCH (e)-[:REPRESENTS_ASSET]->(a:Asset)
RETURN e.idShort, a.globalAssetId
```

## Value-bearing elements

| AAS Type | JSON/Java field | Neo4j | Details |
|---|---|---|---|
| Property | `value` | `.value` (property) | Scalar string on the node |
| Property | `valueType` | `.valueType` (property) | |
| Property | `valueId` | `HAS_VALUE_ID` | Reference target |
| MultiLanguageProperty | `value` (LangString[]) | `HAS_VALUE` | `:LangString` (.language, .text) |
| MultiLanguageProperty | `valueId` | `HAS_VALUE_ID` | Reference target |
| File | `value` | `.value` (property) | URL path |
| File | `contentType` | `.contentType` (property) | MIME type |
| Blob | `value` | `.value` (property) | Base64-encoded |
| Range | `min`, `max` | `.min`, `.max` (property) | |

## Relationship-bearing elements

| AAS Type | JSON/Java field | Neo4j relationship |
|---|---|---|
| RelationshipElement | `first`, `second` | `HAS_FIRST`, `HAS_SECOND` |
| AnnotatedRelationshipElement | `first`, `second` | `HAS_FIRST`, `HAS_SECOND` |
| AnnotatedRelationshipElement | `annotations` | `HAS_ANNOTATION` |
| Operation | `inputVariables` | `HAS_INPUT_VARIABLE` |
| Operation | `outputVariables` | `HAS_OUTPUT_VARIABLE` |
| Operation | `inoutputVariables` | `HAS_INOUTPUT_VARIABLE` |
| BasicEventElement | `observed` | `OBSERVES` |
| BasicEventElement | `messageBroker` | `USES_MESSAGE_BROKER` |

**Note:** Operation variables are wrapped in `OperationVariable` — the
plugin extracts `.value` from each, so the `HAS_*_VARIABLE` edges point
directly to the contained SubmodelElement.

## Shared metadata (every SubmodelElement)

Applied automatically by `AbstractSmeNode` — inherited by all SME types:

| JSON/Java field | Neo4j relationship |
|---|---|
| `semanticId` | `HAS_SEMANTIC_ID` |
| `supplementalSemanticIds` | `HAS_SUPPLEMENTAL_SEMANTIC_ID` |
| `qualifiers` | `HAS_QUALIFIER` |
| `description` | `HAS_DESCRIPTION` |
| `displayName` | `HAS_DISPLAY_NAME` |
| `extensions` | `HAS_EXTENSION` |
| `embeddedDataSpecifications` | `HAS_EMBEDDED_DATA_SPECIFICATION` |

## Auxiliary nodes

| AAS Type | JSON field | Neo4j relationship |
|---|---|---|
| AssetInformation | `specificAssetIds` | `HAS_SPECIFIC_ASSET_ID` |
| AdministrativeInformation | `embeddedDataSpecifications` | `HAS_EMBEDDED_DATA_SPECIFICATION` |
| AdministrativeInformation | `creator` | `CREATED_BY` |
| SpecificAssetId | `externalSubjectId` | `HAS_EXTERNAL_SUBJECT_ID` |
| SpecificAssetId | `semanticId` | `HAS_SEMANTIC_ID` |
| SpecificAssetId | `supplementalSemanticIds` | `HAS_SUPPLEMENTAL_SEMANTIC_ID` |

**Next:** `get_manual_page("cypher")` for traversal patterns and anti-patterns;
`get_graph_schema()` for the complete node/relationship catalogue.
"""


_PAGES = {
    "cypher": _CYPHER,
    "templates": _TEMPLATES,
    "writing": _WRITING,
    "troubleshooting": _TROUBLESHOOTING,
    "recipes": _RECIPES,
    "mapping": _MAPPING,
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
