# CLAUDE.md

Guidance for Claude Code working in this repository. Phase-detail planning and paper-eval design have been moved to memory files (see pointers below) to keep this lean.

## Project Overview
AAS Hybrid MCP — a hybrid MCP server combining Neo4j graph queries and Weaviate vector search for Asset Administration Shell environments. Targets IDTA Handover Documentation (VDI 2770). DFKI GmbH, MIT-licensed.

## Tech Stack
- **MCP Server:** Python / FastMCP, streamable-http, port 8110
- **Neo4j:** read-only Cypher via async driver
- **Weaviate:** hybrid search (keyword + vector), langchain embeddings
- **Embedding service:** Flask/gunicorn, PDF ingestion via Kafka events, **docling-only**
- **Open WebUI:** chat frontend, port 8090, talks to LangGraph agent (not MCP directly)
- **aas-agent:** LangGraph + FastAPI, OpenAI-compatible API, MCP client
- **Infra:** Docker Compose, single bridge `aas-network`, BaSyx + MongoDB
- **GPU (optional):** H200 + Triton + vLLM via `docker-compose.vllm.yml`

## Key Decisions
- Single network (`aas-network`).
- Neo4j Kafka Connect plugin as pre-built image `dfkibasys/aas-neo4j-kafka-connect-plugin`. Source lives in sibling repo `C:\repo\hackathon\mcp-playground\aas-repository-neo4j-kafka-plugin` (the `i4.0\basys\…` clone is stale).
- **PDF processing — docling only** (~3 GB image with PyTorch CPU). ML-based layout/table recognition, image extraction, sound heading hierarchies. Initial ingest is slow (~seconds per page); real-world manual updates are rare and the quality delta compounds across the retrieval/reranking/template-awareness stack.
- **Embedding model configurable** via `EMBEDDING_MODEL=provider:model` (openai, ollama, google_genai, voyageai; Triton via OpenAI-compatible endpoint).
- **Secrets in `~/.env.secrets`**, referenced via `SECRETS_PATH` in `.env`.
- **Ports hardcoded in `docker-compose.yml`**, not in `.env` — ports don't change, versions do.
- **Data sovereignty — whole stack self-hostable** on H200 / EU cloud. No data leaves the premises. Cloud LLM remains configurable for non-sensitive deployments. Future: SOOFI 120B (~Sept 2026) as plug-in replacement via `LLM_BASE_URL` / `LLM_MODEL`, no code changes.

## Phase Status
- ✅ 1 Scaffold + Compose
- ✅ 2 MCP server + `query_aas_graph` + `aas://schema/graph`
- ✅ 4 Weaviate `search_aas_documents` (reranker / query-rewrite / neighbor-expansion are paper eval axes — see `paper_etfa2026.md`)
- ✅ 6 IDTA template integration + Open WebUI
- ✅ 6.5 Test fixtures (Hall3/4 + 7 robot instances + 5 type shells)
- ✅ 7 LangGraph agent + OTel/Langfuse plumbing
- ✅ 7.5 Six generic write tools (`put_*`/`delete_*`), basyx-python-sdk validation, httpx → BaSyx
- 🟦 8a (paper-relevant): image URLs in Weaviate metadata
- 🟦 9, 10, 11, 12: future — see `memory/future_phases.md`

## AAS Neo4j Graph Schema
Created by the Kafka Connect plugin. Core traversal:
```
(:AAS)-[:MANAGES_ASSET]->(:Asset)
(:AAS)-[:HAS_SUBMODEL]->(:Submodel)-[:HAS_ELEMENT*]->(:SubmodelElement)
```

**SubmodelElement subtypes:** Property, File, Blob, Range, MultiLanguageProperty, SubmodelElementCollection, SubmodelElementList, ReferenceElement, RelationshipElement, AnnotatedRelationshipElement, Entity, Operation, BasicEventElement, Capability.

**All 34 relationship types** documented in the `aas://schema/graph` MCP resource. Entity-nested statements use `HAS_ELEMENT` like all other containment slots; slot-specific labels are reserved for relations carrying semantic role beyond containment (`HAS_ANNOTATION`, Operation variables, `HAS_FIRST` / `HAS_SECOND`).

## Project Structure
```
aas-hybrid-mcp/
├── mcp-server/              # FastMCP server (Python, port 8110)
├── submodel-templates-sync/ # Init: clone IDTA templates, extract JSON, ingest PDFs
├── open-webui/              # Chat frontend + seed init container
├── aas-agent/               # LangGraph agent (OpenAI-compatible API)
├── embedding-service/       # PDF ingestion (Flask, docling)
├── kafka-connect-rag/       # HTTP Sink Kafka Connect
├── neo4j/                   # Custom Neo4j with APOC
├── aasx/                    # Test AASX files
├── docker-compose.yml
├── .env / .env.embedding
└── up.sh / down.sh
```

## Conventions
- Python: pyproject.toml with pinned ranges (`>=x.y,<major`).
- `src/` layout for installable packages (mcp-server); flat layout for simple services (embedding-service).
- Docker: all versions pinned, no `:latest`.
- All services `restart: unless-stopped`.
- English for code, comments, log messages.

## Memory pointers (for deeper context — load on demand)
- `memory/paper_etfa2026.md` — paper working file, Benchmark A/B/C scope, ablation axes, compression strategy
- `memory/future_phases.md` — Phases 8a–12 detailed planning
- `memory/related_work.md` — full bibliography and "Our Differentiator" pitch
- `memory/benchmark_c_plan.md` — write-path ablation (deferred from ETFA 2026, follow-up paper)
