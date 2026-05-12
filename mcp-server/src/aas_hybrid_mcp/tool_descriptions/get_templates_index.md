**Call early in your plan (once per session)** — results are cached, don't plan repeated calls. Returns all published IDTA templates with name, version, semanticId, description. `graphSemanticIds` shows which IDs actually exist in the graph — use it to spot mismatches between your AASX files and the IDTA reference. Use `semanticId` verbatim for Cypher queries.

Return the index of all published IDTA submodel templates: name,
version, semanticId, description. The `graphSemanticIds` field
lists matching IDs currently present in the graph.
