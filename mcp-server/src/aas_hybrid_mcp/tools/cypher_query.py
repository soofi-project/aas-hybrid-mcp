"""MCP tool for querying the AAS Neo4j knowledge graph."""

from fastmcp import FastMCP

from aas_hybrid_mcp import neo4j_client
from aas_hybrid_mcp.tool_descriptions import load as load_description

MAX_ROWS = 1000


def register(mcp: FastMCP) -> None:
    """Register Neo4j query tool on the MCP server."""

    @mcp.tool(description=load_description("query_aas_graph"))
    async def query_aas_graph(
        cypher: str,
        params: dict | str | None = None,
    ) -> dict:
        """Execute a read-only Cypher query against the AAS knowledge graph.

        ``params`` is conceptually a dict; ``str`` is accepted only as a
        tolerance for clients that pass a JSON-encoded string instead of an
        object — it gets parsed back to a dict here.
        """
        import json as _json
        if isinstance(params, str):
            try:
                params = _json.loads(params)
            except Exception:
                params = None
        try:
            rows = await neo4j_client.read_query(cypher, params)
        except Exception as e:
            return {"error": str(e)}

        truncated = len(rows) > MAX_ROWS
        return {
            "rows": rows[:MAX_ROWS],
            "total": len(rows),
            "truncated": truncated,
        }
