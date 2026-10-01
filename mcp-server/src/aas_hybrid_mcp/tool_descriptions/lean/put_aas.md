Create or replace an AssetAdministrationShell (idempotent).
INPUT: `aas_json` (JSON string; required fields `modelType`, `id`, `assetInformation`).
OUTPUT: `{"status": "ok", "id": ...}` or `{"error": ...}`. Validation runs before any write.
