"""Synchronous Weaviate client — singleton connection and vector search.

The embedding-service ingests documents into Weaviate. This module only
searches. Query embeddings are computed with the same langchain model
(shared EMBEDDING_MODEL env var) to guarantee vector compatibility.
"""

import asyncio
import logging
import os

import weaviate
import weaviate.classes.query as wvq

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WEAVIATE_HOST: str = os.getenv("WEAVIATE_HOST", "weaviate")
WEAVIATE_HTTP_PORT: int = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT: int = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_COLLECTION: str = os.getenv("WEAVIATE_COLLECTION", "aas_documents")

# ---------------------------------------------------------------------------
# Embedding model (lazy singleton)
# ---------------------------------------------------------------------------

_embedding_model = None


def _get_embedding_model():
    """Create the langchain embedding model from EMBEDDING_MODEL env var.

    Mirrors embedding-service/config.py to guarantee identical vectors.
    """
    global _embedding_model
    if _embedding_model is not None:
        return _embedding_model

    embedding_config = os.getenv("EMBEDDING_MODEL")
    if not embedding_config:
        raise ValueError("EMBEDDING_MODEL not set (expected format: provider:model)")

    if ":" not in embedding_config:
        raise ValueError(
            f"EMBEDDING_MODEL must be in provider:model format, got: {embedding_config}"
        )

    provider, model = embedding_config.split(":", 1)

    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings

        ollama_host = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
        log.info("Using embedding model ollama:%s at %s", model, ollama_host)
        _embedding_model = OllamaEmbeddings(model=model, base_url=ollama_host)
        return _embedding_model

    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_openai import OpenAIEmbeddings
    from langchain_voyageai import VoyageAIEmbeddings

    providers = {
        "openai": ("OPENAI_API_KEY", lambda key: OpenAIEmbeddings(model=model, api_key=key)),
        "google_genai": ("GOOGLE_API_KEY", lambda key: GoogleGenerativeAIEmbeddings(model=model, google_api_key=key)),
        "voyageai": ("VOYAGE_API_KEY", lambda key: VoyageAIEmbeddings(model=model, api_key=key)),
    }

    if provider not in providers:
        supported = ", ".join(["ollama", *providers.keys()])
        raise ValueError(f"Unknown embedding provider: {provider} (supported: {supported})")

    env_var, factory = providers[provider]
    api_key = os.getenv(env_var)
    if not api_key:
        raise ValueError(f"API key {env_var} not set for provider {provider}")

    log.info("Using embedding model %s:%s", provider, model)
    _embedding_model = factory(api_key)
    return _embedding_model


# ---------------------------------------------------------------------------
# Weaviate client (lazy singleton)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Search (sync — called via asyncio.to_thread from MCP tools)
# ---------------------------------------------------------------------------


def _search_sync(
    query: str,
    *,
    submodel_id: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Compute query embedding and run a near_vector search in Weaviate."""
    client = _get_client()

    if not client.collections.exists(WEAVIATE_COLLECTION):
        return []

    model = _get_embedding_model()
    vector = model.embed_query(query)

    collection = client.collections.get(WEAVIATE_COLLECTION)

    # Build optional filter
    filters = None
    if submodel_id:
        filters = wvq.Filter.by_property("submodelId").equal(submodel_id)

    response = collection.query.near_vector(
        near_vector=vector,
        limit=limit,
        filters=filters,
        return_metadata=wvq.MetadataQuery(distance=True),
    )

    return [
        {
            "text": obj.properties.get("text", ""),
            "source": obj.properties.get("source", ""),
            "submodelId": obj.properties.get("submodelId", ""),
            "smElementPath": obj.properties.get("smElementPath", ""),
            "idShort": obj.properties.get("idShort", ""),
            "score": 1 - (obj.metadata.distance or 0),
        }
        for obj in response.objects
    ]


async def search(
    query: str,
    *,
    submodel_id: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Async wrapper — runs the sync Weaviate search in a thread pool."""
    return await asyncio.to_thread(
        _search_sync,
        query,
        submodel_id=submodel_id,
        limit=limit,
    )


def close() -> None:
    """Close the Weaviate client connection."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
        log.info("Weaviate client closed")
