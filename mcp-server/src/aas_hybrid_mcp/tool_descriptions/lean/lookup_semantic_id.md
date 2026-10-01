Resolve a semanticId (IRDI or IRI) to its IEC 61360 ConceptDescription: preferredName, shortName, definition, dataType, unit.
INPUT: `id` (str).
OUTPUT: `resolved=true` with the content, or `resolved=false` with `reason` (no local definition) or `error` (repository unreachable).
