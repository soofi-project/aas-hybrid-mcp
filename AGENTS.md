# AGENTS.md — AAS Hybrid MCP

## Quick start

```bash
cp .env.secrets.example ~/.env.secrets   # edit with your API key(s)
./up.sh --build                           # first time: build images
./up.sh                                   # start stack
./down.sh                                 # stop + wipe mongo/kafka/neo4j (keep weaviate)
./down.sh --clean                         # stop + wipe everything
./down.sh --keep-all                      # stop only
```

**Always start with `--vllm`:** `./down.sh && ./up.sh --vllm` (or `--vllm --build`). The `.env.vllm` overlay sets `AGENT_RECURSION_LIMIT=100`, `AGENT_DEFAULT_THINKING=false`, and the correct `LLM_BASE_URL`/`LLM_MODEL`. Without `--vllm`, the agent calls the wrong endpoint. Always use the `--vllm` flag for any stack restart — it's not optional.

**Always use default `./down.sh` after changing AASX files** — without wiping mongo/kafka/neo4j, BaSyx logs 409 conflicts and changes silently don't reach the graph.

## Architecture (one-paragraph refresher)

BaSyx loads `.aasx` files from `aasx/` → publishes Kafka events. Two Kafka Connect pipelines consume them: `kafka-connect-neo4j` builds a Neo4j graph (structure), `kafka-connect-rag` → `embedding-service` → extracts PDFs → chunks → embeds → stores in Weaviate (vectors). The MCP server (port 8110) queries both. A LangGraph agent (port 8120) calls MCP tools and serves an OpenAI-compatible API for Open WebUI (port 8090). All services on single bridge network `aas-network`.

**Detailed architecture + diagrams: `memory/architecture.md`**

## Service ports (the ones you need)

| Port | Service |
|---|---|
| 8110 | **AAS Hybrid MCP** (streamable-http) |
| 8120 | AAS Agent (OpenAI-compatible API) |
| 8090 | Open WebUI |
| 7474 | Neo4j Browser |
| 8070 | Weaviate HTTP |
| 8000 | Embedding Service (`/health`) |
| 6274 | MCP Inspector |
| 8099 | BaSyx GUI |
| 8081 | BaSyx AAS Environment |

## Secrets are outside the repo

API keys live in `~/.env.secrets` (git-ignored), referenced via `SECRETS_PATH=~/.env.secrets` in `.env`. Docker Compose loads them via `env_file: ${SECRETS_PATH}`. Never hardcode keys.

## Embedding model changes

- Configured in `.env` via `EMBEDDING_MODEL=provider:model`. **Both embedding-service and MCP server must use the same model.**
- Changing `EMBEDDING_MODEL` auto-creates a new Weaviate collection: `{WEAVIATE_COLLECTION}_{model_slug}`. Old collection stays untouched.
- Slug is model part only (after `:`) — provider is stripped. `openai:text-embedding-3-small` and `ollama:text-embedding-3-small` share a collection.
- Rebuild after changing: `./up.sh --build`
- PDF variant controlled by `EMBEDDING_VARIANT`: `fast` (pymupdf4llm, ~50 MB) or `precise` (docling ML, ~3 GB). Default is `fast`.

## Key directories

| Directory | What you'll find |
|---|---|
| `mcp-server/src/aas_hybrid_mcp/` | MCP server — tools in `tools/`, clients in `neo4j_client.py`, `weaviate_client.py`, `basyx_client.py` |
| `mcp-server/src/aas_hybrid_mcp/tool_descriptions/` | Tool description .md files — **bind-mounted** into container (edits reload on restart) |
| `mcp-server/src/aas_hybrid_mcp/manual_pages/` | Manual pages — **bind-mounted** (edits reload on restart) |
| `aas-agent/src/aas_agent/` | LangGraph agent — prompts in `system-prompt.md`, `agent_plan_prompts/` — **all bind-mounted** |
| `embedding-service/` | Flask app, PDF extraction, Weaviate vector storage |
| `aasx/` | Test AASX files (MiR100/250, UR3e/20, CRX10iA, Hall3/4) |
| `memory/tasks/` | Tasks: `open/` (active) + `closed/` (done) |
| `kafka-connect-rag/` | HTTP Sink Kafka Connect config (custom Dockerfile, `pull_policy: never`) |

**Build the RAG connector with `--build`** — it uses `pull_policy: never` and a version-suffix tag (`kafka-connect-rag:${KAFKA_VERSION}-${RAG_CONNECT_VERSION}`).

## Neo4j graph schema

Core traversal created by Kafka Connect plugin:

```
(:AAS)-[:MANAGES_ASSET]->(:Asset)
(:AAS)-[:HAS_SUBMODEL]->(:Submodel)-[:HAS_ELEMENT*]->(:SubmodelElement)
```

