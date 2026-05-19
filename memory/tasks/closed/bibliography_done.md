---
name: Bibliography — Audit + Downloads Done
description: 33 Bib-Einträge verifiziert, 32 PDFs heruntergeladen, Korrekturen + Archivierung abgeschlossen
type: task
status: done
---

## Was umgesetzt

Alle 33 `main.bib`-Einträge gegen autoritative Quellen (DOI-Resolver, arXiv, Verlags-Websites) geprüft. 32/33 PDFs in `paper/papers_downloaded/{key}/` mit `metadata.txt`. 1 fehlt hinter IEEE-Paywall.

**Korrekturen an main.bib:**
- `yan2024crag`: `@article` → `@misc` (arXiv-only, kein Peer-Review)
- `gao2022hyde`: Eintrag entfernt — HyDE aus Paper gestrichen
- `docling2024`: Autoren von "Deep Search Team" auf 19 echte Autoren korrigiert, DOI ergänzt
- `soofi_reranker`: Eintrag entfernt — wurde nicht im Paper zitiert

**Neu hinzugefügt:**
- `ma2023rewrite` (EMNLP 2023, ACL Anthology) — für Query Rewriting §08
- `sakurada2025mas_aas_type3` (Future Internet 2025, OA, CC BY 4.0) — zitiert in §03 + §04

**Archivierung:** Unreferenzierte Paper in `paper/papers_downloaded/archived/` verschoben (`autopromptopt/`, `du2023multiagent_debate/`, `semantic_aas_2019/`, `tool_call_emnlp2025/`).

## Paper-Relevanz

- `main.bib` ist bereinigt und verifiziert — keine falschen DOIs, keine erfundenen Venue-Angaben
- Alle im Paper zitierten Einträge haben PDF lokal unter `papers_downloaded/{key}/`
