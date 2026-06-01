---
name: BibTeX Review Done
description: Alle 29 BibTeX-Einträge gegen Crossref/Semantic Scholar geprüft, 4 Fixes angewendet.
type: task
status: done
---

## Summary
Alle 29 BibTeX-Einträge in `paper/etfa2026/main.bib` systematisch durchgehen und mit offiziellen Quellen (Crossref, IEEE Xplore, arXiv, Publisher-Seiten) abgleichen. Nutzer liefert/bestätigt die korrekten Einträge nach und nach.

## Einträge (chronologisch nach Sektion)

### Sektion: AAS and MCP
- [x] `smartfactorykl_aasmcp` — GitHub Repo, @misc — OK, kein DOI
### Sektion: Retrieval-Augmented Generation for AAS
- [x] `shi2025enhancing` — Computers in Industry, 2025 — **Fix:** volume=171, pages=104330 ergänzt
- [x] `shi2024zdm` — J. Manufacturing Systems, 2024 — OK
- [x] `shi2025cdt_rag` — Robotics & CIM, 2026 — **Fix:** volume=97, pages=103105 ergänzt
- [x] `xia2024aasbyllm` — IEEE Access, 2024 — OK
- [x] `basyx_pdf2aas` — GitHub Repo, @misc — OK, kein DOI
### Sektion: Knowledge Graphs / AAS + Neo4j
- [x] `sonnenberg2025aas_kg` — ETFA 2025 — OK
- [x] `ruebel2025agent_comm` — Springer inbook, 2025 — OK
- [x] `garmaev2023submodel_classes` — ETFA 2023 — OK
### Sektion: Agent Safety / Alignment
- [x] `chan2023harms` — FAccT 2023 — OK
- [x] `sclar2024quantifying` — **Fix:** falsche Venue+DOI (war ACL-Fremdpaper) → korrigiert zu ICLR 2024
### Sektion: LLM / Agent Evaluation
- [x] `qwen35` — Blog, @misc, 2026 — OK, kein DOI
- [x] `neo4j2025text2cypher` — HuggingFace dataset, @misc — OK, kein DOI
- [x] `bfcl2024` — ICML 2025 — OK
- [x] `liu2024agentbench` — ICLR 2024 — OK
- [x] `ouyang2024nondeterminism` — **Fix:** Jahr 2024→2025, volume=34, number=2, pages=1--28 ergänzt
### Sektion: IDTA / AAS Standards
- [x] `idta_templates_repo` — GitHub, @misc — OK, kein DOI
- [x] `idta_srn` — IDTA PDF, @misc — OK, kein DOI
- [x] `idta_mi` — IDTA URI, @misc — OK, kein DOI
### Sektion: Regulatory and Safety Standards
- [x] `iec61508` — IEC Standard, @techreport — OK, kein DOI
- [x] `eu_ai_act_2024` — EU Regulation, @misc — OK, kein DOI
### Sektion: Software Tools / SDKs
- [x] `basyx_python_sdk` — GitHub, @misc — OK, kein DOI
- [x] `rwthiat_template2py` — GitHub, @misc — OK, kein DOI
### Sektion: Agent Orchestration
- [x] `yao2022react` — ICLR 2023 — OK
- [x] `wang2023plan_solve` — ACL 2023 — OK
- [x] `yan2024crag` — arXiv, @misc — OK
- [x] `shinn2023reflexion` — NeurIPS 2023 — OK
- [x] `wu2023autogen` — arXiv, @misc — OK
### Sektion: Query Rewriting
- [x] `ma2023rewrite` — EMNLP 2023 — OK
### Sektion: PDF Layout Extraction
- [x] `docling2024` — arXiv, @techreport — OK
- [x] `santos2026pdfrag` — Applied Sciences, 2026 — OK
- [x] `pymupdf4llm_doc` — Docs, @software — OK
### Sektion: Quantization
- [x] `kurtic2025bf16` — ACL 2025 — OK
### Sektion: ImplAAS 2025 Workshop Papers
- [x] `stolze2025aas_events` — ETFA 2025 — OK
- [x] `gneuss2025aas_sdk` — ETFA 2025 — OK
- [x] `aas_test_engines` — GitHub, @misc — OK, kein DOI
- [x] `aas_spec_part2` — IDTA Spec, @misc — OK, kein DOI

## Acceptance Criteria
- Jeder Eintrag mit offizieller Quelle abgeglichen (DOI, Seitenzahlen, Jahresangaben, Autorennamen)
- Fehlende Felder ergänzt (volume, number, pages wo zutreffend)
- Konsistente Groß-/Kleinschreibung in Titeln
- Keine verwaisten Einträge (alle `\cite{}` im .tex gefunden)
- BibTeX kompiliert ohne Warnungen (außer bekannte: pymupdf4llm Eintragstyp, docling Institution)

## References
- Files: `paper/etfa2026/main.bib`
- Verwandte Tasks: `[[task-paper-style-fixes]]`
