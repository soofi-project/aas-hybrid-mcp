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
- **PDF processing — docling only** (~3 GB image with PyTorch CPU). ML-based layout/table recognition, image extraction, sound heading hierarchies. Single pipeline, no variant switch — initial ingest is slower (~seconds per page) but real-world manual updates are rare and the quality delta vs. rule-based parsers compounds across the retrieval/reranking/template-awareness stack.
- **Future: hybrid mode** — per-page dispatcher routing pages between local docling and GPU/Triton based on heuristics (OCR need, vector density, table quality)
- **Embedding model configurable:** Via `EMBEDDING_MODEL` env var (provider:model format). Supports openai, ollama, google_genai, voyageai. Triton via OpenAI-compatible endpoint.
- **Secrets outside repo:** `~/.env.secrets`, referenced via `SECRETS_PATH` in `.env`
- **Ports hardcoded in docker-compose.yml:** Not in `.env` — ports don't change, versions do.
- **Data sovereignty — whole stack self-hostable:** BaSyx, Kafka, Neo4j, Weaviate, embeddings, reranker, LLM can all run on-premise (H200 setup validated at Hannover Messe with the SOOFI project) or on German/EU cloud providers. No data leaves the premises — addresses the main adoption blocker for industrial AI in EU/German manufacturing (GDPR, AI-Act, trade-secret protection). Cloud LLM (OpenAI etc.) remains configurable for non-sensitive deployments but is not required.
- **Future LLM option — SOOFI 120B:** the DFKI SOOFI project is preparing a 120B-parameter open-source model with transparent, GDPR/EU-compliant training-data provenance. Available ~September 2026 (too late for ETFA submission but referenced as future work — plug-in replacement via the configurable `LLM_BASE_URL` / `LLM_MODEL` env vars, no code changes).

## Development Phases

### Phase 1: Project Scaffold and Docker Compose ✅
Infrastructure stack without MCP server.

### Phase 2: Minimal MCP Server with Cypher Tool ✅
- `query_aas_graph` tool — Cypher queries against Neo4j with read-only enforcement
- `aas://schema/graph` resource — complete AAS graph schema documentation (derived from Kafka Connect plugin source)
- Dockerfile, docker-compose service on port 8110, streamable-http via fastmcp + uvicorn

### Phase 3: ~~Schema Tool~~ (merged into Phase 2)

### Phase 4: Weaviate Client and Document Search ✅ (Reranker + Query-Rewriting + Neighbor-Expansion planned for paper eval)
- `search_aas_documents` tool — semantic vector search over ingested PDF documents
- Optional `submodel_id` filter (LLM discovers IDs via `query_aas_graph`, then scopes search)
- Sync Weaviate client with langchain query embeddings (same model as embedding-service)
- Shared `.env.embedding` ensures vector compatibility between services
- **Planned extension — Cross-Encoder Reranker (paper eval axis 1):**
  - Port existing Qwen3-Reranker-4b integration from `soofi-trainer/vector-mcp/src/vector_mcp/server.py` — production-tested at Hannover Messe, runs on H200 via vLLM with Cohere-compatible `/rerank` API
  - `RERANKER_MODE={distance|vllm}` env switch: `distance` falls back to `1 - cosine_distance` score when no reranker is reachable; `vllm` calls the real cross-encoder. Graceful fallback on failure.
  - Over-fetch (`RERANKER_CANDIDATE_LIMIT`) beyond requested `limit`, then re-rank top-K
  - Each result carries a `reranker_score` — directly usable for Precision@K metrics in the paper's evaluation
  - Applies to both `HandoverDocument` (asset docs) and `IdtaTemplateSpec` (template specs) collections
