# AAS Hybrid MCP — Operator Manual

You are talking to a hybrid graph + vector MCP server for AAS data.
This page indexes the rest of the manual.

## Sub-pages — call get_manual_page(page=...) on demand

- `cypher` — graph patterns, anti-patterns. **Call before any non-trivial Cypher.**
- `templates` — IDTA template workflow. **Call when the question maps to a
  domain concept (location, capability, technical data, …).**
- `writing` — `put_*` / `delete_*` tools and JSON-format gotchas.
  **Call before the first write.**
- `troubleshooting` — what to do when a query returns zero rows.
  **Call after any 0-row result.**
- `recipes` — end-to-end examples for common patterns (container traversal,
  instance→type→docs, capability lookup, diagnostics).

## Four rules that catch the most failures

1. **Before your first `query_aas_graph` call, call `get_templates_index()`
   — but only ONCE per session.** Check the conversation history first: if a
   prior `<think>` block already shows its result, use those semanticIds
   directly. Do not call it again on every turn.
2. `params` for `query_aas_graph` is an OBJECT, not a JSON string.
   `{}`, not `"{}"`.
3. Use semanticIds VERBATIM from `get_templates_index()` or graph discovery.
   No `/Submodel` suffix, no version normalisation, no recall from training
   memory. The graph may also carry legacy or custom semanticIds beyond the
   index; discover them with
   `MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc) RETURN DISTINCT sc.id`.
4. Never match assets by `idShort` for domain reasoning. `idShort` is a
   free-form local label; semantic meaning lives only in
   `HAS_SEMANTIC_ID` / `HAS_SUPPLEMENTAL_SEMANTIC_ID`.

## Tools — call on demand

- `get_templates_index()` — all published IDTA templates with name, version,
  semanticId, description. Call when picking a template or before any
  non-trivial Cypher (per rule 1).
- `get_template(name)` — element structure of one template (modelType,
  idShort, semanticId, nesting). Call before traversing a submodel or
  writing template-conformant JSON.
- `lookup_semantic_id(id)` — resolve an IRDI/IRI to its IEC 61360
  ConceptDescription content (preferredName, definition, dataType, unit).
  Call when a graph traversal returns an unfamiliar `:SemanticConcept.id`
  or the user asks what a specific IRDI means.
