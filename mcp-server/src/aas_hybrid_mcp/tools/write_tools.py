"""MCP write tools — create, replace, and delete AAS objects via BaSyx REST API."""

import io
import json
import logging

from fastmcp import FastMCP

from aas_hybrid_mcp import basyx_client, template_validator
from aas_hybrid_mcp.tool_descriptions import load as load_description

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

_VALID_MODEL_TYPES = {
    "AssetAdministrationShell", "Submodel",
    "Property", "MultiLanguageProperty", "File", "Blob", "Range",
    "SubmodelElementCollection", "SubmodelElementList",
    "ReferenceElement", "RelationshipElement", "AnnotatedRelationshipElement",
    "Entity", "Operation", "BasicEventElement", "Capability",
}


def _check_nonempty(**kwargs: str) -> str | None:
    """Return an error message if any kwarg value is empty/whitespace, else None."""
    for name, value in kwargs.items():
        if not value or not value.strip():
            return f"'{name}' must not be empty"
    return None


def _validate_aas(aas_dict: dict) -> str | None:
    """Return an error string if the dict is not a valid AAS, or None if OK."""
    if aas_dict.get("modelType") != "AssetAdministrationShell":
        return "modelType must be 'AssetAdministrationShell'"
    if not aas_dict.get("id", "").strip():
        return "AAS 'id' field is required and must not be empty"
    if "assetInformation" not in aas_dict:
        return "'assetInformation' field is required"
    try:
        from basyx.aas.adapter.json import read_aas_json_file

        env = {
            "assetAdministrationShells": [aas_dict],
            "submodels": [],
            "conceptDescriptions": [],
        }
        read_aas_json_file(io.StringIO(json.dumps(env)), failsafe=False)
    except Exception as exc:
        return str(exc)
    return None


def _validate_submodel(submodel_dict: dict) -> tuple[str | None, object | None]:
    """Validate Submodel structure with the basyx SDK.

    Returns (error_string, submodel_object).  On success error_string is None
    and submodel_object is the deserialised basyx Submodel (reused for the
    template conformance check to avoid parsing twice).
    """
    if submodel_dict.get("modelType") != "Submodel":
        return "modelType must be 'Submodel'", None
    if not submodel_dict.get("id", "").strip():
        return "Submodel 'id' field is required and must not be empty", None
    try:
        from basyx.aas.adapter.json import read_aas_json_file
        from basyx.aas.model import Submodel as BasyxSubmodel

        env = {
            "assetAdministrationShells": [],
            "submodels": [submodel_dict],
            "conceptDescriptions": [],
        }
        obj_store = read_aas_json_file(io.StringIO(json.dumps(env)), failsafe=False)
        submodel_obj = next((o for o in obj_store if isinstance(o, BasyxSubmodel)), None)
        return None, submodel_obj
    except Exception as exc:
        return str(exc), None


def _validate_element(element_dict: dict) -> str | None:
    """Return an error string if the dict is not a valid SubmodelElement, or None if OK."""
    model_type = element_dict.get("modelType", "")
    if model_type not in _VALID_MODEL_TYPES - {"AssetAdministrationShell", "Submodel"}:
        return (
            f"modelType '{model_type}' is not a valid SubmodelElement type. "
            f"Valid types: {', '.join(sorted(_VALID_MODEL_TYPES - {'AssetAdministrationShell', 'Submodel'}))}"
        )
    if not element_dict.get("idShort", "").strip():
        return "'idShort' field is required and must not be empty"
    try:
        from basyx.aas.adapter.json import read_aas_json_file

        # Wrap in a minimal Submodel envelope so the SDK can deserialize it.
        wrapper = {
            "modelType": "Submodel",
            "id": "urn:aas-hybrid-mcp:validation-wrapper",
            "submodelElements": [element_dict],
        }
        env = {
            "assetAdministrationShells": [],
            "submodels": [wrapper],
            "conceptDescriptions": [],
        }
        read_aas_json_file(io.StringIO(json.dumps(env)), failsafe=False)
    except Exception as exc:
        return str(exc)
    return None


# ---------------------------------------------------------------------------
# Tool registration
# ---------------------------------------------------------------------------

def register(mcp: FastMCP) -> None:
    """Register AAS write tools on the MCP server."""

    @mcp.tool(description=load_description("put_aas"))
    async def put_aas(aas_json: str) -> dict:
        err = _check_nonempty(aas_json=aas_json)
        if err:
            raise ValueError(err)

        try:
            aas_dict = json.loads(aas_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

        err = _validate_aas(aas_dict)
        if err:
            raise ValueError(f"AAS validation failed: {err}")

        return await basyx_client.put_aas(aas_dict)

    @mcp.tool(description=load_description("delete_aas"))
    async def delete_aas(aas_id: str) -> dict:
        err = _check_nonempty(aas_id=aas_id)
        if err:
            raise ValueError(err)
        return await basyx_client.delete_aas(aas_id)

    @mcp.tool(description=load_description("put_submodel"))
    async def put_submodel(aas_id: str, submodel_json: str) -> dict:
        err = _check_nonempty(aas_id=aas_id, submodel_json=submodel_json)
        if err:
            raise ValueError(err)

        try:
            submodel_dict = json.loads(submodel_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

        # Stage 1: metamodel structure (SDK strict deserialisation).
        sdk_err, submodel_obj = _validate_submodel(submodel_dict)
        if sdk_err:
            raise ValueError(f"Submodel validation failed: {sdk_err}")

        # Stage 2: IDTA template conformance (generated class instantiation).
        if submodel_obj is not None:
            tpl_err = template_validator.validate_conformance(submodel_obj)
            if tpl_err:
                raise ValueError(tpl_err)

        return await basyx_client.put_submodel(aas_id, submodel_dict)

    @mcp.tool(description=load_description("delete_submodel"))
    async def delete_submodel(aas_id: str, submodel_id: str) -> dict:
        err = _check_nonempty(aas_id=aas_id, submodel_id=submodel_id)
        if err:
            raise ValueError(err)
        return await basyx_client.delete_submodel(aas_id, submodel_id)

    @mcp.tool(description=load_description("put_submodel_element"))
    async def put_submodel_element(
        submodel_id: str, id_short_path: str, element_json: str
    ) -> dict:
        err = _check_nonempty(
            submodel_id=submodel_id, id_short_path=id_short_path, element_json=element_json
        )
        if err:
            raise ValueError(err)

        try:
            element_dict = json.loads(element_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

        err = _validate_element(element_dict)
        if err:
            raise ValueError(f"SubmodelElement validation failed: {err}")

        return await basyx_client.put_submodel_element(
            submodel_id, id_short_path, element_dict
        )

    @mcp.tool(description=load_description("delete_submodel_element"))
    async def delete_submodel_element(submodel_id: str, id_short_path: str) -> dict:
        err = _check_nonempty(submodel_id=submodel_id, id_short_path=id_short_path)
        if err:
            raise ValueError(err)
        return await basyx_client.delete_submodel_element(submodel_id, id_short_path)
