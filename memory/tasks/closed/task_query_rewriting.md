---
name: Task - Query Rewriting (Scoped, Ma et al. 2023)
description: LLM-basierte Query-Expansion mit Synonymen und Domänenbegriffen vor Vector Search nach Rewrite-Retrieve-Read [ma2023rewrite], adaptiert für scoped retrieval
type: task
status: done
priority: high
depends_on: task_reranker_integration
---

## Status

**Nicht gestartet.** Ready – Reranker Integration abgeschlossen (2026-05-13).

## Ziel

Raw User Query durch LLM expandieren mit Synonymen, Domänenbegriffen und alternativen Formulierungen, bevor der Vector Search in Weaviate stattfindet. Ziel: besserer Recall bei domain-spezifischen Queries, die nicht wörtlich im Corpus vorkommen.

**Unterscheidung zu Ma et al.:** Unser Setup filtert bereits per `submodel_id` auf ein spezifisches Dokument. Der Rewrite-Prompt muss aware sein, dass Entity-Namen (Asset, Hersteller, Modell) bereits durch den Filter abgedeckt sind – sonst produziert das Rewrite redundanten Text, der im embedding-space Rauschen erzeugt (viele Erwähnungen von "MiR100" im Header, aber nicht die relevanten specs). Der rewrite entfernt scoped entity references und erweitert stattdessen den content-intent (Fachbegriffe, technische Vokabeln, Synonyme).

## paper reference

**Ma et al. – "Query Rewriting for Retrieval-Augmented Large Language Models" (EMNLP 2023, 818 citations)**

- Rewrite-Retrieve-Read pipeline: LLM rewrites query → retriever search → reader answer
- Unseren Rewrite-Schritt begründet als etabliertes Pattern
- **Unsere Contribution:** Adaptung für scoped retrieval. Ma et al. arbeiten mit "open corpus" – bei uns ist der search scope durch `submodel_id` bereits eingeschränkt. Der rewrite prompt erhält den scope context (Asset-Name, Doc-Language) und strippt redundante Entity-References.
- Paper in `paper/papers_downloaded/ma2023rewrite/` laden:
  - PDF: `ma2023rewrite.pdf` von ACL Anthology (`https://aclanthology.org/2023.emnlp-main.322.pdf`)
  - `metadata.txt`: Title, Authors, Year, Venue, DOI
  - Optional: markdown extraction (`ma2023rewrite.md`) mit docling oder pymupdf4llm
- **BibTeX entry** in `paper/etfa2026/main.bib`:
  ```bibtex
  @inproceedings{ma2023rewrite,
    author = {Ma, Xinbei and Gong, Yeyun and He, Pengcheng and Zhao, Hai and Duan, Nan},
    title = {Query Rewriting in Retrieval-Augmented Large Language Models},
    booktitle = {Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
    year = {2023},
    address = {Singapore},
    month = dec,
    publisher = {Association for Computational Linguistics},
    pages = {5303--5315},
    doi = {10.18653/v1/2023.emnlp-main.322},
    url = {https://aclanthology.org/2023.emnlp-main.322/},
    note = {Open access. Originally arXiv:2305.14283 (2023-05-23)}
  }
  ```
- **Latex update in `paper/etfa2026/content/08-retrieval-pipeline.tex`** (§Planned Retrieval Enhancements):
  - Query Rewriting Eintrag um `\cite{ma2023rewrite}` erweitern:
    ```latex
    (ii) \textbf{LLM-based query rewriting} \cite{ma2023rewrite}, adapted for our scoped retrieval setup: the rewrite prompt is aware that entity names are already covered by the \texttt{submodel\_id} document filter, and thus strips redundant entity references while expanding technical synonyms, domain terminology, and language variants that bridge the gap between worker utterances and manual vocabulary;
    ```
  - Oder alternativ: den ganzen §Planned Retrieval Enhancements absplittern in eigenen §Query Rewriting and Reranking mit eigener Untergliederung (wenn die Implementierung + Bench-B-Zahlen dazukommen).

## Architektur

Neues Modul `mcp-server/src/aas_hybrid_mcp/query_rewriter.py` analog zu `reranker.py`:
- Lazy `httpx.Client`-Singleton
- POST an LLM endpoint (vLLM, `QUERY_REWRITE_URL`) mit domain-spezifischem prompt
- Gibt expanded query string zurück
- Graceful fallback: Fehler → original query unverändert
- Neue Config: `QUERY_REWRITE_MODE` (`on`/`off`), `QUERY_REWRITE_URL`, `QUERY_REWRITE_MODEL`, `QUERY_REWRITE_TIMEOUT`

