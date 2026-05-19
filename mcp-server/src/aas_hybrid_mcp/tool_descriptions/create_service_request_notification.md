Creates an IDTA-conformant Service Request Notification (IDTA 02010-1-0, SRN) for a known asset and registers it on its AAS.

Call this when a fault or maintenance need is identified — **before** any repair begins (Pre-Action SRN). All fields are derivable from the conversation context; do NOT ask the user for values.

`Status` is always `"Open"` (hardcoded). Derive all other fields from context:

- `aas_id` — AAS identifier of the affected asset (from spatial disambiguation or prior tool calls)
- `short_text` — brief fault or request description (from the user's fault report)
- `service_type` — one of `CorrectiveMaintenance` | `PreventiveMaintenance` | `Inspection` | `Return`
- `priority` — one of `High` (safety/emergency stop) | `Medium` (functional fault) | `Low` (routine/preventive)
- `long_text` — optional extended description
- `error_code` — optional machine error code

**Bypass rule:** Do NOT use `put_submodel` or `put_submodel_element` to construct an SRN piece-by-piece. This tool is the only correct path for SRN creation — it guarantees IDTA structural conformance and prevents partial or invalid writes.

OUTPUT: `{"status": "ok", "id": "<srn_submodel_id>"}` or raises on validation failure.
