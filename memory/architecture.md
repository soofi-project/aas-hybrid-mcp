---
name: Architecture overview
description: System architecture with inbound data flow, outbound query/write flow, service inventory, agent variants, and MCP tool surface
type: project
---

## Overview

BaSyx loads `.aasx` files → publishes Kafka events. Two Kafka Connect pipelines consume them: `kafka-connect-neo4j` baut den Neo4j-Wissensgraphen, `kafka-connect-rag` → `embedding-service` extrahiert PDFs → chunking → Embeddings → Weaviate. Die Retrieval-Strecke läuft heute **Rewrite → Embed → Vector Search → optionaler Reranker**, bevor Ergebnisse zurück an den Agent gehen. LangGraph-Varianten rufen 15 MCP-Tools auf Port 8110 auf, um Graph + Vektorspeicher zu lesen und CRUD via BaSyx-REST auszuführen. Alle Services hängen auf dem Bridge-Netz `aas-network`.

---

## Architecture (Mermaid Draft)

```mermaid
flowchart TB
    subgraph sub_inbound ["(a) Inbound Data Flow"]
        A[AASX Files] --> B[BaSyx AAS Repository]
        B --> C[Kafka Events]
        C --> D[Kafka Connect Neo4j<br/>Cypher over Bolt]
        C --> E[Kafka Connect RAG<br/>HTTP Sink]
        D --> F[Neo4j<br/>27 labels / 34 relations]
        E --> G[Embedding Service<br/>Docling → chunks → embed]
        G --> H[Weaviate<br/>aas_documents + aas_templates]
        I[IDTA Templates Repo] --> J[templates-sync init]
        J --> H
        J --> K[Filesystem JSON]
    end
    
    subgraph sub_outbound ["(b) Outbound Query/Write Flow"]
        U[Worker / Open WebUI] --> A2[aas-agent API<br/>4 variants (+verbose)]
        A2 --> M2[MCP Server<br/>15 tools]
        M2 -->|graph / schema| F
        M2 -->|vector search| H
        M2 -->|CRUD| BS[BaSyx REST]
        M2 -->|IRDI lookup| CD[CD-Repository]
        M2 -->|templates / manual| FS[FS JSON / Bind-mounted]
        BS -->|Kafka events| C
    end
```

---

## Service Inventory

| Port(s) | Service | Rolle |
|---|---|---|
| 9093 | Kafka (single-node KRaft) | Event-Bus für BaSyx → Kafka Connect |
| 8086 | AKHQ | Kafka UI / Topic-Inspection |
| 8085 | kafka-connect-rag | HTTP-Sink → Embedding-Service |
| 8084 | kafka-connect-neo4j | Cypher-Sink → Neo4j |
| 8083 | AAS Registry | Registry-API für AAS-Shells |
| 8082 | Submodel Registry | Registry-API für Submodelle |
| 9100 | AAS Discovery | Discovery-Endpoint (BaSyx) |
| 8081 | BaSyx AAS Environment | AAS-Repository & REST-API |
| 8099 | AAS GUI | BaSyx-Frontend |
| 8091 | basyx-viewer-proxy | NGINX Proxy für Inline-PDF-Viewer |
| 8000 | Embedding-Service | Flask: Docling → Embeddings → Weaviate |
| 8070 / 50051 | Weaviate HTTP / gRPC | Vector Store + gRPC Ingest |
| 7474 / 7687 | Neo4j Browser / Bolt | Graph UI & Treiber-Port |
| 8110 | AAS Hybrid MCP | FastMCP-Server mit 15 Tools |
| 8120 | aas-agent | LangGraph-API (OpenAI-kompatibel) |
| 8090 | Open WebUI | Chat-Frontend mit Agent-Auswahl |
| 6274 / 6277 | MCP Inspector | MCP-Debugging-UI |

Kafka läuft ohne separaten ZooKeeper-Container; KRaft übernimmt die Controller-Rolle.

---

## Ingestion Data Flow

1. **AASX Upload**: Operator places `.aasx` files in `aasx/` → BaSyx AAS Environment loads them
2. **Kafka Event Emission**: Every create/update/delete emits a JSON event to `aas.repository.events.topic`
3. **Graph Pipeline** (kafka-connect-neo4j):
   - Consumer reads Kafka events
   - Transforms each event into Cypher statements
   - Executes over native Bolt protocol with buffering (40 MB, 20K node limit)
   - Result: 27 node labels, 34 relationship types, full AAS metamodel coverage
4. **Document Pipeline** (kafka-connect-rag → embedding-service):
    - Kafka events referencing AAS `File` elements trigger HTTP sink → embedding-service downloads PDF → Docling extracts text/layout → chunks with metadata → embeds → writes to Weaviate (`aas_documents_{model_slug}`)
5. **Template Pipeline** (templates-sync init container):
   - Clones IDTA submodel-templates repository → extracts JSON specs → ingests into Weaviate (`IdtaTemplateSpec`) AND writes filesystem JSON files for exact lookup

