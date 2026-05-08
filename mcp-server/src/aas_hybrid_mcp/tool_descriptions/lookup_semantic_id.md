Resolve a semanticId (IRDI like `0173-1#02-ABL884#002`, or IRI like
`https://admin-shell.io/...`) to its IEC 61360 ConceptDescription content:
preferredName, shortName, definition, dataType, and unit — multilingual
where available.

Use this whenever a graph traversal returns a `:SemanticConcept.id` that
the agent does not recognise, or when the user asks what an unfamiliar
IRDI means.

Three response classes:

1. `resolved=true` — the CD is registered in the local repository
   (project-namespace CDs shipped in the AASX, or IDTA-template CDs
   pushed at sync time). The full IEC 61360 payload is returned.

2. `resolved=false` with `reason="no local definition ..."` — the id
   is not registered locally. This is the expected answer for raw
   ECLASS IRDIs whose dictionary content is not redistributed under
   our license. Communicate this transparently to the user as a
   standardised external reference rather than fabricating semantics.

3. `resolved=false` with `error=...` — the BaSyx repository was
   unreachable or returned an unexpected status.

Pair this with `query_aas_graph` for the canonical discovery flow:
Cypher returns a `:SemanticConcept.id`, `lookup_semantic_id` resolves
it to human-readable semantics. Never reason about a property by its
`idShort` when its `semanticId` can be resolved.