- **Planned extension — Query-Rewriting / HyDE (paper eval axis 2):**
  - LLM rewrites the user query before retrieval to bridge technical-vocabulary gaps (e.g. „Getriebe klemmt" → „Antriebsstrang, mechanische Blockade, Lagerschaden")
  - Optional HyDE variant: LLM generates a hypothetical answer passage, embed that instead of (or alongside) the raw query
  - Implementation option: Weaviate **named vectors** (multiple vector spaces per object) — raw-text and HyDE-answer embeddings stored side-by-side on the same chunk, switched at query time via `target_vector` instead of re-ingest
  - Added as an ablation axis, not as default — measured against reranker-only and template-aware variants
- **Planned extension — Neighbor/Context Expansion (paper eval axis 3):**
  - Known RAG pattern: first hit is a good anchor, but the actual answer often sits one paragraph above or below (technical manuals: warning above, instruction below)
  - **Ingest-side prerequisites** — each chunk persists `chunk_index: int`, `source_id: str`, `heading_path: [str]` (Markdown heading chain from docling), optional `prev_chunk_uuid` / `next_chunk_uuid`
  - **Tool design:** dual surface — keep `search_aas_documents` lean, add a separate `get_document_context(chunk_uuid, direction={before|after|section}, count=1)` tool so the agent decides whether to expand. Cheap default search, explicit navigation when needed.
  - Paper-relevant as third ablation axis (flat top-K vs. neighbor-expanded vs. section-scoped) — independent of reranker and query-rewrite, measurable separately
  - Priority: park until after Phase 7.5 (write tools); re-ingest needed for heading metadata, so batch with any other schema change
- **Optional extension — Contextual Retrieval (paper eval axis 4, only if budget allows):**
  - Anthropic (2024) pattern: prepend each chunk with a 1-sentence LLM-generated context line ("This chunk is from the MiR100 troubleshooting section, LED indicators chapter") *before* embedding. Empirically measurable Recall improvement.
  - Cost: one LLM call per chunk at ingest time. At Benchmark-B scale (~30–50 PDFs, a few thousand chunks) tractable; does not scale to the full 50k-shell ingest.
  - Different alternative hypothesis than reranker/query-rewrite: "the problem is chunk semantics, not ranking" — if both axes are in, they test independent claims.
  - **Decision deferred:** skip by default to keep the ablation matrix at 6 configs; only include if drafting shows Benchmark B has headroom and the 8-page budget still fits. If kept, bumps eval to 7 configs × ~50 questions ≈ 350 runs.
- **Paper eval ablation (ETFA 2026):** baseline hybrid search / +reranker / +query-rewrite / +neighbor-expansion / +IDTA-template-awareness (Phase 6) / full system — shows each component's contribution independently. Six configs × ~50 questions ≈ 300 runs (up from 250); confirm fit against 8-page budget before including all axes in the final matrix. Optional seventh axis (Contextual Retrieval) only if budget allows.

### ETFA 2026 Paper — Two-Benchmark Scope (sharpened)
Keep the two evaluations cleanly separated to avoid misleading scale claims:

**Benchmark A — Structural graph ingestion at scale (50k shells):**
- Lives in the sibling repo `aas-repository-neo4j-kafka-plugin`, not here. Plugin is consumed as Docker image `dfkibasys/aas-neo4j-kafka-connect-plugin:7.9.1-1.0.0` (the tag pinned in `.env`; image `version()` string still reports `1.0.0` but contains the v2 architecture below).
- Graph-only: Kafka events with AAS metadata → Neo4j. **No PDFs, no documents.** Shells are synthetic or metadata-only.
- Measures: ingestion latency per event, Cypher query latency on realistic multi-hop queries, plugin robustness under load
- **Engineering delta vs. ETFA 2025 — architectural resolution of the commit-bottleneck:**
  - **HTTP-Sink + Pebble templates → native Bolt driver** (`Neo4jBoltSinkTask`, `BoltRunner`) — eliminates per-event HTTP round-trip and JSON-error parsing
  - **CREATE-event buffering** (`MAX_BUFFER_BYTES = 40 MB`, `SAFETY_NODE_LIMIT = 20 000`) — many small events become one atomic transaction; UPDATE/DELETE still processed immediately for correctness
  - **Async ParameterModel building** in single-thread executor — `put()` returns without waiting; `flush()` synchronizes via `waitForModelBuilder()` before commit
  - **Chunked Cypher inserts** within a single transaction: `NODE_CHUNK_SIZE = 10 000`, `RELATION_CHUNK_SIZE = 50 000` — keeps individual statements within Neo4j parser limits while preserving atomicity via `executeWriteWithoutResult`
  - **Full AAS metamodel coverage** — all 35 relationship types from `RelationLabel` enum; ETFA 2025 covered only a subset
