Create or replace a Submodel on a given AAS. Idempotent: creates the submodel
in the repository if absent, replaces it if present, and ensures the AAS
carries a reference to it. Kafka propagates the change to Neo4j and Weaviate
automatically.

Before calling: invoke `get_template(name)` for the target template's
element structure so the submodel conforms to the expected idShort hierarchy
and semanticIds.

INPUT:
- `aas_id` — the parent AAS id URI (non-empty string)
- `submodel_json` — complete Submodel object as a JSON **string**. Required
  fields: `modelType` ("Submodel"), `id` (URI). Include `semanticId` for
  template-conformant submodels. The SDK validates before any HTTP call.

OUTPUT: `{"status": "ok", "id": "<submodel-id>"}` or `{"error": "…"}`.
