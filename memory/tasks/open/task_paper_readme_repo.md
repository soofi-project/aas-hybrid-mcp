---
name: Task - Paper README & GitHub Mirror
description: README für Paper-Zitatfähigkeit ausbauen und GitLab-Repo auf GitHub spiegeln
type: task
status: open
priority: medium
---

## Summary

Wir brauchen eine README, die im Paper direkt referenziert werden kann (Motivation, Architektur, Reproduzierbarkeit, Kontakt) und einen öffentlichen GitHub-Spiegel des aktuellen GitLab-Repos. Ziel: Paper-Leser:innen können die Infrastruktur nachvollziehen und das Repo ohne GitLab-Zugang abrufen.

## Scope

- README im Wurzelverzeichnis (`README.md`)
- Remote-Konfiguration / Dokumentation für GitHub-Mirror
- Begleitende Hinweise in `memory/` falls nötig (keine Änderung an Paper-Dateien selbst)

## Subtasks

### T1: Anforderungen zusammentragen

- Pflicht-Hinweise aus `AGENTS.md`, bestehenden Tasks, `README.md` konsolidieren
- Paper-spezifische Erwartungen (Reproduzierbarkeit, Evaluationsartefakte, Lizenz) herausarbeiten

### T2: README-Struktur definieren und aktualisieren

- Gliederung mit Motivation, Architektur-Überblick, Setup/Runbook, Datenquellen, GitHub-Mirror-Anleitung, Zitierempfehlung erstellen
- Änderungen in `README.md` umsetzen (inkl. Verweise auf relevante Skripte/Tasks)

### T3: GitHub-Mirror vorbereiten

- Anleitung für neues GitHub-Remote (z. B. `github`) dokumentieren
- Hinweise zur Authentifizierung und Push-Strategie aufnehmen (primär `git push --mirror` bzw. ausgewählte Branches)

### T4: Review & Ablage

- README auf Konsistenz mit `AGENTS.md`/Stack-Workflow prüfen
- Task-Status aktualisieren, ggf. Follow-up-Tasks für Automatisierung oder CI notieren

## Acceptance Criteria

- `README.md` enthält alle für das Paper benötigten Informationen (Motivation, Architektur, Reproduzierbarkeit, Kontakt/Zitat, GitHub-Link)
- Abschnitt zur GitHub-Spiegelung erklärt Einrichtung und laufende Pflege (inkl. Hinweis auf Secrets außerhalb des Repos)
- Task-Datei dokumentiert verbleibende Risiken oder offene Fragen
- Keine Inkonsistenzen zwischen README und `AGENTS.md` hinsichtlich Stack-Start/Stop und vLLM-Anforderungen

## Non-Goals

- Kein automatisiertes Mirror-Skript (nur Anleitung)
- Keine Änderung an Paper-Inhalten oder BibTex-Dateien
- Kein CI/CD-Setup für GitHub

## References

- README.md
- AGENTS.md
- memory/index.md
- memory/tasks/open
