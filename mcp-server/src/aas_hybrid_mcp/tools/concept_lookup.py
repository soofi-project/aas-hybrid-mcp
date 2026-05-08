"""MCP tool for resolving a semanticId to its IEC 61360 ConceptDescription content.

Wraps the BaSyx ConceptDescription Repository (`GET /concept-descriptions/{id}`)
and projects the AAS V3 CD payload into a flat, agent-friendly contract:

  {
    "id": "<IRDI or IRI>",
    "resolved": true,
    "idShort": "...",
    "preferredName": {"en": "...", "de": "..."},
    "shortName":     {"en": "..."},
    "definition":    {"en": "..."},
    "dataType": "REAL_MEASURE" | "STRING" | ...,
    "unit": "mm",
    "source": "basyx"
  }

If the id is not registered in the local repository (typical for raw ECLASS
IRDIs without a locally-shipped CD), the tool answers honestly:

  {"id": "...", "resolved": false, "reason": "no local definition"}
"""

import logging

import httpx
from fastmcp import FastMCP

from aas_hybrid_mcp import basyx_client
from aas_hybrid_mcp.tool_descriptions import load as load_description

log = logging.getLogger(__name__)


def _langs_to_dict(items: list | None) -> dict[str, str]:
    """[{language, text}, ...] → {language: text}."""
    if not items:
        return {}
    out: dict[str, str] = {}
    for entry in items:
        lang = entry.get("language")
        text = entry.get("text")
        if lang and text:
            out[lang] = text
    return out


def _extract_iec61360(cd: dict) -> dict:
    """Pull preferredName / shortName / definition / dataType / unit out of
    the first IEC 61360 embeddedDataSpecification entry, if present.
    """
    eds_list = cd.get("embeddedDataSpecifications") or []
    for eds in eds_list:
        content = eds.get("dataSpecificationContent") or {}
        if content.get("modelType") != "DataSpecificationIec61360":
            continue
        return {
            "preferredName": _langs_to_dict(content.get("preferredName")),
            "shortName": _langs_to_dict(content.get("shortName")),
            "definition": _langs_to_dict(content.get("definition")),
            "dataType": content.get("dataType"),
            "unit": content.get("unit"),
        }
    return {
        "preferredName": {},
        "shortName": {},
        "definition": {},
        "dataType": None,
        "unit": None,
    }


def register(mcp: FastMCP) -> None:
    """Register the ConceptDescription lookup tool on the MCP server."""

    @mcp.tool(description=load_description("lookup_semantic_id"))
    async def lookup_semantic_id(id: str) -> dict:
        """Resolve a semanticId (IRDI/IRI) to its IEC 61360 content."""
        try:
            cd = await basyx_client.get_concept_description(id)
        except httpx.HTTPError as exc:
            log.warning("CD lookup failed for %s: %s", id, exc)
            return {"id": id, "resolved": False, "error": str(exc)}

        if cd is None:
            return {
                "id": id,
                "resolved": False,
                "reason": "no local definition (likely an external reference)",
            }

        iec = _extract_iec61360(cd)
        return {
            "id": cd.get("id", id),
            "resolved": True,
            "idShort": cd.get("idShort"),
            **iec,
            "source": "basyx",
        }