**All 34 relationship types** available via the `aas://schema/graph` MCP resource. Entity-nested statements use `HAS_ELEMENT` (same as all containment slots); slot-specific labels (`HAS_ANNOTATION`, `HAS_FIRST`/`HAS_SECOND`, Operation variables) are reserved for relations carrying semantic role beyond containment.

## Writing tools (Phase 7.5)

Six generic write tools: `put_aas`, `put_submodel`, `put_submodel_element`, `delete_aas`, `delete_submodel`, `delete_submodel_element`. All validated via `basyx-python-sdk` before sending. Register via `tools/write_tools.py`.

## Agent variants

Variants are selectable **per-conversation** via OpenAI model name (`aas`, `aas:plan`, `aas:crag`, etc.). `api.py` lazily initializes each runner on first request. Shared MCP client, tools, and context loaded once at startup. `AGENT_VARIANT` env var is deprecated. **Full details in `memory/agent_variants.md`** — model ID → variant routing, graph topology, budget env vars, and paper mapping. Keep that file in sync when adding/changing variants or budget parameters. `AGENT_INJECT_MANUAL` and `AGENT_INJECT_SCHEMA` control whether system prompt gets manual/schema injected at startup vs. agent fetching on demand.

**Variants must be comparable:** every runner must combine `system-prompt.md` + `mcp_context` as its `base_system`. The variant-specific prompt layer adds topology/strategy instructions (plan, judge, reflect, etc.), but the core directives ("Act, don't ask permission", idShort anti-pattern, two entry points, output style) must never be dropped. If one variant deviates, the others will fail silently on the same queries. See `reflexion.py`, `crag.py`, `agent_plan.py`, `rewoo.py`, `agent.py`.

## Bind-mounted-over-pacakaged files

The following are bind-mounted over their installed copies so edits take effect on container restart **without rebuilding**:
- `./mcp-server/src/aas_hybrid_mcp/tool_descriptions/` → `/usr/local/lib/.../aas_hybrid_mcp/tool_descriptions`
- `./mcp-server/src/aas_hybrid_mcp/manual_pages/` → `/usr/local/lib/.../aas_hybrid_mcp/manual_pages`
- `./aas-agent/src/aas_agent/system-prompt.md` → installed path
- `./aas-agent/src/aas_agent/agent_plan_prompts/` → installed path

## Testing

No formal test framework. Test scripts exist flat in `mcp-server/src/` (e.g. `test_hierarchical.py`, `test_hierarchical_final.py`) — they're ad-hoc Cypher verification scripts, not pytest suites.

## No lint/typecheck/CI

This repo has no pre-commit hooks, lint config, typecheck, CI workflows, or formatter. Python packages use `pyproject.toml` with pinned ranges (`>=x.y,<major`). No generated code, no migrations.

## Existing instruction sources

- `CLAUDE.md` — phase tracking, key decisions, paper context
- `QWEN.md` — more detailed architecture + data flow
- `memory/index.md` — overview of all memory context files. Check first for project knowledge.
- **Tasks in `memory/tasks/open/task_*.md`:** Actionable work items with Subtasks, Acceptance Criteria, References. Completed tasks move to `memory/tasks/closed/`.

## Task workflow

Before starting implementation work, check `memory/tasks/open/task_*.md` for open tasks. When implementing:
1. Read the task file for subtasks, acceptance criteria, references
2. Work through subtasks in order (T1, T2, ...)
3. On completion: update `status: done` in the task file, move it to `memory/tasks/closed/` + update `memory/planned_features.md` / `memory/future_phases.md` accordingly

## Common gotchas

1. **Changing AASX files after stack is up:** you MUST stop + wipe (`./down.sh` default). Otherwise BaSyx 409s on upload.
2. **Embedding model mismatch:** MCP server and embedding-service must share the same `EMBEDDING_MODEL`. Vectors from different models are incompatible.
3. **Neo4j connector source:** the Java plugin code lives in `C:\repo\hackathon\mcp-playground\aas-repository-neo4j-kafka-plugin` (not in this repo). The Docker image `dfkibasys/aas-neo4j-kafka-connect-plugin` is used as-is.
4. **vLLM overlay:** GPU backend requires `./up.sh --vllm` which loads `docker-compose.vllm.yml`. Changes LLM_BASE_URL, LLM_MODEL, RERANKER_MODE.
5. **`docker compose` (v2), not `docker-compose` (v1):** `up.sh` uses `docker compose` (space, not hyphen).
6. **One-shot init containers:** `submodel-templates-sync` and `open-webui-seed` must complete before MCP is considered ready. `mcp-inspector` is the anchor for `docker compose up --wait`.
7. **Weaviate collection naming:** collections include model slug. Don't query `aas_documents` directly — use `aas_documents_text-embedding-3-small` (or whatever your model slug is). The MCP server and embedding service compute this automatically.
