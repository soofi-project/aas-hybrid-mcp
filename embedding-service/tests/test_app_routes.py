"""Route contract of POST /events — the part that decides whether the
connector task survives.

Needs flask, so it skips outside the service image. ``config`` and ``handlers``
are stubbed to keep weaviate and docling out of the picture; the handlers are
spies, because the interesting question here is *which* handler is called with
*what* and which HTTP status comes back — not what the ingest itself does.
"""

import sys
import types

import pytest

pytest.importorskip("flask")

SUBMODEL = "urn:submodel:mir100:001:eventdemo"


def make_handler(calls, name, exc=None):
    def handler(event):
        calls.append((name, event))
        if exc is not None:
            raise exc

    return handler


@pytest.fixture
def service(monkeypatch):
    calls = []

    class PermanentProcessingError(Exception):
        pass

    handlers = types.ModuleType("handlers")
    handlers.PermanentProcessingError = PermanentProcessingError
    handlers.handle_create = make_handler(calls, "create")
    handlers.handle_update = make_handler(calls, "update")
    handlers.handle_delete = make_handler(calls, "delete")

    config = types.ModuleType("config")
    config.ON_PROCESSING_ERROR = "skip"

    monkeypatch.setitem(sys.modules, "handlers", handlers)
    monkeypatch.setitem(sys.modules, "config", config)
    monkeypatch.delitem(sys.modules, "app", raising=False)

    import app as app_module

    assert app_module.ON_PROCESSING_ERROR == "skip"
    return types.SimpleNamespace(
        client=app_module.app.test_client(), calls=calls, module=app_module
    )


def adapter_body(change="Created", model_type="Submodel", keys=None):
    return {
        "sourceSemanticId": f"https://fai2.cos.dfki.de/aas/ChangeType/{change}",
        "observableReference": {
            "type": "ModelReference",
            "keys": keys or [{"type": "Submodel", "value": SUBMODEL}],
        },
        "payload": {"modelType": model_type, "id": SUBMODEL, "idShort": "Demo"},
    }


def test_created_submodel_reaches_create_handler(service):
    resp = service.client.post("/events", json=adapter_body())
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "success"
    name, event = service.calls[0]
    assert name == "create"
    assert event["type"] == "SUBMODEL_CREATED"
    assert event["submodel"]["modelType"] == "Submodel"


def test_element_update_reaches_update_handler_with_path(service):
    keys = [
        {"type": "Submodel", "value": SUBMODEL},
        {"type": "SubmodelElement", "value": "Documents"},
    ]
    resp = service.client.post(
        "/events", json=adapter_body("Updated", "SubmodelElementList", keys)
    )
    assert resp.status_code == 200
    name, event = service.calls[0]
    assert name == "update"
    assert event["smElementPath"] == "Documents"


def test_delete_reaches_delete_handler(service):
    resp = service.client.post("/events", json=adapter_body("Deleted", "File"))
    assert resp.status_code == 200
    assert service.calls[0][0] == "delete"


def test_native_shape_still_works(service):
    body = {"type": "SM_ELEMENT_CREATED", "id": "urn:aas:mir100:001:x", "submodel": {}}
    resp = service.client.post("/events", json=body)
    assert resp.status_code == 200
    assert service.calls[0] == ("create", body)


def test_aas_event_is_acked_with_200_and_no_handler(service):
    """The regression that broke the pipeline: a 4xx here kills the task."""
    body = adapter_body(
        "Created",
        "AssetAdministrationShell",
        [{"type": "AssetAdministrationShell", "value": "urn:aas:mir100:001"}],
    )
    resp = service.client.post("/events", json=body)
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ignored"
    assert service.calls == []


def test_unknown_event_type_is_acked_with_200(service):
    resp = service.client.post("/events", json=adapter_body("Announced"))
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ignored"
    assert service.calls == []


def test_non_object_body_is_a_400(service):
    resp = service.client.post("/events", json=["nope"])
    assert resp.status_code == 400
    assert service.calls == []


def test_permanent_error_is_skipped_with_200(service):
    # app.py binds the handlers with `from handlers import ...`, so they have
    # to be replaced in the app module, not in the stub module.
    service.module.handle_create = make_handler(
        service.calls, "create", service.module.PermanentProcessingError("no text")
    )
    resp = service.client.post("/events", json=adapter_body())
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "skipped"


def test_transient_error_is_500_so_kafka_retries(service):
    service.module.handle_create = make_handler(
        service.calls, "create", RuntimeError("weaviate down")
    )
    resp = service.client.post("/events", json=adapter_body())
    assert resp.status_code == 500
