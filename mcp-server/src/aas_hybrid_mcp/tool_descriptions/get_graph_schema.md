Return the AAS Neo4j graph schema — node labels, relationship types, the
SubmodelElement subtype catalogue, MultiLanguageProperty traversal via
`HAS_VALUE`, and an anti-patterns section covering the most common Cypher
mistakes.

Call this before composing any non-trivial Cypher query. Zero rows almost
always trace back to a wrong relationship label or a forgotten `HAS_VALUE`
step — both documented here.
