"""MCP tool for querying the AAS Neo4j knowledge graph."""

from fastmcp import FastMCP

from aas_hybrid_mcp import neo4j_client

_QUERY_DESCRIPTION = """\
Execute a read-only Cypher query against the AAS Neo4j knowledge graph.
Use $paramName syntax in Cypher and pass values via the params argument.
Read the aas://schema/graph resource first to understand the graph structure.\
"""

MAX_ROWS = 1000


def register(mcp: FastMCP) -> None:
    """Register Neo4j query tool on the MCP server."""

    @mcp.tool(description=_QUERY_DESCRIPTION)
    async def query_aas_graph(
        cypher: str,
        params: dict | None = None,
    ) -> dict:
        """Execute a read-only Cypher query against the AAS knowledge graph."""
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
