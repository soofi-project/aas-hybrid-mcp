# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AAS Hybrid MCP — a hybrid MCP server combining Neo4j graph queries and Weaviate vector search for Asset Administration Shell environments. Targets IDTA Handover Documentation (VDI 2770). A project by DFKI GmbH. Licensed under MIT.

## Tech Stack

- **MCP Server:** Python with FastMCP SDK (streamable-http transport), port 8110
- **Neo4j:** Read-only Cypher queries via async driver
- **Weaviate:** Hybrid search (keyword + vector) with langchain embeddings
- **Embedding Service:** Flask/gunicorn, PDF ingestion via Kafka events
- **Open WebUI:** Chat frontend with native MCP tool server integration (streamable-http)
- **Infrastructure:** Docker Compose, single bridge network (`aas-network`), BaSyx AAS with MongoDB backend
- **GPU (optional):** NVIDIA H200 with Triton Inference Server for layout analysis, OCR, VLM, and embeddings

## Key Decisions

- **Single network:** All services on one `aas-network` bridge
- **No Java code:** Neo4j Kafka Connect plugin as pre-built image `dfkibasys/aas-neo4j-kafka-connect-plugin`
- **PDF processing — two build variants (`EMBEDDING_VARIANT` in `.env`):**
  - `fast` (~50 MB) — pymupdf4llm, rule-based, good for structured PDFs
  - `precise` (~3 GB) — docling + PyTorch CPU, ML-based table/layout recognition
  - Runtime auto-detection via import, no config switch needed
- **Future: hybrid mode** — per-page dispatcher using PyMuPDF pre-flight check to route pages to local (fast) or GPU/Triton (precise) based on heuristics (empty page/OCR need, vector density, table quality)
- **Embedding model configurable:** Via `EMBEDDING_MODEL` env var (provider:model format). Supports openai, ollama, google_genai, voyageai. Triton via OpenAI-compatible endpoint.
- **Secrets outside repo:** `~/.env.secrets`, referenced via `SECRETS_PATH` in `.env`
- **Ports hardcoded in docker-compose.yml:** Not in `.env` — ports don't change, versions do.

## Development Phases

### Phase 1: Project Scaffold and Docker Compose ✅
Infrastructure stack without MCP server.

### Phase 2: Minimal MCP Server with Cypher Tool ✅
- `query_aas_graph` tool — Cypher queries against Neo4j with read-only enforcement
- `aas://schema/graph` resource — complete AAS graph schema documentation (derived from Kafka Connect plugin source)
- Dockerfile, docker-compose service on port 8110, streamable-http via fastmcp + uvicorn

### Phase 3: ~~Schema Tool~~ (merged into Phase 2)

### Phase 4: Weaviate Client and Document Search ✅
- `search_aas_documents` tool — semantic vector search over ingested PDF documents
- Optional `submodel_id` filter (LLM discovers IDs via `query_aas_graph`, then scopes search)
- Sync Weaviate client with langchain query embeddings (same model as embedding-service)
- Shared `.env.embedding` ensures vector compatibility between services

### Phase 5: ~~Hybrid Document Search~~ (merged into Phase 4)
LLM orchestrates graph traversal + document search itself using the two tools — no need for automatic traversal logic.

