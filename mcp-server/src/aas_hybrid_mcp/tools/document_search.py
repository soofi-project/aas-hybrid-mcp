"""MCP tool for semantic search over AAS documents in Weaviate."""

from fastmcp import FastMCP

from aas_hybrid_mcp import weaviate_client

_SEARCH_DESCRIPTION = """\
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

TYPE vs INSTANCE: handover documentation typically lives on the *type* AAS
rather than the instance, because manuals describe the product model. From
a scanned/identified instance, traverse
`(:AssetAdministrationShell)-[:DERIVED_FROM]->(:AssetAdministrationShell)`
to the type shell and use the type's HandoverDocumentation submodel ID.
Instance-level docs (calibration certificates, delivery protocols) stay
on the instance.

PRE-FILTER STRATEGY: only search submodels that actually contain File
elements. Submodels without PDFs return nothing — query the graph for
`(:Submodel)-[:HAS_ELEMENT*]->(:File)` first to identify candidates.

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
OUTPUT: `results` list with chunk text and metadata; `total` count.\
"""

MAX_LIMIT = 50


def register(mcp: FastMCP) -> None:
    """Register the document search tool on the MCP server."""

    @mcp.tool(description=_SEARCH_DESCRIPTION)
    async def search_aas_documents(
        query: str,
        submodel_id: str | None = None,
        limit: int = 10,
    ) -> dict:
        """Search AAS documents by semantic similarity."""
        limit = max(1, min(limit, MAX_LIMIT))

        try:
            results = await weaviate_client.search(
                query,
                submodel_id=submodel_id,
                limit=limit,
            )
        except Exception as e:
            return {"error": str(e)}

        return {
            "results": results,
            "total": len(results),
        }
