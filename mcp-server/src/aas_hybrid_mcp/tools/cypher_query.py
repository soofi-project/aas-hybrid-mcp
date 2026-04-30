"""MCP tool for querying the AAS Neo4j knowledge graph."""

from fastmcp import FastMCP

from aas_hybrid_mcp import neo4j_client

_QUERY_DESCRIPTION = """\
Execute a read-only Cypher query against the AAS knowledge graph (Neo4j).

WHEN TO USE: structural questions about the AAS environment — which shells
exist, which submodels they expose, which elements and properties those
submodels carry, and how shells relate to each other. Also for ID
resolution: turning a natural-language reference into a concrete AAS-ID by
matching properties or relationships.

GRAPH SHAPE — memorise this. The Asset node has no outgoing relations:
  (:AssetAdministrationShell)-[:MANAGES_ASSET]->(:Asset)
  (:AssetAdministrationShell)-[:HAS_SUBMODEL]->(:Submodel)
                                  -[:HAS_ELEMENT*]->(:SubmodelElement)
  (:AssetAdministrationShell)-[:DERIVED_FROM]->(:AssetAdministrationShell)
                                  -- instance shell → type shell

Read the `aas://schema/graph` resource for the full catalogue (27 node
labels, 34 relations) before composing non-trivial queries — it lists all
SubmodelElement subtypes and their relationship semantics, plus an
anti-patterns section covering the four most common Cypher mistakes.

CORRECTNESS — recurring mistakes that silently return zero rows:
  1. `Repository` is AAS-storage, not a physical location. Never filter
     `Repository.url` to find assets at a hall, room, or factory section.
  2. `semanticId` is a relation, not a property. Use
     `-[:HAS_SEMANTIC_ID]->(:SemanticConcept {id:'…'})`, never
     `MATCH (sm:Submodel {semanticId:'…'})`.
  3. IDTA semanticIds are used verbatim — do not append `/Submodel` or
     other suffixes. The exact strings are in `aas://templates/index`.
  4. `assetType` and `assetKind` are optional and often null. Use
     `DERIVED_FROM` for type/instance distinction and submodel
     semanticIds for domain classification, not these properties.

COMPOSITION: this tool resolves the *structural* part of a question. For
PDF content (manuals, troubleshooting, procedures), pass the discovered
`submodel_id` to `search_aas_documents`. To find which IDTA template a
submodel conforms to or should conform to, use `search_idta_templates` or
the `aas://templates/index` resource.

TYPE vs INSTANCE: per VDI 2770, product-level documentation
(operating instructions, maintenance manuals) is conventionally attached
to the *type* AAS, while instance-specific records (calibration
certificates, delivery protocols) live on the instance. Traverse
`DERIVED_FROM` from an instance to its type before locating product-level
manuals.

INPUT: Cypher with `$paramName` placeholders + a `params` dict. Write
operations are rejected at the driver level.
OUTPUT: rows as a list of dicts; capped at 1000 rows (the response carries
`total` and `truncated` for paging decisions).\
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
