# Benchmark A — Neo4j Ingestion (v2 Bolt+UNWIND)

Measures ingestion drain time and Cypher p95 query latency for the v2 Bolt-based
Kafka Connect Neo4j plugin during BaSyx AASX auto-ingestion.

## Prerequisites

- Docker Compose v2
- Main stack must be **stopped** (port conflicts on 8081, 8082, 8083, 7474, 7687, 9093)

```bash
cd tests/ingest-bench

python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv/Scripts/activate

pip install neo4j kafka-python
```

## Setup

Place AASX files in the `aasx/` directory. BaSyx auto-ingests them on startup.

```
tests/ingest-bench/aasx/
├── Shell_001.aasx
├── Shell_002.aasx
└── ...
```

## Running

The script manages the Docker stack automatically.

```bash
python bench_ingest.py
```

The script runs:
1. `docker compose down -v` (wipe previous data)
2. `docker compose up -d` (starts Kafka, Mongo, Neo4j, BaSyx, Connect, AKHQ)
3. BaSyx auto-ingests `aasx/` → Kafka events → monitor connector lag until 0 → Cypher p95
4. `docker compose down -v`
5. Result JSON written to `results/`

### Cypher queries only (on a running stack)

```bash
python bench_ingest.py --cypher-only
```

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `--poll-interval` | 5 | Lag polling interval in seconds |
| `--query-repetitions` | 100 | Cypher query repetitions |
| `--cypher-only` | — | Only run Cypher p95 on a running stack |
| `-v` | — | Verbose logging |

The script exits when connector lag reaches 0.
It aborts if lag has not decreased for 30 minutes (crashed connector).

### Stop the stack manually

```bash
docker compose -f docker-compose.bench.yml --env-file .env.bench down -v
```

## Output

### Result JSON

`results/bench_ingest_YYYYMMDDTHHMMSSZ.json`:

```json
{
  "timestamp": "20260528T175258Z",
  "aasx_count": 39510,
  "metrics": {
    "drain_time_s": 3487.92,
    "throughput_events_per_s": 75.91,
    "mean_latency_ms": 13.17,
    "peak_lag": 427
  },
  "neo4j_counts": {
    "shells": 39508,
    "submodels": 225252,
    "elements": 8502693
  },
  "cypher": {
    "2hop": { "p95_ms": 2.89 },
    "4hop_semID": { "p95_ms": 2.65 }
  },
  "lag_samples": [...]
}
```

### Analyze results

```bash
python analyze_bench.py                      # latest result
python analyze_bench.py results/bench_*.json # specific file
```

## Architecture

```
tests/ingest-bench/
├── aasx/                    ← AASX files (BaSyx auto-ingests on startup)
├── docker-compose.bench.yml ← Reduced stack: Kafka + Mongo + Neo4j + BaSyx + Connect + AKHQ
├── .env.bench               ← image tags + infra versions
├── bench_ingest.py          ← Benchmark script
├── analyze_bench.py         ← Extract paper values from result JSON
└── results/                 ← JSON results
```

### Services

| Service | Port | Role |
|---|---|---|
| bench-kafka | 9093 | Kafka (KRaft single-node) |
| bench-mongo | — | MongoDB for BaSyx |
| bench-neo4j | 7474, 7687 | Neo4j 5 + APOC |
| bench-aas-registry | 8083 | AAS Registry |
| bench-submodel-registry | 8082 | Submodel Registry |
| bench-aas-discovery | 9100 | AAS Discovery |
| bench-aas-environment | 8081 | BaSyx AAS Environment (auto-ingest aasx/) |
| bench-kafka-connect-neo4j | 8084 | Kafka Connect Neo4j v2 (Bolt+UNWIND) |
| bench-akhq | 8086 | AKHQ Kafka UI |

**Not included:** Weaviate, embedding service, MCP server, agent, Open WebUI, GUI.

## Troubleshooting

**"No consumer group found"**: Kafka Connect needs ~15s to start. The script waits automatically (up to 5 min).

**Port conflicts**: Stop the main stack first (`./down.sh` in the repo root).

**Neo4j image not found**: Run `docker compose -f docker-compose.bench.yml build neo4j`.
