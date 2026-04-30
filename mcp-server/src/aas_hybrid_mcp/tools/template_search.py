"""MCP tool for semantic search over IDTA submodel template specifications."""

from fastmcp import FastMCP

from aas_hybrid_mcp import weaviate_client

_SEARCH_DESCRIPTION = """\
Semantic vector search over the specification PDFs of ~45 published IDTA
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

COMPLEMENTS the deterministic resources:
- `aas://templates/index` lists *all* templates with name/version/
  semanticId/description — use it when you want the full catalogue.
- `aas://template/{name}` returns one template's element structure
  (modelType, idShort, semanticId, nesting) — use it once you know the
  template name and need the field-level structure.
- This tool is the *fuzzy* surface: use it when you don't know the
  template name in advance and need to retrieve by intent.

TEMPLATE NAMES are CamelCase without spaces, as published in the
`aas://templates/index` resource (e.g. `CapabilityDescription`,
`HierarchicalStructures`, `HandoverDocumentation`). Resource URIs follow
this exact form: `aas://template/CapabilityDescription`, **not**
`aas://template/Capability Description`. Take the name from the index
verbatim; do not invent spaced variants.

SCOPE WITH `template_name` (e.g. `Nameplate`) to search only that
template's specification when you already know which one you mean.

QUERY HYGIENE: template specs are written in technical English.
Use AAS/IEC vocabulary ("submodel element", "semanticId", "Property
valueType") rather than colloquial terms.

INPUT: `query` (str), `template_name` (optional str), `limit` (1–50,
default 5).
OUTPUT: `results` list with chunk text and template metadata; `total`
count.\
"""

MAX_LIMIT = 50


def register(mcp: FastMCP) -> None:
    """Register the template search tool on the MCP server."""

    @mcp.tool(description=_SEARCH_DESCRIPTION)
    async def search_idta_templates(
        query: str,
        template_name: str | None = None,
        limit: int = 5,
    ) -> dict:
        """Search IDTA template specifications by semantic similarity."""
        limit = max(1, min(limit, MAX_LIMIT))

        try:
            results = await weaviate_client.search_templates(
                query,
                template_name=template_name,
                limit=limit,
            )
        except Exception as e:
            return {"error": str(e)}

        return {
            "results": results,
            "total": len(results),
        }
