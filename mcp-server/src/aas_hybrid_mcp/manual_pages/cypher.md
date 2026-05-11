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

When a traversal returns a `:SemanticConcept.id` you do not recognise
(e.g. a raw ECLASS IRDI like `0173-1#02-ABL884#002`), call
`lookup_semantic_id(id)` to resolve it to its IEC 61360 payload
(preferredName, definition, dataType, unit). If the tool returns
`resolved=false`, the IRDI is a standardised external reference whose
dictionary content is not available locally — say so transparently
rather than fabricating a meaning.

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
