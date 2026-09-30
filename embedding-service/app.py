"""Flask application — receives AAS Kafka events via HTTP sink."""

import logging

from flask import Flask, jsonify, request

from config import ON_PROCESSING_ERROR
from events import normalize
from handlers import PermanentProcessingError, handle_create, handle_delete, handle_update

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/events", methods=["POST"])
def handle_aas_event():
    raw = request.get_json(silent=True)
    if not isinstance(raw, dict):
        return jsonify({"status": "error", "message": "No JSON object body"}), 400

    event, reason = normalize(raw)
    if event is None:
        # Well-formed but nothing to ingest (AAS-level event, unknown change
        # type). ACK with 200 on purpose: the Kafka sink runs with
        # errors.tolerance=none, so a 4xx here would kill the connector task
        # and silently stop ingestion for every later event on the topic.
        log.info("Ignoring event: %s", reason)
        return jsonify({"status": "ignored", "message": reason}), 200

    event_type = event["type"]

    handler = None
    if event_type.endswith("_CREATED"):
        handler = handle_create
    elif event_type.endswith("_UPDATED"):
        handler = handle_update
    elif event_type.endswith("_DELETED"):
        handler = handle_delete
    else:  # pragma: no cover — normalize() only emits the three suffixes
        return jsonify({"status": "ignored", "message": reason}), 200

    try:
        handler(event)
        return jsonify({"status": "success"}), 200
    except PermanentProcessingError as exc:
        # Permanent error — retrying won't help (corrupt PDF, 404, no text).
        # In "skip" mode: log and ACK so Kafka moves on.
        # In "abort" mode: return 500 so Kafka retries (blocks the partition).
        if ON_PROCESSING_ERROR == "skip":
            log.warning("Skipping unprocessable %s event: %s", event_type, exc)
            return jsonify({"status": "skipped", "message": str(exc)}), 200
        log.error("Aborting on permanent error in %s event: %s", event_type, exc)
        return jsonify({"status": "error", "message": str(exc)}), 500
    except Exception:
        # Transient error — always return 500 so Kafka retries.
        log.exception("Transient error processing %s event", event_type)
        return jsonify({"status": "error", "message": "Internal processing error"}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "online"}), 200
