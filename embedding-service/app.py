"""Flask application — receives AAS Kafka events via HTTP sink."""

import logging

from flask import Flask, jsonify, request

from handlers import handle_create, handle_delete, handle_update

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
    except Exception:
        log.exception("Failed to process %s event", event_type)
        return jsonify({"status": "error", "message": "Internal processing error"}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "online"}), 200
