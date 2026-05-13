"""Synchronous Weaviate client — singleton connection and vector search.

The embedding-service ingests documents into Weaviate. This module only
searches. Query embeddings are computed with the same langchain model
(shared EMBEDDING_MODEL env var) to guarantee vector compatibility.
"""

import asyncio
import logging
import os
import re

import weaviate
import weaviate.classes.query as wvq

from aas_hybrid_mcp import reranker

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WEAVIATE_HOST: str = os.getenv("WEAVIATE_HOST", "weaviate")
WEAVIATE_HTTP_PORT: int = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT: int = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_COLLECTION: str = os.getenv("WEAVIATE_COLLECTION", "aas_documents")
IDTA_TEMPLATE_BASE: str = "IdtaTemplateSpec"


def _get_collection_name(base: str) -> str:
    """Build model-aware collection name from base + EMBEDDING_MODEL slug.

    Must match the helper in embedding-service/vectorstore.py.
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


def _count_chunks_for_submodel(submodel_id: str) -> int:
    """Cheap presence check: how many chunks are stored under this submodel_id."""
    client = _get_client()
    collection_name = _get_collection_name(WEAVIATE_COLLECTION)
    if not client.collections.exists(collection_name):
        return 0
    collection = client.collections.get(collection_name)
    result = collection.aggregate.over_all(
        filters=wvq.Filter.by_property("submodel_id").equal(submodel_id),
        total_count=True,
    )
    return result.total_count or 0


def _search_sync(
    query: str,
    *,
    submodel_id: str | None = None,
    limit: int = 10,
) -> dict:
    """Compute query embedding and run a near_vector search in Weaviate.

    Returns a dict with `results` and an optional `diagnostic` describing why
    a scoped query came back empty (chunks missing vs. semantic miss).
    """
    client = _get_client()

    collection_name = _get_collection_name(WEAVIATE_COLLECTION)

    if not client.collections.exists(collection_name):
        return {"results": [], "diagnostic": "collection_missing"}

    model = _get_embedding_model()
    vector = model.embed_query(query)

    collection = client.collections.get(collection_name)

    filters = None
    if submodel_id:
        filters = wvq.Filter.by_property("submodel_id").equal(submodel_id)

    # In vllm-mode pull a wider candidate set so the reranker has something to reorder.
    candidate_limit = (
        reranker.RERANKER_CANDIDATE_LIMIT
        if reranker.RERANKER_MODE == "vllm"
        else limit
    )

    response = collection.query.near_vector(
        near_vector=vector,
        limit=candidate_limit,
        filters=filters,
        return_metadata=wvq.MetadataQuery(distance=True),
    )

    results = []
    for obj in response.objects:
        props = obj.properties
        raw_url = props.get("source_url", "")
        raw_page = props.get("source_page", 0) or 0

        # Build a jump-URL for browser navigation to the specific PDF page.
        jump_url = f"{raw_url}#page={raw_page}" if raw_url and raw_page > 0 else raw_url

        # Only emit fields that carry information; empty strings / zero-page
        # signal "not applicable" (e.g. SubmodelElementList children have no
        # idShort) and are dropped to reduce LLM context noise.
        item: dict = {
            "text": props.get("text", ""),
            "source": props.get("source", "other"),
            "score": 1 - (obj.metadata.distance or 0),
        }
        for key, value in (
            ("source_heading", props.get("source_heading", "")),
            ("source_page", raw_page),
            ("source_url", raw_url),
            ("source_filename", props.get("source_filename", "")),
            ("source_jump_url", jump_url),
            ("submodel_id", props.get("submodel_id", props.get("submodelId", ""))),
            ("sm_element_path", props.get("sm_element_path", props.get("smElementPath", ""))),
            ("id_short", props.get("id_short", props.get("idShort", ""))),
            ("content_hash", props.get("content_hash", props.get("contentHash", ""))),
        ):
            if value not in ("", 0, None):
                item[key] = value
        results.append(item)

    reranker_used = False
    if reranker.RERANKER_MODE == "vllm" and results:
        ranked = reranker.rerank(query, [r["text"] for r in results])
        if ranked is not None:
            reranked = []
            for item in ranked[:limit]:
                idx = item["index"]
                if idx >= len(results):
                    log.warning(
                        "Reranker returned out-of-bounds index %d (results size=%d), skipping",
                        idx, len(results),
                    )
                    continue
                r = results[idx]
                r["reranker_score"] = round(float(item["score"]), 4)
                reranked.append(r)
            results = reranked
            reranker_used = True
        else:
            results = results[:limit]
    else:
        results = results[:limit]

    out: dict = {"results": results, "reranker_used": reranker_used}
    if not results and submodel_id:
        chunk_count = _count_chunks_for_submodel(submodel_id)
        out["chunk_count"] = chunk_count
        out["diagnostic"] = "not_indexed" if chunk_count == 0 else "no_match"
    return out


async def search(
    query: str,
    *,
    submodel_id: str | None = None,
    limit: int = 10,
) -> dict:
    """Async wrapper — runs the sync Weaviate search in a thread pool."""
    return await asyncio.to_thread(
        _search_sync,
        query,
        submodel_id=submodel_id,
        limit=limit,
    )


# ---------------------------------------------------------------------------
# Template search (sync — called via asyncio.to_thread from MCP tools)
# ---------------------------------------------------------------------------


def _search_templates_sync(
    query: str,
    *,
    template_name: str | None = None,
    limit: int = 5,
) -> dict:
    """Compute query embedding and run a near_vector search on IdtaTemplateSpec.

    Returns `{"results": [...], "reranker_used": bool}`.
    """
    client = _get_client()

    collection_name = _get_collection_name(IDTA_TEMPLATE_BASE)

    if not client.collections.exists(collection_name):
        return {"results": [], "reranker_used": False}

    model = _get_embedding_model()
    vector = model.embed_query(query)

    collection = client.collections.get(collection_name)

    filters = None
    if template_name:
        filters = wvq.Filter.by_property("templateName").equal(template_name)

    candidate_limit = (
        reranker.RERANKER_CANDIDATE_LIMIT
        if reranker.RERANKER_MODE == "vllm"
        else limit
    )

    response = collection.query.near_vector(
        near_vector=vector,
        limit=candidate_limit,
        filters=filters,
        return_metadata=wvq.MetadataQuery(distance=True),
    )

    results = []
    for obj in response.objects:
        item: dict = {
            "text": obj.properties.get("text", ""),
            "score": 1 - (obj.metadata.distance or 0),
        }
        for key in ("templateName", "pdfSource", "version", "semanticId"):
            value = obj.properties.get(key, "")
            if value:
                item[key] = value
        results.append(item)

    reranker_used = False
    if reranker.RERANKER_MODE == "vllm" and results:
        ranked = reranker.rerank(query, [r["text"] for r in results])
        if ranked is not None:
            reranked = []
            for item in ranked[:limit]:
                idx = item["index"]
                if idx >= len(results):
                    log.warning(
                        "Reranker returned out-of-bounds index %d (results size=%d), skipping",
                        idx, len(results),
                    )
                    continue
                r = results[idx]
                r["reranker_score"] = round(float(item["score"]), 4)
                reranked.append(r)
            results = reranked
            reranker_used = True
        else:
            results = results[:limit]
    else:
        results = results[:limit]

    return {"results": results, "reranker_used": reranker_used}


async def search_templates(
    query: str,
    *,
    template_name: str | None = None,
    limit: int = 5,
) -> dict:
    """Async wrapper — runs the sync template search in a thread pool."""
    return await asyncio.to_thread(
        _search_templates_sync,
        query,
        template_name=template_name,
        limit=limit,
    )


def close() -> None:
    """Close the Weaviate client connection."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
        log.info("Weaviate client closed")
