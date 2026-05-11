---
name: Planned features
description: Features claimed in paper as future work, not yet implemented
type: project
---

Planned features moved from paper sections 4.4-4.5 to "future work". Paper updated:
Sec 4.4+4.5 merged in Sec 4.6 "Planned Retrieval Enhancements" + Benchmark B ablation table adjusted (Reranker/Query Rewrite rows removed).

| # | Feature | Paper Section | .env vars | Code status | Notes |
|---|---|---|---|---|---|
| 1 | **Cross-encoder Reranker** | Sec 4.4 | `RERANKER_MODE`, `RERANKER_URL`, `RERANKER_CANDIDATE_LIMIT` | Env vars defined; no reranker code in MCP server or Weaviate client | Default `distance` mode works; `vllm` mode is a no-op. Need: add reranker call in `weaviate_client.py` `_search_sync` + vLLM reranker endpoint |
| 2 | **LLM-based Query Rewriting** | Sec 4.5 | — | Not implemented | Expand raw query with synonyms/domain terms before vector search. Could live in `search_aas_documents` tool or as a pre-retrieval agent node |
| 3 | **HyDE (Hypothetical Document Embeddings)** | Sec 4.5 | — | Not implemented | Agent generates hypothetical answer passage, then embeds that for retrieval instead of raw query. Paper cites `gao2022hyde` |

### Dependencies
- Reranker: requires `up.sh --vllm` (Qwen2-Reranker-7B on separate vLLM instance) OR plugging into existing reranker model if already deployed.
- Query Rewrite / HyDE: require additional LLM call per search — latency impact to benchmark.

### Paper impact
If implemented before final submission, Sec 4.6 can be split back into three subsections (4.4/4.5/4.6) and the three rows can be restored to the ablation matrix in Table 2.
