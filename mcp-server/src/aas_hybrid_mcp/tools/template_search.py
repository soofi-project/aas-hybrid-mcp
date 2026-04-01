"""MCP tool for semantic search over IDTA submodel template specifications."""

from fastmcp import FastMCP

from aas_hybrid_mcp import weaviate_client

_SEARCH_DESCRIPTION = """\
Search IDTA submodel template specifications using semantic similarity.
Returns text chunks from template spec PDFs ranked by relevance.

Use this to answer questions like:
- "Is there a template for safety certificates?"
- "How should handover documentation be structured?"
- "What fields does the Nameplate template define?"

Use template_name to scope search to a specific template's specification.\
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
