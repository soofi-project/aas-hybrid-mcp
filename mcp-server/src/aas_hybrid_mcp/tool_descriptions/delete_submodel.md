Remove a Submodel from a given AAS and delete it from the repository.
Both the AAS reference and the submodel object are removed.

INPUT:
- `aas_id` — the parent AAS id URI (non-empty string)
- `submodel_id` — the Submodel id URI (non-empty string)

OUTPUT: `{"status": "ok", "id": "…"}` or `{"error": "…"}`.
