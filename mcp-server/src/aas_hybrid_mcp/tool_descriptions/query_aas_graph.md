**Required before first use — call all three in parallel:**
- `get_manual_page("cypher")` — query patterns and anti-patterns (mandatory)
- `get_graph_schema()` — relationship labels and node properties
- `get_templates_index()` — semantic IDs for submodel templates

Do not skip these calls. Guessing Cypher patterns from memory produces anti-patterns that work on clean fixture data but fail silently in production.

**Anti-pattern — never use CONTAINS or =~ on idShort or id for asset lookup:**
```
-- WRONG (breaks on any non-trivial naming):
WHERE toLower(aas.idShort) CONTAINS 'my_robot'
-- CORRECT: exact match as entry point, then traverse by semanticId
WHERE aas.idShort = $idShort
```
See cypher.md anti-patterns #3 and #4 for the full list.

Execute a read-only Cypher query against the AAS knowledge graph.

WHEN TO USE: structural questions about the AAS environment — which shells
exist, which submodels they expose, which elements and properties those
submodels carry, and how shells relate to each other. Also for ID
resolution: turning a natural-language reference into a concrete AAS-ID by
matching properties or relationships.

GRAPH SHAPE — the Asset node has no outgoing relations:
  (:AssetAdministrationShell)-[:MANAGES_ASSET]->(:Asset)
  (:AssetAdministrationShell)-[:HAS_SUBMODEL]->(:Submodel)
                                   -[:HAS_ELEMENT*]->(:SubmodelElement)
  (:AssetAdministrationShell)-[:DERIVED_FROM]->(:AssetAdministrationShell)
                                   -- instance shell → type shell

CONTAINMENT QUESTIONS — "what is in / inside / installed in / contained in
<container>" (hall, truck, room, cabinet, machine): use ONLY the container
traversal (HAS_SUBMODEL -> HAS_ELEMENT* -> Entity -> REPRESENTS_ASSET).
Do NOT include the container's own asset (via MANAGES_ASSET) in the answer.
A hall is not "inside itself" — the shell-to-asset link is a modeling artifact
with no real-world meaning; the asking user (worker, operator) does not know it.
MANAGES_ASSET only answers identity questions: "which asset IS this shell" or
"what does shell X represent".

COMPOSITION: this tool resolves the *structural* part of a question. For
PDF content, pass the discovered `submodel_id` to `search_aas_documents`.
To identify the domain function of an asset, use `search_idta_templates`
to find the relevant capability template, then query its semanticId via
`HAS_SUPPLEMENTAL_SEMANTIC_ID`.

INPUT: Cypher with `$paramName` placeholders + a `params` dict. Write
operations are rejected at the driver level.
OUTPUT: rows as a list of dicts; capped at 1000 rows (the response carries
`total` and `truncated` for paging decisions).
