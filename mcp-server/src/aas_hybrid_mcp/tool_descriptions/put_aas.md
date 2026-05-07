Create or replace an AssetAdministrationShell in the BaSyx environment.
Idempotent: if the shell already exists it is fully replaced; otherwise it
is created. The graph and vector store sync automatically via Kafka after the
write — no manual re-ingestion required.

INPUT: `aas_json` — the complete AssetAdministrationShell serialised as a
JSON **string** (call `json.dumps` if you constructed a dict). Required
fields: `modelType` ("AssetAdministrationShell"), `id` (URI), `assetInformation`.
The SDK validates the full structure before any HTTP call; validation errors
are returned as `{"error": "…"}` for self-correction — nothing is written.

OUTPUT: `{"status": "ok", "id": "<aas-id>"}` on success, or
`{"error": "…"}` on validation or HTTP failure.
