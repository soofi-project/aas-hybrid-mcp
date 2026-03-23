"""AAS Hybrid MCP Server — Neo4j graph queries and Weaviate vector search."""

import logging

from mcp.server.fastmcp import FastMCP

from aas_hybrid_mcp.resources import schema
from aas_hybrid_mcp.tools import cypher_query

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

mcp = FastMCP("AAS Hybrid MCP", host="0.0.0.0", port=8110)

cypher_query.register(mcp)
schema.register(mcp)


def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
