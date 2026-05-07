Semantic vector search over PDF chunks ingested from AAS Submodel File
elements. Returns chunks ranked by relevance with `submodel_id`, source
filename, page number, and a relevance score.

WHEN TO USE: content questions whose answers live inside referenced PDFs
and are not exposed as Submodel Properties — troubleshooting steps, safety
instructions, calibration procedures, specifications buried in datasheets,
LED/error-code tables.

SCOPE WITH `submodel_id` — the hinge of the hybrid design. Pass the ID of a
specific Submodel to restrict search to that Submodel's PDFs only. Without
scoping you search the entire ingested corpus and the agent loses the
asset-pinning property that prevents cross-asset hallucinations. Discover
the `submodel_id` via `query_aas_graph` first; never invent or guess one
(IDs are URIs like `https://…` or `urn:…`, not human labels).

PICK THE RIGHT SUBMODEL — manuals, troubleshooting steps, error codes,
calibration procedures and other handover content live in the
`HandoverDocumentation` Submodel of the **Type AAS**, never in the
Instance AAS's `Nameplate`. Instance Nameplates carry serial number /
year-of-construction Property values, not PDF File elements. If your
question is about behaviour, faults or operating procedures, walk
`Instance-AAS -[:DERIVED_FROM]-> Type-AAS -[:HAS_SUBMODEL]-> HandoverDocumentation`
in the graph first, then search that submodel's ID here.

DIAGNOSTICS ON EMPTY RESULTS — when `submodel_id` is given and the result
is empty, the response includes a `diagnostic` field that distinguishes
two very different situations:
- `not_indexed`: zero chunks exist for this `submodel_id` in Weaviate
  (PDF was never ingested, ingestion failed, or the wrong ID was passed).
  Re-check the ID via `query_aas_graph`, or escalate ingestion — do not
  conclude "the manual says nothing about X".
- `no_match`: chunks exist but none scored above the retrieval threshold
  for this query. Rephrase, simplify, or translate the query and retry.
Without `submodel_id`, an empty result is a plain corpus miss and no
diagnostic is emitted.

QUERY HYGIENE:
- Strip asset names and identifiers from the query — `submodel_id` already
  scopes to the right asset; including the name dilutes the embedding.
- Match the documentation's language. Most industrial manuals are English
  or the manufacturer's locale; translate the query accordingly even if
  the user asked in another language.
- Use technical vocabulary (the docs do); a worker's literal phrase
  ("Getriebe klemmt") often misses the manual's term ("drive-train
  blockage, bearing damage").

INPUT: `query` (str), `submodel_id` (optional str), `limit` (1–50,
default 10).
OUTPUT: `results` list with chunk text and metadata; `total` count.
