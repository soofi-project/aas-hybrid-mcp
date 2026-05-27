"""Characterization test for the IDTA template-conformance validator.

Pins down what the ``put_submodel`` validation path actually enforces today:
``write_tools._validate_submodel`` (basyx SDK structural check) followed by
``template_validator.validate_conformance`` (generated-class instantiation).

WHY THIS EXISTS
---------------
The SRN write-path benchmark (Bench C) recorded zero validator rejections across
all 450 runs. This script reproduces *why*: the validator enforces metamodel
structure but NOT template conformance in depth. Specifically it does not check
controlled-vocabulary values, and it does not recurse into nested required fields
-- it only instantiates the top-level generated class, passing the agent's
already-built child objects into optional constructor slots. So an empty SRN, an
SRN with an invalid ServiceType value, and an SRN missing required inner fields
all pass. See task_paper_bench_c_bypass_rewrite.

It doubles as a regression guard: if a future change closes a documented gap, the
corresponding line flips and the script exits non-zero -- prompting an update here
and in the Bench C paper narrative.

HOW TO RUN
----------
Inside the mcp-server container (it needs the generated template classes under
TEMPLATES_DIR and the installed ``aas_hybrid_mcp`` package)::

    docker exec -i aas-hybrid-mcp python - < tests/validator-tests/test_template_validator_gap.py
"""

from __future__ import annotations

import sys

from aas_hybrid_mcp.template_validator import _registry, validate_conformance
from aas_hybrid_mcp.tools.write_tools import _validate_submodel


def run_validation(payload: dict) -> tuple[str, str | None]:
    """Mirror the put_submodel path: SDK structure check, then template conformance."""
    sdk_err, obj = _validate_submodel(payload)
    if sdk_err:
        return "reject", f"SDK: {sdk_err[:110]}"
    tpl_err = validate_conformance(obj)
    if tpl_err:
        return "reject", f"template: {tpl_err[:110]}"
    return "conform", None


def srn_semantic_id() -> str | None:
    for sid, cls in _registry().items():
        if "ServiceRequest" in cls.__name__:
            return sid
    return None


def _submodel(sid: str, elements: list[dict]) -> dict:
    return {
        "modelType": "Submodel",
        "id": "urn:validator-test:srn:1",
        "idShort": "ServiceRequestNotification",
        "semanticId": {
            "type": "ExternalReference",
            "keys": [{"type": "GlobalReference", "value": sid}],
        },
        "submodelElements": elements,
    }


def _notification(fields: list[dict]) -> dict:
    return {
        "modelType": "SubmodelElementCollection",
        "idShort": "ServiceRequestNotification",
        "value": fields,
    }


def _prop(id_short: str, value: str) -> dict:
    return {"modelType": "Property", "idShort": id_short, "valueType": "xs:string", "value": value}


def main() -> int:
    sid = srn_semantic_id()
    if sid is None:
        print(
            "SKIP: no ServiceRequestNotification template class registered. "
            "Run inside the mcp-server container with TEMPLATES_DIR populated."
        )
        return 0

    # (label, payload, expected_outcome, category)
    #   category "enforced" -> the validator SHOULD and DOES reject (structural)
    #   category "gap"      -> the validator SHOULD reject but does NOT (documented gap)
    cases = [
        (
            "non-Submodel modelType",
            {"modelType": "NotASubmodel", "id": "urn:x"},
            "reject",
            "enforced",
        ),
        (
            "Submodel without id",
            {"modelType": "Submodel", "id": ""},
            "reject",
            "enforced",
        ),
        (
            "empty SRN submodel (no notification at all)",
            _submodel(sid, []),
            "conform",
            "gap",
        ),
        (
            "SRN with invalid ServiceType value 'Emergency Maintenance'",
            _submodel(sid, [_notification([_prop("ServiceType", "Emergency Maintenance")])]),
            "conform",
            "gap",
        ),
        (
            "SRN notification missing required inner fields (only ServiceType present)",
            _submodel(sid, [_notification([_prop("ServiceType", "CorrectiveMaintenance")])]),
            "conform",
            "gap",
        ),
    ]

    print(f"SRN template semanticId: {sid}\n")
    print(f"{'#':>2}  {'kind':8} {'expect':8} {'actual':8} {'match':5} case")
    print("-" * 96)

    mismatches = 0
    for i, (label, payload, expected, category) in enumerate(cases, 1):
        actual, reason = run_validation(payload)
        match = actual == expected
        mismatches += not match
        kind = "ENFORCED" if category == "enforced" else "GAP"
        print(f"{i:>2}  {kind:8} {expected:8} {actual:8} {'ok' if match else 'XX':5} {label}")
        if reason:
            print(f"      -> {reason}")

    print("-" * 96)
    if mismatches:
        print(
            f"\n{mismatches} case(s) no longer match documented behaviour. A validator "
            "change may have opened or closed a gap -- update this file and the Bench C "
            "narrative in task_paper_bench_c_bypass_rewrite."
        )
        return 1
    print(
        "\nAll cases match documented behaviour: metamodel structure is enforced, "
        "template conformance (controlled-vocabulary values, nested required fields) is NOT."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
