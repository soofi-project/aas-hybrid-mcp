---
name: Planned features
description: Features claimed in paper as future work, not yet implemented
type: project
---

Planned features moved from paper sections 4.4-4.5 to "future work". Paper updated:
Sec 4.4+4.5 merged in Sec 4.6 "Planned Retrieval Enhancements" + Benchmark B ablation table adjusted (Reranker/Query Rewrite rows removed).

| # | Feature | Paper Section | .env vars | Code status | Notes |
|---|---|---|---|---|---|
| 1 | **Cross-encoder Reranker** | Sec 4.4 | `RERANKER_MODE`, `RERANKER_URL`, `RERANKER_CANDIDATE_LIMIT`, `RERANKER_MODEL` | ✅ **Implemented (2026-05-13)** | Two-phase retrieval in both `_search_sync` and `_search_templates_sync`; new `reranker.py` module; `reranker_used` flag + per-item `reranker_score` exposed in MCP tool responses; graceful fallback when reranker unreachable. Model: `qwen3-reranker-4b` on H200 vLLM. |
| 2 | **LLM-based Query Rewriting** | Sec 4.5 | `QUERY_REWRITE_MODE`, `QUERY_REWRITE_URL`, `QUERY_REWRITE_MODEL`, `QUERY_REWRITE_TIMEOUT` | ✅ **Implemented (2026-05-13, ma2023rewrite)** | Scoped adaptation: asset-name stripping when `submodel_id` is set. New `query_rewriter.py` module; `asset_name` + `doc_language` params in `search()`; `query_rewritten` + `rewritten_query` in MCP tool responses; graceful fallback when rewriter unreachable. |
| 3 | **HyDE (Hypothetical Document Embeddings)** | Sec 4.5 | — | Not implemented | Agent generates hypothetical answer passage, then embeds that for retrieval instead of raw query. Paper cites `gao2022hyde` |

### Dependencies
- Reranker: `up.sh --vllm` activates it (Qwen3-Reranker-4b vLLM endpoint on H200 `10.2.10.33:8003`). Without `--vllm`, `RERANKER_MODE=distance` keeps behavior unchanged.
- Query Rewrite / HyDE: require additional LLM call per search — latency impact to benchmark.

### Paper impact
If implemented before final submission, Sec 4.6 can be split back into three subsections (4.4/4.5/4.6) and the three rows can be restored to the ablation matrix in Table 2.
