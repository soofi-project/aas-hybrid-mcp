# CLAUDE.md

**Canonical operations guide: `AGENTS.md`.** Read it first — it covers stack
commands (`./up.sh --vllm`, `./down.sh`), service ports, secrets, embedding-model
swaps, agent variants, bind-mount strategy, Neo4j schema, and common gotchas.
This file holds only the few things `AGENTS.md` deliberately omits.

## Phase status

- ✅ **1–7.5 committed** — Compose stack, MCP server + `query_aas_graph`,
  Weaviate `search_aas_documents`, IDTA templates, Open WebUI, LangGraph agent +
  OTel/Langfuse, 6 generic `put_*`/`delete_*` write tools with basyx-python-sdk
  validation
- ✅ **6.5** test fixtures (Hall3/4 + 7 robot instances + 5 type shells)
- ✅ **Agent variants live** — 5 Model-IDs selectable per-request:
  `aas-agent:react` (default), `:plan`, `:crag`, `:reflexion`, `:rewoo`.
  Open WebUI utility tasks (title/tag/follow-up) bypass the agent and go
  directly to `LLM_BASE_URL` via a second endpoint.
  Details in `memory/agent_variants.md`.
- ✅ **Phase 9 — Retrieval enhancements committed** (commits d9db611 + 6e8b0a4):
  cross-encoder reranker (`reranker.py`, qwen3-reranker-4b via vLLM) and LLM
  query rewriting (`query_rewriter.py`, 30s timeout). HyDE dropped — removed
  from paper §08 and from `main.bib`. See `memory/future_phases.md`.
- 🟦 **Phase X — Kubernetes / Helm** packaging
- 🟦 **Bench B eval running** — 4 variants (react / plan / crag / reflexion)
  × 6 queries, manual grading. Protocol in `memory/bench_b_evaluation.md`
- 🔴 **Research idea** — specialized worker vs. generalist agent (paper §Future Work)

Attachments (binary File/Blob upload), image extraction, GPU/Triton dispatcher,
PDF → AAS extraction, ConceptDescription semantic layer: all in
`memory/future_phases.md` and `memory/planned_features.md`.

## Memory entry point

`memory/index.md` is the authoritative table of contents for all project memory
files. Load on demand — covers architecture, AAS modeling decisions, template
compliance, paper-summary digests (react / plan-and-solve / rewoo / reflexion /
crag / multiagent-debate / autogen / self-refine), Bench-B protocol, and paper
build setup.

## Data sovereignty

The whole stack is self-hostable on H200 / EU cloud — no data leaves the premises.
Cloud LLM remains configurable for non-sensitive deployments. SOOFI 120B (DFKI,
~Sept 2026) will plug in via `LLM_BASE_URL` / `LLM_MODEL` with no code changes.
Today's eval model is Qwen3.5-120B on the user's H200.
