---
name: Task - Reranker Integration
description: Integriere qwen3-reranker-4b (H200) in AAS MCP Weaviate search
type: task
status: open
priority: high
depends_on: task_rag_metadata_overhaul
---

## Summary

Reranker läuft bereits auf H200 (`10.2.10.33:8003`), ENV-Vars sind in `.env.vllm`
gescaffolded. Fehlt: Python-Code in `weaviate_client.py` der die ENV-Vars liest
und das two-phase retrieval durchführt.

**Reference implementation:** `soofi-trainer/vector-mcp/src/vector_mcp/server.py`
(func `rerank()` :60-126, func `search_documents()` :268-302)

## Subtasks

### T1: Reranker-Modul anlegen
**File:** `mcp-server/src/aas_hybrid_mcp/reranker.py` (neu)
- `RERANKER_MODE`, `RERANKER_URL`, `RERANKER_CANDIDATE_LIMIT` aus ENV lesen
- Lazy `httpx.Client` singleton (base_url + 5s timeout wie in soofi-trainer)
- `rerank(query, texts) -> list[dict] | None` — POST `/rerank`, model `qwen3-reranker-4b`
- Graceful fallback: Exception → `None` zurück, kein hard failure
- Logging mit timing (ms), top/bottom score

### T2: `_search_sync()` two-phase retrieval + metadata im response
**File:** `mcp-server/src/aas_hybrid_mcp/weaviate_client.py:158-209`
- Wenn `RERANKER_MODE == "vllm"`:
  1. `near_vector(limit=RERANKER_CANDIDATE_LIMIT)` statt `limit`
  2. `rerank(query, [r["text"] ...])` aufrufen
  3. Results per `reranker_score` sortiert, auf `limit` truncieren
  4. Fallback bei `None`: `results[:limit]`, `score = 1 - distance`
- Ergebnisse: `reranker_score` + `reranker_used` flag hinzufügen
- Neue fields aus Task rag_metadata_overhaul:
  `source_heading`, `source_page`, `source_url`, `source_filename`, `content_hash`
- Computed: `source_jump_url` = `{source_url}#page={source_page}`
- Ref: soofi-trainer `server.py:268-302`

### T3: `_search_templates_sync()` two-phase retrieval
**File:** `mcp-server/src/aas_hybrid_mcp/weaviate_client.py:232-272`
- Gleiches Pattern wie T2 für template search
- Collection: `IdtaTemplateSpec{slug}`

### T4: Dependency hinzufügen
**File:** `mcp-server/pyproject.toml`
- `httpx>=0.28.1`

### T5: Agent evidence classification fix
**File:** `aas-agent/src/aas_agent/agent_plan_nodes.py:187-193`
- `source == "document"` → jetzt matcht (war filename, fiel durch zu "other")
- Agent kann `source_heading`, `source_page`, `source_jump_url` im answer zitieren

### T6: Planungsdoku updaten
**Files:**
- `memory/planned_features.md` — Reranker-Zeile: "Env vars defined" → "Implemented"
- `memory/future_phases.md` — Phase 9 Reranker: 🟦 Planned → ✅ Done
- `memory/task_reranker_integration.md` — this file, status → done

## Config

| Variable | Default | vllm | Source |
|---|---|---|---|
| `RERANKER_MODE` | `distance` | `vllm` | `.env` → `.env.vllm` |
| `RERANKER_URL` | — | `http://10.2.10.33:8003` | `.env.vllm` |
| `RERANKER_CANDIDATE_LIMIT` | — | `20` | `.env.vllm` |

## Acceptance Criteria

- `./up.sh --vllm` → Reranker live, `reranker_used: true` in search results
- `./up.sh` (ohne --vllm) → distance fallback, behavior unverändert
- Reranker down / nicht erreichbar → graceful fallback, kein crash
- Top-K results haben `reranker_score` field (float, 0-1)
- `httpx` timeout (5s) → fallback, nicht hang
- Template search + document search beide reranked
- Agent evidence classification fix
- `source_jump_url` berechnet
- Alle properties snake_case
