# Write tools — `put_*` / `delete_*`

Six generic, symmetric tools cover the full mutation surface:

- `put_aas(aas_json)` — idempotent create-or-replace shell
- `delete_aas(aas_id)`
- `put_submodel(aas_id, submodel_json)` — idempotent
  create-or-replace submodel under a shell
- `delete_submodel(aas_id, submodel_id)`
- `put_submodel_element(submodel_id, id_short_path, element_json)` —
  covers ALL SubmodelElement subtypes (Property, File, SMC, SML,
  MultiLanguageProperty, Range, ReferenceElement, RelationshipElement,
  Entity, Operation, …) via a single tool
- `delete_submodel_element(submodel_id, id_short_path)`

Writes go through the AAS server; client-side SDK validation runs first,
so constraint violations (missing `semanticId`, wrong nesting, wrong
`modelType`) come back as an error you can react to.

## JSON-format gotchas

All `*_json` parameters are JSON STRINGS, not dicts. Pass the
serialised JSON of the AAS / Submodel / SubmodelElement object:
```
put_submodel(
  aas_id="https://example.com/aas/MyAsset",
  submodel_json='{"modelType":"Submodel","id":"https://...","idShort":"Nameplate", ...}'
)
```

`id_short_path` is a dot-separated path from the submodel root, e.g.
`MarkingsObject.0.MarkingFile` for the first MarkingFile in a
SubmodelElementList.

## Read template structure first

Before writing a submodel that should conform to a published IDTA
template:

1. Find the template name from `get_templates_index()`.
2. Read `get_template(name)` — gives you the modelType, idShort,
   semanticId, and full nesting structure.
3. Build your JSON from that skeleton. Set `semanticId` verbatim from
   the template; use the same idShorts.

Skipping this step is the most common cause of validation failures
on write.

## After writing

Changes propagate automatically to the graph and document store.
You can observe your write through `query_aas_graph` and
`search_aas_documents` — allow a second for propagation.

## Attachments

Binary `File` / `Blob` upload is not yet an MCP tool. Write the `File`
element metadata (contentType, empty value) via `put_submodel_element`;
the binary must be uploaded out-of-band.

**Next:** `get_manual_page("cypher")` to verify what you wrote;
`get_manual_page("troubleshooting")` if a write fails.