### Phase 6: MCP Resources, IDTA Submodel Templates, and Open WebUI ✅
- `aas://schema/graph` resource (already done in Phase 2)
- **IDTA Submodel Template integration:**
  - Init container (`submodel-templates-sync`) clones https://github.com/admin-shell-io/submodel-templates
  - Repo structure: `published/<Name>/<Major>/<Minor>/[<Patch>/]` — numeric dirs, PDFs fall back to parent level if absent at patch level
  - Idempotent: stores repo HEAD SHA in Weaviate `SyncMetadata` collection, skips re-ingestion on unchanged repo
  - Shares `template_data` volume with MCP server (read-only)
  - **Structured index resource** `aas://templates/index` — generated from template JSONs (name, semanticId, description per template)
  - **Per-template resource** `aas://template/{name}` — element structure extracted from JSON (modelType, idShort, semanticId, nesting)
  - **Semantic search over spec PDFs** — init container converts PDFs via pymupdf4llm, chunks, embeds, and inserts into separate Weaviate collection (`IdtaTemplateSpec`). ~43 PDFs, ~6200 chunks.
  - **MCP tool** `search_idta_templates(query, template_name?, limit?)` — vector search over template specifications, for questions like "is there a template for safety certificates?" or "how to store handover documentation?"
  - ~45 published templates, auto-discovered from directory structure, latest version per template
- **Open WebUI integration:**
  - Chat frontend on port 8090 with MCP tool server connection via `TOOL_SERVER_CONNECTIONS` env var
  - For `type: "mcp"`, Open WebUI uses `streamablehttp_client(url)` directly — the full MCP endpoint URL goes in `url`, not split across `url`+`path`
  - Workspace model seeded via init container (`open-webui-seed`): signup/signin → model import API
  - `DEFAULT_MODELS` env var pre-selects the AAS Assistant in new chats
  - **Limitation:** Open WebUI v0.8.6 exposes MCP tools but not MCP resources to the LLM — resources require the LangGraph agent layer (Phase 7)

### Phase 7: LangGraph Agent + Observability
- **Architecture:** `Open WebUI (UI) → LangGraph Agent (orchestration) → MCP Server (tools + resources)`
- **LangGraph agent container** (`aas-agent`) exposes OpenAI-compatible `/v1/chat/completions` endpoint
  - Open WebUI talks to it like any OpenAI API — no MCP support in Open WebUI needed
  - Agent connects to MCP server via streamable-http as MCP client
- **Resource injection:** Agent loads `aas://schema/graph` into context automatically, not as tool call
- **Workflow enforcement via LangGraph states:**
  - Schema loaded → Graph query → Submodel ID extraction → Document search → Response
  - Automatic retry/fallback: if one submodel returns no docs, try next with File elements
  - Prevents common LLM mistakes (e.g. `Asset→Submodel` instead of `AAS→Submodel`)
- **OpenTelemetry instrumentation:**
  - Auto-instrumentation via `opentelemetry-instrument` (zero code changes)
  - LangChain has native OTel integration — spans per tool call, LLM invocation, chain step
  - Traces: which tools called, parameters, results, latency, errors
- **Langfuse as OTel-compatible trace backend:**
  - Aggregates traces, visualizes agent workflows, tracks success/error rates
  - Enables analysis: "X% of graph queries fail because model uses wrong start node"
- **Feedback loop (async, future):**
  - Error pattern detection from Langfuse traces
  - Automatic system prompt refinement based on observed failure modes
  - Tool description optimization based on parameter error rates
  - MCP endpoint adjustment (e.g. adding validation, rewriting descriptions)
- **vLLM support:** Configurable LLM backend — OpenAI API, vLLM on H200, or Ollama
  - `docker-compose.vllm.yml` overlay for GPU deployment with embedding + chat on H200

### Phase 8 (Future): Image Extraction + MinIO
- Extract images from PDFs (docling) → store on MinIO → reference in Weaviate metadata
- Weaviate schema: `HandoverDocument` and `TechnicalImage` classes with cross-references
- Each image gets two text layers:
  - `extracted_text`: raw OCR text (article numbers, IDs)
  - `generated_description`: VLM-generated semantic alt-text ("Schaltplan", "Warnsymbol")
- Hybrid search over both layers for exact terms + semantic concepts
- Photo-based asset identification (camera photo → match stored images → identify AAS)

