---
name: Docling Benchmark Results — Done
description: CPU/GPU Benchmark-Zahlen in §06, Benchmark A2 Tabelle in §10, Santos-Cite, Discussion-Satz zu Ingestion-Kosten.
type: task
status: done
---

## Was umgesetzt

**§06 Architecture** (`06-architecture.tex:18`): Platzhalter ersetzt durch echte Zahlen — "21–193 s CPU, 6–47 s GPU, 3.8× speedup, ±0.3% chunk count". `santos2026pdfrag` als externe Evaluierung zitiert (Docling + hierarchical splitting = 94.1% QA-Accuracy).

**§10 Evaluation — Benchmark A2** (`10-evaluation.tex:26-48`): Neue Tabelle `tab:bench_a2` mit 5 Dokumenten, CPU vs. GPU, N=3 Runs. Setup-Paragraph (Hardware, Docling-Version, Pipeline-Phasen) + Results-Paragraph (Speedup, Chunk-Stabilität).

**§11 Discussion** (`11-discussion.tex:27`): Satz zur Ingestion-Latenz — seltene manuelle Updates + Content-Hash-Dedup machen die Ingestion zu einem einmaligen Cost.

**BibTeX** (`main.bib:331-341`): Eintrag `santos2026pdfrag` (Applied Sciences 16(10):5069, DOI 10.3390/app16105069).

**Reverted**: Santos-Cite aus §04 Related Work entfernt (wieder in §06 Architecture) — es ist eine Evaluierungsstudie, kein konkurrierendes System.

## Nicht umgesetzt

- T3 (Hybrid-Parser-Routing als Future Work): bewusst weggelassen — würde den 8-Seiten-Limit weiter belasten und ist nicht evaluiert.
- Benchmark A1 (Neo4j Ingestion): weiterhin Platzhalter, wartet auf echte Zahlen.