- **Scale delta:** 50× jump (1k → 50k shells) is enabled by the architectural changes above, not by hardware; same commodity Neo4j instance
- **Optional micro-benchmark:** old HTTP-Sink variant vs. new Bolt+buffered variant on the same 1k-shell workload — quantifies the per-event speedup directly (if the v1 image remains reproducible)

**Benchmark B — Document-aware agent evaluation (10 assets, realistic):**
- 10 real assets with their IDTA Handover Documentation (~30–50 PDFs total)
- ~50 maintenance/troubleshooting questions with manually curated ground truth
- Ablation matrix: baseline hybrid / +reranker / +query-rewrite / +IDTA-template-awareness / full system (5 configs × ~50 questions ≈ 250 agent runs)
- LLM-as-Judge for scoring, ~20-question human spot-check for judge calibration
- Measures: Precision@K, answer correctness, retrieved-chunk relevance, agent step count, end-to-end latency

**Out of paper scope (future work):**
- Document-ingestion throughput at scale — real shops reference PDFs via URL, download dominates compute; motivates but does not require GPU-accelerated docling
- GPU-accelerated docling (Phase 9) — technically deployable now (same pattern as reranker), but not paper-relevant at 10-asset scale
- CRUD-roundtrip write eval — narrative scenario + screenshots rather than quantitative comparison (no meaningful baseline exists)
- **ConceptDescription semantic layer (Phase 12)** — Kafka-plugin extension to ingest CDs as Neo4j nodes, plus a `ConceptDescription` Weaviate collection for vocabulary-discovery via vector search. Two MCP tools: `lookup_concept(semantic_id)` (deterministic) and `search_concepts(query)` (fuzzy). Strong follow-up-paper hook — orthogonal to Benchmark C write-path eval; the two could be combined into a single journal-length paper covering write-eval and semantic-layer eval together. Frame in ETFA 2026 outlook as a concrete, technically-scoped extension (specific plugin change + specific tool surface), not as generic „more semantics".

### ETFA 2026 — Page Budget and Compression Priorities (8-page hard limit)
Last year the paper filled exactly 8 pages; no extension fees are offered by ETFA. The current draft overruns budget by ~2 pages. Compression priorities, in order — cut from the bottom up only as space requires:

1. **Cut first — Benchmark C (write-path ablation).** At ~1.5–2 pages (5 configs × 3 models × 2 regimes × 5 metrics, 4 500+ runs) this is a journal-paper-sized evaluation inside a workshop paper. Keep §7 Write Loop as design + qualitative walkthrough + Listing 1. Move the quantitative ablation to an extended/journal version or a follow-up paper. Benchmark C plan retained in `memory/benchmark_c_plan.md` for the follow-up.
2. **Compress §5 Plugin v2 to ~0.75 page.** ETFA 2025 readers already know the HTTP-Sink + Pebble baseline. Collapse the six subsections (Bolt, Buffering, Async, Chunking, Metamodel, Rollout) into one fluent paragraph with inline emphasis on the key constants (`MAX_BUFFER_BYTES = 40 MB`, `NODE_CHUNK_SIZE = 10 000`, `RELATION_CHUNK_SIZE = 50 000`).
3. **Trim §2 Related Work's 8-point delta list to 4.** Keep hybrid retrieval, template-awareness prior, commit-bottleneck resolution, CRUD loop. Fold the rest into single sentences inside the kept points.
4. **Tighten the JSON Listing in §7.** Reduce to the six most informative fields (idShort, Status, Priority, RelatedAsset, ShortText, ServiceType); replace `DetailedInformation` contents with "…" and reference the accompanying release repo for the full payload.
5. **Replace ASCII architecture diagram with TikZ.** An ASCII block uses more lines than a properly typeset figure, and looks worse in review.
6. **Walk-Through compression.** Screenshot-based single figure rather than prose for the write-path walkthrough.

