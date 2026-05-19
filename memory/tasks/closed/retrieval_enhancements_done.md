---
name: Retrieval Enhancements — Phase 9 Done
description: Cross-encoder Reranker + LLM Query Rewriting + Weaviate Metadata + PDF Inline Viewer — alle live
type: task
status: done
---

## Was umgesetzt

**Cross-encoder Reranker** (`mcp-server/.../reranker.py`): Qwen3-Reranker-4B via vLLM (`RERANKER_MODE=vllm`, Port 8003). Two-phase Retrieval: fetch `RERANKER_CANDIDATE_LIMIT` Kandidaten, reranken, auf Top-K truncaten. Graceful Distance-Fallback wenn Reranker nicht erreichbar. Response-Felder: `reranker_used: bool`, `reranker_score: float`.

**LLM Query Rewriting** (`query_rewriter.py`): basiert auf Ma et al. 2023 (`ma2023rewrite`). Scoped-Modus: wenn `submodel_id`-Filter aktiv, werden Asset-Entity-Referenzen aus dem Query gestripppt und technische Synonyme expandiert. `QUERY_REWRITE_MODE=on` in `.env.vllm`, 30s Timeout (`QUERY_REWRITE_TIMEOUT`), graceful Fallback auf Original-Query.

**Weaviate Metadata Overhaul**: Chunks haben jetzt `source_heading`, `source_page` (int), `source_url` (user-visible BaSyx-URL), `source_filename`, `content_hash`, `source_jump_url` = `{source_url}#page={source_page}`. Alle Properties snake_case. `source` ist fixed category `"document"`. Docling-Modelle ins Image gebakt (`HF_HUB_OFFLINE=1`).

**PDF Inline Viewer**: Nginx-Sidecar `basyx-viewer-proxy` (Port 8091) schreibt `Content-Disposition: attachment` → `inline` um. `BASYX_PUBLIC_URL=http://localhost:8091`. Source-Jump-URLs öffnen PDFs im Browser-Tab mit korrektem Page-Jump. BaSyx bleibt intern unverändert auf Port 8081.

## Paper-Relevanz

- §08 "Retrieval Pipeline" → Unterabschnitt "Retrieval Enhancements": Reranker + Query Rewriting beschrieben
- `\cite{ma2023rewrite}` in `08-retrieval-pipeline.tex` für Query Rewriting
- HyDE explizit verworfen — aus Paper §08 und `main.bib` entfernt (kein `gao2022hyde`)
