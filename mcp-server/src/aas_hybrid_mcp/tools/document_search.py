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
        submodel_id: str,
        limit: int = 10,
        asset_name: str | None = None,
        doc_language: str | None = None,
    ) -> dict:
        """Search AAS documents by semantic similarity."""
        # Mandatory scoping: only submodel_id builds the Weaviate filter
        # (asset_name feeds the query rewriter, it does NOT restrict results).
        # An unscoped search would return chunks from unrelated assets, so we
        # reject it server-side rather than silently falling back to a
        # repository-wide search.
        if not submodel_id or not submodel_id.strip():
            raise ValueError(
                "'submodel_id' is required and must be non-empty. Locate the "
                "relevant submodel first via query_aas_graph (follow "
                "DERIVED_FROM to the type shell for documentation), then pass "
                "its full ID. An unscoped search would surface documentation "
                "from unrelated assets."
            )
        limit = max(1, min(limit, MAX_LIMIT))

        try:
            response = await weaviate_client.search(
                query,
                submodel_id=submodel_id,
                limit=limit,
                asset_name=asset_name,
                doc_language=doc_language,
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
        if "diagnostic" in response:
            out["diagnostic"] = response["diagnostic"]
        if "chunk_count" in response:
            out["chunk_count"] = response["chunk_count"]
        return out