Compression is a final-pass concern, not a drafting concern. Keep drafting with full content; compress when numbers and figures are in. Workshop submission deadline: 31 May 2026; final version: 4 July 2026.

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

### Phase 6.5 (Next Up): Test-Data Fixtures for Benchmark B
Current `aasx/` contains only two MiR100 shells (`mir100_0_aas`, `mir100_type_aas`) — insufficient for Benchmark B (10 assets with handover docs) and for the worker-scenario walk-through ("der Transportroboter in Halle 4").

- **Halls as their own AAS shells:** Halle 3 + Halle 4 (matches paper scenario). Distinct character per hall (e.g. logistics vs. assembly) so location-based disambiguation is non-trivial.
- **Containment direction: Hall → Assets** via IDTA `HierarchicalStructures` (02011). Rationale:
  - Uses a real IDTA template, reinforcing the paper's template-awareness narrative (vs. a custom `InstalledIn` ReferenceElement on asset side)
  - Entity-nested containment has an unambiguous owner (the container). `RelationshipElement` was considered and rejected — it has no natural owner, forcing an asymmetric placement where one side's AAS-native reader cannot see the relation.
  - Asset shells stay free of location metadata — location lives exclusively on the hall side. Neo4j supplies the reverse traversal ("what's in hall 4") via a 3–4-hop Cypher for free, so unidirectional AAS modeling costs nothing at query time.
- **Hall submodels (three):**
  - `Nameplate` (IDTA 02006) — acknowledged template abuse (hall is not a product); paper notes IDTA has no facility standard.
  - `HierarchicalStructures` (IDTA 02011) — Entity tree with `ReferenceElement` pointing to each contained Asset's AAS.
  - `FacilityInformation` (custom `semanticId`, no IDTA equivalent) — area m², primary use, power connection kV. Marked clearly as custom.
