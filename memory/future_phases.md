---
name: Future phases and open tasks
description: Phases 8a–12 and ongoing improvement tasks
type: project
---

## Phase 8a: Image URLs in Weaviate metadata
**Status:** 🟦 Not started
Goal: Extract image references from docling output; store image URL as Weaviate document metadata property. Enables future multimodal retrieval (CLIP/VLM) without touching text embeddings.

## Phase 9: Retrieval ablation techniques
**Status:** 🟦 Planned

### Query Rewriting
- LLM-based query expansion with synonyms and domain terminology before vector search
- Bench B ablation axis (Table 3)
- Where: `search_aas_documents` MCP tool — add optional `rewrite_query` flag; agent invokes LLM with domain prompt to generate expanded query terms

### HyDE (Hypothetical Document Embeddings)
- Generate a hypothetical answer passage; embed _that_ instead of the raw user query
- Bench B ablation axis (Table 3), ref: gao2022hyde
- Where: embedding-service — new endpoint `/embed_with_hyde` that takes query + system context → generates hypothetical doc → embeds

## Phase 10: Multimodal retrieval
**Status:** 🟦 Planned
- CLIP-based image retrieval for schematics and diagrams in manuals
- VLM-generated alt-text for images stored as Weaviate metadata
- Depends on Phase 8a (image URLs in metadata)

## Phase 11: AAS population from documentation
**Status:** 🟦 Planned
- Agent reads datasheets and automatically populates empty AAS submodels
- Bridges raw documentation → structured digital twin
- Heavy write-path usage; depends on Phase 9 quality improvements

## Phase 12: Concept Description semantic layer
**Status:** 🟦 Planned
- `lookup_semantic_id` MCP tool wrapping BaSyx CD-Repository API
- Resolves any IRDI → IEC 61360 payload (preferredName, definition, dataType, unit)
- Distinguishes local CDs (project-namespace, IDTA-template) from external (ECLASS)

## Open engineering tasks

### Pydantic coercion centralization
- **Where:** `qwen_parser.py`, `agent_plan_nodes.py`, `crag_nodes.py`, `rewoo_nodes.py`, `reflexion_graph_nodes.py`, `agent_supervisor_nodes.py`
- **Problem:** Each parse function has its own ad-hoc coercion (`str → list`, `float → literal`, etc.)
- **Fix:** Extract `_coerce_final_answer`, `_coerce_judgment`, etc. into a single module (e.g. `aas_agent/coercion.py`) with per-schema normalizers reused by all parsers

### Bind-mount `C:\134` issue
- **Where:** `docker-compose.yml` lines 477-501
- **Problem:** Individual file mounts work but are fragile — new files must be added manually
- **Nice-to-have:** Investigate `docker compose` on Windows WSL2 / Hyper-V for reliable directory mounts

### Reflexion finalizer quality
- **Where:** `reflexion_graph_nodes.py`
- **Problem:** Best answer text is now tracked but the LLM may still regenerate instead of using it
- **Improvement:** Prompt tweak to make the finalizer _use_ the best answer as-is when confidence is high
