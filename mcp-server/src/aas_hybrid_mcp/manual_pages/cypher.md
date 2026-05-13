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

**3. Use semanticIds verbatim.** Exact strings from `get_templates_index()`
or graph discovery. Do not append `/Submodel`, change versions, or
recall URIs from training memory.

**4. `assetType` and `assetKind` are often null.**
Use `DERIVED_FROM` for type vs instance; use submodel semanticIds for
domain classification.

**5. Never use `idShort` for domain reasoning.**
Acceptable as an entry point when the user explicitly names an asset —
but do not derive purpose or structure from `idShort`. Verify via
submodels and their semanticIds.

Unrecognised `SemanticConcept.id` values: call `lookup_semantic_id(id)`
to resolve to human-readable semantics.

**Next:** `get_manual_page("troubleshooting")` on zero-row results;
`get_manual_page("recipes")` for worked examples.
