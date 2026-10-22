"""Put the service directory on sys.path.

pytest only prepends the tests/ directory itself, but the modules under test
are flat top-level scripts (app.py, events.py, …) in the service root.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# config.py reads its settings at import time; the tests run without the compose environment.
for name, value in {
    "WEAVIATE_HOST": "weaviate", "WEAVIATE_PORT": "8080", "WEAVIATE_GRPC_PORT": "50051", "WEAVIATE_COLLECTION": "Documents",
    "BASYX_SUBMODEL_REPO": "http://basyx", "BASYX_PUBLIC_URL": "http://basyx", "CHUNK_SIZE": "500", "CHUNK_OVERLAP": "50",
    "EMBEDDING_BATCH_SIZE": "8", "DOWNLOAD_TIMEOUT": "30", "ON_PROCESSING_ERROR": "skip", "OLLAMA_HOST": "http://ollama",
    "EMBEDDING_MODEL": "ollama:test",
}.items():
    os.environ.setdefault(name, value)
