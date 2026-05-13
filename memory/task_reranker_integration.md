---
name: Task - Reranker Integration
description: Integriere qwen3-reranker-4b (H200) in AAS MCP Weaviate search
type: task
status: done
priority: high
depends_on: task_rag_metadata_overhaul
---

## Status (2026-05-13)

**Done.** Two-phase retrieval läuft in beiden Search-Pfaden
(`_search_sync` + `_search_templates_sync`); `reranker_used`-Flag
+ `reranker_score` pro Item sind im MCP-Tool-Response.

**Was beim Ist-Soll-Abgleich schon erledigt war:**
- T4 (`httpx>=0.28,<1`) — bereits in `mcp-server/pyproject.toml:18`
- T5 (Evidence-Klassifikation) — `"document"` war bereits in der Whitelist
  in `agent_plan_nodes.py:191`. Seit `task_rag_metadata_overhaul` kommt aus
  dem Search bereits `source="document"` als fixed category statt Filename,
  fällt nicht mehr auf `"other"` zurück.
- T2-Metadata-Teil (`source_heading`, `source_page`, `source_url`,
  `source_filename`, `source_jump_url`, `content_hash` im Response) — schon
  durch rag_metadata_overhaul geliefert (`weaviate_client.py:201-214`).

**Was tatsächlich geliefert wurde:**
- `mcp-server/src/aas_hybrid_mcp/reranker.py` (neu) — Port aus
  `soofi-trainer/vector-mcp/src/vector_mcp/server.py:60-126`. Strikte
  ENV-Validierung beim Import (`RERANKER_MODE` muss `vllm` oder
  `distance` sein; im `vllm`-Mode sind `RERANKER_URL` +
  `RERANKER_CANDIDATE_LIMIT` Pflicht, sonst RuntimeError). Lazy
  `httpx.Client`-Singleton mit 5s timeout. `rerank()` gibt `None` bei
  Exception zurück (Caller fällt graceful auf distance zurück).
  Default-Modell `qwen3-reranker-4b` via `RERANKER_MODEL` env var
  überschreibbar.
- `weaviate_client.py:_search_sync` — im `vllm`-Mode
  `near_vector(limit=RERANKER_CANDIDATE_LIMIT)`, danach Reranker mit
  Out-of-Bounds-Index-Guard, Top-K-Truncation auf `limit`. Response-Dict
  erweitert um `reranker_used: bool`. `score = 1 - distance` bleibt
  zusätzlich zum `reranker_score: float` (4 Stellen gerundet).
- `weaviate_client.py:_search_templates_sync` + async-Wrapper — gleiches
  Pattern; **Vertragsänderung:** Rückgabe von `list[dict]` → `dict`
  (`{results, reranker_used}`).
- `tools/template_search.py` — auf neue Rückgabe-Shape angepasst,
  `reranker_used` ans MCP-Response durchgereicht.
- `tools/document_search.py` — `reranker_used` aus `weaviate_client.search()`
  ins MCP-Response durchgereicht (war vorher stripped).
- `memory/planned_features.md` + `memory/future_phases.md` — Status auf
  ✅ Done gesetzt.

**Noch zu tun (manuell vom User):**
- `./down.sh && ./up.sh --vllm` → Sanity-Check `reranker_used: true` in
  Search-Tool-Responses, Top-K nach `reranker_score` sortiert.
- `./down.sh && ./up.sh` (ohne `--vllm`) → Baseline-Check
  `reranker_used: false`, Verhalten unverändert.
- Reranker-Endpoint kurzfristig blockieren (z.B. `RERANKER_URL` auf einen
  ungültigen Port setzen) → 5s-Timeout, graceful Fallback, keine Crashes
  zur Caller-Seite.

## Summary (ursprünglich)

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
