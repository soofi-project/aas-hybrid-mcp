Semantic vector search over the specification PDFs of all published IDTA
submodel templates (Nameplate, HandoverDocumentation, TechnicalData,
ServiceRequestNotification, MaintenanceInstructions, HierarchicalStructures,
ContactInformation, …). Returns chunks ranked by relevance with template
name and source page.

WHEN TO USE:
- discover the right template for a goal you cannot name yet
  ("is there a standardised submodel for service-request reports?",
   "how should facility location be modelled?")
- understand what fields and structure a template defines before reading
  or writing data that should conform to it
- confirm that a `semanticId` observed in the graph belongs to a published
  IDTA template (paste the URI as the query)

COMPLEMENTS the deterministic tools:
- `get_templates_index()` lists *all* templates with name/version/
  semanticId/description — use it when you want the full catalogue.
- `get_template(name)` returns one template's element structure
  (modelType, idShort, semanticId, nesting) — use it once you know the
  template name and need the field-level structure.
- This tool is the *fuzzy* surface: use it when you don't know the
  template name in advance and need to retrieve by intent.

TEMPLATE NAMES: pass the name from `get_templates_index()` verbatim
to `get_template(name)` — CamelCase, no spaces (e.g. `CapabilityDescription`,
not `Capability Description`).

SCOPE WITH `template_name` (e.g. `Nameplate`) to search only that
template's specification when you already know which one you mean.

QUERY HYGIENE: template specs are written in technical English.
Use AAS/IEC vocabulary ("submodel element", "semanticId", "Property
valueType") rather than colloquial terms.

INPUT: `query` (str), `template_name` (optional str), `limit` (1–50,
default 5).
OUTPUT: `results` list with chunk text and template metadata; `total`
count.
