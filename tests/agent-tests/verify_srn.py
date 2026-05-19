"""Post-hoc BaSyx verification for Service Request Notification ablation runs.

Queries BaSyx after an eval run to check whether a ServiceRequestNotification
submodel was actually written — agent claims are not a reliable pass indicator.

Usage (standalone):
    python verify_srn.py <aas_id>
    python verify_srn.py "urn:aas-hybrid-mcp:mir100_001"

Environment:
    AAS_REPO_URL      — BaSyx AAS repository  (default: http://localhost:8081)
    SUBMODEL_REPO_URL — BaSyx submodel repository (default: http://localhost:8081)
"""

from __future__ import annotations

import base64
import json
import os
import sys
from typing import TypedDict

import httpx


AAS_REPO_URL = os.environ.get("AAS_REPO_URL", "http://localhost:8081").rstrip("/")
SUBMODEL_REPO_URL = os.environ.get("SUBMODEL_REPO_URL", "http://localhost:8081").rstrip("/")

_VALID_PRIORITIES = {"High", "Medium", "Low"}
_VALID_SERVICE_TYPES = {"CorrectiveMaintenance", "PreventiveMaintenance", "Inspection", "Return"}


class SRNVerification(TypedDict):
    found: bool
    submodel_id: str | None
    status: str | None
    priority: str | None
    short_text: str | None
    valid_structure: bool
    errors: list[str]


def _b64url(s: str) -> str:
    return base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")


def _find_element(elements: list[dict], id_short: str) -> dict | None:
    for el in elements:
        if el.get("idShort") == id_short:
            return el
    return None


def _extract_string_value(elements: list[dict], id_short: str) -> str | None:
    el = _find_element(elements, id_short)
    if el is None:
        return None
    if el.get("modelType") == "Property":
        return el.get("value")
    if el.get("modelType") == "MultiLanguageProperty":
        vals = el.get("value", [])
        if vals:
            return vals[0].get("text")
    return None


def verify_srn(aas_id: str, *, timeout: float = 10.0) -> SRNVerification:
    """Return verification result for the most recent SRN submodel on *aas_id*.

    Queries BaSyx synchronously (blocking). Suitable for post-run verification
    scripts; not for async eval harness use.
    """
    errors: list[str] = []

    with httpx.Client(timeout=timeout) as client:
        # Step 1: get submodel references from the AAS.
        r = client.get(f"{AAS_REPO_URL}/shells/{_b64url(aas_id)}/submodel-refs")
        if r.status_code != 200:
            return SRNVerification(
                found=False, submodel_id=None, status=None, priority=None,
                short_text=None, valid_structure=False,
                errors=[f"GET submodel-refs failed: HTTP {r.status_code}"],
            )

        refs_data = r.json()
        refs = refs_data.get("result", refs_data) if isinstance(refs_data, dict) else refs_data

        # Step 2: find a ServiceRequestNotification submodel by fetching each ref.
        srn_submodel: dict | None = None
        srn_id: str | None = None
        for ref in refs:
            keys = ref.get("keys", [])
            if not keys:
                continue
            sm_id = keys[0].get("value", "")
            r2 = client.get(f"{SUBMODEL_REPO_URL}/submodels/{_b64url(sm_id)}")
            if r2.status_code != 200:
                continue
            sm = r2.json()
            if sm.get("idShort") == "ServiceRequestNotification":
                srn_submodel = sm
                srn_id = sm_id
                break

        if srn_submodel is None:
            return SRNVerification(
                found=False, submodel_id=None, status=None, priority=None,
                short_text=None, valid_structure=False,
                errors=["No ServiceRequestNotification submodel found"],
            )

        # Step 3: extract and validate mandatory fields from the SRN SMC.
        top_elements = srn_submodel.get("submodelElements", [])
        srn_smc = _find_element(top_elements, "ServiceRequestNotification")
        inner: list[dict] = srn_smc.get("value", []) if srn_smc else top_elements

        status_val = _extract_string_value(inner, "Status")
        priority_val = _extract_string_value(inner, "Priority")
        short_text_val = _extract_string_value(inner, "ShortText")
        service_type_val = _extract_string_value(inner, "ServiceType")

        if status_val != "Open":
            errors.append(f"Status is {status_val!r}, expected 'Open'")
        if priority_val not in _VALID_PRIORITIES:
            errors.append(f"Priority {priority_val!r} not in {sorted(_VALID_PRIORITIES)}")
        if not short_text_val:
            errors.append("ShortText is missing or empty")
        if service_type_val not in _VALID_SERVICE_TYPES:
            errors.append(f"ServiceType {service_type_val!r} not in {sorted(_VALID_SERVICE_TYPES)}")

        return SRNVerification(
            found=True,
            submodel_id=srn_id,
            status=status_val,
            priority=priority_val,
            short_text=short_text_val,
            valid_structure=len(errors) == 0,
            errors=errors,
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_srn.py <aas_id>", file=sys.stderr)
        sys.exit(1)
    result = verify_srn(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["valid_structure"] else 1)
