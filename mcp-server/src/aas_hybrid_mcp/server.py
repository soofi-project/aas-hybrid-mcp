"""AAS Hybrid MCP Server — Neo4j graph queries and Weaviate vector search."""

import logging

import uvicorn
from fastmcp import FastMCP

from aas_hybrid_mcp.resources import schema
from aas_hybrid_mcp.tools import cypher_query, document_search

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

mcp = FastMCP("AAS Hybrid MCP")

cypher_query.register(mcp)
document_search.register(mcp)
schema.register(mcp)


def main():
    app = mcp.http_app()
    uvicorn.run(app, host="0.0.0.0", port=8110)


if __name__ == "__main__":
    main()
