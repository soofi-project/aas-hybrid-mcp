---
name: Task – Benchmark A: Neo4j Ingestion v1 vs v2
description: Eigenständiges Benchmark-Setup in tests/ingest-bench/ zum Vergleich der Kafka Connect Neo4j Plugin-Versionen v1 (HTTP Sink) vs v2 (Bolt+Buffer) inkl. Kafka Lag Messung und Cypher p95 Queries.
type: task
status: open
priority: high
---

## Status

**Open** — Plan finalisiert, wartet auf Implementierung.

## Background

§10 Benchmark A enthält 10 unfüllte `[EVAL: ...]` Platzhalter (E1, E2 in claim_audit.md).
Der v2 Plugin (Bolt+Buffer, `7.9.1-2.1.3`) soll den per-event HTTP-Sink-Flaschenhals
aus ETFA 2025 (`sonnenberg2025aas_kg`, Plugin v1 `7.9.1-0.1.13`) beheben.

Bisherige Evaluation (Benchmark A2, Docling) maß PDF-Konvertierung direkt per Python.
Benchmark A1 braucht ein neues Setup weil der Flaschenhals im Kafka Connect Plugin liegt
— nicht im Embedding Service. Kafka Consumer Lag ist die geeignetere Metrik weil sie
exakt Stufe 4→5 (Kafka Connect → Neo4j) misst ohne BaSyx-Overhead und ohne
Neo4j-Polling-Overhead.

Offene Frage aus Diskussion: Ob v1 bei 50k Shells überhaupt durchläuft oder crashed
— das wäre ein starker Befund fürs Paper ("v1 fails beyond N shells").

## Messgrößen → Paper-Zellen

| Paper-Zelle | Metrik | Quelle |
|---|---|---|
| [EVAL: a1] / [EVAL: b1] | Mean ingest latency / event (ms) | `total_events / drain_time` aus Lag-Kurve |
| [EVAL: a2] / [EVAL: b2] | Full-load wall-clock (s) | `drain_time + BaSyx POST time` |
| [EVAL: a3] / [EVAL: b3] | Cypher p95 2-hop (ms) | 100 Queries auf fertigem Graph |
| [EVAL: a4] / [EVAL: b4] | Cypher p95 4-hop w/ semID (ms) | 100 Queries auf fertigem Graph |
| [EVAL: T_50k] | 50k wall-clock (v2 only) | drain_time_50k |
| [EVAL: S] | Scale factor | 50 (hardcoded: 50k/1k) |
| [EVAL]× | Speed-up | a/b Ratios |

## Architektur

### Dateien

```
tests/ingest-bench/
├── docker-compose.bench.yml    # Reduzierter Stack: Kafka + Mongo + Neo4j + BaSyx + Connect v1/v2
├── .env.bench                  # NEO4J_V1_TAG=7.9.1-0.1.3, NEO4J_V2_TAG=7.9.1-2.1.3
├── bench_ingest.py             # Hauptskript: Stack starten → Import → Lag messen → Queries
├── results/                    # JSON-Ergebnisse
```

### docker-compose.bench.yml — Reduzierter Stack

Nur Services auf dem Ingest-Pfad (kein Weaviate, Embedding, MCP, Agent, UI):

- `kafka`, `mongo`, `neo4j` (eigenes Volume: `bench_neo4j`)
- `aas-registry`, `submodel-registry`, `aas-discovery`, `aas-environment`
- `kafka-connect-neo4j-v1` (profile: `v1`, image: `${NEO4J_V1_TAG}`)
- `kafka-connect-neo4j-v2` (profile: `v2`, image: `${NEO4J_V2_TAG}`)

Kein: Weaviate, Embedding-Service, MCP Server, Agent, Open WebUI, GUI, AKHQ, Inspector,
kafka-connect-rag, submodel-templates-sync, basyx-viewer-proxy, open-webui-seed, mcp-inspector.

### Kafka Lag Messung

**Lag = log_end_offset - consumer_committed_offset**

Polling über `kafka-consumer-groups` CLI via `docker exec bench-kafka`:
- Intervall: 200ms während Ingest
- Zeitreihe: `lag(t)` für v1 und v2
- Metriken: peak lag, drain time (peak → 0), mean throughput (events/s)
- Optional: Lag-Kurve als Plot (v1 vs v2 overlay) — paper-würdiges Diagramm

Consumer Group Name: auto-detect via `kafka-consumer-groups --list`.

### Datensatz

Echter Industrie-Datensatz als AASX-Dateien in `tests/ingest-bench/aasx/`.
BaSyx auto-ingested die AASX-Dateien beim Hochfahren des Stacks.
Kein separater Import-Mechanismus nötig.

