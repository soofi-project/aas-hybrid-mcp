"""MCP tool for semantic search over IDTA submodel template specifications."""

from fastmcp import FastMCP

from aas_hybrid_mcp import weaviate_client
from aas_hybrid_mcp.tool_descriptions import load as load_description

MAX_LIMIT = 50


def register(mcp: FastMCP) -> None:
    """Register the template search tool on the MCP server."""

    @mcp.tool(description=load_description("search_idta_templates"))
    async def search_idta_templates(
        query: str,
        template_name: str | None = None,
        limit: int = 5,
    ) -> dict:
        """Search IDTA template specifications by semantic similarity."""
        limit = max(1, min(limit, MAX_LIMIT))

        try:
            response = await weaviate_client.search_templates(
                query,
                template_name=template_name,
                limit=limit,
            )
        except Exception as e:
            return {"error": str(e)}

        results = response.get("results", [])
        out: dict = {
            "results": results,
            "total": len(results),
            "reranker_used": response.get("reranker_used", False),
            "query_rewritten": response.get("query_rewritten", False),
        }
        if response.get("rewritten_query"):
            out["rewritten_query"] = response["rewritten_query"]
        if response.get("hint"):
            out["hint"] = response["hint"]
        return out
