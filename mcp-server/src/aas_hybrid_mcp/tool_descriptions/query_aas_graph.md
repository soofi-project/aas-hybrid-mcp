**Before first use: plan `get_graph_schema()` and `get_templates_index()` in parallel** — they return the relationship labels and semantic IDs you need to write correct Cypher. Don't guess either from memory.

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

COMPOSITION: this tool resolves the *structural* part of a question. For
PDF content, pass the discovered `submodel_id` to `search_aas_documents`.
To identify the domain function of an asset, use `search_idta_templates`
to find the relevant capability template, then query its semanticId via
`HAS_SUPPLEMENTAL_SEMANTIC_ID`.

INPUT: Cypher with `$paramName` placeholders + a `params` dict. Write
operations are rejected at the driver level.
OUTPUT: rows as a list of dicts; capped at 1000 rows (the response carries
`total` and `truncated` for paging decisions).
