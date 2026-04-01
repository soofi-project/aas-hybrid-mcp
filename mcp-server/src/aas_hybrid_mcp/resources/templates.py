"""MCP resources: IDTA submodel template index and per-template structure."""

import json
import logging
import os
from pathlib import Path

from fastmcp import FastMCP

log = logging.getLogger(__name__)

TEMPLATES_DIR = Path(os.getenv("TEMPLATES_DIR", "/data/templates"))


def register(mcp: FastMCP) -> None:
    """Register IDTA template resources."""

    @mcp.resource("aas://templates/index")
    def get_templates_index() -> str:
        """Index of all IDTA submodel templates: name, version, idShort, semanticId, description."""
        index_path = TEMPLATES_DIR / "index.json"
        if not index_path.is_file():
            return json.dumps({
                "error": "Template index not available. The submodel-templates-sync container may not have run yet.",
                "templates": [],
            })
        return index_path.read_text(encoding="utf-8")

    @mcp.resource("aas://template/{name}")
    def get_template_structure(name: str) -> str:
        """Element structure of a specific IDTA submodel template (modelType, idShort, semanticId, children)."""
        template_path = TEMPLATES_DIR / f"{name}.json"
        if not template_path.is_file():
            # Try case-insensitive match
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
    """List available template names from the volume."""
    if not TEMPLATES_DIR.is_dir():
        return []
    return sorted(
        f.stem for f in TEMPLATES_DIR.glob("*.json") if f.name != "index.json"
    )
