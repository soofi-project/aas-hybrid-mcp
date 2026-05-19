**Call before any `query_aas_graph`, `search_aas_documents`, or `get_graph_schema` call.** Start with `cypher` — it contains the anti-patterns that cause the most failures.

Return a sub-page of the operator manual. Valid pages:
  cypher          — Cypher patterns and anti-patterns
  templates       — IDTA template workflow
  writing         — put_*/delete_* tools and JSON gotchas
  troubleshooting — what to do on zero-row results
   recipes         — end-to-end worked examples
   mapping         — AAS field → graph relationship mapping
