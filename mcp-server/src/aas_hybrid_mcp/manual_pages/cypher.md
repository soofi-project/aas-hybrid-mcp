# Cypher patterns and anti-patterns

**Pre-condition.** Call `get_graph_schema()` (relationship labels) and
`get_templates_index()` (verbatim semanticIds) before composing any
Cypher. Invented labels and semanticIds are the largest source of
zero-row results.

## Anti-patterns

**1. `semanticId` is a relation, not a property.**
```cypher
// WRONG
MATCH (sm:Submodel {semanticId: 'https://...'})

// RIGHT
MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: 'https://...'})
```

**2. Use semanticIds verbatim.** Exact strings from `get_templates_index()`
or graph discovery. Do not append `/Submodel`, change versions, or
recall URIs from training memory.

**3. `assetType` and `assetKind` are often null.**
Use `DERIVED_FROM` for type vs instance; use submodel semanticIds for
domain classification.

**4. Never use `idShort` for domain reasoning.**
Acceptable as an entry point when the user explicitly names an asset —
but do not derive purpose or structure from `idShort`. Verify via
submodels and their semanticIds.

Unrecognised `SemanticConcept.id` values: call `lookup_semantic_id(id)`
to resolve to human-readable semantics.

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

All submodels conforming to a given template across all shells:
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

Container traversal — a container submodel owns an Entity tree linked
to the contained assets:
```cypher
MATCH (container:AssetAdministrationShell)-[:HAS_SUBMODEL]->(sm:Submodel)
      -[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: $containerTemplateSemanticId})
MATCH (sm)-[:HAS_ELEMENT*]->(parent:Entity)-[:HAS_ELEMENT]->(child:Entity)
MATCH (child)-[:REPRESENTS_ASSET]->(asset:Asset)
RETURN container.idShort, parent.idShort, child.idShort, asset.globalAssetId
```

**Next:** `get_manual_page("troubleshooting")` on zero-row results;
`get_manual_page("recipes")` for end-to-end worked examples.
