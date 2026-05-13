---
name: Task - Query Rewriting
description: LLM-basierte Query-Expansion mit Synonymen und Dominentminologie vor Vector Search
type: task
status: pending
priority: high
depends_on: task_reranker_integration
---

## Status

**Nicht gestartet.** Wart auf: Reranker Integration (Phase 9, nach `task_reranker_integration`).

## Ziel

Raw User Query durch LLM.expandieren mit Synonymen, Domänenbegriffen und alternativen Formulierungen, bevor der Vector Search in Weaviate stattfindet. Ziel: bessere Recall bei domain-spezifischen Queries, die nicht wörtlich im Corpus vorkommen.

## Architektur

Neues Modul `mcp-server/src/aas_hybrid_mcp/query_rewriter.py` analog zu `reranker.py`:
- Lazy `httpx.Client`-Singleton
- POST an LLM endpoint (vLLM, `QUERY_REWRITE_URL`) mit domain-spezifischem prompt
- Gibt expanded query string zurück
- Graceful fallback: Fehler → original query unverändert
- Neue Config: `QUERY_REWRITE_MODE` (`on`/`off`), `QUERY_REWRITE_URL`, `QUERY_REWRITE_MODEL`, `QUERY_REWRITE_TIMEOUT`

Integration in `weaviate_client.py`:
- `_search_sync` und `_search_templates_sync`: vor `near_vector()` den Query rewrite (wenn `QUERY_REWRITE_MODE=on`)
- Response-Dict erweitert um `query_rewritten: bool`, `rewritten_query: str` (when rewrite ran)

## Subtasks

- **T1:** `query_rewriter.py` modul:
  - `rewrite(query, domain_context=None) → str` 
  - LLM prompt: domain terminology expansion für AAS/Industrie
  - Lazy httpx client, timeout from env
  - Exception → original query return

- **T2:** `.env` + `.env.vllm` config vars:
  - `QUERY_REWRITE_MODE=off` (default)
  - `QUERY_REWRITE_MODE=on` (vllm overlay)
  - `QUERY_REWRITE_URL` (vllm, same as LLM_BASE_URL or separate)
  - `QUERY_REWRITE_MODEL` (default: same as main LLM)
  - `QUERY_REWRITE_TIMEOUT=5` (seconds)

- **T3:** `weaviate_client.py:_search_sync` integration:
  - Vor `near_vector()`: wenn `QUERY_REWRITE_MODE=on`, Query rewrite aufrufen
  - Response: `query_rewritten: bool`, `rewritten_query: str` hinzufügen
  - Fallback: rewrite error → original query, `query_rewritten: false`

- **T4:** `weaviate_client.py:_search_templates_sync` + async wrapper:
  - Gleiches Pattern wie T3
  - `tools/template_search.py`: `query_rewritten`, `rewritten_query` an MCP Response durchreichen

- **T5:** `tools/document_search.py`:
  - `query_rewritten`, `rewritten_query` aus `weaviate_client.search()` ins MCP Response

- **T6:** Planungsdoku updaten:
  - `memory/planned_features.md` — Query Rewriting: "Not implemented" → "Implemented"
  - `memory/future_phases.md` — Phase 9 Query Rewriting: 🟦 Planned → ✅ Done
  - `memory/task_query_rewriting.md` — this file, status → done

## Config

| Variable | Default | vllm | Source |
|---|---|---|---|
| `QUERY_REWRITE_MODE` | `off` | `on` | `.env` → `.env.vllm` |
| `QUERY_REWRITE_URL` | — | `http://localhost:8120` (or vLLM direct) | `.env.vllm` |
| `QUERY_REWRITE_MODEL` | — | same as `LLM_MODEL` | `.env.vllm` |
| `QUERY_REWRITE_TIMEOUT` | `5` | `5` | `.env` |

## Acceptance Criteria

- `QUERY_REWRITE_MODE=off` → behavior unverändert, kein LLM call
- `QUERY_REWRITE_MODE=on` → Query wird expandiert, `query_rewritten: true` im Response
- Rewrite LLM endpoint down/error → graceful fallback, original query, `query_rewritten: false`
- Template search + document search beide rewritten query verwenden
- Rewritten query im MCP tool response sichtbar (Debug/Inspection)
- Latency overhead: < `QUERY_REWRITE_TIMEOUT` (5s) 
- Works with Reranker: Rewrite → Vector Search → Rerank (kein Konflikt, rewrite vor Vector Search, reranker afterward)
