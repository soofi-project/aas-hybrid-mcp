---
name: Task - Skill: Paper Writing
description: Entwickle einen Claude-Code-Skill für das Schreiben und Bauen des ETFA-2026-Papers — kodiert Build-Prozess, Paper-Constraints und Eskalationsregel
type: task
status: open
priority: high
---

## Summary

Einen wiederverwendbaren `/paper`-Skill entwickeln, der bei jeder Paper-Session den
Kontext nicht neu erklärt bekommt, sondern ihn aus dem Skill trägt. Ziel: weniger
Korrektur-Prompting, konsistenteres Vorgehen beim Schreiben.

## Was der Skill wissen muss

### Pfade
- Paper-Root: `c:\repo\soofi\aas-hybrid-mcp\paper\etfa2026\`
- Haupt-TeX: `paper/etfa2026/conference_etfa_2026.tex`
- Content-Sections: `paper/etfa2026/content/*.tex`
- Build-Compose: `paper/etfa2026/docker-compose.yml`
- Bibliographie: `paper/etfa2026/main.bib`
- Heruntergeladene Papers: `paper/papers_downloaded/`

### Build-Prozess
LaTeX wird via Docker gebaut (nicht WSL-lokal, `texlive-full` noch nicht installiert).
Befehl: `docker compose -f paper/etfa2026/docker-compose.yml up --build`
Ausgabe auswerten: LaTeX-Warnings + Errors aus dem Container-Log, nicht
nur Exit-Code prüfen.

### Paper-Constraints (hartcodiert im Skill)
- **8 Seiten** IEEE-Format (ImplAAS-Workshop @ ETFA 2026)
- Thesis: **Layered Determinism** — MCP-Validator als deterministischer Guard
  über nicht-deterministischen LLM-Output
- Benchmark-Scope: Bench A (retrieval ablation), Bench B (containment), Bench C (write-path, deferred)
- Eval-Modell: Qwen3.6-27B-FP8 (lokal auf H200) — kein Cloud-LLM
- Data-Sovereignty-Framing: selbst-hostbar, EU/AI-Act-konform
- SOOFI 120B als Future-Work / Plug-in-Ersatz (nicht als aktuelles Eval-Modell!)

### Eskalationsregel (zwingend)
- **Kleine Änderungen** (Formulierung, Zahl, Zitat, Satz umstellen): direkt machen
- **Mittlere Änderungen** (Paragraph neu schreiben, Claim anpassen): kurz ankündigen, dann machen
- **Große Umbauten** (Section-Struktur ändern, Benchmark-Darstellung verschieben,
  Thesis-Formulierung überarbeiten): **erst fragen, dann warten** — nie einfach umbauen

## Subtasks

### T1: Skill-Datei schreiben
Datei: `.claude/skills/paper.md` (oder wo Skills im Projekt liegen)

Inhalt des Skills:
- Kontext-Block (Pfade, Constraints, Eskalationsregel)
- Build-Anweisung inkl. Log-Analyse
- Anweisung: Style-Review nach größeren Edits via [[task_paper_style_review]]
- Anweisung: Claim-Audit-Referenz via [[task_paper_claim_audit]]

### T2: Build-Test
Skill einmal durchlaufen mit minimalem Edit → Build → Log auswerten.
Sicherstellen dass der Skill den docker-compose-Befehl korrekt ausführt
und LaTeX-Fehler erkennt.

### T3: Eskalationsregel testen
Dem Skill einen "großen Umbau" hinwerfen und prüfen ob er nachfragt statt
direkt zu schreiben.

## Acceptance Criteria
- Skill läuft ohne Paper-Kontext erneut zu erklären
- Build-Ausgabe wird inhaltlich ausgewertet (nicht nur Exit-Code)
- Eskalationsregel greift bei Struktur-Änderungen nachweislich
- Skill referenziert Style-Review und Claim-Audit als Folge-Steps

## Non-Goals
- Kein automatischer Commit nach Paper-Edit (manuell bleiben)
- Kein vollautomatischer Review-Loop — Reviewer-Perspektive bleibt manueller Step

## References
- Build: `paper/etfa2026/docker-compose.yml`
- Style-Review: [[task_paper_style_review]]
- Claim-Audit: [[task_paper_claim_audit]]
- Download-Skill: [[task_skill_paper_download]]
