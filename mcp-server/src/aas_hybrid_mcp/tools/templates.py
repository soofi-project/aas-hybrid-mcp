"""MCP tools: IDTA submodel template index and per-template structure."""

import json
import logging
import os
import re
from pathlib import Path

from fastmcp import FastMCP

from aas_hybrid_mcp import neo4j_client
from aas_hybrid_mcp.tool_descriptions import load as load_description

log = logging.getLogger(__name__)

TEMPLATES_DIR = Path(os.getenv("TEMPLATES_DIR", "/data/templates"))


def _match_template_by_semantic(template_semantic_id: str, graph_id: str) -> bool:
    """Check whether a graph semanticId matches an index semanticId.

    Handles the common mismatches:
    - `/Submodel` suffix difference
    - Trailing segment mismatch (index `/1/0/Submodel` vs graph `/1/0`)
    """
    if template_semantic_id == graph_id:
        return True

    # Strip /Submodel suffix for comparison
    t_bare = re.sub(r"/Submodel$", "", template_semantic_id, flags=re.IGNORECASE)
    g_bare = re.sub(r"/Submodel$", "", graph_id, flags=re.IGNORECASE)
    if t_bare == g_bare:
        return True

    # One is a prefix of the other: split and compare common segments
    t_parts = t_bare.rstrip("/").split("/")
    g_parts = g_bare.rstrip("/").split("/")
    min_len = min(len(t_parts), len(g_parts))

    if min_len > 0 and t_parts[:min_len] == g_parts[:min_len]:
        return True

    return False


async def _discover_graph_semantic_ids() -> list[str]:
    """Fetch all live semanticIds present in the Neo4j graph."""
    try:
        rows = await neo4j_client.read_query(
            "MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept)\n"
            "RETURN DISTINCT sc.id AS graphSemanticId",
            {},
        )
        return [r["graphSemanticId"] for r in rows if r.get("graphSemanticId")]
    except Exception as exc:
        log.warning("Failed to discover graph semanticIds: %s", exc)
        return []


async def _match_graph_ids(index_entries: list[dict], graph_ids: list[str]) -> list[dict]:
    """Merge index entries with live graph semanticIds."""
    graph_set = graph_ids  # preserve order
    matched = []
    for entry in index_entries:
        idx_id = entry.get("semanticId", "")
        if not idx_id:
            matched.append({**entry, "graphSemanticIds": []})
            continue
        found = [gid for gid in graph_set if _match_template_by_semantic(idx_id, gid)]
        matched.append({**entry, "graphSemanticIds": found})
    return matched


def register(mcp: FastMCP) -> None:
    """Register IDTA template tools."""

    @mcp.tool(description=load_description("get_templates_index"))
    async def get_templates_index() -> str:
        """Index of all IDTA submodel templates with live graph semanticIds."""
        index_path = TEMPLATES_DIR / "index.json"
        if not index_path.is_file():
            return json.dumps({
                "error": "Template index not available. The submodel-templates-sync container may not have run yet.",
                "templates": [],
            })
        index_entries = json.loads(index_path.read_text(encoding="utf-8"))

        graph_ids = await _discover_graph_semantic_ids()
        if graph_ids:
            index_entries = await _match_graph_ids(index_entries, graph_ids)
        else:
            # Fallback: no graph access, just add empty field so the shape is stable
            for e in index_entries:
                e.setdefault("graphSemanticIds", [])

        return json.dumps(index_entries, indent=2, ensure_ascii=False)

    @mcp.tool(description=load_description("get_template"))
    def get_template(name: str) -> str:
        """Element structure of one IDTA submodel template."""
        template_path = TEMPLATES_DIR / f"{name}.json"
        if not template_path.is_file():
            for f in TEMPLATES_DIR.glob("*.json"):
                if f.stem.lower() == name.lower() and f.name != "index.json":
                    template_path = f
                    break

        if not template_path.is_file():
            return json.dumps({
                "error": f"Template '{name}' not found.",
                "available": _list_available_templates(),
            })
        return template_path.read_text(encoding="utf-8")


def _list_available_templates() -> list[str]:
    if not TEMPLATES_DIR.is_dir():
        return []
    return sorted(
        f.stem for f in TEMPLATES_DIR.glob("*.json") if f.name != "index.json"
    )
