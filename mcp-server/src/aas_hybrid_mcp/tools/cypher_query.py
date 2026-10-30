"""MCP tool for querying the AAS Neo4j knowledge graph."""

import json as _json
import logging
import re

from fastmcp import FastMCP

from aas_hybrid_mcp import cypher_validator, neo4j_client
from aas_hybrid_mcp.tool_descriptions import lean_mode
from aas_hybrid_mcp.tool_descriptions import load as load_description

log = logging.getLogger(__name__)

MAX_ROWS = 1000

_FORBIDDEN_HINT = (
    "Rewrite without CONTAINS/=~ on idShort/id. Call get_manual_page('cypher') "
    "and get_templates_index() to learn the correct pattern before retrying."
)
_FORBIDDEN_HINT_LEAN = (
    "Rewrite without CONTAINS/=~ on idShort/id: use exact equality "
    "(WHERE x.idShort = 'ExactName') as the entry point."
)

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


_MANUAL_REF_RE = re.compile(r"\s*See cypher\.md anti-pattern #\d+\.")


def _violations(violations) -> list[dict]:
    """Serialize validator violations; drop manual references in lean mode."""
    lean = lean_mode()
    return [
        {
            "rule": v.rule,
            "hint": _MANUAL_REF_RE.sub("", v.hint) if lean else v.hint,
            "match": v.match,
        }
        for v in violations
    ]


# (kind from neo4j_client.unknown_names, warning rule, whether to list the
# known names via the neo4j_client function of the same name, hint). Property
# keys get a weaker hint and no known list: a key can be unknown just because
# no node has carried it yet.
_UNKNOWN_NAME_KINDS = (
    (
        "relationship_types",
        "unknown_relationship_type",
        True,
        "These relationship types do not exist in the database, so the "
        "pattern cannot match. Check the spelling and use only existing types.",
    ),
    (
        "labels",
        "unknown_label",
        True,
        "These labels do not exist in the database, so the pattern cannot "
        "match. Check the spelling and use only existing labels.",
    ),
    (
        "property_keys",
        "unknown_property_key",
        False,
        "No node or relationship in the database carries these property keys. "
        "Check the spelling; if the key is optional, an empty result may be correct.",
    ),
)


async def _unknown_names_warnings(unknown: dict[str, list[str]]) -> list[dict]:
    """Warnings for relationship types, labels and property keys the graph lacks."""
    warnings = []
    for kind, rule, list_known, hint in _UNKNOWN_NAME_KINDS:
        if kind not in unknown:
            continue
        warning = {"rule": rule, "unknown": unknown[kind], "hint": hint}
        if list_known:
            try:
                known = await getattr(neo4j_client, kind)()
            except Exception:
                log.warning("Could not list known %s", kind, exc_info=True)
                known = []
            if known:
                warning[f"known_{kind}"] = known
        warnings.append(warning)
    return warnings


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

        vr = cypher_validator.validate(cypher)
        if not vr.allowed:
            return {
                "error": "forbidden_pattern",
                "violations": _violations(vr.violations),
                "hint": _FORBIDDEN_HINT_LEAN if lean_mode() else _FORBIDDEN_HINT,
            }

        try:
            rows, notices = await neo4j_client.read_query_with_notices(
                cypher, params
            )
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
        warnings = _violations(vr.violations)
        warnings.extend(await _unknown_names_warnings(notices["unknown_names"]))
        warnings.extend(
            {"rule": "neo4j_notification", **n} for n in notices["notifications"]
        )
        if warnings:
            result["_warnings"] = warnings
        return result
