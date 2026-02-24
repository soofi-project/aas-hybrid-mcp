"""Centralized configuration from environment variables."""

import os
import logging

log = logging.getLogger(__name__)

# Weaviate
WEAVIATE_HOST: str = os.getenv("WEAVIATE_HOST", "weaviate")
WEAVIATE_HTTP_PORT: int = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT: int = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_COLLECTION: str = os.getenv("WEAVIATE_COLLECTION", "aas_documents")

# BaSyx
BASYX_SUBMODEL_REPO: str = os.getenv("BASYX_SUBMODEL_REPO", "http://aas-environment:8081")

# PDF processing
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "150"))
EMBEDDING_BATCH_SIZE: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "100"))
DOWNLOAD_TIMEOUT: int = int(os.getenv("DOWNLOAD_TIMEOUT", "30"))

# Flask
FLASK_PORT: int = int(os.getenv("FLASK_PORT", "8000"))


OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")


def get_embedding_model():
    """Create a langchain embedding model from EMBEDDING_MODEL env var.

    Format: provider:model_name
    Examples:
        openai:text-embedding-3-small
        ollama:nomic-embed-text
        google_genai:text-embedding-004
        voyageai:voyage-3
    """
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

        log.info("Using embedding model ollama:%s at %s", model, OLLAMA_HOST)
        return OllamaEmbeddings(model=model, base_url=OLLAMA_HOST)

    # Cloud providers — require an API key
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
    return factory(api_key)
