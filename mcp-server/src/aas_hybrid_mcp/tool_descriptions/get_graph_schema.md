**Call early in your plan (once per session)** — small, fast, essential. Returns node labels, relationship types, and the anti-patterns section covering the most common Cypher mistakes. Read the `HAS_SEMANTIC_ID` relationship section and the `HAS_VALUE` / MultiLanguageProperty section before writing any Cypher.

Return the AAS graph schema — node labels, relationship types, the
SubmodelElement subtype catalogue, MultiLanguageProperty traversal via
`HAS_VALUE`, and an anti-patterns section covering the most common Cypher
mistakes.

Call this before composing any non-trivial Cypher query. Zero rows almost
always trace back to a wrong relationship label or a forgotten `HAS_VALUE`
step — both documented here.
