"""Weaviate client — singleton connection and collection operations."""

import logging
import os
import re
from typing import Sequence

import weaviate
import weaviate.collections.classes.config as wvc
import weaviate.collections.classes.data as wcd
import weaviate.collections.classes.filters as wvf

from config import (
    WEAVIATE_HOST,
    WEAVIATE_HTTP_PORT,
    WEAVIATE_GRPC_PORT,
    WEAVIATE_COLLECTION,
)

log = logging.getLogger(__name__)


def _get_collection_name(base: str) -> str:
    """Build model-aware collection name from base + EMBEDDING_MODEL slug.

    Embeddings from different models are incompatible, so each model gets its
    own collection.  Changing EMBEDDING_MODEL automatically creates a new
    collection; the old one stays untouched for easy rollback.

    The base name is upper-cased (Weaviate auto-cases it to camelCase) and the
    model slug is converted to camelCase so special characters are handled
    cleanly, e.g.  ``text-embedding-3-small`` → ``TextEmbedding3Small``.
    """
    raw = os.environ.get("EMBEDDING_MODEL")
    if not raw or ":" not in raw:
        raise ValueError(
            f"EMBEDDING_MODEL must be set in provider:model format "
            f"(e.g. openai:text-embedding-3-small), got: {raw!r}"
        )
    model = raw.split(":", 1)[1]
    if not model:
        raise ValueError(
            f"EMBEDDING_MODEL must specify a model after the colon "
            f"(e.g. openai:text-embedding-3-small), got: {raw!r}"
        )
    # Weaviate class names must be alphanumeric only.
    base = base[0].upper() + base[1:]
    # Split on hyphens/dots, then Title-Case each part.
    parts = re.split(r'[-\.]', model)
    slug = "".join(p.title() for p in parts)
    return f"{base}{slug}"

_client: weaviate.WeaviateClient | None = None


def _get_client() -> weaviate.WeaviateClient:
    """Return a shared Weaviate client, creating it on first call."""
    global _client
    if _client is None or not _client.is_connected():
        log.info(
            "Connecting to Weaviate at %s (http=%d, grpc=%d)",
            WEAVIATE_HOST, WEAVIATE_HTTP_PORT, WEAVIATE_GRPC_PORT,
        )
        _client = weaviate.connect_to_custom(
            http_host=WEAVIATE_HOST,
            http_port=WEAVIATE_HTTP_PORT,
            http_secure=False,
            grpc_host=WEAVIATE_HOST,
            grpc_port=WEAVIATE_GRPC_PORT,
            grpc_secure=False,
            skip_init_checks=True,
        )
    return _client


def _ensure_collection(client: weaviate.WeaviateClient, collection_name: str) -> None:
    """Create the document collection if it does not exist yet."""
    if not client.collections.exists(collection_name):
        log.info("Creating Weaviate collection %s", collection_name)
        client.collections.create(
            name=collection_name,
            vector_config=wvc.Configure.Vectors.self_provided(),
            properties=[
                wvc.Property(name="text", data_type=wvc.DataType.TEXT),
                wvc.Property(name="source", data_type=wvc.DataType.TEXT),
                wvc.Property(name="submodelId", data_type=wvc.DataType.TEXT),
                wvc.Property(name="smElementPath", data_type=wvc.DataType.TEXT),
                wvc.Property(name="idShort", data_type=wvc.DataType.TEXT),
                wvc.Property(name="contentHash", data_type=wvc.DataType.TEXT),
            ],
        )


def insert_chunks(
    texts: Sequence[str],
    vectors: Sequence[list[float]],
    source: str,
    submodel_id: str,
    sm_element_path: str | None,
    id_short: str,
    content_hash: str,
) -> None:
    """Insert text chunks with pre-computed vectors into Weaviate.

    All chunks from the same source document share the same ``content_hash``,
    so ``has_chunks`` can answer *"is this exact document already ingested?"*
    before the caller pays for PDF conversion and embedding.
    """
    client = _get_client()
    collection_name = _get_collection_name(WEAVIATE_COLLECTION)
    _ensure_collection(client, collection_name)

    collection = client.collections.get(collection_name)
    data_objects = [
        wcd.DataObject(
            properties={
                "text": t,
                "source": source,
                "submodelId": submodel_id,
                "smElementPath": sm_element_path or "",
                "idShort": id_short,
                "contentHash": content_hash,
            },
            vector=v,
        )
        for t, v in zip(texts, vectors)
    ]
    collection.data.insert_many(data_objects)
    log.info(
        "Inserted %d chunks for submodel=%s idShort=%s hash=%s",
        len(data_objects), submodel_id, id_short, content_hash[:12],
    )


def has_chunks(
    submodel_id: str,
    sm_element_path: str | None,
    content_hash: str,
) -> bool:
    """Return True if chunks for this exact (element, content_hash) already exist.

    Used to skip re-ingestion when an UPDATE event arrives but the document
    bytes have not actually changed.
    """
    client = _get_client()

    collection_name = _get_collection_name(WEAVIATE_COLLECTION)
    if not client.collections.exists(collection_name):
        return False

    collection = client.collections.get(collection_name)
    where_filter = (
        wvf.Filter.by_property("submodelId").equal(submodel_id)
        & wvf.Filter.by_property("smElementPath").equal(sm_element_path or "")
        & wvf.Filter.by_property("contentHash").equal(content_hash)
    )

    result = collection.query.fetch_objects(filters=where_filter, limit=1)
    return len(result.objects) > 0


def delete_documents(submodel_id: str, sm_element_path: str | None = None) -> None:
    """Delete all chunks matching submodel_id (optionally scoped to smElementPath)."""
    client = _get_client()

    collection_name = _get_collection_name(WEAVIATE_COLLECTION)
    if not client.collections.exists(collection_name):
        return

    collection = client.collections.get(collection_name)
    where_filter = wvf.Filter.by_property("submodelId").equal(submodel_id)

    if sm_element_path:
        where_filter = where_filter & wvf.Filter.by_property("smElementPath").equal(
            sm_element_path
        )

    collection.data.delete_many(where=where_filter)
    log.info(
        "Deleted chunks for submodel=%s smElementPath=%s",
        submodel_id, sm_element_path,
    )
