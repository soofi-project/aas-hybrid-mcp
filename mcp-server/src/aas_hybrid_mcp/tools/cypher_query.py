"""MCP tool for querying the AAS Neo4j knowledge graph."""

import json as _json
import re

from fastmcp import FastMCP

from aas_hybrid_mcp import neo4j_client
from aas_hybrid_mcp.tool_descriptions import load as load_description

MAX_ROWS = 1000

# IDTA semanticIds are published in two forms — with and without a trailing
# ``/Submodel`` segment. The official spec AASX files (and therefore our
# template JSONs) carry the suffix; live AAS instances in this graph were
# imported without it. The Cypher tool transparently strips the suffix from
# any string literal or parameter value, so agent queries work regardless of
# which form they pass.
_SUBMODEL_SUFFIX = "/Submodel"
_LITERAL_RE = re.compile(
    r'("(?:[^"\\]|\\.)*?/Submodel"|\'(?:[^\'\\]|\\.)*?/Submodel\')'
)


def _strip_suffix_in_cypher(cypher: str) -> tuple[str, list[str]]:
    """Drop ``/Submodel`` from quoted string literals inside the query.

    Returns the rewritten Cypher and a list of literals that were normalized,
    for audit in the response.
    """
    rewrites: list[str] = []

    def repl(m: re.Match) -> str:
        lit = m.group(1)
        quote = lit[0]
        inner = lit[1:-1]
        stripped = inner[: -len(_SUBMODEL_SUFFIX)]
        rewrites.append(inner)
        return f"{quote}{stripped}{quote}"

    return _LITERAL_RE.sub(repl, cypher), rewrites


def _strip_suffix_in_params(params: dict | None) -> tuple[dict | None, list[str]]:
    """Same normalization for parameter dict values."""
    if not isinstance(params, dict):
        return params, []
    rewrites: list[str] = []
    out: dict = {}
    for k, v in params.items():
        if isinstance(v, str) and v.endswith(_SUBMODEL_SUFFIX):
            out[k] = v[: -len(_SUBMODEL_SUFFIX)]
            rewrites.append(f"{k}={v}")
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, str) and item.endswith(_SUBMODEL_SUFFIX):
                    new_list.append(item[: -len(_SUBMODEL_SUFFIX)])
                    rewrites.append(f"{k}[]={item}")
                else:
                    new_list.append(item)
            out[k] = new_list
        else:
            out[k] = v
    return out, rewrites


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

        Any IDTA semanticId of the form ``.../Submodel`` is transparently
        normalized to its suffix-less form (the form actually present in the
        graph). This applies to both string literals inside the Cypher and
        to values in ``params``. Normalizations are reported in the response
        under ``normalized`` for transparency.
        """
        if isinstance(params, str):
            try:
                params = _json.loads(params)
            except Exception:
                params = None

        cypher, cypher_rewrites = _strip_suffix_in_cypher(cypher)
        params, param_rewrites = _strip_suffix_in_params(params)

        try:
            rows = await neo4j_client.read_query(cypher, params)
        except Exception as e:
            return {"error": str(e)}

        truncated = len(rows) > MAX_ROWS
        result: dict = {
            "rows": rows[:MAX_ROWS],
            "total": len(rows),
            "truncated": truncated,
        }
        if cypher_rewrites or param_rewrites:
            result["normalized"] = {
                "note": "Stripped trailing /Submodel suffix to match graph data.",
                "cypher_literals": cypher_rewrites,
                "params": param_rewrites,
            }
        return result