**Rewrite prompt design:**
- Input: raw query + optional domain context (asset name, doc language if known)
- Wenn `submodel_id` gesetzt: prompt instruiert den LLM, Asset-Entity-References vom query zu strip pen, weil sie bereits durch den filter abgedeckt sind
- Output: expanded query string mit technischen Synonymen und domain terminology
- **Beispiel:**
  - Input: `query="MiR100 max speed", asset="MiR100", doc_lang="en"`
  - Rewrite: `maximum rotational speed performance limit RPM torque specifications`
  - (Kein "MiR100" – submodel filtert schon)
- Wenn `submodel_id` NICHT gesetzt (unscoped search): rewrite expandiert normal, mit Entities

Integration in `weaviate_client.py`:
- `_search_sync` und `_search_templates_sync`: vor `near_vector()` den Query rewrite (wenn `QUERY_REWRITE_MODE=on`)
- Response-Dict erweitert um `query_rewritten: bool`, `rewritten_query: str` (when rewrite ran)

## Subtasks

### T0: Paper laden + Latex/BibTeX

**T0a:** `paper/papers_downloaded/ma2023rewrite/` erstellen:
- PDF runterladen: `https://aclanthology.org/2023.emnlp-main.901.pdf` → `ma2023rewrite.pdf`
- `metadata.txt`:
  ```
  Title: Query Rewriting for Retrieval-Augmented Large Language Models
  Authors: Xinbei Ma, Yeyun Gong, Pengcheng He, Hai Zhao, Nan Duan
  Year: 2023
  Venue: EMNLP 2023
  DOI: 10.18653/v1/2023.emnlp-main.44
  Note: arXiv:2305.14283, ACL Anthology 2023.emnlp-main.44
  ```
- Optional: markdown extraction (`ma2023rewrite.md`) – abstract + intro + methodology section für future reference

**T0b:** `paper/etfa2026/main.bib` — `ma2023rewrite` BibTeX entry hinzufügen (siehe oben)

**T0c:** `paper/etfa2026/content/08-retrieval-pipeline.tex` — §Planned Retrieval Enhancements: Query Rewriting Eintrag mit `\cite{ma2023rewrite}` + scoped adaptation formulieren

**T0d:** `paper/papers_downloaded/ma2023rewrite/` verifizieren:
- PDF exists: `ls paper/papers_downloaded/ma2023rewrite/ma2023rewrite.pdf`
- BibTeX compiles: `pdflatex` test build
- Ref exists: grep `ma2023rewrite` in `.tex` files

### T1: `query_rewriter.py` modul

**File:** `mcp-server/src/aas_hybrid_mcp/query_rewriter.py`
- `rewrite(query: str, *, submodel_id: str | None, asset_name: str | None, doc_language: str | None) -> str`
- Rewrite prompt design:
  - System prompt: Domain terminology expansion für AAS/Industrielle Automatisierung
  - Wenn `asset_name` gesetzt: "The user is searching within the manual for {asset_name}. This asset name is already covered by the document filter. Do NOT include {asset_name} or variants of it in the rewritten query. Instead, focus on the technical intent: expand 'max speed' to 'maximum rotational speed performance limits RPM torque specifications'."
  - Wenn `doc_language` gesetzt: "Match the documentation's language ({doc_language}) in the rewritten query."
  - Raw user phrases → technical vocabulary: "drehzahl" → "rotational speed RPM", "payload" → "payload capacity load limit", "safe to operate" → "operational safety requirements hazard"
- Lazy httpx client (analog zu `reranker.py`), timeout from env
- Exception → original query return (graceful fallback)
- Log: rewritten query, rewrite latency

### T2: `.env` + `.env.vllm` config vars

- `.env`:
  ```
  QUERY_REWRITE_MODE=off
  QUERY_REWRITE_TIMEOUT=5
  ```
- `.env.vllm`:
  ```
  QUERY_REWRITE_MODE=on
  QUERY_REWRITE_URL=http://10.2.10.33:8003/v1
  QUERY_REWRITE_MODEL=qwen36-27b
  ```
- `QUERY_REWRITE_TIMEOUT=5` (seconds) — rewrite darf nicht die Gesamt-Latency dominieren

### T3: `weaviate_client.py:_search_sync` integration

**File:** `mcp-server/src/aas_hybrid_mcp/weaviate_client.py`
- Import `from aas_hybrid_mcp import query_rewriter`
- Vor `near_vector()`: wenn `query_rewriter.QUERY_REWRITE_MODE == "on"`, Query rewrite aufrufen
  - `asset_name` und `doc_language`: NICHT aus weaviate_client selbst ableiten – diese kommen vom Aufrufer. `search()` signature erweitern: `asset_name: str | None = None, doc_language: str | None = None`
  - Im rewrite call: `rewritten = query_rewriter.rewrite(query, submodel_id=submodel_id, asset_name=asset_name, doc_language=doc_language)`
- Response: `query_rewritten: bool`, `rewritten_query: str | None` hinzufügen
- Pipeline: Rewrite → Embedding → Vector Search → Rerank (rewrite vor embedding, kein Konflikt mit reranker)
- Fallback: rewrite error/timeout → original query, `query_rewritten: false`

