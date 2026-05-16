---
name: Task - ImplAAS 2025 Citations + Bib Sweep (ETFA 2026)
description: Add missing ImplAAS-2025 papers to main.bib + papers_downloaded/, then walk through every existing BibTeX entry step by step for hygiene & relevance
type: task
status: open
priority: high
---

## Summary

Audit der `main.bib` für die ETFA-2026-ImplAAS-Einreichung. Zwei Stoßrichtungen:

1. **Pflicht-/strategische Zitate aus ImplAAS-2025 nachziehen** — von 15 Workshop-Papers
   ist aktuell nur 1 (das eigene `sonnenberg2025aas_kg`) im Bib. Mehrere sind thematisch
   direkt anschlussfähig + Organisatoren/DFKI-Kollegen sind dort Autoren.
2. **Schritt-für-Schritt-Review aller bestehenden Bib-Einträge** — Hygiene, Vollständigkeit,
   Venue-Korrektheit, Page-Ranges, Workshop-Flags, ob jeder Eintrag im Paper tatsächlich
   verwendet wird.

## Scope

- `paper/etfa2026/main.bib`
- `paper/papers_downloaded/<bibkey>/` (PDF + Markdown-Extract via `extract_markdown.py`)

## Subtasks

### T1: ImplAAS-2025 Pflicht-Zitate hinzufügen

Priorität-Reihenfolge (nach Reviewer-Risiko bei Weglassung):

1. **[PFLICHT] Büttner et al. 2025** — *"Bridging the Qualification Gap for the AAS: A Modular
   and Role-Based Learning Framework"*
   - Autoren: Büttner, Schöttke, Knoch, Bayha, Ocando Röhricht, Schäfer, **Porta**, Schwartz, Zielstorff
   - ETFA25-000345
   - Grund: DFKI-Cognitive-Assistants-Kollegen (Porta = ImplAAS-2026-Organisator)
   - Wo zitieren: §Introduction (DFKI-Kontext) oder §Related Work (AAS-Practical-Adoption)

2. **[PFLICHT] Stolze et al. 2025** — *"Towards an AAS Event Mechanism: A proposal to extend
   the AAS specification"*
   - Autoren: Stolze, Ritz, Belyaev, Fischer, Kosel, Ungarala
   - ETFA25-000321
   - Grund: Direkter Anker zu unserem Event-Driven Neo4j-Plugin (Kafka-Sync)
   - Wo zitieren: §Architecture (Ingestion-Plugin) oder §Related Work

3. **[PFLICHT] Ein Miny-Paper** — Miny ist 2026 ImplAAS-Organisator + 3× Co-Author in 2025
   - **Option A:** Farkas, Guo, Mboudia, Garmaev, Miny, Kleinert — *"Toward Low-Code Industrial
     Data Integration through AAS-Based Flow Generation in Node-RED"* (ETFA25-000284)
     → Kontrastiert mit unserem Agent-Ansatz (low-code vs. agentic)
   - **Option B:** Otto, Miny, Garmaev, Ristin, Heppner, Braunisch, Kleinert, van de Venn,
     Wollschlaeger — *"Semantic Comparison of AAS"* (ETFA25-000264)
     → IDTA-Submodel-nähere Welt
   - Entscheidung: A präferiert (kontrastiver Mehrwert), B als Fallback
   - Wo zitieren: §Related Work

### T2: ImplAAS-2025 strategische Zitate

4. **[STRATEGISCH] Gneuss, Ristin, Braunisch, van de Venn, Wollschlaeger 2025** — *"Combining
   Publicly Available SDKs and Code Generation Tools to Streamline the Implementation of AAS
   Applications"*
   - ETFA25-000278
   - Grund: behandeln SDK+Code-Gen für AAS-Apps, wir nutzen basyx-python-sdk
   - Wo zitieren: §Implementation oder §Discussion

5. **[OPTIONAL] Vaz et al. 2025** — *"Automated Configuration of BaSyx DataBridge using
   Standardized AAS Interface Modelling"*
   - ETFA25-000018
   - Nur falls Platz / falls Data-Integration-Diskussion ausgebaut wird

