Create or replace a Submodel under an AssetAdministrationShell (idempotent).
INPUT: `aas_id` (URI), `submodel_json` (JSON string; required fields `modelType`, `id`, `idShort`).
OUTPUT: `{"status": "ok", "id": ...}` or `{"error": ...}`. Validation runs before any write.
