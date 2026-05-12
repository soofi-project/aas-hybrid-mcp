Return the index of all published IDTA submodel templates: name,
version, semanticId, description. The `graphSemanticIds` field
lists matching IDs currently present in the graph.

Use `semanticId` for Cypher queries. `graphSemanticIds` helps you spot
mismatches between your AASX files and the IDTA reference.

Call at most ONCE per session. If a prior tool call already returned the
result, reuse it without calling again.