### T4: `weaviate_client.py:_search_templates_sync` + async wrapper

- Gleiches Pattern wie T3 (aber templates haben kein `submodel_id` filtering, also rewrite ohne scope context)
- `search_templates()` signature: `asset_name` param nicht nötig für templates (anders als documents)
- `tools/template_search.py`: `query_rewritten`, `rewritten_query` an MCP Response durchreichen

### T5: `tools/document_search.py`

- `search_aas_documents` tool signature: `asset_name: str | None = None` hinzufügen (optional)
- Agent übergibt `asset_name` wenn er den Asset-Namen aus dem Graph kennt — der rewrite prompt kann dann wissen, welche Entity gescoped ist
- `query_rewritten`, `rewritten_query` aus `weaviate_client.search()` ins MCP Response
- `tool_descriptions/search_aas_documents.md`: Query Hygiene Sektion um rewrite-Hinweis erweitern

### T6: paper/planungsdoku updaten

- `memory/planned_features.md` — Query Rewriting: "Not implemented" → "Implemented (2026-05-13, based on ma2023rewrite)\n- Scoped adaptation: asset-name stripping when submodel_id is set"
- `memory/future_phases.md` — Phase 9 Query Rewriting: 🟦 Planned → ✅ Done
- `memory/tasks/open/task_query_rewriting.md` — this file, status → done

### T7: `query_rewriter.py` close function + shutdown hook

- `close()` function (analog zu `reranker.close()`) in `mcp-server/src/aas_hybrid_mcp/__init__.py` oder beim server-shutdown aufrufen

## Config

| Variable | Default | vllm | Source |
|---|---|---|---|
| `QUERY_REWRITE_MODE` | `off` | `on` | `.env` → `.env.vllm` |
| `QUERY_REWRITE_URL` | — | `http://10.2.10.33:8003/v1` | `.env.vllm` |
| `QUERY_REWRITE_MODEL` | — | same as `LLM_MODEL` | `.env.vllm` |
| `QUERY_REWRITE_TIMEOUT` | `5` | `5` | `.env` |

## Rewrite prompt design (draft)

```
You are a query rewriting engine for technical documentation search.
Expand the user's query with technical synonyms, domain terminology, and
alternative phrasings that match industrial equipment manuals.

{scope_block}

Focus on technical terms an equipment manual would use. Expand informal
worker phrasing into datasheet vocabulary (e.g. "max speed" → "maximum
rotational speed RPM performance limit torque", "broken" → "malfunction
fault error diagnostic troubleshooting").

Output only the rewritten query, nothing else.
```

`{scope_block}` wenn `asset_name` gesetzt:
```
The user is searching within the manual for {asset_name}. This asset name
is already covered by the document filter. Do NOT include "{asset_name}"
or any variant of it in the rewritten query — the search is already scoped
to this asset's documentation. Focus on the technical intent and vocabulary
expansion instead.
```

wenn `doc_language` gesetzt:
```
The documentation is in {doc_language}. Rewrite the query in {doc_language}.
```

## Acceptance Criteria

- `QUERY_REWRITE_MODE=off` → behavior unverändert, kein LLM call
- `QUERY_REWRITE_MODE=on` → Query wird expandiert, `query_rewritten: true` im Response
- Rewrite LLM endpoint down/error → graceful fallback, original query, `query_rewritten: false`
- Template search + document search beide rewritten query verwenden
- Rewritten query im MCP tool response sichtbar (Debug/Inspection)
- Latency overhead: < `QUERY_REWRITE_TIMEOUT` (5s)
- Works with Reranker: Rewrite → Embedding → Vector Search → Rerank (kein Konflikt)
- **Scoped rewrite:** Wenn `submodel_id` + `asset_name` gesetzt → Asset-Namen nicht im rewritten query enthalten
- **Unscoped rewrite:** Ohne scope → normaler expansion query
- Paper: `ma2023rewrite` in `main.bib`, `\cite{ma2023rewrite}` in `08-retrieval-pipeline.tex`, PDF in `papers_downloaded/`

## References

- Ma et al. (2023): "Query Rewriting for Retrieval-Augmented Large Language Models", EMNLP 2023
- Gao et al. (2022): "Precise Zero-Shot Dense Retrieval without Relevance Labels" (HyDE, `gao2022hyde`)
- Tool description: `mcp-server/src/aas_hybrid_mcp/tool_descriptions/search_aas_documents.md` (Query Hygiene Sektion)
- Analog modul: `mcp-server/src/aas_hybrid_mcp/reranker.py` (Pattern für httpx client)
- Existing weaviate_client: `mcp-server/src/aas_hybrid_mcp/weaviate_client.py`
- paper/etfa2026/content/08-retrieval-pipeline.tex
- paper/etfa2026/main.bib
