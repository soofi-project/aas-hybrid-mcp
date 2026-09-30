"""Normalisation of inbound events onto the shape the handlers expect.

Two producers reach ``/events``:

1. **The aas-stream-adapter** (Kafka ``aas-events`` / ``submodel-events``),
   whose envelope looks like::

       {
         "sourceSemanticId": "https://fai2.cos.dfki.de/aas/ChangeType/Created",
         "observableReference": {
           "type": "ModelReference",
           "keys": [{"type": "Submodel", "value": "urn:submodel:mir100:001:demo"},
                    {"type": "SubmodelElement", "value": "Documents"}],
         },
         "commitId": "...",
         "timestamp": "...",
         "payload": {},   # the Submodel or SubmodelElement itself
       }

   The change type lives in the last segment of ``sourceSemanticId``, the
   submodel id in ``observableReference.keys[0]``, the element idShort path in
   the remaining keys, and the body in ``payload``.

2. **Direct callers** already speaking the internal shape::

       {"type": "SUBMODEL_CREATED", "id": "urn:submodel:...",
        "submodel": {}}          # or "smElement": {}

Both are accepted: the adapter envelope is translated, the internal shape
passes through unchanged.

Deliberately free of Flask/Weaviate/Docling imports — this is pure data
shifting, and the tests import it without the heavy service dependencies.
"""

from __future__ import annotations

CHANGE_SUFFIXES = {
    "created": "_CREATED",
    "updated": "_UPDATED",
    "deleted": "_DELETED",
}

SUBMODEL_KEY_TYPE = "Submodel"


def _last_segment(uri: object) -> str:
    return str(uri or "").rstrip("/").rsplit("/", 1)[-1]


def change_suffix(source_semantic_id: object) -> str | None:
    """Map an ``.../ChangeType/<X>`` URI onto a handler suffix.

    Only the tail matters, so the adapter's more specific variants
    (``PropertyValueCreated`` and friends) resolve to the same suffix.
    """
    token = _last_segment(source_semantic_id).lower()
    for name, suffix in CHANGE_SUFFIXES.items():
        if token.endswith(name):
            return suffix
    return None


def has_handler_suffix(event_type: object) -> bool:
    token = str(event_type or "").upper()
    return any(token.endswith(suffix) for suffix in CHANGE_SUFFIXES.values())


def _reference_keys(raw: dict) -> list[dict]:
    ref = raw.get("observableReference")
    if not isinstance(ref, dict):
        return []
    keys = ref.get("keys")
    if not isinstance(keys, list):
        return []
    return [k for k in keys if isinstance(k, dict)]


def element_path(keys: list[dict]) -> str:
    """idShort path of the addressed element, e.g. ``Documents.Manual``.

    Every key after the submodel key contributes one segment. One known limit:
    the adapter addresses list children by idShort, while
    :class:`handlers.AasPathBuilder` addresses them by index (``[n]``). For a
    PDF reached through a list the two notations differ and the adapter gives
    no index, so the idShort form is the best answer available here.
    """
    return ".".join(str(k.get("value", "")) for k in keys[1:] if k.get("value"))


def normalize(raw: object) -> tuple[dict | None, str]:
    """Translate an inbound event into the handler-facing shape.

    Returns ``(event, reason)``. ``event`` is ``None`` when the payload
    carries nothing ingestible — a well-formed event we deliberately do
    nothing about, which the caller must acknowledge with ``200`` and not
    ``4xx``: the Kafka sink runs with ``errors.tolerance=none``, so a single
    rejected record would kill the task and stop ingestion for every later
    event. Only a body that is not a JSON object at all is a client bug.
    """
    if not isinstance(raw, dict):
        return None, "no JSON object body"

    if has_handler_suffix(raw.get("type")):
        return raw, "internal shape"

    suffix = change_suffix(raw.get("sourceSemanticId"))
    if suffix is None:
        return None, f"Unsupported event type: {raw.get('type', '')}"

    keys = _reference_keys(raw)
    if not keys:
        return None, "event carries no observableReference keys"

    root = keys[0]
    if root.get("type") != SUBMODEL_KEY_TYPE:
        # AAS / asset events carry references, not elements: nothing to ingest.
        return None, f"not a submodel event ({root.get('type')})"

    submodel_id = str(root.get("value", ""))
    payload = raw.get("payload")
    if not isinstance(payload, dict):
        return None, "event carries no payload object"

    event = {
        "type": f"{SUBMODEL_KEY_TYPE.upper()}{suffix}",
        "id": submodel_id,
    }

    if payload.get("modelType") == SUBMODEL_KEY_TYPE:
        event["submodel"] = payload
    else:
        event["smElement"] = payload

    path = element_path(keys)
    if path:
        # Only meaningful for element-scoped work: DELETE scopes by it, and
        # UPDATE re-ingests under it instead of re-deriving a flat path.
        event["smElementPath"] = path

    return event, f"adapter envelope ({event['type']})"