### T3: Externes Comparison-Paper prüfen

- **"Comparison of Data Integration Concepts for Asset Administration Shell"** — vergleicht
  basyx-python-sdk vs. DataBridge vs. AID/AIMC anhand 12 Kriterien.
  - Autor/Venue/Jahr noch nicht eindeutig identifiziert — User liefert Link nach
  - Falls peer-reviewed: aufnehmen als Anker für „why we use basyx-python-sdk"
  - Wo zitieren: §Implementation (SDK-Wahl rechtfertigen)

### T4: Schritt-für-Schritt-Review aller bestehenden Bib-Einträge

Pro Eintrag in `main.bib` durchgehen (aktuell ~30 Einträge):

Pro Eintrag prüfen:
- **Wird im Paper tatsächlich `\cite{}`-t?** (`grep` über `content/*.tex`)
  → Wenn nein: streichen oder begründen warum behalten
- **Venue-Feld korrekt + peer-reviewed?**
  → arXiv-only Quellen mit `note={arXiv preprint}` markieren
  → Workshop-Paper mit `note={Workshop paper at <Venue>}` markieren
- **Pflichtfelder vollständig?** (author, title, year, venue, pages/volume)
  → Insb. Page-Ranges bei Journal-/Conference-Einträgen ergänzen
- **DOI vorhanden + korrekt?** (Crossref-Check)
- **BibKey-Konvention konsistent?** (`<firstauthor><year><slug>`)
- **Duplikate erkennen** (gleicher DOI in mehreren Einträgen)

Ausgabe: pro Eintrag in dieser Task-Datei abhaken (✅ / 🔧 fix needed / ❌ remove).

### T5: Procedure pro neu aufzunehmendem Paper

1. DOI / IEEE-Xplore-Link sammeln (User liefert; Claude kann nicht hinter Paywall)
2. PDF herunterladen → `paper/papers_downloaded/<bibkey>/<bibkey>.pdf`
3. `python .claude/skills/paper-download/extract_markdown.py <bibkey>` ausführen
4. BibTeX-Eintrag in `main.bib` einfügen (Sektion entsprechend dem Thema)
5. In dieser Task-Datei abhaken + notieren wo im Paper zitiert wird

## Acceptance Criteria

- Alle 3 Pflicht-Zitate (T1) sind in `main.bib` + im Paper an passender Stelle eingebaut
- Mindestens 1 strategisches Zitat aus T2 ist eingebaut
- T3-Comparison-Paper-Status: entweder integriert oder begründet abgelehnt
- T4-Sweep abgeschlossen: jeder existierende Eintrag hat ✅ / 🔧 / ❌ Status
- Keine `🔧 fix needed`-Einträge mehr offen
- Keine ungenutzten Einträge (alle werden in `content/*.tex` mit `\cite{}` referenziert
  oder sind explizit begründet als „reserviert für §Future Work")

## Non-Goals

- **Keine Claim-Belegbarkeit** — das ist `task_paper_claim_audit.md`
- **Keine Stilfragen / Reviewer-Antizipation** — separate Tasks
- **Keine PDF-Beschaffung durch Claude** — User liefert PDFs in `papers_downloaded/`,
  Claude macht den Bib-Eintrag + Mapping

## References

- Bibliography: `paper/etfa2026/main.bib`
- PDF-Sammelordner: `paper/papers_downloaded/`
- Markdown-Extraktion: `paper/papers_downloaded/extract_markdown.py`
- ImplAAS-2025-Sessions: WS01.9-1 bis WS01.9-4 (15 Papers total, ETFA25-000018 bis -000424)
- Workshop-CFP-Themen 2026: AI/ML supported by AAS, Data Provision/Integration, Continuous
  Engineering, Data Sovereignty, Inter-AAS Communication
- Verwandte Tasks:
  - `task_paper_claim_audit.md` (Claim-Belegbarkeit)
  - `task_paper_style_review.md` (Stil)
  - `task_paper_write_validation_defense.md`
  - `task_paper_future_work_template_cypher.md`