- **Asset count:** 10–12 instances backed by 4–6 type shells (free type/instance story). MiR family (MiR100 + MiR250 + MiR600, 3–4 instances) concentrated in Halle 4 so "the transport robot in hall 4" resolves uniquely via hall membership. Remaining 6–8 assets in Halle 3 from other domains (Festo / KUKA / UR / SICK / conveyor) for diversity.
- **Asset submodels (three mandatory):** `Nameplate` + `TechnicalData` + `HandoverDocumentation`. Handover docs are public PDFs (MiR-Support for the MiR family, vendor support sites for the rest).
- **Fixture generation path:** prefer creating fixtures **via the Phase 7.5 write tools** once they land (agent-driven population demonstrates the CRUD loop). Hand-edit AASX files only if Benchmark B deadline forces it.
- **Capability vocabulary on Type AAS** — IDTA 02020 ships only *structural* semanticIds (the `Capability` slot), no controlled vocabulary for concrete capabilities like Transport / Handling / Assembly. Decision: **own URI namespace `https://aas-hybrid-mcp.dfki.de/capability/{Name}`** attached as **`supplementalSemanticIds`** on each Capability element. The IDTA structural `semanticId` stays as primary (signals „this slot conforms to IDTA 02020"); the project-specific URI is the actual matching anchor. Cypher disambiguation matches against the supplementalSemanticIds, **not** `idShort` (which is just a free-form local label). Optional extension: add VDI 2860 handling-function references (Bewegen / Handhaben / Fügen) as additional supplemental semanticIds for standard-vocabulary anchoring, if the paper narrative calls for it. Active capabilities in this project: `Transport` (MiR family, conveyor), `Handling` (UR family, CRX), `Assembly` (UR20, CRX). Asset Type files in `aasx/*_type/sm_capabilitydescription.json` need to be updated to reflect this — current versions still rely on idShort matching.

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

### Phase 7.5 (Planned): MCP Write Tools — BaSyx AAS Mutation
- **Goal:** complete the MCP endpoint so it covers the full CRUD surface — reads via Neo4j/Weaviate, writes via BaSyx REST. Closes the loop: writes emit Kafka events, Neo4j + Weaviate auto-sync, agent observes its own changes through existing read tools.
- **`basyx-python-sdk` as client-side validation layer:** LLM-provided JSON is deserialized via `basyx.aas.adapter.json` before any BaSyx call. Constraint violations (missing `semanticId`, invalid element nesting, wrong `modelType`, …) surface as Python exceptions and are returned to the agent for self-correction — no invalid state ever reaches the shell.
- **httpx client to BaSyx AAS Environment** (port 8081) — SDK does not ship a REST client for remote BaSyx servers, so we build a thin wrapper (Base64-URL path encoding, PUT/POST/DELETE).
- **Tool set — 6 generic, symmetric tools:**
  - `put_aas(aas_json)` — idempotent create-or-replace shell
  - `delete_aas(aas_id)`
  - `put_submodel(aas_id, submodel_json)`
  - `delete_submodel(aas_id, submodel_id)`
  - `put_submodel_element(submodel_id, id_short_path, element_json)` — covers **all** SubmodelElement subtypes (Property, File, SMC, SML, MultiLanguageProperty, Range, ReferenceElement, RelationshipElement, Entity, Operation, …) via a single tool, because the SDK resolves `modelType` during deserialization
  - `delete_submodel_element(submodel_id, id_short_path)`
- **IDTA template awareness:** agent is expected to read `aas://template/{name}` (Phase 6) before writing, so structure follows standardized submodel layouts.
- **Attachments deferred to Phase 10:** binary File/Blob upload is explicitly out of scope here. Without an active extraction use case (Agent reads document → extracts values → fills submodel), an attachment tool would be redundant with a direct BaSyx upload by the user. See Phase 10 for the full rationale and the planned attachment tools.

### Phase 8a (Paper scope): Image URLs in Weaviate Metadata
- **Goal:** when a chunk comes from a manual page containing a schematic, return the image URL alongside the text so the UI renders it — huge UX win at minimal cost.
- Docling already extracts images during PDF processing → store on MinIO → add `image_urls: [...]` to the chunk's Weaviate metadata
- Agent response includes Markdown image syntax (`![](http://minio/...)`) — Open WebUI renders natively
- No embedding of images yet, no multimodal retrieval — purely text-based chunk selection, visual payload attached
- Paper-relevant: „Agent zeigt den Schaltplan direkt im Chat" is a visually compelling demo, and motivates Phase 8b/11 as future work

### Phase 8b (Future): Full Image Understanding
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
- Configurable `ExtractionPolicy`: local-docling / triton-gpu / hybrid
- Map extracted data to IDTA Teilmodell attributes (DocumentID, Status, Version)

### Phase 10 (Future): PDF-to-AAS Extraction + Attachments
- **Builds on Phase 7.5 write tools** — this phase adds the extraction layer and the attachment handling that was deliberately deferred from 7.5.
- **PDF-to-AAS workflow:** user references an asset document (datasheet, manual, certificate) → agent extracts information via LLM (using the existing docling-based PDF pipeline) → agent calls Phase 7.5 `put_submodel` / `put_submodel_element` to populate a submodel structured according to IDTA templates (Phase 6).
- **Attachment handling** (deferred from Phase 7.5 because it only yields value once the agent actively processes document content):
  - `upload_attachment_from_url(submodel_id, id_short_path, source_url, content_type?)` — MCP server downloads bytes server-side via `httpx`, then PUTs to BaSyx `/submodel-elements/{path}/attachment`. The agent never handles binary data — only a URL string.
  - **Two-step flow:** agent first creates the `File`/`Blob` element via `put_submodel_element` (with `contentType`, empty `value`), then calls `upload_attachment_from_url` to fill the binary payload.
  - **Source URL forms:** public HTTP(S), or a MinIO path pre-staged by the user / upstream process (a dedicated chat UI with an upload button could push to MinIO and hand the resulting path to the agent).
  - **SSRF protections:** scheme allowlist (`https://`, internal `minio://`), host allowlist, size + timeout caps — the URL flows indirectly from user prompt through the LLM, so the MCP server must defend itself.
  - **Content-Type** from HTTP response headers; LLM-provided parameter as override.
- **Automatic classification:** agent determines which IDTA template fits (Nameplate, Technical Data, Handover Documentation, …) via `search_idta_templates` + `aas://template/{name}` before writing.
- **Conversational:** user can refine, correct, add context in natural language; agent uses Phase 7.5 tools to iterate on the same submodel.
- **Rationale for splitting 7.5 / 10:** pure write access (7.5) is immediately useful for other agents and direct API consumers. Attachment upload only earns its complexity (SSRF defense, staging story, two-step flow) once paired with an extraction use case — which is precisely what Phase 10 delivers.

### Phase 12 (Future): ConceptDescription Semantic Layer
- **Goal:** close the semantic gap between „agent sees an IRDI on a Property" and „agent understands what that IRDI means". ConceptDescriptions (top-level AAS metamodel element) carry the human-readable definition for every semanticId — currently invisible to the agent.
- **Two complementary surfaces (the lookup-vs-discovery split):**
  - **Lookup (graph, deterministic):** MCP tool `lookup_concept(semantic_id)` returns the CD payload (preferredName, definition, description, dataSpec) for a known IRDI/URI. Backed by Neo4j — every CD becomes a graph node referenceable from any Property/Element via `semanticId`.
  - **Discovery (vector, fuzzy):** MCP tool `search_concepts(query, limit)` over a new Weaviate `ConceptDescription` collection. Embedding source per CD: `preferredName + definition + description` (multilingual concatenated). Answers „is there a standardized property for ‚manufacturer order code'?" by returning candidate IRDIs the agent can then plug into `query_aas_graph`.
- **Kafka-Connect plugin extension required** — current plugin (`dfkibasys/aas-neo4j-kafka-connect-plugin`) does **not** ingest ConceptDescription nodes. Adding a `ConceptDescription` label + relations (`HAS_PREFERRED_NAME`, `HAS_DEFINITION`, `HAS_DATA_SPEC`, …) is the prerequisite for the lookup tool. Owned in the sibling repo `aas-repository-neo4j-kafka-plugin`.
- **eCl@ss bulk import deferred** — eCl@ss BAP alone is ~50k properties. Pragmatic alternative: walk Neo4j, collect all distinct `semanticId` values currently referenced across the project's AAS, fetch CDs only for those (scales with the project, not with the standard). Bulk import only if a real query motivates it.
- **Paper relevance:** strong follow-up-paper hook — orthogonal to Benchmark C (write-path eval) but thematically adjacent. Could form a single journal-length follow-up covering both write-eval and semantic-layer eval. For ETFA 2026 itself: scoped as future work in the outlook section.

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
│   ├── pdf.py               # PDF conversion via docling
│   └── vectorstore.py       # Weaviate client (singleton)
├── kafka-connect-rag/       # HTTP Sink Kafka Connect
├── neo4j/                   # Custom Neo4j with APOC
├── aasx/                    # Test AASX files
├── docker-compose.yml
├── .env                     # Version pins
├── .env.embedding           # Embedding model config
├── up.sh / down.sh          # Stack management
```

## Conventions

- Python: pyproject.toml with pinned version ranges (`>=x.y,<major`)
- Docker: all versions pinned, no `:latest` tags
- All services have `restart: unless-stopped`
- English for code, comments, and log messages
