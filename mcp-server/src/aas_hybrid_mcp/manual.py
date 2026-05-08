"""MCP manual: index + sub-pages as tools.

The agent may pre-fetch the index at startup (controlled by the
``AGENT_INJECT_MANUAL`` flag in aas-agent) or call ``get_manual_index``
on demand. Sub-pages are loaded individually via ``get_manual_page``.

Pages are loaded dynamically from the ``manual_pages/`` directory.
The page index is auto-generated from available ``*.md`` files.
"""

import os
from pathlib import Path

from fastmcp import FastMCP

from aas_hybrid_mcp.tool_descriptions import load as load_description

_PAGES_DIR = Path(__file__).parent / "manual_pages"


def _load_page(name: str) -> str | None:
    """Load a single manual page from its markdown file."""
    path = _PAGES_DIR / f"{name}.md"
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def _build_pages_dict() -> dict[str, str]:
    """Build the pages dict by scanning the manual_pages directory."""
    pages: dict[str, str] = {}
    for md_file in _PAGES_DIR.glob("*.md"):
        if md_file.name == "index.md":
            continue  # index is handled separately
        page_name = md_file.stem
        content = md_file.read_text(encoding="utf-8")
        pages[page_name] = content
    return pages


_PAGES = _build_pages_dict()


def _build_index() -> str:
    """Build the index page from manual_pages/*.md headers and content."""
    index_content = """\
# AAS Hybrid MCP — Operator Manual

You are talking to a hybrid Neo4j + Weaviate MCP server that wraps a
BaSyx AAS environment. This page indexes the rest of the manual.

## Sub-pages — call get_manual_page(page=...) on demand
"""
    # List pages in alphabetical order
    for page_name in sorted(_PAGES.keys()):
        index_content += f"- `{page_name}` — see the page for details.\n"

    index_content += """

## Four rules that catch the most failures

1. **Before your first `query_aas_graph` call, call `get_templates_index()`
   — but only ONCE per session.** Check the conversation history first: if a
   prior `<think>` block already shows its result, use those semanticIds
   directly. Do not call it again on every turn.
2. `params` for `query_aas_graph` is an OBJECT, not a JSON string.
   `{}`, not `"{}"`.
3. Use IDTA semanticIds VERBATIM from `get_templates_index()`. No `/Submodel`
   suffix, no version normalisation, no recall from training memory. The graph
   may also carry non-IDTA semanticIds (e.g. ZVEI Nameplate); discover them
   with `MATCH (sm:Submodel)-[:HAS_SEMANTIC_ID]->(sc) RETURN DISTINCT sc.id`.
4. Never match by `idShort` for domain reasoning. `idShort` is a
   free-form local label; semantic meaning lives only in
   `HAS_SEMANTIC_ID` / `HAS_SUPPLEMENTAL_SEMANTIC_ID`.

## Tools — call on demand

- `get_templates_index()` — all published IDTA templates with name, version,
  semanticId, description. Call when picking a template or before any
  non-trivial Cypher (per rule 1).
- `get_template(name)` — element structure of one template (modelType,
  idShort, semanticId, nesting). Call before traversing a submodel or
  writing template-conformant JSON.
"""
    return index_content


_INDEX = _build_index()


def register(mcp: FastMCP) -> None:
    """Register operator-manual tools."""

    @mcp.tool(description=load_description("get_manual_index"))
    def get_manual_index() -> str:
        """Operator manual index. Cheap to call repeatedly; static content."""
        return _INDEX

    @mcp.tool(description=load_description("get_manual_page"))
    def get_manual_page(page: str) -> str:
        """Return one sub-page of the operator manual."""
        content = _PAGES.get(page.lower())
        if content is None:
            return (
                f"Unknown page '{page}'. Valid pages: "
                + ", ".join(sorted(_PAGES))
            )
        return content
