Delete an AssetAdministrationShell from the BaSyx environment by its id.

INPUT: `aas_id` — the full AAS id URI (non-empty string).

OUTPUT: `{"status": "ok", "id": "…"}` on success, or `{"error": "…"}` on
failure (including 404 if the shell does not exist).
