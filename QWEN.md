# QWEN.md — AAS Hybrid MCP

## Project Overview

**AAS Hybrid MCP** is a hybrid Model Context Protocol (MCP) server that combines Neo4j graph queries and Weaviate vector search for Asset Administration Shell (AAS) environments, targeting IDTA Handover Documentation (VDI 2770). Developed by DFKI GmbH under the SOOFI project. MIT-licensed.

The system ingests AAS/Submodel data (including robot type shells for UR3e, UR20, CRX10iA, MiR100, MiR250 and factory layouts Hall3/Hall4), builds a Neo4j knowledge graph, extracts and embeds PDF documents via Weaviate, and exposes hybrid search tools to AI agents.

**Key architecture:** BaSyx publishes AAS events to Kafka → two Kafka Connect pipelines consume them (Neo4j graph builder + RAG embedding pipeline) → hybrid MCP server queries both databases → LangGraph agent + Open WebUI provides chat-based AI assistant.

## Tech Stack

- **MCP Server:** Python / FastMCP, streamable-http transport, port 8110
- **Neo4j:** read-only Cypher queries via async driver, custom APOC plugin
- **Weaviate:** hybrid search (keyword + vector), langchain embeddings
- **Embedding Service:** Flask/gunicorn, PDF ingestion via Kafka events, **docling** (ML-based layout/table recognition)
- **Agent:** LangGraph + FastAPI, OpenAI-compatible API (port 8120), multiple variants (`plan_reflect`, `react`)
- **Frontend:** Open WebUI (port 8090), chat interface
- **Infrastructure:** Docker Compose, single bridge `aas-network`, all versions pinned
- **GPU (optional):** H200 + Triton + vLLM via `docker-compose.vllm.yml`

## Project Structure

```
aas-hybrid-mcp/
├── mcp-server/              # FastMCP server (Python/FastMCP, port 8110)
│   └── src/aas_hybrid_mcp/  # Tool descriptions, manual pages
├── aas-agent/               # LangGraph agent (OpenAI-compatible API, port 8120)
│   └── src/aas_agent/       # Prompts (system-prompt.md, agent_plan_prompts/)
├── embedding-service/       # PDF ingestion: Kafka events → Weaviate (docling)
├── kafka-connect-rag/       # HTTP Sink Kafka Connect (events → embedding-service)
├── submodel-templates-sync/ # Init: clone IDTA templates, extract JSON, ingest
├── open-webui/              # Chat frontend + seed init container
├── neo4j/                   # Custom Neo4j image with APOC plugin
├── aasx/                    # Test AASX files (robots + factory layouts)
├── paper/                   # ETFA 2026 paper working files
├── memory/                  # Session memory files (non-MCP persistent context)
├── docs/                    # Additional documentation
├── idta_templates/          # Synced IDTA template data
├── docker-compose.yml       # Main stack definition
├── docker-compose.vllm.yml  # GPU/vLLM overlay
├── .env / .env.embedding / .env.vllm
└── up.sh / down.sh          # Stack management
```

## Building and Running

### Start the stack
```bash
./up.sh              # Start containers (use existing images)
./up.sh --build      # First time: build images from Dockerfiles
```

### Stop modes
| Command | mongo/kafka/neo4j | weaviate/templates/open-webui |
|---|---|---|
| `./down.sh` (default) | wiped | kept |
| `./down.sh --keep-all` | kept | kept |
| `./down.sh --clean` | wiped | wiped |

**Use default `./down.sh` when changing AASX files** — a clean slate guarantees BaSyx re-ingests them. Without the wipe, MongoDB retains old IDs and BaSyx logs 409 conflicts.

### Secrets
API keys go into `~/.env.secrets` (outside the repo). Referenced via `SECRETS_PATH` in `.env`.

### Embedding Model
Configured in `.env.embedding` via `EMBEDDING_MODEL=provider:model`. Must match across embedding service and MCP server. Supported: `openai`, `ollama`, `google_genai`, `voyageai`, Triton via OpenAI-compatible endpoint.

### PDF Processing
Controlled via `EMBEDDING_VARIANT` in `.env`:
- `fast` (default): pymupdf4llm (~50 MB image, well-structured PDFs)
- `precise`: docling ML-based (~3 GB, complex layouts/tables/images)

## Key Services

| Service | Port | Purpose |
|---|---|---|
| **AAS Hybrid MCP** | 8110 | Core MCP server |
| AAS Agent | 8120 | LangGraph agent (OpenAI-compatible API) |
| Open WebUI | 8090 | Chat frontend |
| AAS Environment | 8081 | BaSyx AAS/Submodel Repository |
| BaSyx GUI | 8099 | Web UI |
| Neo4j | 7474 / 7687 | Graph database |
| Weaviate | 8070 / 50051 | Vector database |
| Embedding Service | 8000 | PDF ingestion |
| MCP Inspector | 6274 | MCP debugging |

## Architecture & Data Flow

1. **AAS Ingestion:** BaSyx loads `.aasx` files from `aasx/` volume, publishes events to Kafka
2. **Graph Path:** Kafka → `kafka-connect-neo4j` → builds Neo4j graph (`AAS → MANAGES_ASSET → Asset`, `AAS → HAS_SUBMODEL → Submodel → HAS_ELEMENT → SubmodelElement`)
3. **RAG Path:** Kafka → `kafka-connect-rag` (HTTP Sink) → `embedding-service` → extracts PDFs → chunks → embeds → stores in Weaviate
4. **Query Path:** MCP server queries Neo4j (structure/relationships) + Weaviate (document content) → exposes tools via MCP
5. **Agent:** LangGraph agent (port 8120) calls MCP tools, serves OpenAI-compatible API for Open WebUI

**Neo4j graph schema:** 34 relationship types (`HAS_ANNOTATION`, `HAS_FIRST`, `HAS_SECOND`, etc.), 13+ SubmodelElement subtypes (Property, File, Blob, SubmodelElementCollection, etc.). All documented in `aas://schema/graph` MCP resource.

## Development Conventions

- **Python:** `pyproject.toml` with pinned ranges (`>=x.y,<major`). `src/` layout for installable packages.
- **Docker:** All versions pinned, no `:latest`. All services `restart: unless-stopped`.
- **Secrets:** `~/.env.secrets` (git-ignored). Ports hardcoded in `docker-compose.yml`, not in `.env`.
- **Config:** `.env` for defaults, `.env.embedding` for model config, `.env.vllm` for GPU overlay.
- **English** for code, comments, log messages.
- **Single network:** `aas-network` bridge for all services.
- **Bind-mounts for prompts/tools:** Agent prompts and MCP tool descriptions are bind-mounted over packaged copies so edits take effect on container restart without rebuilding.

## Memory System

Persistent session memory lives in `memory/` directory (loaded into conversation context via `MEMORY.md`). Contains:
- Project phase tracking, paper preparation notes, AAS template compliance
- Configuration troubleshooting (vLLM structured output, paper-search-mcp, etc.)

## Research / Paper Context

This project supports the DFKI SOOFI project and IEEE ETFA 2026 paper preparation. Paper files are in `paper/`. Key evaluation axes: reranker, query-rewrite, neighbor-expansion, template-awareness, image URLs in Weaviate metadata.
