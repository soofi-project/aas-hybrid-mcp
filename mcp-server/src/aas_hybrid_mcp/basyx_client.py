"""Thin async httpx wrapper for the BaSyx AAS V3 REST API.

Two separate base URLs allow AAS repository and submodel repository to run
as independent services (the default BaSyx AAS Environment exposes both on
the same host, so both vars can point to the same address).

  AAS_REPO_URL      — AAS repository  (/shells/…, /shells/{id}/submodel-refs)
  SUBMODEL_REPO_URL — Submodel repository (/submodels/…)
"""

import base64
import logging
import os
from urllib.parse import quote

import httpx

log = logging.getLogger(__name__)

AAS_REPO_URL = os.environ.get("AAS_REPO_URL", "http://aas-environment:8081")
SUBMODEL_REPO_URL = os.environ.get("SUBMODEL_REPO_URL", "http://aas-environment:8081")
CD_REPO_URL = os.environ.get("CD_REPO_URL", "http://aas-environment:8081")
_TIMEOUT = 30.0

_aas_client: httpx.AsyncClient | None = None
_sm_client: httpx.AsyncClient | None = None
_cd_client: httpx.AsyncClient | None = None


def _get_aas_client() -> httpx.AsyncClient:
    global _aas_client
    if _aas_client is None:
        _aas_client = httpx.AsyncClient(base_url=AAS_REPO_URL, timeout=_TIMEOUT)
        log.info("BaSyx AAS repo client created for %s", AAS_REPO_URL)
    return _aas_client


def _get_sm_client() -> httpx.AsyncClient:
    global _sm_client
    if _sm_client is None:
        _sm_client = httpx.AsyncClient(base_url=SUBMODEL_REPO_URL, timeout=_TIMEOUT)
        log.info("BaSyx submodel repo client created for %s", SUBMODEL_REPO_URL)
    return _sm_client


def _get_cd_client() -> httpx.AsyncClient:
    global _cd_client
    if _cd_client is None:
        _cd_client = httpx.AsyncClient(base_url=CD_REPO_URL, timeout=_TIMEOUT)
        log.info("BaSyx CD repo client created for %s", CD_REPO_URL)
    return _cd_client


def _b64url(s: str) -> str:
    """Base64-URL encode an AAS identifier (no padding, per IDTA Part 2 REST spec)."""
    return base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")


def _path_enc(id_short_path: str) -> str:
    """Percent-encode an idShortPath for use as a URL path segment."""
    return quote(id_short_path, safe="")


def _raise_for_status_with_body(r: httpx.Response) -> None:
    """Raise HTTPStatusError with response body included in the message."""
    try:
        r.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise httpx.HTTPStatusError(
            f"{exc.response.status_code} {exc.response.reason_phrase}: {r.text[:500]}",
            request=exc.request,
            response=exc.response,
        ) from None


async def put_aas(aas_dict: dict) -> dict:
    aas_id: str = aas_dict.get("id", "")
    client = _get_aas_client()
    r = await client.put(f"/shells/{_b64url(aas_id)}", json=aas_dict)
    if r.status_code == 404:
        r = await client.post("/shells", json=aas_dict)
    _raise_for_status_with_body(r)
    return {"status": "ok", "id": aas_id}


async def delete_aas(aas_id: str) -> dict:
    client = _get_aas_client()
    r = await client.delete(f"/shells/{_b64url(aas_id)}")
    _raise_for_status_with_body(r)
    return {"status": "ok", "id": aas_id}


async def put_submodel(aas_id: str, submodel_dict: dict) -> dict:
    sm_id: str = submodel_dict.get("id", "")

    # 1. Create or replace submodel in the submodel repository.
    sm_client = _get_sm_client()
    r = await sm_client.put(f"/submodels/{_b64url(sm_id)}", json=submodel_dict)
    if r.status_code == 404:
        r = await sm_client.post("/submodels", json=submodel_dict)
    _raise_for_status_with_body(r)

    # 2. Ensure the AAS holds a reference to this submodel.
    ref = {
        "type": "ModelReference",
        "keys": [{"type": "Submodel", "value": sm_id}],
    }
    aas_client = _get_aas_client()
    r2 = await aas_client.post(f"/shells/{_b64url(aas_id)}/submodel-refs", json=ref)
    # 400/409 = reference already present — not an error.
    if r2.status_code not in (201, 400, 409):
        _raise_for_status_with_body(r2)

    return {"status": "ok", "id": sm_id}


async def delete_submodel(aas_id: str, submodel_id: str) -> dict:
    # 1. Remove reference from AAS (404 = already absent, ignore).
    aas_client = _get_aas_client()
    r = await aas_client.delete(
        f"/shells/{_b64url(aas_id)}/submodel-refs/{_b64url(submodel_id)}"
    )
    if r.status_code not in (204, 404):
        _raise_for_status_with_body(r)

    # 2. Delete submodel from the submodel repository.
    sm_client = _get_sm_client()
    r2 = await sm_client.delete(f"/submodels/{_b64url(submodel_id)}")
    _raise_for_status_with_body(r2)

    return {"status": "ok", "id": submodel_id}


async def put_submodel_element(
    submodel_id: str, id_short_path: str, element_dict: dict
) -> dict:
    client = _get_sm_client()
    sm_enc = _b64url(submodel_id)
    path_enc = _path_enc(id_short_path)

    r = await client.put(
        f"/submodels/{sm_enc}/submodel-elements/{path_enc}", json=element_dict
    )
    if r.status_code == 404:
        # Element does not exist yet — POST to parent collection or submodel root.
        parts = id_short_path.rsplit(".", 1)
        if len(parts) == 1:
            post_url = f"/submodels/{sm_enc}/submodel-elements"
        else:
            post_url = f"/submodels/{sm_enc}/submodel-elements/{_path_enc(parts[0])}"
        r = await client.post(post_url, json=element_dict)
    _raise_for_status_with_body(r)
    return {"status": "ok", "idShortPath": id_short_path}


async def delete_submodel_element(submodel_id: str, id_short_path: str) -> dict:
    client = _get_sm_client()
    r = await client.delete(
        f"/submodels/{_b64url(submodel_id)}/submodel-elements/{_path_enc(id_short_path)}"
    )
    _raise_for_status_with_body(r)
    return {"status": "ok", "idShortPath": id_short_path}


async def get_submodel(submodel_id: str) -> dict | None:
    """Fetch a Submodel by id. Returns the raw submodel dict, or None on 404."""
    client = _get_sm_client()
    r = await client.get(f"/submodels/{_b64url(submodel_id)}")
    if r.status_code == 404:
        return None
    _raise_for_status_with_body(r)
    return r.json()


async def get_concept_description(cd_id: str) -> dict | None:
    """Fetch a ConceptDescription by id. Returns the raw CD dict, or None on 404."""
    client = _get_cd_client()
    r = await client.get(f"/concept-descriptions/{_b64url(cd_id)}")
    if r.status_code == 404:
        return None
    _raise_for_status_with_body(r)
    return r.json()


async def close() -> None:
    global _aas_client, _sm_client, _cd_client
    for client, name in (
        (_aas_client, "AAS repo"),
        (_sm_client, "submodel repo"),
        (_cd_client, "CD repo"),
    ):
        if client is not None:
            await client.aclose()
            log.info("BaSyx %s client closed", name)
    _aas_client = None
    _sm_client = None
    _cd_client = None
