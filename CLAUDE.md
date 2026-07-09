# CLAUDE.md — AAS Hybrid MCP

## Project Overview
Hybrid MCP server combining Neo4j graph queries and Weaviate vector search for AAS environments. AI agents explore AAS structures via Cypher and search embedded PDF documents.

## Commands
- `./up.sh` — start full stack (with `--vllm` for local backend, `--build` for first time)
- `./down.sh` — stop stack
- `./eval-model.sh` — run agent evaluations

## Key Directories
- `mcp-server/src/aas_hybrid_mcp/` — Server code (FastMCP)
- `embedding-service/` — PDF ingestion pipeline (Kafka → Weaviate)
- `aas-agent/` — LangGraph agent
- `tests/` — Agent tests, ingest benchmarks, docling benchmarks

## Key Files (server)
- `server.py` — entry point, tool registration
- `neo4j_client.py` — Neo4j connection + raw Cypher execution
- `weaviate_client.py` — Weaviate vector search
- `tools/` — MCP tool implementations (cypher_query, document_search, write_tools, etc.)
- `cypher_validator.py` — regex-based Cypher safety gate
- `query_rewriter.py` — query decomposition

## Architecture Rules
- **No raw Cypher in agent prompts** — use `cypher_query` tool instead
- **No `idShort`-based lookups** — always prefer `semanticId` / IRDI references
- **Prompts are hints, validators are guarantees** — always validate before writing

## Companion Project
- [aas-layered-qa](https://mrk40.dfki.de/fai2/soofi/aas-layered-qa) — layered DSL → Cypher compiler that plugs into this server
