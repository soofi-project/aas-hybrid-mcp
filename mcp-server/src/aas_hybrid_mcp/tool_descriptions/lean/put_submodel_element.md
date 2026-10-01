Create or replace a SubmodelElement inside an existing Submodel (idempotent).
INPUT: `submodel_id` (URI), `id_short_path` (dot-separated from the submodel root, e.g. `Items.0.Label`), `element_json` (JSON string).
OUTPUT: `{"status": "ok"}` or `{"error": ...}`. A non-existent Submodel is rejected.
