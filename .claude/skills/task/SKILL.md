---
name: task
description: Anlegen und Abschließen von Tasks unter `memory/tasks/` im aas-hybrid-mcp-Repo. Erzwingt Pfad, Snake-Case-Namensschema, Frontmatter-Template und Workflow (open → closed mit `_done`-Suffix). Aufrufen wenn neuer Task entstehen soll oder bestehender abgeschlossen wird.
---

# Task-Workflow (aas-hybrid-mcp)

Du verwaltest Tasks unter `memory/tasks/` als Markdown-Dateien mit YAML-Frontmatter. Dieser Skill kodiert die Konventionen aus dem Repo.

## Verzeichnisstruktur

```
memory/tasks/
├── open/        # aktive Tasks: task_<name>.md
└── closed/      # erledigte Tasks: <name>_done.md
```

## Neuen Task anlegen

1. **Dateiname:** `memory/tasks/open/task_<snake_case_name>.md`
   - Snake_case, prägnant (z. B. `task_crag_diagnosis.md`, `task_paper_style_review.md`).
   - Präfix `task_` ist Pflicht in `open/`.

2. **Frontmatter (verpflichtend):**
   ```yaml
   ---
   name: Task – <Kurztitel>
   description: <Ein-Satz-Zweck, max ~140 Zeichen — erscheint in Listings>
   type: task
   status: open
   priority: low | medium | high
   ---
   ```

3. **Body-Struktur (Konvention, nicht starr):**
   ```markdown
   ## Summary | Background
   <Kontext, Problemstellung, ggf. Trace/Daten-Pfade>

   ## Subtasks
   ### T1 — <Titel>
   <Was, wo, Files>

   ### T2 — <Titel>
   ...

   ## Acceptance Criteria
   - <prüfbare Bedingung 1>
   - <prüfbare Bedingung 2>

   ## References
   - Files: `pfad/zur/datei.py`
   - Verwandte Tasks: `[[task-other-task-name]]`
   ```

   Subtasks-Status inline (`**Status:** ✅ Done (YYYY-MM-DD)`) wenn Teile schon
   abgearbeitet sind — siehe `task_prompt_quality.md` als Vorlage.

4. **Verwandte Tasks** mit `[[wiki-link]]`-Syntax markieren (Bindestriche statt
   Underscores im Link, ohne `.md`).

## Task abschließen

1. **Verschieben + umbenennen**: `memory/tasks/open/task_<name>.md` → `memory/tasks/closed/<name>_done.md`
   - `task_`-Präfix entfernen, `_done`-Suffix anhängen.
   - Beispiel: `task_retrieval_enhancements.md` → `retrieval_enhancements_done.md`.

2. **Frontmatter aktualisieren:**
   ```yaml
   ---
   name: <Topic> Done
   description: <Was wurde umgesetzt — knapp>
   type: task
   status: done
   ---
   ```
   `priority` entfernen.

3. **Body umschreiben** zu „Was umgesetzt"-Stil (siehe `retrieval_enhancements_done.md`,
   `agent_cleanup_done.md` als Vorlagen): Bullets oder fett-markierte Themen,
   jeweils 1–3 Sätze. Ergebnisse stehen im Vordergrund, nicht der Plan.

4. **NICHT löschen, NICHT zusammenfassen** — closed-Tasks sind die Historie.

## Anti-Patterns

- ❌ Task ohne `priority` in `open/` anlegen.
- ❌ Closed-Task mit `task_`-Präfix lassen.
- ❌ Closed-Task löschen oder in MEMORY.md inline zusammenfassen.
- ❌ Frontmatter-Felder `name` und `description` weglassen — sie sind die ToC-Quelle.
- ❌ Tasks außerhalb `memory/tasks/` ablegen.

## Index-Pflege

`memory/index.md` listet Tasks nicht explizit — die Ordnerstruktur ist self-documenting.
Kein Eintrag dort nötig beim Anlegen/Abschließen.

## Vorlagen im Repo

- Detaillierter Task mit Subtasks + Acceptance: `memory/tasks/open/task_crag_diagnosis.md`
- Task mit inline-erledigten Subtasks: `memory/tasks/open/task_prompt_quality.md`
- Closed-Format „Was umgesetzt": `memory/tasks/closed/retrieval_enhancements_done.md`