### Phase 9 (Future): GPU/Triton Hybrid Dispatcher
- Per-page routing with PyMuPDF pre-flight check:
  - **Empty page check:** < 100 chars text but large file size → OCR needed → Triton
  - **Vector density:** > 500 graphic paths (get_drawings()) → complex drawings → Triton
  - **Table quality:** PyMuPDF table extraction produces overlapping/implausible cells → Triton
- Triton Inference Server on H200 for: layout analysis, OCR, VLM, embeddings
- Configurable `ExtractionPolicy`: fast / precise / hybrid
- Map extracted data to IDTA Teilmodell attributes (DocumentID, Status, Version)

### Phase 10 (Future): Natural Language AAS Editor
- Write access to BaSyx AAS API (create/update shells, submodels, elements)
- **PDF-to-AAS workflow:** User uploads asset PDFs (datasheets, manuals, certificates) → agent extracts information → creates/updates AAS with correct IDTA submodel structure
- Agent uses IDTA templates (from Phase 6) as structural guide for correct element placement
- Automatic classification: agent determines which IDTA template fits (Nameplate, Technical Data, Handover Documentation, etc.)
- MCP tools: `create_submodel`, `update_element`, `upload_document`
- Conversational: user can refine, correct, add context in natural language

### Phase 11 (Future/Research): Multimodal AAS Media Search
- **Goal:** Bilder und Schulungsvideos aus der Verwaltungsschale in Weaviate aufnehmen und multimodal durchsuchbar machen
- **Configurable:** Kafka Connect Sink konfigurierbar ob Medienverarbeitung aktiv (`MEDIA_PROCESSING_ENABLED`), da rechenintensiv und nicht für jeden Anwendungsfall nötig
- **Bilder (direkt aus AAS):**
  - Kafka-Event erkennt `File`/`Blob`-Elemente mit Bild-MIME-Type → Bild laden → MinIO
  - Multimodales Embedding (CLIP/SigLIP via Triton) für Bild + Text gemeinsam
  - Weaviate `AssetImage` Collection mit multi2vec (Bild-Embedding + Text-Embedding)
  - Ergänzt Phase 7 (PDF-extrahierte Bilder) um direkte AAS-Medien
- **Videos (Schulungs-/Wartungsvideos):**
  - Kafka-Event erkennt Video-MIME-Types (mp4, webm) → Video auf MinIO ablegen
  - **Keyframe-Extraktion:** ffmpeg scene-detect → relevante Frames als Bilder
  - **Audio-Transkription:** Whisper (auf H200/Triton) → timestamped Transkript
  - **Multimodales Embedding:** Keyframes via CLIP/SigLIP, Transkript-Chunks via Text-Embedding
  - Weaviate `TrainingVideo` Collection: Chunks mit Timestamp-Referenz (Keyframe + Transkript-Segment)
  - Videos ändern sich selten → einmalige Verarbeitungskosten akzeptabel
- **Multimodaler Reranker:**
  - Cross-Encoder Reranking über Text + Bild-Ergebnisse gemeinsam
  - Ermöglicht Queries wie "zeig mir den Schaltplan für Motor X" (Text→Bild) oder Foto-Upload → ähnliche Dokumentation finden (Bild→Text)
  - Modell: Jina CLIP v2 oder ColPali für visuelle Dokument-Retrieval, auf H200/Triton
- **MCP Tools:**
  - `search_aas_media(query, media_type=["image","video","all"])` — multimodale Suche
  - Ergebnisse mit MinIO-Links, Timestamps (Video), Thumbnail-Previews
- **Forschungsaspekte:**
  - Optimale Keyframe-Sampling-Strategie (scene-detect vs. fixed interval vs. content-aware)
  - Granularität der Video-Chunks (pro Szene vs. Zeitfenster vs. Sprecherwechsel)
  - Cross-modale Retrieval-Qualität (Text-Query → Video-Segment, Bild-Query → Dokumentation)
  - Benchmark: Retrieval-Precision bei technischen Schulungsvideos vs. generischen Video-QA-Datasets

