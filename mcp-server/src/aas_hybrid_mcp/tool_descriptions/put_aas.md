**Before the first write in a session, call `get_manual_page("writing")`** — it covers JSON-format gotchas and the template-read-first workflow. The `aas_json` argument must be a JSON string, not a dict. SDK validates the full structure before any HTTP call — validation errors return an error for self-correction, nothing is written.

Create or replace an AssetAdministrationShell. Idempotent: if it exists
already it is fully replaced; otherwise created. Changes propagate
automatically to the graph and document store — no manual re-ingestion required.

Required fields: `modelType` ("AssetAdministrationShell"), `id` (URI), `assetInformation`.

OUTPUT: `{"status": "ok", "id": "<aas-id>"}` on success, or `{"error": "..."}` on
validation or HTTP failure.
