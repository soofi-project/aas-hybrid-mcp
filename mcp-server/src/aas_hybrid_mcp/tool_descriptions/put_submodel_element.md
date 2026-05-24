**Before the first write in a session, call `get_manual_page("writing")`** — it covers JSON-format gotchas and the template-read-first workflow. **Before calling: obtain element structure from `get_template(name)`.** Know the correct `modelType`, `idShort`, and nesting before creating the JSON. Pass `element_json` as a JSON string. `id_short_path` is dot-separated from the submodel root (e.g. `Items.0.Label`). SDK validates before HTTP.

Create or replace a SubmodelElement (all subtypes: Property, File, SMC, SML, Entity, Operation, etc.) under an **existing** Submodel. Idempotent.

**Restriction:** This tool updates individual elements inside an already-existing Submodel. The server enforces this: calls against a non-existent Submodel are rejected. Do NOT use it to construct a new Submodel piece-by-piece — use `put_submodel` instead. If `put_submodel` fails validation, analyze the error, correct the payload, and retry. Only escalate to the user if you cannot resolve it yourself.

INPUT: `submodel_id` (URI), `id_short_path` (dot-separated path), `element_json` (JSON string).

OUTPUT: `{"status": "ok"}` or `{"error": "..."}`.
