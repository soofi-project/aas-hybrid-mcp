# When retrieval is empty

A zero-row Cypher result or empty document-search result means your
query was wrong, NOT that the data is missing. Stopping early —
"there's no such data" — after a single failed query is a failure
mode. Before concluding the data is absent, exhaust all of these moves:

1. **Sanity-check against the schema.** If you filtered on a property
   like `semanticId`, you almost certainly meant the
   `HAS_SEMANTIC_ID` relation. See `get_graph_schema()` anti-patterns.
2. **Open the search.** Drop the most restrictive clause (a hard `=`
   filter, an exact-string match) and re-run with `CONTAINS` /
   case-insensitive comparison or no filter at all to see what is
   actually in the graph.
3. **List the actual semanticIds.** If you assumed a current IDTA URI
   and got nothing, the graph may carry an older or alternative URI
   variant. Run the `RETURN DISTINCT sc.id` discovery query from
   `get_manual_page("cypher")`.
4. **Re-skim the templates index.** If you assumed a specific template
   carries the answer and the submodel isn't there, a sibling template
   may. The index is at `get_templates_index()`.
5. **Walk type ↔ instance.** If the question is about an instance and
   you came up empty, the answer probably lives on its type AAS via
   `DERIVED_FROM` (and vice-versa for instance-specific records like
   serial number, calibration certificates, delivery protocols — those
   live on the *instance*, not the type).
5a. **`value: null` on text-carrying elements means MultiLanguageProperty.**
   Read `.text` / `.language` via `(el)-[:HAS_VALUE]->(:LangString)`.
6. **List what *is* on the shell.** Run the
   "submodels of a shell with their templates" recipe from
   `get_manual_page("cypher")`; the actual contents will usually point you
   at the right path.

Only after all moves have been tried may you state the gap. State it
specifically — name the templates you checked, the semanticIds you
searched for, and what the graph actually contains:

> *"No AAS in the graph carries a submodel for X (template Y). The
> closest matches I see are A, B, C — let me know if one of those is
> what you mean."*

Do not say "you would need to add this data" after a single failed
query. Do not silently substitute generic advice for missing data.

**Next:** `get_manual_page("recipes")` for end-to-end worked examples that
exercise these moves.
