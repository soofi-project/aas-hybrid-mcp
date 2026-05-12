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

JSON rules when building `submodel_json` from a template (`get_template(name)`):
- The template's `elements` array maps to `submodelElements` in the submodel.
- A `SubmodelElementCollection` child list is stored under the key
  **`value`** (NOT `values`, NOT `children`).  The template uses `value`
  verbatim — copy it directly.
- An `Entity`'s statements are stored under the key **`statements`**.
- Every `Property` must carry a `valueType` (e.g. `xs:string`,
  `xs:integer`, `xs:double`, `xs:boolean`, `xs:dateTime`).  The template
  already includes `valueType` — never omit it.
- Nested structures must use the same `value` / `statements` keys at every
  level.

Minimal example:
{
  "modelType": "Submodel",
  "id": "urn:submodel:example:001:report",
  "idShort": "Report",
  "kind": "Instance",
  "submodelElements": [
    {
      "modelType": "SubmodelElementCollection",
      "idShort": "Readings",
      "value": [
        {"modelType": "Property", "idShort": "Temperature", "value": "42.5", "valueType": "xs:string"}
      ]
    }
  ]
}

OUTPUT: `{"status": "ok", "id": "<submodel-id>"}` or `{"error": "…"}`.
