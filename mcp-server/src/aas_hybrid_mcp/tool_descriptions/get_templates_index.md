Return the index of all published IDTA submodel templates: name,
version, semanticId, description.

Call this to discover which template covers a domain concept (location,
capability, maintenance, technical data, …) and to obtain the verbatim
semanticId for Cypher queries.

Call at most ONCE per session — the index is static. If a prior tool
call in this conversation already returned the result, reuse it without
calling again.
