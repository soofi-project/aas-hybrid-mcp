Delete a SubmodelElement at an idShortPath within a Submodel.

INPUT:
- `submodel_id` — the Submodel id URI (non-empty string)
- `id_short_path` — dot-separated path, e.g. `"Documents.Section1.File1"`
  (non-empty string)

OUTPUT: `{"status": "ok", "idShortPath": "…"}` or `{"error": "…"}`.
