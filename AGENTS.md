Use as few tokens as possible. Don't start implementing unless explicitly asked to.

# AGENTS.md — AAS Hybrid MCP

## Quick start

```bash
cp .env.secrets.example ~/.env.secrets   # edit with your API key(s)
git submodule update --init               # one-time; up.sh does this automatically
./up.sh --vllm --build                    # first time
./up.sh --vllm                            # start stack
./down.sh                                 # stop + wipe mongo/kafka/neo4j
./down.sh --clean                         # stop + wipe everything
```

**Always `--vllm`** — sets `AGENT_RECURSION_LIMIT=100`, `AGENT_DEFAULT_THINKING=false`, correct `LLM_BASE_URL`/`LLM_MODEL`. Not optional.

**`./down.sh` (default) after changing AASX files** — otherwise BaSyx 409s.

## Key directories

| Dir | What |
|---|---|
| `mcp-server/src/aas_hybrid_mcp/` | MCP server — tools in `tools/`, clients `neo4j_client.py`, `weaviate_client.py`, `basyx_client.py` |
| `mcp-server/src/aas_hybrid_mcp/tool_descriptions/` | Tool .md files — **bind-mounted** (edits reload on restart) |
| `mcp-server/src/aas_hybrid_mcp/manual_pages/` | Manual pages — **bind-mounted** |
| `aas-agent/src/aas_agent/` | LangGraph agent — `system-prompt.md`, `agent_plan_prompts/` — **bind-mounted** |
| `embedding-service/` | Flask app, PDF extraction, Weaviate storage |
| `aasx/` | Test AASX files (MiR100/250, UR3e/20, CRX10iA, Hall3/4) |
| `memory/tasks/` | `open/` (active) + `closed/` (done) |

All bind-mounted files: tool_descriptions, manual_pages, system-prompt.md, agent_plan_prompts. Edits take effect on restart without rebuild.

## Important ports

8110 = MCP server · 8120 = Agent API · 8090 = Open WebUI · 7474 = Neo4j Browser · 8081 = BaSyx · 9093 = Kafka

## Architecture (one-liner)

BaSyx → Kafka → Neo4j (graph) + Weaviate (vectors). MCP server (15 tools) → LangGraph agent (react/plan/crag/reflexion variants) → OpenAI-compatible API. Full details: `memory/architecture.md`, `memory/agent_variants.md`.

## Gotchas

1. **AASX changed → `./down.sh` first** (wipe mongo/kafka/neo4j, else BaSyx 409)
2. **Embedding model must match** between `embedding-service` and MCP server (`EMBEDDING_MODEL` in `.env`)
3. **`docker compose`** (v2, space) not `docker-compose` (v1, hyphen)
4. **RAG connector needs `--build`** — uses `pull_policy: never` + version-suffix tag
5. **No lint/typecheck/CI** in this repo. No formal test framework.
6. **Secrets in `~/.env.secrets`** — never hardcode keys. Docker Compose loads via `env_file: ${SECRETS_PATH}`.

## Task workflow

Check `memory/tasks/open/task_*.md` before implementing. Read subtasks → work in order → on completion: move to `closed/`. Paper tasks use `task_paper_*` prefix.

## Implementation gate

**Never implement without explicit go-ahead.** Discuss → Plan → Wait for approval → Implement. Applies to: code, Docker/config, AASX, paper edits, BibTeX. Does NOT apply to read-only operations.

## Deeper reference

- `CLAUDE.md` — phase tracking, key decisions
- `memory/index.md` — overview of all memory context files
- `memory/architecture.md` — detailed architecture + diagrams
- `memory/agent_variants.md` — variant routing, graph topology, budget env vars