---

## Query/Write Data Flow

1. **User Input**: Worker asks maintenance question in Open WebUI
2. **Agent Routing**: `api.py` routes to variant based on `model` field (`aas-agent:react`, `aas-agent:plan`, etc.)
3. **Tool Execution**: Der Agent nutzt die MCP-Tools zielgerichtet:
   - `query_aas_graph(cypher, params?)` → Neo4j (read-only, 1000 Zeilen Limit, `/Submodel`-Suffix wird normalisiert)
   - `search_aas_documents(query, submodel_id?, limit?, asset_name?, doc_language?)` → Weaviate (Vector Search mit optionalem Scope, liefert `reranker_used`, `query_rewritten`, `rewritten_query`, `diagnostic`, `chunk_count`)
   - `search_idta_templates(query, template_name?, limit?)` → Weaviate (Template-Vektorsuche, gleicher Rewrite/Reranker-Flow)
   - `get_graph_schema()` → kompletter Node-/Relationship-Katalog für Cypher-Generierung
   - `get_templates_index()` / `get_template(name)` → Filesystem-JSON (Index + einzelnes Template) inkl. gematchter Graph-SemanticIds
   - `get_manual_index()` / `get_manual_page()` → bind-mount Operator-Handbuch
   - `lookup_semantic_id(id)` → BaSyx Concept-Description Repository (IEC 61360)
4. **Write Operations** (`put_*`/`delete_*`):
   - Metamodel validation via `basyx-python-sdk` deserialization
   - Template conformance check via generated Python classes
   - BaSyx REST call → triggers Kafka events → auto-sync back to Neo4j + Weaviate
   - Agent's next turn observes its own previous writes

---

## Agent Variants (4 Basismodelle + `*-verbose`)

Alle Modell-IDs existieren als Basismodell (`aas-agent:react` etc.) und automatisch generierter `*-verbose` Alias (identische Graph-Topologie, aber Streaming mit zusätzlichen Debug-Details).

| Model ID | Variant | Beschreibung |
|---|---|---|
| `aas-agent:react` | `AgentRunner` | ReAct-Loop via LangGraph (`create_react_agent`), Standard für `AGENT_DEFAULT_MODEL` |
| `aas-agent:plan` | `PlanReflectAgentRunner` | `planner → executor → reflector → finalizer`, begrenzte ReAct-Subloops pro Schritt |
| `aas-agent:crag` | `CragAgentRunner` | `executor → relevance → (refine → executor) → synthesizer`, Multi-Query mit Re-Ranking |
| `aas-agent:reflexion` | `ReflexionAgentRunner` | `executor → judge → (reflect → executor) → finalizer`, Trial-basiertes Selbstfeedback |

---

## MCP Tools (15)

| Kategorie | Tool | Zweck |
|---|---|---|
| **Graph** | `query_aas_graph(cypher, params?)` | Read-only Cypher (1000 Zeilen Limit, `/Submodel`-Suffix wird automatisch entfernt) |
| **Graph** | `get_graph_schema()` | Vollständiger Node-/Relationship-Katalog inkl. Beispielqueries |
| **Document** | `search_aas_documents(query, submodel_id?, limit?, asset_name?, doc_language?)` | Vektorsuche mit Rewrite + optionalem Reranker; Response liefert `reranker_used`, `query_rewritten`, `rewritten_query`, `diagnostic`, `chunk_count` |
| **Manual** | `get_manual_index()` | Liste verfügbarer Manual-Seiten |
| **Manual** | `get_manual_page(name)` | Einzelne Manual-Seite abrufen |
| **Template** | `search_idta_templates(query, template_name?, limit?)` | Template-Vektorsuche (gleicher Rewrite/Reranker-Flow) |
| **Template** | `get_templates_index()` | JSON-Index aller Templates inkl. gematchter `graphSemanticIds` |
| **Template** | `get_template(name)` | Strukturelles Template-JSON laden |
| **Semantic** | `lookup_semantic_id(id)` | IRDI/IRI → IEC-61360-Content via BaSyx |
| **CRUD** | `put_aas(aas_json)` | AssetAdministrationShell anlegen/ersetzen (SDK-validiert) |
| **CRUD** | `delete_aas(id)` | AAS löschen |
| **CRUD** | `put_submodel(aas_id, sm_json)` | Submodel schreiben (SDK + Template-Validator) |
| **CRUD** | `delete_submodel(aas_id, sm_id)` | Submodel löschen |
| **CRUD** | `put_submodel_element(sm_id, id_path, elem_json)` | Beliebiges SubmodelElement validiert schreiben |
| **CRUD** | `delete_submodel_element(sm_id, id_path)` | SubmodelElement entfernen |

Die LangGraph-Runner bringen zusätzlich das Hilfstool `get_current_utc_time()` mit; es wird agentseitig bereitgestellt und ist kein MCP-Endpunkt.
