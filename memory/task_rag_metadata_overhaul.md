---
name: Task - RAG Metadata Overhaul
description: Rich metadata für Weaviate chunks: source URL, page, heading, filename, snake_case schema
type: task
status: open
priority: high
depends_on: []
---

## Summary

Weaviate chunks speichern nur filename als "source" — kein original URL, keine page number,
kein heading context. Agent kann keine source attribution liefern, kein PDF page jump,
keine evidence classification.

**Ziel:** Jeder chunk hat vollständige source metadata. `source` wird zum fixed category
string ("document"), alle anderen infos in eigene properties. Snake_case durchgehend
(Python konvention, konsistent mit vector store standards).

## New Weaviate Schema

| Property | Type | Old Value | New Value |
|---|---|---|---|
| `text` | TEXT | chunk text | chunk text (unchANGED) |
| `source` | TEXT | filename ("manual.pdf", "attachment") | `"document"` (fixed category) |
| `source_heading` | TEXT | *(nicht vorhanden)* | Heading path: `"4.2 Elektrischer Antrieb"` |
| `source_page` | INT | *(nicht vorhanden)* | Page number: `3` |
| `source_url` | TEXT | *(nicht vorhanden)* | User-visible URL oder attachment URL |
| `source_filename` | TEXT | *(nicht vorhanden)* | Original filename: `"manual.pdf"` |
| `submodel_id` | TEXT | camelCase | snake_case |
| `sm_element_path` | TEXT | camelCase | snake_case |
| `id_short` | TEXT | camelCase | snake_case |
| `content_hash` | TEXT | camelCase | snake_case |

`source_url` Logik:
- External PDF (`File.value` starts with `http`): URL direkt (`https://example.com/manual.pdf`)
- BaSyx attachment: `{BASYX_PUBLIC_URL}/submodels/{base64(submodelId)}/submodel-elements/{smElementPath}/attachment`
- `BASYX_PUBLIC_URL` = `http://localhost:8081` (user-facing), **nicht** interne Docker URL

`source_jump_url` = `{source_url}#page={source_page}` — gebaut vom MCP endpoint für den agent.

## Subtasks

### T1: ENV + Config

**`.env`:**
- `BASYX_PUBLIC_URL=http://localhost:8081` — user-facing BaSyx URL für `source_url`

**`docker-compose.yml` embedding-service:**
- `- BASYX_PUBLIC_URL=${BASYX_PUBLIC_URL}` via `env_file` — kein extra `environment:` entry

**`embedding-service/config.py`:**
- `BASYX_PUBLIC_URL: str = os.environ["BASYX_PUBLIC_URL"]` — KeyError wenn fehlt, kein default
- `BASYX_SUBMODEL_REPO` bleibt unverändert (interne download URL)

### T2: Page numbers aus docling extrahieren

**`embedding-service/pdf.py`:**
- `convert_pdf_to_markdown()` — docling's `ConversionResult`遍历 document tree,
  jedem text element die `page_no` aus `.prov` (provenance) holen
- Page markers als markdown comment injectieren: `<!--page:1-->` vor dem section text
- `export_to_markdown()` mit den annotated pages

### T3: Chunking mit MarkdownHeaderTextSplitter

**`embedding-service/pdf.py`:**
- `chunk_text(markdown_text) -> list[dict]` statt `list[str]`
- 1. `MarkdownHeaderTextSplitter` (headings headers, titles) teilt nach headings → metadata
- 2. `RecursiveCharacterTextSplitter` auf oversized sections — metadata bleibt attached
- Return: `[{text, heading, page}, ...]`
  - `heading`: dict oder string (z.B. `{"Header 1": "4", "Header 2": "Elektrischer Antrieb"}`)
  - `page`: int (aus page marker im chunk text)

### T4: Weaviate schema + insert

**`embedding-service/vectorstore.py`:**
- `_ensure_collection()` — neue properties: `source_heading` (TEXT), `source_page` (INT),
  `source_url` (TEXT), `source_filename` (TEXT)
- Bestehende properties: `submodel_id`, `sm_element_path`, `id_short`, `content_hash`
  (snake_case rename — migration via collection drop/recreate)
- `insert_chunks()`:
  - Signatur: `insert_chunks(chunks: list[ChunkData], vectors, source, source_url, source_filename, submodel_id, sm_element_path, id_short, content_hash)`
  - `ChunkData = {text, heading, page}`
  - Pro chunk: `{text, source, source_heading, source_page, source_url, source_filename, ...}`

### T5: Ingestion pipeline

**`embedding-service/handlers.py`:**
- `_ingest_pdf()` — `source="document"`, `source_url` via neue `_public_pdf_url()`,
  `source_filename` (URL: last path segment, attachment: `"attachment"`)
- `chunk_text()` result ist jetzt list of dicts → page + heading pro chunk
- `insert_chunks()` mit neuen fields

### T6: MCP search response

**`mcp-server/src/aas_hybrid_mcp/weaviate_client.py`:** im `_search_sync()` response dict:
- `source` → `"document"`
- `source_heading` → heading string aus metadata
- `source_page` → page number
- `source_url` → user-visible URL
- `source_filename` → filename
- `content_hash` → SHA-256 (bisher nicht returned)
- `source_jump_url` → `{source_url}#page={source_page}` (computed)
- `smElementPath` / `idShort` → snake_case im response (oder camelCase für backwards compat)

### T7: Template sync (optional/konsistenz)

**`submodel-templates-sync/main.py`** — gleiche metadata für template chunks?
Nicht dringend — templates sind separate collection, haben eigene `templateName`, `pdfSource`.
Können später nachgezogen werden.

### T8: Tests + Validate

- `./down.sh && ./up.sh --build --vllm`
- Weaviate collection erstellt mit neuen properties
- PDF ingest: chunks haben `source_heading`, `source_page`, `source_url` gesetzt
- MCP search → jedes result hat alle fields + `source_jump_url`
- `source == "document"` für alle chunks
- `BASYX_PUBLIC_URL` fehlt → embedding-service crasht mit KeyError

## Acceptance Criteria

- Weaviate chunks haben `source_page` (>0) + `source_heading` (non-empty wenn heading vorhanden)
- `source` ist immer `"document"` für PDF chunks
- `source_url` ist eine user-öffnbare URL (external PDF oder BaSyx attachment)
- `source_jump_url` springt im browser zur richtigen PDF page
- `source` == "document" für alle chunks
- `BASYX_PUBLIC_URL` fehlt → embedding-service crasht mit sinnvollem KeyError
- Alle properties snake_case in Python code + Weaviate

## Notes

- Collection wird drop + recreate beim nächsten ingest (neu ingestieren ist ok)
- Bestehende chunks mit altem schema werden ignoriert (neue collection hat neuen slug
  wenn model sich geändert hat, ansonsten manual delete der alten collection)
- `BASYX_PUBLIC_URL` ist in `.env` — docker compose `env_file` lädt es automatisch
