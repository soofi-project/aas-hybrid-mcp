---
name: Task - Skill: Task Workflow
description: Entwickle einen Claude-Code-Skill der das Anlegen, Lesen und Abschließen von Tasks im memory/tasks/-System kodiert
type: task
status: open
priority: medium
---

## Summary

Ein `/task`-Skill der den Pfad, das Namensschema und das Frontmatter-Template für
das projekteigene Task-System trägt — damit neue Tasks ohne Erklärung korrekt
angelegt werden und kein Format-Prompting nötig ist.

## Was der Skill wissen muss

### Pfade + Namensschema
- Offene Tasks: `memory/tasks/open/task_<kurzname>.md`
- Abgeschlossene Tasks: `memory/tasks/done/task_<kurzname>.md` (falls vorhanden)
- Namensschema: snake_case, sprechend, kein Datum im Namen

### Frontmatter-Template
```yaml
---
name: Task - <Titel>
description: <1-Satz-Zusammenfassung — wird vom Index gelesen>
type: task
status: open   # open | in-progress | done
priority: high | medium | low
---
```

### Aufbau-Konvention (Subtasks, Acceptance Criteria, Non-Goals)
- `## Summary` — Warum existiert dieser Task?
- `## Subtasks` — `### T1:`, `### T2:` usw., mit konkreter Ausgabe pro Subtask
- `## Acceptance Criteria` — messbar, kein "looks good"
- `## Non-Goals` — was explizit ausgeschlossen ist
- `## References` — Dateipfade + `[[task_<name>]]`-Links zu verwandten Tasks

### Was der Skill NICHT tut
- Kein automatisches Eintragen in `memory/index.md` — Tasks haben eigene Struktur
- Kein Status-Tracking über Git (kein Commit pro Status-Wechsel)
- Tasks werden beim Abschließen nach `memory/tasks/done/` verschoben, nicht gelöscht

## Subtasks

### T1: Skill-Datei schreiben
Datei: `.claude/skills/task.md`

Inhalt:
- Kontext-Block (Pfade, Namensschema, Frontmatter)
- Aufbau-Konvention als Template
- Kurzanweisung: bei "Task anlegen" immer Pfad + Frontmatter korrekt setzen,
  bei "Task abschließen" nach `done/` verschieben

### T2: Smoke-Test
Skill aufrufen mit "Leg einen Task für X an" — prüfen ob Pfad, Name und Frontmatter
ohne Korrektur stimmen.

## Acceptance Criteria
- Neue Tasks landen ohne Korrektur im richtigen Pfad mit korrektem Frontmatter
- Namensschema (snake_case, kein Datum) wird eingehalten
- "Abschließen" bedeutet Verschieben, nicht Löschen

## Non-Goals
- Kein Task-Board / Kanban-Visualisierung
- Kein automatischer Git-Commit bei Status-Wechsel

## References
- Bestehende Tasks als Format-Referenz: `memory/tasks/open/task_paper_style_review.md`
- Paper-Writing-Skill: [[task_skill_paper_writing]]
- Paper-Download-Skill: [[task_skill_paper_download]]
