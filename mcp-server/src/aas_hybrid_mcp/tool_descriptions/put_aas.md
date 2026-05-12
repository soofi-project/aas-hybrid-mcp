**The `aas_json` argument must be a JSON string, not a dict.** SDK validates the full structure before any HTTP call — validation errors return an error for self-correction, nothing is written.

Create or replace an AssetAdministrationShell in the BaSyx environment.
Idempotent: if the shell already exists it is fully replaced; otherwise it
is created. The graph and vector store sync automatically via Kafka after the
write — no manual re-ingestion required.

Required fields: `modelType` ("AssetAdministrationShell"), `id` (URI), `assetInformation`.

OUTPUT: `{"status": "ok", "id": "<aas-id>"}` on success, or `{"error": "..."}` on
validation or HTTP failure.
