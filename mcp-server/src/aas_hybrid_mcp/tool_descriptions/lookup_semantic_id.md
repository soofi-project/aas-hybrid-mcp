**Before calling: obtain the semanticId from a `query_aas_graph` result** — look for the `SemanticConcept.id` value on `HAS_SEMANTIC_ID` / `HAS_SUPPLEMENTAL_SEMANTIC_ID` relationships. Don't paste raw IRDIs from memory.

Resolve a semanticId (IRDI like `0173-1#XX-ABC123#001`, or IRI like
`https://admin-shell.io/...`) to its IEC 61360 ConceptDescription content:
preferredName, shortName, definition, dataType, and unit — multilingual
where available.

Three response classes:

1. `resolved=true` — the CD is registered in the local repository
   (project-namespace CDs shipped in the AASX, or IDTA-template CDs
   pushed at sync time). The full IEC 61360 payload is returned.

2. `resolved=false` with `reason="no local definition ..."` — the id
   is not registered locally. This is the expected answer for raw
   ECLASS IRDIs whose dictionary content is not redistributed under
   our license. Communicate this transparently to the user as a
   standardised external reference rather than fabricating semantics.

3. `resolved=false` with `error=...` — the AAS repository was
   unreachable or returned an unexpected status.

Pair with `query_aas_graph`: Cypher returns a `SemanticConcept.id`, this tool
resolves it to human-readable semantics. Never reason about a property by its
`idShort` when its `semanticId` can be resolved.
