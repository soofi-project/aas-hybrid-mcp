---
name: Future phases and open tasks
description: Phase 9 and ongoing improvement tasks
type: project
---

## Phase 9: Retrieval ablation techniques
**Status:** 🟦 Planned (reranker ✅ done 2026-05-13)

### Cross-encoder Reranker
**Status:** ✅ Done (2026-05-13)
- Two-phase retrieval in `weaviate_client.py` (both `_search_sync` and `_search_templates_sync`): pull `RERANKER_CANDIDATE_LIMIT` candidates, POST to `RERANKER_URL/rerank` (Cohere-compatible), sort by `relevance_score`, truncate to `limit`
- New module `mcp-server/src/aas_hybrid_mcp/reranker.py` — ported from `soofi-trainer/vector-mcp/src/vector_mcp/server.py:60-126`
- Graceful fallback: reranker down → `reranker_used: false`, distance-based ranking, no crash
- Search tool responses now expose `reranker_used: bool` at top level and `reranker_score: float` per item (when reranker ran)
- Model: `qwen3-reranker-4b` (vLLM on H200, `http://10.2.10.33:8003`)

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
- **Where:** `qwen_parser.py`, `agent_plan_nodes.py`, `crag_nodes.py`, `rewoo_nodes.py`, `reflexion_graph_nodes.py`
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

## Phase: Specialized Worker vs. Generalist Agent
**Status:** 🔴 Research idea (Future Work in paper §Future Work)

**Concept:** Supervisor decomposes queries → domain-specialized fine-tuned workers → supervisor evaluat → (re-dispatch unresolved → ... → synthesize)

**Two competing approaches:**

1. **Multi-specialist:** Small models (1.5--3B) each fine-tuned with a LoRA adapter for one retrieval domain
   - Worker A: trained on Cypher query generation (graph specialist)
   - Worker B: trained for NL query rewriting (vector search specialist)
   - Worker C: trained for template schema resolution
   - Supervisor: generalist orchestrator (routing + evaluation + resynthesis, iterativer loop for error recovery)

2. **Single generalist:** One larger model (7--12B) fine-tuned across all tool domains
   - Unified tool understanding
   - No routing overhead, simpler deployment
   - One training run, one model

**Architectural advantage — context isolation:** Each worker operates with a fresh context window.  
In a sequential agent (ReAct, Plan-and-Reflect), every turn appends tool results + history to the same context — on a 32k window, 8-10 turns fill ~35%. With multi-agent decomposition, the supervisor, each worker, and the synthesizer each get a clean window. No history accumulation. This is particularly relevant when context windows are bounded (cost-sensitive or edge deployment) or when queries naturally decompose into independent sub-tasks. The paper discusses this as a design rationale for the supervisor variant, not as a limitation.

**Evaluation:** Same Bench B questions, same hardware budget. Does multi-specialist match/exceed generalist?

**Key question:** For AAS retrieval patterns (hierarchical containment, semantic search, template matching) is per-domain specialization beneficial? The domain is relatively well-structured, which may favor the generalist.

**Reference:** AutoGen (wu2023autogen) for the supervisor/worker decomposition pattern. MAD (du2023multiagent_debate) not applicable — iterative debate requires identical agents, not domain-specialized workers.
