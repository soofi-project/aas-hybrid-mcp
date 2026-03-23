"""MCP tools for querying the AAS Neo4j knowledge graph."""

from mcp.server.fastmcp import FastMCP

from aas_hybrid_mcp import neo4j_client

_QUERY_DESCRIPTION = """\
Execute a read-only Cypher query against the AAS Neo4j knowledge graph.
Use $paramName syntax in Cypher and pass values via the params argument.
Read the aas://schema/graph resource first to understand the graph structure.\
"""

_SCHEMA_DESCRIPTION = """\
Return the current Neo4j graph schema: node labels, relationship types, \
and property keys. Use this to discover the live structure before writing queries.\
"""

MAX_ROWS = 1000


def register(mcp: FastMCP) -> None:
    """Register Neo4j query tools on the MCP server."""

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

    @mcp.tool(description=_SCHEMA_DESCRIPTION)
    async def get_aas_graph_schema() -> str:
        """Return the AAS Neo4j graph schema (labels, relationships, properties)."""
        try:
            labels = await neo4j_client.read_query(
                "CALL db.labels() YIELD label RETURN collect(label) AS labels"
            )
            rels = await neo4j_client.read_query(
                "CALL db.relationshipTypes() YIELD relationshipType "
                "RETURN collect(relationshipType) AS types"
            )
            props = await neo4j_client.read_query(
                "CALL db.schema.nodeTypeProperties() YIELD nodeLabels, propertyName, propertyTypes "
                "RETURN nodeLabels, propertyName, propertyTypes"
            )
        except Exception as e:
            return f"Error: {e}"

        lines = ["# AAS Graph Schema", ""]
        lines.append(f"**Node Labels:** {', '.join(labels[0]['labels'])}")
        lines.append(f"**Relationship Types:** {', '.join(rels[0]['types'])}")
        lines.append("")
        lines.append("## Node Properties")

        by_label: dict[str, list[str]] = {}
        for row in props:
            for label in row["nodeLabels"]:
                by_label.setdefault(label, []).append(
                    f"  - {row['propertyName']} ({', '.join(row['propertyTypes'])})"
                )

        for label, prop_lines in sorted(by_label.items()):
            lines.append(f"\n**{label}**")
            lines.extend(sorted(set(prop_lines)))

        return "\n".join(lines)
