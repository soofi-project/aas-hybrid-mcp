Create or replace a SubmodelElement at an idShortPath within a Submodel.
Idempotent: replaces the element if the path exists, creates it otherwise.

Covers all SubmodelElement subtypes — Property, MultiLanguageProperty, File,
Blob, Range, SubmodelElementCollection, SubmodelElementList, ReferenceElement,
RelationshipElement, Entity, Operation, BasicEventElement, Capability — via
the `modelType` field. The SDK validates the element structure by wrapping it
in a temporary Submodel envelope before any HTTP call.

INPUT:
- `submodel_id` — the Submodel id URI (non-empty string)
- `id_short_path` — dot-separated path to the element, e.g. `"Documents"`
  for a root element or `"Documents.Section1.File1"` for a nested element.
  Every segment except the last must be an existing parent's idShort.
- `element_json` — the SubmodelElement as a JSON **string**. Required fields:
  `modelType` (e.g. "Property", "SubmodelElementCollection") and `idShort`.

OUTPUT: `{"status": "ok", "idShortPath": "…"}` or `{"error": "…"}`.
