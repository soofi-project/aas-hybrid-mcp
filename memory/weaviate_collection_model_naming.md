---
name: Weaviate collection naming by embedding model
description: Weaviate collections include embedding model name in their name (e.g. aas_documents_text-embedding-3-small) for zero-downtime model switching
type: project
---

Weaviate collections are named `{base_collection}_{model_slug}` where the slug is extracted from `EMBEDDING_MODEL=provider:model` (model part only, no provider prefix).

**Pattern:** `aas_documents_text-embedding-3-small`, `IdtaTemplateSpec_text-embedding-3-small`

**Why:** Embedding model changes produce incompatible vectors. Without model-aware naming, switching models invalidates all existing vectors — no migration path.

**How to apply:** When changing `EMBEDDING_MODEL`, a new collection is automatically created (e.g. `aas_documents_nomic-embed-text`). Old collection remains untouched. Both embedding-service and MCP-server use the same `WEAVIATE_COLLECTION` env var, so the full path is `{WEAVIATE_COLLECTION}_{EMBEDDING_MODEL_slug}`. A/B comparison and rollback are instant.

**Slug rule:** Only the model part (after `:`) is used — not the provider. This means `openai:text-embedding-3-small` and `ollama:text-embedding-3-small` share the same collection (vectors are compatible, computation source differs).

**Files updated (2026-05-08):**
- `embedding-service/vectorstore.py` — `_get_collection_name()` helper, `_ensure_collection()` takes collection_name param
- `mcp-server/src/aas_hybrid_mcp/weaviate_client.py` — `_get_collection_name()` helper (must match embedding-service)
- `.env` — added documentation comments for EMBEDDING_MODEL → collection name expansion
- `submodel-templates-sync/main.py` — `_idta_collection()` and `_sync_hash_collection()` helpers, all IDTA/Hash references model-aware

**Not changed:**
- `IDTA_TEMPLATE_COLLECTION` = `IdtaTemplateSpec` — no hot-swap needed
- `submodel-templates-sync/` — uses fixed model, no swapping
- `docker-compose.yml` — `WEAVIATE_COLLECTION=aas_documents` stays as base name
- `embedding-service/config.py` — only documentation comment

**Runtime behavior:** On first read/write after model change, the new collection is auto-created with the standard properties. Existing collections are never modified or deleted.
