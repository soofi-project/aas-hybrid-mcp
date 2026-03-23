"""MCP tool for semantic search over AAS documents in Weaviate."""

from fastmcp import FastMCP

from aas_hybrid_mcp import weaviate_client

_SEARCH_DESCRIPTION = """\
Search PDF documents ingested from AAS submodels using semantic similarity.
Returns text chunks ranked by relevance to the query.

Use submodel_id to scope search to a specific submodel's documents.
Use query_aas_graph first to discover submodel IDs, then use this tool \
to search their document content.\
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
