# AAS Hybrid MCP

A hybrid MCP (Model Context Protocol) server that combines Neo4j graph queries and Weaviate vector search for Asset Administration Shell (AAS) environments.

The server enables AI agents to explore AAS structures via Cypher queries against a Neo4j knowledge graph and to search PDF documents embedded in Weaviate — including automatic graph traversal from AAS to linked documents.

## Architecture

```
                  +-----------+
                  | BaSyx AAS |
                  | Environment|
                  +-----+-----+
                        |
                   Kafka Events
                   /         \
                  v           v
  +---------------+   +------------------+
  | kafka-connect |   | kafka-connect    |
  | neo4j         |   | rag (HTTP Sink)  |
  +-------+-------+   +--------+---------+
          |                     |
          v                     v
     +--------+        +-----------------+
     | Neo4j  |        | embedding-      |
     | (Graph)|        | service (Flask) |
     +--------+        +--------+--------+
          |                     |
          |                     v
          |              +-----------+
          |              | Weaviate  |
          |              | (Vectors) |
          |              +-----------+
          |                     |
          +----------+----------+
                     |
              +------+-------+
              | aas-hybrid-  |
              | mcp (Server) |
              +--------------+
```

**Data flow:** BaSyx publishes AAS/Submodel events to Kafka. Two Kafka Connect instances consume these events — one builds a Neo4j graph (structure), the other triggers the embedding service which extracts PDF text, chunks it, and stores vectors in Weaviate. The hybrid MCP server queries both databases.

## Prerequisites

- Docker and Docker Compose
- API key for the configured embedding provider (see [Embedding Configuration](#embedding-configuration))

## Quickstart

```bash
# 1. Create your secrets file
cp .env.secrets.example ~/.env.secrets
# Edit ~/.env.secrets and add your API key(s)

# 2. Start the stack
./up.sh

# 3. First time: build images
./up.sh --build

# 4. Stop — wipes ephemeral state (mongo/kafka/neo4j), keeps Weaviate embeddings
./down.sh

# 5. Stop and keep everything (just stop containers)
./down.sh --keep-all

# 6. Stop and wipe ALL data including Weaviate embeddings
./down.sh --clean
```

### What `./down.sh` keeps and what it wipes

Weaviate embeddings (PDF chunks via docling) are expensive to compute, so they live in a **named volume** (`weaviate_content`) along with the IDTA template index and Open WebUI state. mongo/kafka/neo4j only have anonymous volumes and are cheap to repopulate: BaSyx redeploys all `aasx/` files into MongoDB on startup, BaSyx emits Kafka events, and the Neo4j Connect plugin replays them into the graph.

| Mode | mongo / kafka / neo4j | weaviate / templates / open-webui |
|---|---|---|
| `./down.sh` (default) | wiped | kept |
| `./down.sh --keep-all` | kept | kept |
| `./down.sh --clean` | wiped | wiped |

**Use the default `./down.sh` whenever you change AASX files** — that guarantees BaSyx re-ingests them cleanly. Without the wipe, mongo still holds the previous IDs and BaSyx logs `Uploading shell ... was not successful` (409 conflict) on the second start, so changes silently never reach the graph.

## Services

| Service | Port | Description |
|---|---|---|
| AAS GUI | [localhost:8099](http://localhost:8099) | BaSyx Web UI |
| AAS Environment | [localhost:8081](http://localhost:8081) | AAS/Submodel Repository (MongoDB-backed) |
| AAS Registry | [localhost:8083](http://localhost:8083) | AAS Registry |
| Submodel Registry | [localhost:8082](http://localhost:8082) | Submodel Registry |
| AAS Discovery | [localhost:9100](http://localhost:9100) | AAS Discovery |
| Neo4j Browser | [localhost:7474](http://localhost:7474) | Graph database UI |
| Neo4j Bolt | localhost:7687 | Neo4j driver protocol |
| Weaviate | [localhost:8070](http://localhost:8070) | Vector database HTTP API |
| Weaviate gRPC | localhost:50051 | Vector database gRPC API |
| Embedding Service | [localhost:8000](http://localhost:8000/health) | PDF ingestion service |
| AKHQ | [localhost:8086](http://localhost:8086) | Kafka management UI |
| Kafka (external) | localhost:9093 | Kafka broker |
| Kafka Connect Neo4j | localhost:8084 | Neo4j connector REST API |
| Kafka Connect RAG | localhost:8085 | HTTP Sink connector REST API |
| **AAS Hybrid MCP** | **localhost:8110** | **Hybrid MCP Server** |
| AAS Agent | [localhost:8120](http://localhost:8120) | LangGraph agent (OpenAI-compatible API) |
| Open WebUI | [localhost:8090](http://localhost:8090) | Chat UI (connects to AAS Agent) |
| MCP Inspector | [localhost:6274](http://localhost:6274) | MCP debugging tool |

## Embedding Configuration

The embedding model is configured in `.env.embedding` and shared between the embedding service and the MCP server. Both **must** use the same model — vectors from different models are incompatible.

```bash
# .env.embedding
EMBEDDING_MODEL=openai:text-embedding-3-small
```

Supported providers:

| Provider | Example | API Key Variable |
|---|---|---|
| OpenAI | `openai:text-embedding-3-small` | `OPENAI_API_KEY` |
| Ollama (local) | `ollama:nomic-embed-text` | none |
| Google GenAI | `google_genai:text-embedding-004` | `GOOGLE_API_KEY` |
| Voyage AI | `voyageai:voyage-3` | `VOYAGE_API_KEY` |

API keys go into `~/.env.secrets` (outside the repo, referenced via `SECRETS_PATH` in `.env`).

## PDF Processing Variants

The embedding service has two PDF backends, controlled via `EMBEDDING_VARIANT` in `.env`:

| Variant | Backend | Image Size | Best for |
|---|---|---|---|
| `fast` (default) | pymupdf4llm | ~50 MB | Well-structured PDFs, fast builds |
| `precise` | docling (ML) | ~3 GB | Complex layouts, tables without lines, future image extraction |

Rebuild after changing: `./up.sh --build`

## Project Structure

```
aas-hybrid-mcp/
├── mcp-server/              # Hybrid MCP Server (Python/FastMCP)
│   └── src/aas_hybrid_mcp/
├── embedding-service/       # PDF ingestion: Kafka events -> Weaviate
├── kafka-connect-rag/       # HTTP Sink Kafka Connect (sends events to embedding-service)
├── neo4j/                   # Custom Neo4j image with APOC plugin
├── aasx/                    # Test AASX files
├── docker-compose.yml
├── .env                     # Version pins
├── .env.embedding           # Embedding model configuration
├── up.sh / down.sh          # Stack management scripts
└── CLAUDE.md
```

The Neo4j Kafka Connect plugin is used as a pre-built Docker image (`dfkibasys/aas-neo4j-kafka-connect-plugin`) — no Java code in this repo.

## Testing

The agent test framework drives the AAS Agent variants over HTTP, collects tool-call
metrics, and grades responses (regex + optional LLM judge).

```bash
# from tests/agent-tests/
python run_tests.py --cases cases/containment_hall4.yaml
```

See **[tests/agent-tests/README.md](tests/agent-tests/README.md)** for the full CLI
reference, the recommended two-phase eval workflow (agent runs first, LLM judge
separately), and the ETFA 2026 Bench-B protocol.

## License

MIT — DFKI GmbH




 