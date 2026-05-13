---
name: Task - HyDE (Hypothetical Document Embeddings)
description: Hypothetisches Antwortfragment generieren und dessen Embedding für Vector Search verwenden
type: task
status: pending
priority: high
depends_on: task_reranker_integration
---

## Status

**Nicht gestartet.** Wartet auf: Reranker Integration (Phase 9, nach `task_reranker_integration`).

## Ziel

Statt dem raw user query ein hypothetisches Antwortfragment (Hypothetical Document) via LLM generieren und dessen Embedding für den Vector Search in Weaviate verwenden. Basierend auf HyDE (Gao et al., ACL 2023, `gao2022hyde`). Verbessert Retrieval-Qualität bei questions/queries, die nicht wörtlich im Corpus vorkommen.

## Architektur

Neues Modul `mcp-server/src/aas_hybrid_mcp/hyde.py` analog zu `reranker.py`:
- Lazy `httpx.Client`-Singleton
- POST an LLM endpoint (vLLM, `HYDE_URL`) mit HyDE-spezifischem prompt
- Gibt hypothetical document text zurück
- Embedding via existing embedding service oder direkt über embedding model
- Graceful fallback: Fehler → original query embedding unverändert
- Neue Config: `HYDE_MODE` (`on`/`off`), `HYDE_URL`, `HYDE_MODEL`, `HYDE_TIMEOUT`, `HYDE_MAX_TOKENS`

Integration in `weaviate_client.py`:
- `_search_sync` und `_search_templates_sync`: wenn `HYDE_MODE=on`, zuerst HyDE doc generieren, dann embedding davon verwenden statt query embedding
- Response-Dict erweitert um `hyde_used: bool`, `hyde_document: str`

## Subtasks

- **T1:** `hyde.py` modul:
  - `generate(query, domain_context=None) → str` — hypothetical document text
  - HyDE prompt: "Generate a hypothetical answer document for the following query in the context of AAS/Industrial Digital Twin..."
  - Lazy httpx client, timeout from env
  - Exception → original query return als fallback

- **T2:** `.env` + `.env.vllm` config vars:
  - `HYDE_MODE=off` (default)
  - `HYDE_MODE=on` (vllm overlay)
  - `HYDE_URL` (vLLM endpoint, same as LLM_BASE_URL or separate)
  - `HYDE_MODEL` (default: same as main LLM)
  - `HYDE_TIMEOUT=10` (seconds, HyDE generation is longer)
  - `HYDE_MAX_TOKENS=512` (max length of hypothetical document)

- **T3:** `weaviate_client.py:_search_sync` integration:
  - Vor `near_vector()`: wenn `HYDE_MODE=on`, HyDE doc generieren
  - Embedding des HyDE docs verwenden (via existing embedding logic oder direct embedding service call)
  - Response: `hyde_used: bool`, `hyde_document: str` hinzufügen
  - Fallback: HyDE error → original query embedding, `hyde_used: false`

- **T4:** `weaviate_client.py:_search_templates_sync` + async wrapper:
  - Gleiches Pattern wie T3
- **T5:** `tools/template_search.py`:
  - `hyde_used`, `hyde_document` aus `weaviate_client` an MCP Response durchreichen

- **T6:** `tools/document_search.py`:
  - `hyde_used`, `hyde_document` aus `weaviate_client.search()` ins MCP Response

- **T7:** Planungsdoku updaten:
  - `memory/planned_features.md` — HyDE: "Not implemented" → "Implemented"
  - `memory/future_phases.md` — Phase 9 HyDE: 🟦 Planned → ✅ Done
  - `memory/task_hyde.md` — this file, status → done

## Config

| Variable | Default | vllm | Source |
|---|---|---|---|
| `HYDE_MODE` | `off` | `on` | `.env` → `.env.vllm` |
| `HYDE_URL` | — | `http://localhost:8120` (or vLLM direct) | `.env.vllm` |
| `HYDE_MODEL` | — | same as `LLM_MODEL` | `.env.vllm` |
| `HYDE_TIMEOUT` | `10` | `10` | `.env` |
| `HYDE_MAX_TOKENS` | `512` | `512` | `.env` |

## Acceptance Criteria

- `HYDE_MODE=off` → behavior unverändert, kein LLM call
- `HYDE_MODE=on` → Hypothetical doc generiert, Embedding davon für Vector Search, `hyde_used: true` im Response
- HyDE LLM endpoint down/error → graceful fallback, original query embedding, `hyde_used: false`
- Template search + document search beide HyDE verwenden (when on)
- Hypothetical document text im MCP tool response sichtbar (Debug/Inspection)
- Latency overhead: < `HYDE_TIMEOUT` (10s)
- Works with Query Rewrite + Reranker: Query Rewrite → HyDE doc → Embedding → Vector Search → Rerank (keine Konflikte, HyDE ersetzt query embedding step)
- Benchmark B: ablation test against baseline (no HyDE) → track recall@K, MRR, NDCG@
