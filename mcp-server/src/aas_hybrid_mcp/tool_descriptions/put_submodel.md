**Before the first write in a session, call `get_manual_page("writing")`** — it covers JSON-format gotchas and the template-read-first workflow. **Before calling: obtain the template name from `get_templates_index()` and element structure from `get_template(name)`.** Use `semanticId` verbatim from the template. Pass `submodel_json` as a JSON string. SDK validates before any HTTP call.

Create or replace a Submodel under an AssetAdministrationShell. Idempotent.

INPUT: `aas_id` (URI) + `submodel_json` (JSON string of the full Submodel object).
Required fields: `modelType` ("Submodel"), `id` (URI), `idShort`.

OUTPUT: `{"status": "ok", "id": "<submodel-id>"}` or `{"error": "..."}`.
