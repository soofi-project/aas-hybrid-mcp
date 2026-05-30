---
name: Task – Neo4j Query Timeout & LIMIT Guard
description: Serverseitiger Timeout + saubere MCP-Fehlermeldung für unbeschränkte Cypher-Anfragen ohne LIMIT
type: task
status: open
priority: medium
---

## Background

Bench mit 579k+ Nodes (ingest-bench) zeigt: der Agent kann über `cypher_query`
eine MATCH-Anfrage ohne LIMIT absetzen und damit Neo4j bzw. den MCP-Server zum
Hängen bringen. `cypher_query.py` hat aktuell keinerlei LIMIT-Enforcement.

Ein Fine-Tuning-Datensatz löst das strukturell nicht — der Agent kann auch nach
Training Queries ohne LIMIT generieren. Absicherung muss serverseitig liegen
(Layered-Determinism-These).

## Subtasks

### T1 — Neo4j-seitigen Query-Timeout konfigurieren
Neo4j bietet `dbms.transaction.timeout` (neo4j.conf) bzw. per-Query
`CALL { ... } IN TRANSACTIONS` oder Bolt-Timeout. Konfigurieren, sodass
lang laufende Queries nach N Sekunden abgebrochen werden.

### T2 — MCP-Server fängt Neo4j-Timeout sauber ab
In `cypher_query.py` den `ClientError`/`TransientError` von Neo4j (Timeout)
explizit catchen und als strukturierte Fehlermeldung zurückgeben:
`"Query timed out — add a LIMIT clause to narrow the result set."` o. ä.

### T3 — Paper-Erwähnung prüfen
In §Future Work bzw. §Discussion sicherstellen, dass der Timeout als
Kurzfrist-Mitigation erwähnt ist, bevor GraphQL-Whitelisting / eigene
Query-Sprache (Langfrist) diskutiert wird.

## Acceptance Criteria

- Neo4j wirft bei unbeschränkter Traversal nach konfigurierbarem Timeout einen Fehler
- MCP-Server gibt dem Agent eine lesbare Fehlermeldung statt zu hängen
- Paper nennt den Timeout als ersten Verteidigungsring vor strukturellen Lösungen

## References

- `mcp-server/src/aas_hybrid_mcp/tools/cypher_query.py`
- `neo4j/` (Dockerfile + neo4j.conf)
- Verwandte Diskussion: GraphQL-Whitelisting / eigene Query-Sprache als Langfrist-Alternative
