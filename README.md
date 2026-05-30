# AAS Hybrid MCP

An MCP (Model Context Protocol) server combining Neo4j graph queries and Weaviate vector search for Asset Administration Shell (AAS) environments. AI agents explore AAS structures via Cypher queries and search embedded PDF documents — with automatic graph traversal from AAS to linked manuals.

Built on top of [aas\_neo4j\_integration](https://github.com/dfkibasys/aas_neo4j_integration) (Kafka Connect → Neo4j ingestion plugin).

## Architecture

```
  BaSyx AAS ── Kafka ──┬── Neo4j Connect ─── Neo4j (graph)
                        └── RAG Connect ──── Embedding Service ── Weaviate (vectors)
                                                    │
                          aas-hybrid-mcp ◄──────────┘ (queries both)
                                │
                          AAS Agent (LangGraph, OpenAI-compatible API)
                                │
                          Open WebUI
```

## Quick Start

```bash
cp .env.secrets.example ~/.env.secrets   # add your API key(s)
./up.sh --vllm --build                   # first time: build + start
./up.sh --vllm                           # subsequent starts
./down.sh                                # stop (wipes mongo/kafka/neo4j, keeps Weaviate)
./down.sh --clean                        # stop + wipe everything
```

The `--vllm` flag switches to a local vLLM backend (config in `.env.vllm`). Adjust `LLM_BASE_URL`, `LLM_MODEL`, and `EMBEDDING_MODEL` there to match your setup. Without `--vllm`, the stack uses the OpenAI-compatible defaults from `.env`.

**After changing AASX files:** run `./down.sh` first (default wipe) to avoid BaSyx 409 conflicts.

## Ports

| Port | Service |
|------|---------|
| 8090 | Open WebUI (chat) |
| 8110 | MCP Server |
| 8120 | Agent API (OpenAI-compatible) |
| 7474 | Neo4j Browser |
| 8081 | BaSyx AAS Environment |
| 9093 | Kafka |

## Embedding Model

Configured in `.env.embedding` — the same model must be used for both embedding service and MCP server. API keys go into `~/.env.secrets`.

## Testing & Benchmarks

| Directory | What | Details |
|-----------|------|---------|
| `tests/agent-tests/` | Agent evaluation (9 models, 5 suites, LLM judge) | [→ README](tests/agent-tests/README.md) |
| `tests/ingest-bench/` | Neo4j ingestion v1 vs v2, Cypher latency | [→ README](tests/ingest-bench/README.md) |
| `tests/docling-bench/` | PDF pipeline benchmark (CPU vs GPU) | [→ README](tests/docling-bench/README.md) |

## Project Structure

```
mcp-server/              Hybrid MCP Server (Python/FastMCP)
embedding-service/       PDF ingestion: Kafka → Weaviate
kafka-connect-rag/       HTTP Sink Kafka Connect
neo4j/                   Custom Neo4j image with APOC
aasx/                    Test AASX files (MiR100/250, UR3e/20, CRX10iA, Hall3/4)
```

The Neo4j Kafka Connect plugin is a pre-built image ([`dfkibasys/aas-neo4j-kafka-connect-plugin`](https://github.com/dfkibasys/aas_neo4j_integration)).

## License

MIT — DFKI GmbH
