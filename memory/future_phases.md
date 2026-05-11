---
name: Future phases and open tasks
description: Phase 9 and ongoing improvement tasks
type: project
---

## Phase 9: Retrieval ablation techniques
**Status:** 🟦 Planned

### Cross-encoder Reranker
- Re-rank Weaviate vector search candidates with a locally hosted Qwen2-Reranker-7B via vLLM
- Env vars scaffolded (`RERANKER_MODE`, `RERANKER_URL`, `RERANKER_CANDIDATE_LIMIT`); no functional code yet
- Where: `weaviate_client.py` `_search_sync` — when `RERANKER_MODE=vllm`, fetch `RERANKER_CANDIDATE_LIMIT` candidates, POST + query to `RERANKER_URL`, re-sort and truncate to `limit`

### Query Rewriting
- LLM-based query expansion with synonyms and domain terminology before vector search
- Bench B ablation axis
- Where: `search_aas_documents` MCP tool — add optional `rewrite_query` flag; agent invokes LLM with domain prompt to generate expanded query terms

### HyDE (Hypothetical Document Embeddings)
- Generate a hypothetical answer passage; embed _that_ instead of the raw user query
- Bench B ablation axis, ref: gao2022hyde
- Where: embedding-service — new endpoint `/embed_with_hyde` that takes query + system context → generates hypothetical doc → embeds

## Phase X: Kubernetes Deployment
**Status:** 🟦 Planned
- Package MCP endpoint as a Helm chart for production-grade deployment (auto-scaling, self-healing, rolling updates).
- Makes the endpoint composable: integrable into existing industrial K8s installations (edge/cloud) without requiring the full development stack.
- Ups the architecture from a Docker Compose demonstrator to a deployable component for industrial operators.

## Open engineering tasks

### Pydantic coercion centralization
- **Where:** `qwen_parser.py`, `agent_plan_nodes.py`, `crag_nodes.py`, `rewoo_nodes.py`, `reflexion_graph_nodes.py`, `agent_supervisor_nodes.py`
- **Problem:** Each parse function has its own ad-hoc coercion (`str → list`, `float → literal`, etc.)
- **Fix:** Extract `_coerce_final_answer`, `_coerce_judgment`, etc. into a single module (e.g. `aas_agent/coercion.py`) with per-schema normalizers reused by all parsers

### Bind-mount `C:\134` issue
- **Where:** `docker-compose.yml` lines 477-501
- **Problem:** Individual file mounts work but are fragile — new files must be added manually
- **Nice-to-have:** Investigate `docker compose` on Windows WSL2 / Hyper-V for reliable directory mounts

### Reflexion finalizer quality
- **Where:** `reflexion_graph_nodes.py`
- **Problem:** Best answer text is now tracked but the LLM may still regenerate instead of using it
- **Improvement:** Prompt tweak to make the finalizer _use_ the best answer as-is when confidence is high
