---
name: Task - Skill: Paper Download
description: Entwickle einen Claude-Code-Skill für den Download und die Markdown-Extraktion von Referenz-Papers
type: task
status: open
priority: medium
---

## Summary

Einen `/paper-download`-Skill entwickeln, der weiß wo heruntergeladene Papers landen,
wie `extract_markdown.py` aufgerufen wird, und der das Python-Script nicht jedes Mal
neu schreibt — das Script lebt im Repo, der Skill weiß wo es liegt.

## Was der Skill wissen muss

### Pfade
- Download-Verzeichnis: `paper/papers_downloaded/`
- Namensschema für Unterordner: `<erstautor><jahr><kurztitel>/`
  (z. B. `paper/papers_downloaded/masoumi2026mgcrag/`)
- Extraktion-Script: `paper/papers_downloaded/extract_markdown.py`
- Ausgabe-Datei pro Paper: `<ordner>/paper_<name>.md`

### Workflow (vom Skill als Default-Vorgehen kodiert)
1. PDF in den passenden Unterordner ablegen (oder Pfad vom User nehmen)
2. `extract_markdown.py` auf die PDF aufrufen — Script kennen, nicht neu schreiben
3. Ausgabe-Markdown prüfen: Seitenanzahl, ob Abstract + References erkannt wurden
4. Optional: Paper in `memory/related_work.md` als Eintrag ergänzen (Kurzform:
   Titel, Autoren, Jahr, 1-Satz-Differenziator)
5. Bei Bedarf: Zitat-Key für `main.bib` vorschlagen (Format: `<erstautor><jahr><stichwort>`)

### Was der Skill NICHT tut
- Kein Web-Scraping / DOI-Resolver — PDF kommt immer vom User
- Kein automatisches Einfügen in `.tex` — nur `main.bib`-Vorschlag
- `extract_markdown.py` wird nicht verändert, nur aufgerufen

## Subtasks

### T1: extract_markdown.py lesen und verstehen
Script lesen: Welche Parameter? Welches Ausgabeformat? Welche Abhängigkeiten
(pymupdf4llm / docling)? Das Verständnis fließt in den Skill-Prompt.

Datei: `paper/papers_downloaded/extract_markdown.py`

### T2: Skill-Datei schreiben
Datei: `.claude/skills/paper-download.md`

Inhalt:
- Pfad-Konventionen
- Aufruf-Syntax für `extract_markdown.py`
- Qualitäts-Check der Ausgabe
- Optional: `related_work.md`-Update + bib-Key-Vorschlag

### T3: Smoke-Test mit einem vorhandenen Paper
Ein bereits heruntergeladenes PDF (z. B. `masoumi2026mgcrag/`) durch den
Skill-Workflow laufen lassen — prüfen ob der Aufruf korrekt ist und die
Ausgabe sinnvoll ist.

## Acceptance Criteria
- Skill ruft `extract_markdown.py` korrekt auf (kein Neu-Schreiben des Scripts)
- Ausgabe-Qualität wird geprüft (nicht nur Exitcode)
- bib-Key-Vorschlag folgt einheitlichem Schema
- Kein PDF-Download-Code im Skill (nur lokale Verarbeitung)

## Non-Goals
- Kein DOI-Lookup, kein Semantic Scholar API
- Keine automatische `.tex`-Integration

## References
- Script: `paper/papers_downloaded/extract_markdown.py`
- Download-Ordner: `paper/papers_downloaded/`
- Related Work: `memory/related_work.md` (auto-memory)
- Paper-Writing-Skill: [[task_skill_paper_writing]]
