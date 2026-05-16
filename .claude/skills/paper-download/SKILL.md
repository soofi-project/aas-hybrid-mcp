---
name: paper-download
description: Neues Paper-PDF in `paper/papers_downloaded/` ablegen und via `extract_markdown.py` in chunked Markdown konvertieren. Kodiert Verzeichnis-Naming, Aufruf-Syntax, Qualitäts-Check, bib-Key-Vorschlag und optionalen `related_work.md`-Eintrag. Aufrufen wenn ein Paper neu in den Recherche-Pool soll.
---

# Paper-Download-Workflow

PDFs unter `paper/papers_downloaded/` werden per `extract_markdown.py` in Markdown
umgewandelt, damit Claude sie ohne PDF-Tooling lesen kann. Das Script existiert
schon — nicht neu schreiben, sondern korrekt aufrufen.

## Verzeichnisstruktur

**Script-Lokation:** `.claude/skills/paper-download/extract_markdown.py` (bundled mit dem Skill — Layered Determinism für Skill-Design: das Tool wird nicht prompt-level beschrieben, sondern liegt direkt im Skill-Folder).

**Daten-Lokation:**

```
paper/papers_downloaded/
├── archived/                        # alte/aussortierte Papers (skip im Bulk)
├── yao2022react/
│   ├── paper.pdf
│   └── paper.md                     # gleicher Stem wie PDF
├── shinn2023reflexion/
│   └── ...
└── ...
```

**Naming-Convention** (genau einhalten — wird als Bib-Key-Stem und für Querverweise genutzt):

```
<lastname><year><shortid>/
```

- `lastname`: Erstautor, lowercase, ohne Sonderzeichen (`schäfer` → `schaefer`).
- `year`: 4-stellig.
- `shortid`: 1–3 Wörter, lowercase, `_` als Trenner bei Multi-Word (`plan_solve`, `self_refine`).

Beispiele aus dem Repo: `yao2022react/`, `ma2023rewrite/`, `wang2023plan_solve/`, `masoumi2026mgcrag/`, `xia2025cdt_rag/`.

## Workflow

### 1. Verzeichnis anlegen + PDF reinkopieren

```
paper/papers_downloaded/<lastname><year><shortid>/<filename>.pdf
```

Filename egal — Stem wird zum `.md`-Stem. Sinnvoll: `paper.pdf` oder Original-Filename behalten.

### 2. Extraktion ausführen (single-PDF-Modus bevorzugt)

```bash
python .claude/skills/paper-download/extract_markdown.py paper/papers_downloaded/<dir>/<file>.pdf
```

Output: `<file>.md` daneben (gleicher Stem). Wenn das PDF Standard-IEEE-Layout hat,
greift der Page-Marker-Pfad (saubere `### Page N`-Sektionen). Sonst Fallback auf
PyMuPDF per-page mit Warnung auf stderr — Output ist nutzbar, aber Layout-Heuristiken
können Spalten/Equations verzerren.

**Bulk-Modus** (`python extract_markdown.py` ohne Argumente) nur nutzen wenn mehrere
Papers gleichzeitig neu sind — verarbeitet alle Subdirs mit PDF aber ohne `.md`.

### 3. Qualitäts-Check (Pflicht)

Nach Extraktion das `.md` öffnen und prüfen:

- **Titel-Header** (`# Titel`) erkannt und sinnvoll? Bei Konferenz-Footern landet manchmal
  „IEEE Conference 2024" als Titel — dann manuell fixen.
- **Abstract** als Sektion erkennbar (early in doc).
- **References-Block** am Ende erkennbar (`## References` o. ä.).
- **Page-Count** plausibel? `### Page N`-Sektionen sollten der PDF-Seitenzahl entsprechen.
- **stderr-Warnung** `No page markers found, using PyMuPDF per-page fallback` ist Hinweis
  auf Conference-Footer-Layout — meist OK, aber Tabellen/Formeln prüfen.

Wenn Qualität schlecht ist (verlorene Sections, zerrissene Absätze): kein Re-Run
mit anderen Flags — das Script hat nur die zwei Pfade. Stattdessen für dieses Paper
manuell als Markdown nacharbeiten oder als bekannte Limitation in `related_work.md`
notieren.

### 4. Bib-Key vorschlagen

Format für `main.bib`:

```
<lastname><year><shortid>
```

**Ohne** Underscore zwischen den drei Teilen, aber `shortid` selbst kann Underscore haben
(historische Inkonsistenz im Repo — bei neuen Keys lieber ein Wort).

Beispiele: `yao2022react`, `ma2023rewrite`, `shinn2023reflexion`, `yan2024crag`,
`wang2023plan_solve` (Underscore-Variante existiert).

Vor dem Hinzufügen **immer** in `paper/etfa2026/main.bib` greppen ob Key oder
ähnliche Variante schon existiert — Duplikat-Keys sind ein bekannter BibTeX-Footgun.

### 5. Optional: `related_work.md`-Update

Wenn das Paper für die ETFA-Paper-Argumentation relevant ist:
`~/.claude/projects/C--repo-soofi-aas-hybrid-mcp/memory/related_work.md` öffnen
und einen Bullet im passenden Theme-Cluster ergänzen — 1–2 Sätze, Bib-Key in Backticks,
„Our Differentiator"-Linie nicht aufweichen.

Nicht jedes Paper muss da rein — nur was als Cite kandidaten-fähig ist. Reine
Recherche-Reads (Background-Lesematerial) bleiben unsortiert in `papers_downloaded/`.

## Anti-Patterns

- ❌ PDF unter `paper/papers_downloaded/` ohne Subdir ablegen — Bulk-Modus übersieht das.
- ❌ Markdown manuell neu schreiben statt `extract_markdown.py` aufrufen.
- ❌ Bib-Key raten ohne `main.bib`-grep (Duplikate sind BibTeX-Footgun).
- ❌ Verzeichnis mit Camelcase oder Bindestrichen (`YaoReAct2022/`, `yao-react-2022/`) —
  das Repo nutzt durchgängig lowercase + Underscores für shortid.
- ❌ PDF mit Spaces oder Umlauten im Filename — Shell-Quoting wird unnötig fragil.
- ❌ Auto-Update von `related_work.md` für jedes Background-Paper — Datei soll fokussiert
  auf Cite-Kandidaten bleiben.

## Vorlage prüfen

Format-Referenz bei Zweifeln: `paper/papers_downloaded/yao2022react/` (Standard-IEEE-Paper,
saubere Marker-Extraction) oder `paper/papers_downloaded/yan2024crag/` (gut formatiertes
Beispiel mit Abstract/References-Struktur).
