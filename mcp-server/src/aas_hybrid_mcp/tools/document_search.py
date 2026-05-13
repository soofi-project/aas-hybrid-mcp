"""MCP tool for semantic search over AAS documents in Weaviate."""

from fastmcp import FastMCP

from aas_hybrid_mcp import weaviate_client
from aas_hybrid_mcp.tool_descriptions import load as load_description

MAX_LIMIT = 50


def register(mcp: FastMCP) -> None:
    """Register the document search tool on the MCP server."""

    @mcp.tool(description=load_description("search_aas_documents"))
    async def search_aas_documents(
        query: str,
        submodel_id: str | None = None,
        limit: int = 10,
    ) -> dict:
        """Search AAS documents by semantic similarity."""
        limit = max(1, min(limit, MAX_LIMIT))

        try:
            response = await weaviate_client.search(
                query,
                submodel_id=submodel_id,
                limit=limit,
            )
        except Exception as e:
            return {"error": str(e)}

        results = response.get("results", [])
        out: dict = {
            "results": results,
            "total": len(results),
            "reranker_used": response.get("reranker_used", False),
        }
        if "diagnostic" in response:
            out["diagnostic"] = response["diagnostic"]
        if "chunk_count" in response:
            out["chunk_count"] = response["chunk_count"]
        return out
