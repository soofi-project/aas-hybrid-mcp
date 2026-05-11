# Worked recipes

End-to-end examples for common patterns. These are **starting points**,
not prescriptive answers. Adapt the Cypher to your specific data model.

Each recipe assumes you have already read `get_manual_page("cypher")`
and (for steps involving templates) `get_templates_index()`.

## Recipe A — Container traversal (e.g. container AAS → contained assets)

A container AAS typically has a submodel whose template describes a
containment hierarchy of `Entity` nodes, each linked to `:Asset` via
`REPRESENTS_ASSET`.

1. Find the container AAS from the user's question.
2. Discover which of its submodels carry containment data:

```cypher
MATCH (aas:AssetAdministrationShell {idShort: $containerIdShort})-[:HAS_SUBMODEL]->(sm:Submodel)
OPTIONAL MATCH (sm)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN sm.idShort, sc.id AS templateSemanticId
```

3. Identify the template (check `get_templates_index()` or `get_template(name)`), then traverse:

```cypher
MATCH (container:AssetAdministrationShell {idShort: $containerIdShort})-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(parent:Entity)-[:HAS_ELEMENT]->(child:Entity)
MATCH (child)-[:REPRESENTS_ASSET]->(asset:Asset)
RETURN parent.idShort, child.idShort, asset.globalAssetId
```

**Notes:**
- If the traversal returns zero rows, the nesting may be flat (no parent/child). Try:
  `MATCH (sm)-[:HAS_ELEMENT*]->(e:Entity)-[:REPRESENTS_ASSET]->(a:Asset)`
- The `$containerTemplateSemanticId` must come from `get_templates_index()`.
- Never assume `idShort` for domain classification — use the template's semanticId.

## Recipe A-alt — Custom templates (e.g. FacilityInformation)

Some AAS implementations use **custom templates** for domain-specific
concepts not yet covered by IDTA standards. These have project-specific
URIs (e.g. `urn:custom:...` or a private HTTP namespace) instead of an
IDTA `admin-shell.io` URI.

First, list the actual semanticIds present in your graph to discover what
custom templates exist:

```cypher
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN DISTINCT sc.id ORDER BY sc.id
```

Look for non-IDTA URIs in the result (e.g. custom `urn:` or project-specific
namespaces). Once you have identified the custom template's semanticId,
use it just like an IDTA template:

```cypher
MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $customTemplateSemanticId})
RETURN aas.idShort, aas.id, sm.idShort, sm.id
```

**Notes:**
- Custom templates are valid AAS — they just aren't standardised by IDTA yet.
- The semanticId is the ground truth; never assume the name or structure.
- Use `get_template()` to retrieve the element structure for any template
  that appears in `get_templates_index()` **or** in your graph's discovery query.

## Recipe B — Instance → Type → Documentation

Per VDI 2770 and common practice, product-level documentation often lives on
the *type* AAS, while instance-specific data (serial number, calibration
certificates) live on the *instance* AAS.

```cypher
// 1. instance → type
MATCH (instance:AssetAdministrationShell {id: $instanceId})
      -[:DERIVED_FROM]->(type:AssetAdministrationShell)
RETURN type.id, type.idShort

// 2. type → relevant submodel (e.g. HandoverDocumentation)
MATCH (type:AssetAdministrationShell {id: $typeId})-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $submodelSemanticId})
RETURN sm.id, sm.idShort
```

Then use the discovered `sm.id` with `search_aas_documents` or
`query_aas_graph`.

## Recipe C — Domain classification via capabilities

Functional categories (e.g. "transport robot", "welding station") are
usually expressed on `Capability` elements with project- or standard-specific
semanticIds.

```cypher
MATCH (aas:AssetAdministrationShell {id: $assetId})-[:HAS_SUBMODEL]->(:Submodel)-[:HAS_ELEMENT*]->(c:Capability)
OPTIONAL MATCH (c)-[:HAS_SUPPLEMENTAL_SEMANTIC_ID]->(sup:SemanticConcept)
OPTIONAL MATCH (c)-[:HAS_SEMANTIC_ID]->(sem:SemanticConcept)
RETURN c.idShort, sem.id, collect(sup.id) AS supplementalIds
```

Look for semanticIds containing your target domain (e.g. `Transport`,
`Welding`, `Handling`) — but the exact naming convention is project-specific.

## Recipe D — Diagnostics: "What's on this shell?"

When you have an AAS ID but no idea what submodels it exposes:

```cypher
MATCH (aas:AssetAdministrationShell {id: $aasId})-[:HAS_SUBMODEL]->(sm:Submodel)
OPTIONAL MATCH (sm)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
RETURN sm.idShort, sm.id, sc.id AS templateSemanticId
```

For each template semanticId, look it up in `get_templates_index()` to learn
its purpose. If a semanticId is not in the index, query its elements directly.

## Recipe E — Reading MultiLanguageProperty fields

Some fields (e.g. name, designation) may be `MultiLanguageProperty` and have
**no `.value` property**. Their text lives in `(:LangString)` nodes:

```cypher
MATCH (aas:AssetAdministrationShell {id: $aasId})-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $nameplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(el)
MATCH (el)-[:HAS_VALUE]->(ls:LangString)
RETURN el.idShort AS field, ls.language AS lang, ls.text AS value
```

If you see `value: null` on an element, try traversing `HAS_VALUE` to
`LangString` nodes.

## Recipe F — What does this IRDI mean?

When Cypher returns a `:SemanticConcept.id` that is not in the templates
index and not visibly self-explanatory (e.g. an ECLASS IRDI like
`0173-1#02-ABL884#002`), resolve it with `lookup_semantic_id`:

```
lookup_semantic_id(id="0173-1#02-ABL884#002")
→ {
    "id": "0173-1#02-ABL884#002",
    "resolved": true,
    "preferredName": {"en": "<label>", "de": "<Label>"},
    "definition":    {"en": "<technical definition>"},
    "dataType": "REAL_MEASURE",
    "unit": "mm",
    ...
  }
```

Canonical flow when the user asks about a property by name:

1. `query_aas_graph` returns the property's value plus its
   `:SemanticConcept.id`.
2. `lookup_semantic_id(id)` returns the human-readable meaning.
3. Answer combines both — the value and what the value *means*.

If `resolved=false`, the IRDI is a standardised external reference
without local definition; report it as such instead of guessing.

**Next:** `get_manual_page("troubleshooting")` if any step returned zero rows.
