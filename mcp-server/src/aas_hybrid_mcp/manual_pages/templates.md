# Template workflow

User questions map to a domain concept (location, containment,
capability, technical data, …). The answer lives in a submodel that
conforms to a specific template. Translate:
user intent → template → semanticId → graph traversal.

## Three-step lookup

1. **Skim `get_templates_index()`** for templates matching the concept.
2. **Confirm against the graph.** Only `-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id: ...})`
   proves conformance. If the index ID matches nothing, discover what
   the graph actually carries:
   ```cypher
   MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)
   RETURN DISTINCT sc.id ORDER BY sc.id
   ```
3. **Read `get_template(name)`** for field-level structure before
   composing traversals.

## When no template matches

A custom `semanticId` is the escape hatch for concepts not yet
standardised — finding one confirms the data is correctly modelled,
not missing. State the gap explicitly: name which template domains
exist in the graph, what you looked for, and offer the closest
matches. Do not fabricate the missing template.

## Legacy vs current URIs

Templates in the graph may carry older or alternative URIs that do not
match the published index. The same template concept can have multiple
URI variants across AASX files. When the index semanticId returns zero
rows, use the discovery query above to find what actually exists.

## Custom templates

`get_templates_index()` returns only standardised templates. The graph
may also carry custom templates with project-specific URIs. Discovery
is the same — use the `RETURN DISTINCT sc.id` query above.

**Next:** `get_manual_page("cypher")` for traversal patterns;
`get_manual_page("recipes")` for worked examples.
