"""Model-aware Weaviate collection naming.

Embeddings from different models are incompatible, so each model gets its own
collection: changing ``EMBEDDING_MODEL`` creates a new collection and leaves
the old one untouched for rollback.

The algorithm is duplicated in ``embedding-service/vectorstore.py`` and
``mcp-server/…/weaviate_client.py``. All three must agree — a writer and a
reader that disagree here do not error, they just silently find an empty
collection. Kept in its own module (no Weaviate import) so the parity is
testable on its own.
"""

from __future__ import annotations

import os
import re


def collection_name(base: str, embedding_model: str | None = None) -> str:
    """Build ``<Base><ModelSlug>``, e.g. ``IdtaTemplateSpec`` + ``qwen3-embedding-8b``.

    The base name is upper-cased on the first letter (Weaviate auto-cases
    class names to camelCase) and the model slug is title-cased per
    hyphen/dot-separated part, so special characters never reach the class
    name: ``text-embedding-3-small`` → ``TextEmbedding3Small``.
    """
    raw = embedding_model if embedding_model is not None else os.getenv("EMBEDDING_MODEL")
    if not raw or ":" not in raw:
        raise ValueError(
            "EMBEDDING_MODEL must be set in provider:model format "
            f"(e.g. openai:text-embedding-3-small), got: {raw!r}"
        )
    model = raw.split(":", 1)[1]
    if not model:
        raise ValueError(
            "EMBEDDING_MODEL must specify a model after the colon "
            f"(e.g. openai:text-embedding-3-small), got: {raw!r}"
        )
    parts = re.split(r"[-\.]", model)
    return f"{base[0].upper()}{base[1:]}" + "".join(p.title() for p in parts)
