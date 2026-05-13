Semantic vector search over PDF documents ingested from AAS Submodel File elements. Returns chunks ranked by relevance with `submodel_id`, source filename, page number, and a score.

WHEN TO USE: questions whose answers live inside PDF documentation
(troubleshooting, safety instructions, calibration, datasheets,
error-code tables).

**Always scope with `submodel_id`** — obtained first via `query_aas_graph`.
Never invent or guess one: IDs are URIs (`https://…`, `urn:…`),
not human labels. Unscoped search loses asset-pinning and risks
cross-asset hallucinations. Documentation typically lives on the
Type AAS (discover via `DERIVED_FROM`), not on the instance shell.

DIAGNOSTICS ON EMPTY RESULTS — when `submodel_id` is given:
- `not_indexed`: no document chunks for this submodel. Re-check the ID
  or the PDF was never ingested — do not conclude "the manual says
  nothing about X".
- `no_match`: chunks exist but score below threshold. Rephrase or
  translate the query and retry.

QUERY HYGIENE:
- Strip asset names from the query — `submodel_id` already scopes.
- Match the documentation's language (often English or the manufacturer's locale).
- Use technical vocabulary — a worker's phrase may miss the manual's term.

INPUT: `query` (str), `submodel_id` (optional str), `limit` (1–50,
default 10).
OUTPUT: `results` list with chunk text and metadata; `total` count.
