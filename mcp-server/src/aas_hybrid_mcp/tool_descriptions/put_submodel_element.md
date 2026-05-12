**Before calling: obtain element structure from `get_template(name)`.** Know the correct `modelType`, `idShort`, and nesting before creating the JSON. Pass `element_json` as a JSON string. `id_short_path` is dot-separated from the submodel root (e.g. `MarkingsObject.0.MarkingFile`). SDK validates before HTTP.

Create or replace a SubmodelElement (all subtypes: Property, File, SMC, SML, Entity, Operation, etc.) under an existing Submodel. Idempotent.

INPUT: `submodel_id` (URI), `id_short_path` (dot-separated path), `element_json` (JSON string).

OUTPUT: `{"status": "ok"}` or `{"error": "..."}`.
