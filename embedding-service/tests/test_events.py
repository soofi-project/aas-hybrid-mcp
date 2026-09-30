"""The event normaliser has to agree with the real aas-stream-adapter
envelope — that agreement is the whole point of the module, so the fixtures
below are trimmed copies of actual records off ``submodel-events``.
"""

import pytest

from events import change_suffix, element_path, has_handler_suffix, normalize

SUBMODEL = "urn:submodel:mir100:001:eventdemo"


def adapter_event(change="Created", keys=None, payload=None, topic=""):
    return {
        "sourceSemanticId": f"https://fai2.cos.dfki.de/aas/ChangeType/{change}",
        "observableReference": {
            "type": "ModelReference",
            "keys": keys if keys is not None else [{"type": "Submodel", "value": SUBMODEL}],
        },
        "commitId": "1790768403_20",
        "timestamp": "2026-09-30T11:40:03.7Z",
        "topic": topic,
        "payload": payload if payload is not None else {},
    }


def submodel_payload():
    return {
        "modelType": "Submodel",
        "id": SUBMODEL,
        "idShort": "MiR100EventDemo",
        "submodelElements": [
            {"modelType": "File", "contentType": "application/pdf",
             "idShort": "Manual", "value": "http://example.org/manual.pdf"},
        ],
    }


def element_payload():
    """What the adapter sends for an element update — the element itself."""
    return {
        "modelType": "SubmodelElementList",
        "idShort": "Documents",
        "value": [{"modelType": "SubmodelElementCollection", "idShort": "Manuals"}],
    }


@pytest.mark.parametrize(
    "uri,expected",
    [
        ("https://fai2.cos.dfki.de/aas/ChangeType/Created", "_CREATED"),
        ("https://fai2.cos.dfki.de/aas/ChangeType/Updated", "_UPDATED"),
        ("https://fai2.cos.dfki.de/aas/ChangeType/Deleted", "_DELETED"),
        ("https://fai2.cos.dfki.de/aas/ChangeType/PropertyValueCreated", "_CREATED"),
        ("https://fai2.cos.dfki.de/aas/ChangeType/Created/", "_CREATED"),
        ("https://fai2.cos.dfki.de/aas/ChangeType/Announced", None),
        ("", None),
        (None, None),
    ],
)
def test_change_suffix(uri, expected):
    assert change_suffix(uri) == expected


def test_has_handler_suffix():
    assert has_handler_suffix("SUBMODEL_CREATED")
    assert has_handler_suffix("submodel_deleted")
    assert not has_handler_suffix("SUBMODEL_ANNOUNCED")
    assert not has_handler_suffix("")


def test_submodel_created_maps_to_submodel_key():
    event, reason = normalize(adapter_event("Created", payload=submodel_payload()))
    assert event["type"] == "SUBMODEL_CREATED"
    assert event["id"] == SUBMODEL
    assert event["submodel"]["submodelElements"][0]["idShort"] == "Manual"
    # A whole submodel has no element path.
    assert "smElementPath" not in event
    assert "adapter envelope" in reason


def test_element_update_maps_to_smelement_with_path():
    keys = [
        {"type": "Submodel", "value": "urn:submodel:mir100:type:handoverdocumentation"},
        {"type": "SubmodelElement", "value": "Documents"},
    ]
    event, _ = normalize(
        adapter_event("Updated", keys=keys, payload=element_payload())
    )
    assert event["type"] == "SUBMODEL_UPDATED"
    assert event["id"] == "urn:submodel:mir100:type:handoverdocumentation"
    assert event["smElement"]["idShort"] == "Documents"
    assert event["smElementPath"] == "Documents"


def test_delete_keeps_element_path_so_deletion_stays_scoped():
    keys = [
        {"type": "Submodel", "value": SUBMODEL},
        {"type": "SubmodelElement", "value": "Documents"},
        {"type": "SubmodelElement", "value": "Manual"},
    ]
    event, _ = normalize(
        adapter_event("Deleted", keys=keys, payload={"modelType": "File"})
    )
    assert event["type"] == "SUBMODEL_DELETED"
    assert event["smElementPath"] == "Documents.Manual"


def test_submodel_delete_without_element_key_deletes_whole_submodel():
    event, _ = normalize(adapter_event("Deleted", payload=submodel_payload()))
    assert event["type"] == "SUBMODEL_DELETED"
    assert event["submodel"]["id"] == SUBMODEL
    assert "smElementPath" not in event


def test_aas_event_is_ignored_not_rejected():
    """AAS events share the topics; they carry references, no elements.

    normalize returns None and the caller must answer 200 — a 4xx would kill
    the tolerance=none sink and stop ingestion entirely.
    """
    raw = adapter_event(
        "Created",
        keys=[{"type": "AssetAdministrationShell", "value": "urn:aas:mir100:001"}],
        payload={"modelType": "AssetAdministrationShell", "id": "urn:aas:mir100:001"},
    )
    event, reason = normalize(raw)
    assert event is None
    assert "not a submodel event" in reason


def test_unknown_change_type_is_ignored():
    event, reason = normalize(adapter_event("Announced", payload=submodel_payload()))
    assert event is None
    assert "Unsupported event type" in reason


@pytest.mark.parametrize(
    "mutation",
    [
        {"observableReference": {}},
        {"observableReference": {"type": "ModelReference", "keys": "nope"}},
    ],
)
def test_broken_reference_is_ignored(mutation):
    raw = adapter_event("Created", payload=submodel_payload())
    raw.update(mutation)
    event, reason = normalize(raw)
    assert event is None
    assert "observableReference" in reason


def test_missing_payload_is_ignored():
    raw = adapter_event("Created")
    raw["payload"] = "not-an-object"
    event, reason = normalize(raw)
    assert event is None
    assert "payload" in reason


def test_internal_shape_passes_through_unchanged():
    internal = {"type": "SUBMODEL_CREATED", "id": SUBMODEL, "smElement": {"idShort": "x"}}
    event, reason = normalize(internal)
    assert event is internal
    assert reason == "internal shape"


def test_non_object_body_is_rejected():
    event, reason = normalize(["not", "an", "object"])
    assert event is None
    assert "JSON object" in reason


def test_element_path_joins_all_keys_after_the_submodel():
    keys = [
        {"type": "Submodel", "value": SUBMODEL},
        {"type": "SubmodelElement", "value": "A"},
        {"type": "SubmodelElement", "value": "B"},
    ]
    assert element_path(keys) == "A.B"


def test_element_path_ignores_empty_key_values():
    keys = [{"type": "Submodel", "value": SUBMODEL}, {"type": "SubmodelElement"}]
    assert element_path(keys) == ""