### Cypher p95 Queries

```cypher
-- 2-hop: Shell → Submodel → Property
MATCH (s:AssetAdministrationShell)-[:HAS_SUBMODEL]->(m:Submodel)-[:HAS_PROPERTY]->(p)
WHERE s.id = $id
RETURN s, m, p

-- 4-hop: Shell → Submodel → SME → SemanticID → ConceptDescription
MATCH (s:AssetAdministrationShell)-[:HAS_SUBMODEL]->(m:Submodel)
      -[:HAS_SME]->(sme)-[:HAS_SEMANTIC_ID]->(cd:ConceptDescription)
WHERE s.id = $id
RETURN s, m, sme, cd
```

Je 100 Wiederholungen → p95 Latenz.

## Subtasks

### T1 — docker-compose.bench.yml erstellen

**Status:** ✅ Done (2026-05-28)

Reduzierter Stack aus Haupt-docker-compose.yml extrahiert:
- Services: kafka, mongo, neo4j, aas-registry, submodel-registry, aas-discovery, aas-environment
- kafka-connect-neo4j als v1/v2 Profile
- Eigene Container-Namen (`bench-*`), eigenes Netzwerk `aas-bench-network`
- aas-environment mountet `./aasx/` für Auto-Ingestion
- Keine eigenen Volumes (ephemeral, wird nach jedem Run gewiped)

### T2 — .env.bench erstellen

**Status:** ✅ Done (2026-05-28)

```
NEO4J_V1_TAG=7.9.1-0.1.13
NEO4J_V2_TAG=7.9.1-2.1.3
```

### T3 — bench_ingest.py schreiben

**Status:** ✅ Done (2026-05-28)

Implementiert in `tests/ingest-bench/bench_ingest.py`:
- Stack-Up/Down via `docker compose --profile v1|v2`
- Kafka Lag Messung via `kafka-consumer-groups` CLI (docker exec)
- Cypher p95 Benchmark via neo4j Python driver (2-hop, 4-hop)
- Auto-Detection der Consumer Group
- JSON-Output + [EVAL]-Werte Printout
- CLI: `--skip-v1`, `--profile`, `--lag-interval`, `--lag-timeout`, `--query-repetitions`, `--cypher-only`

### T4 — Datensatz in aasx/ ablegen

User legt AASX-Dateien in `tests/ingest-bench/aasx/` ab.
Für 1k Vergleich: ~1,000 AASX Dateien.
Für 50k Scale: ~50,000 AASX Dateien (separater Durchlauf).

### T5 — Messung durchführen

Stack laufen lassen, Ergebnisse sammeln.

### T6 — [EVAL]-Platzhalter in 10-evaluation.tex befüllen

Alle `[EVAL: a1..a4]`, `[EVAL: b1..b4]`, `[EVAL: T_50k]`, `[EVAL: S]`, `[EVAL]×` ersetzen.

### T7 — claim_audit.md aktualisieren

E1, E2, S3, Z5 Status von ❌ → ✅ setzen.

## Acceptance Criteria

- `tests/ingest-bench/` enthält docker-compose.bench.yml, .env.bench, bench_ingest.py ✅
- AASX-Datensatz in `tests/ingest-bench/aasx/` abgelegt
- v1 und v2 Messungen durchgeführt
- 50k Shell Messung mit v2 durchgeführt
- Kafka Lag Zeitreihen als JSON gespeichert
- Alle `[EVAL: ...]` Platzhalter in 10-evaluation.tex ersetzt
- claim_audit.md E1, E2, S3 auf ✅
- Paper baut ohne Fehler
- §14 Conclusion konsistent mit den gefüllten Zahlen

## References

- Paper §07: `paper/etfa2026/content/07-ingestion-plugin.tex` (v2 Plugin Beschreibung)
- Paper §10: `paper/etfa2026/content/10-evaluation.tex` (Benchmark A [EVAL] Platzhalter)
- claim_audit.md: E1, E2, S3, Z5
- Verwandter Task: [[task-paper-bench-a-fill]] (wird durch diesen Task ersetzt/abgelöst)
- Haupt docker-compose.yml: `docker-compose.yml` (Referenz für Service-Konfigs)
- Docling Benchmark (Referenz-Setup): `tests/docling-bench/bench_docling.py`
- v1 Plugin: `dfkibasys/aas-neo4j-kafka-connect-plugin:7.9.1-0.1.13`
- v2 Plugin: `dfkibasys/aas-neo4j-kafka-connect-plugin:7.9.1-2.1.3`
- ETFA 2025 Paper: `sonnenberg2025aas_kg`
