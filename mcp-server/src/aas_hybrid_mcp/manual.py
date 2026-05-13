"""MCP manual: index + sub-pages as tools.

The agent may pre-fetch the index at startup (controlled by the
``AGENT_INJECT_MANUAL`` flag in aas-agent) or call ``get_manual_index``
on demand. Sub-pages are loaded individually via ``get_manual_page``.

Pages are loaded dynamically from the ``manual_pages/`` directory.
The page index is auto-generated from available ``*.md`` files.
"""

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


_INDEX = _load_page("index") or ""


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
