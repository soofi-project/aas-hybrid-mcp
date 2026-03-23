"""Flask application — receives AAS Kafka events via HTTP sink."""

import logging

from flask import Flask, jsonify, request

from config import ON_PROCESSING_ERROR
from handlers import PermanentProcessingError, handle_create, handle_delete, handle_update

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/events", methods=["POST"])
def handle_aas_event():
    event = request.get_json()
    if not event:
        return jsonify({"status": "error", "message": "No JSON body"}), 400

    event_type = str(event.get("type", "")).upper()

    handler = None
    if event_type.endswith("_CREATED"):
        handler = handle_create
    elif event_type.endswith("_UPDATED"):
        handler = handle_update
    elif event_type.endswith("_DELETED"):
        handler = handle_delete
    else:
        return jsonify({"status": "ignored", "message": f"Unsupported event type: {event_type}"}), 400

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