## Related Work

### AAS Generation from Text/PDFs (related to Phase 9)
- **basyx-pdf-to-aas** (Eclipse BaSyx) — Python library, LLM-based extraction from PDFs → AAS export. Batch tool, not conversational. Potential dependency for Phase 9. [github.com/eclipse-basyx/basyx-pdf-to-aas](https://github.com/eclipse-basyx/basyx-pdf-to-aas)
- **AASbyLLM** (Xia et al., 2024) — LLM agents generate AAS from datasheet text via "Semantic Nodes". 62-79% generation rate. Compares multiple LLMs, uses RAG. [arxiv.org/abs/2403.17209](https://arxiv.org/abs/2403.17209) | [github.com/YuchenXia/AASbyLLM](https://github.com/YuchenXia/AASbyLLM)
- **AAS Submodel Generator** (Fraunhofer) — LLMs map diverse sources into AAS structures. [Fraunhofer Publica](https://publica.fraunhofer.de/entities/publication/81b3ee2a-a0e6-4e8f-8562-0ae5b751b624) | [atp magazin](https://ojs.di-verlag.de/index.php/atp_edition/article/view/2773)
- **Xia & Xiao (2024)** — Interoperable information modelling leveraging AAS and LLM for quality control toward zero defect manufacturing. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0278612524002395)

### AAS + MCP (directly related to our approach)
- **Beyerlein (2025, INNOQ)** — "Asset Administration Shell und Model Context Protocol: Friend or Enemy?" Argues AAS and MCP are complementary: AAS provides semantically normalized submodels, MCP enables flexible AI-driven access via LLMs. Two architectures: with/without AAS normalization. [innoq.com](https://www.innoq.com/de/articles/2025/07/aas-and-mcp-friend-or-enemy/)
- **KIT (Dorn, Barth)** — Bachelor/Master thesis at KIT developing an MCP server as "semantic bridge between LLMs and components within the plant" using AAS. Explores enriching AAS with semantic annotations for MCP access. [kit.edu](https://www.irs.kit.edu/english/people_aut_5472.php)

### AAS + RAG / Knowledge Graphs (related to our hybrid approach)
- **Enhancing RAG for cognitive digital twins** (2025) — Uses AAS for standardized knowledge representation in RAG systems. Encodes AAS for retrieval, fine-tunes LLMs with contrastive selection loss. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0166361525000958)
- **Cognitive digital twins for capability matching** (Xia & Xiao, 2025) — AAS + LLM-based RAG for reconfigurable manufacturing. Structured PPR knowledge via AAS, capability matching via RAG. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0736584525001590)
- **metaphacts** — AI + Knowledge Graphs + AAS for smarter digital twins in Industry 4.0. [Blog](https://blog.metaphacts.com/smarter-digital-twins-with-metaphactory-ai-knowledge-graphs-and-asset-administration-shell-for-industry-4-0)

### Hybrid Graph + Vector Search (architectural pattern)
- **GraphRAG** (Neo4j, 2024) — Combines knowledge graph traversal with vector-based retrieval. Graph provides structural reasoning, vectors provide semantic similarity. [neo4j.com](https://neo4j.com/blog/genai/what-is-graphrag/)
- **Digital Twin meets Knowledge Graph** (2024) — Multi-layer KG architecture for manufacturing digital twins (concept/model/decision layers). Neo4j-based. [Nature](https://www.nature.com/articles/s41598-024-85053-0) | [MDPI](https://www.mdpi.com/1424-8220/24/8/2618)
- **KG-enhanced RAG for FMEA** (2025) — Knowledge graph enhanced RAG for failure mode and effects analysis in manufacturing. [ResearchGate](https://www.researchgate.net/publication/389645060_Knowledge_graph_enhanced_retrieval-augmented_generation_for_failure_mode_and_effects_analysis)

### Our Differentiator
Existing work falls into three categories: (1) batch AAS generation from text, (2) AAS as data source for RAG, (3) generic GraphRAG patterns. **None combines all three in a single interactive system.** Our approach is unique in:
- **Hybrid MCP server** combining graph queries (Neo4j) + vector search (Weaviate) in one tool interface
- **Conversational** via MCP — agent interactively queries, searches, and (Phase 10) creates/edits AAS
- **IDTA template awareness** — agent knows standardized submodel structures for correct element placement
- **Kafka-driven knowledge graph** — live sync from BaSyx AAS environment, not static import
- **LangGraph agent with OTel observability** (Phase 7) — enforced workflows, auto-injected resources, Langfuse trace analysis for async self-improvement
- **Multimodal media search** (Phase 11) — Bilder und Videos aus der AAS via CLIP/Whisper/Reranker durchsuchbar, konfigurierbar über Kafka Connect

## AAS Neo4j Graph Schema

The graph is created by the Kafka Connect plugin (`dfkibasys/aas-neo4j-kafka-connect-plugin`). Key structure:

**Core traversal:** `(:AAS)-[:MANAGES_ASSET]->(:Asset)`, `(:AAS)-[:HAS_SUBMODEL]->(:Submodel)-[:HAS_ELEMENT*]->(:SubmodelElement)`

**SubmodelElement types:** Property, File, Blob, Range, MultiLanguageProperty, SubmodelElementCollection, SubmodelElementList, ReferenceElement, RelationshipElement, AnnotatedRelationshipElement, Entity, Operation, BasicEventElement, Capability

**All 35 relationship types** defined in RelationLabel enum — see `aas://schema/graph` resource for complete documentation.

## Project Structure

```
aas-hybrid-mcp/
├── mcp-server/              # Hybrid MCP Server (Python/FastMCP)
│   └── src/aas_hybrid_mcp/
│       ├── server.py        # FastMCP entry point (streamable-http, port 8110)
│       ├── neo4j_client.py  # Async Neo4j driver (read-only)
│       ├── weaviate_client.py # Sync Weaviate client (aas_documents + IdtaTemplateSpec)
│       ├── tools/           # MCP tools (cypher_query, document_search, template_search)
│       └── resources/       # MCP resources (schema, templates)
├── submodel-templates-sync/ # Init container: clone IDTA templates, extract JSON, ingest PDFs
│   ├── main.py              # Discovery, extraction, chunking, embedding, Weaviate ingestion
│   ├── Dockerfile           # Multi-stage (builder + runtime with git)
│   └── pyproject.toml
├── open-webui/              # Open WebUI configuration + seed init container
│   ├── model.json           # Workspace model definition (seeded via API)
│   ├── seed-model.sh        # Init script: signup/signin → model import
│   ├── system-prompt.md     # AAS assistant system prompt
│   └── Dockerfile           # Alpine + curl + jq for seeding
├── aas-agent/               # (Phase 7) LangGraph agent with OpenAI-compatible API
├── embedding-service/       # PDF ingestion (flat layout, no src/)
│   ├── app.py               # Flask routes
│   ├── config.py            # ENV-based configuration
│   ├── handlers.py          # AAS event handlers + AasPathBuilder
│   ├── pdf.py               # PDF conversion (fast/precise auto-detect)
│   └── vectorstore.py       # Weaviate client (singleton)
├── kafka-connect-rag/       # HTTP Sink Kafka Connect
├── neo4j/                   # Custom Neo4j with APOC
├── aasx/                    # Test AASX files
├── docker-compose.yml
├── .env                     # Version pins + EMBEDDING_VARIANT
├── .env.embedding           # Embedding model config
├── up.sh / down.sh          # Stack management
```

## Conventions

- Python: pyproject.toml with pinned version ranges (`>=x.y,<major`)
- Docker: all versions pinned, no `:latest` tags
- All services have `restart: unless-stopped`
- English for code, comments, and log messages
