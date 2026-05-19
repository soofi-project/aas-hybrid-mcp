---
name: Task – Retreat: Skills-Story + Quellen-Lese-Disziplin
description: Skills/Layered-Determinism in Retreat-Vortrag aufnehmen, plus „Extrakt ist kein Ersatz fürs Lesen"-Regel als Skill-Anti-Pattern + Feedback-Memory verankern
type: task
status: open
priority: medium
---

## Background

Beim Skill-Bau (siehe `memory/tasks/closed/skills_create_done.md`) sind zwei Erkenntnisse entstanden, die ins SOOFI-Retreat gehören:

1. **Skills-Architektur als angewandte Layered-Determinism-These** — der ETFA-Paper-Kern („Prompts sind Hinweise, Validatoren sind Garantien") wurde rekursiv auf die eigene Tooling-Schicht angewandt: Skills tragen jetzt ihr Tool (`extract_markdown.py`, `build_paper.py`, `search_openalex.py`), nicht nur Prompt-Anweisungen. Das ist ein methodisch interessanter Punkt fürs Retreat, weil er die These nicht nur am Beispiel des MCP-Stacks, sondern auch am eigenen Arbeitsprozess vorführt.

2. **Extrakt-Workflow-Falle** — die `extract_markdown.py`-Pipeline produziert chunked Markdown, mit dem die KI sinnvoll über ein Paper sprechen kann. *Aber*: wenn der menschliche Autor das Original-PDF nicht selbst gelesen hat, treffen zwei Fehlerquellen aufeinander:
   - KI-Hallu/Konfabulation (Modell „füllt Lücken" plausibel statt korrekt)
   - eigene Unwissenheit des Schreibers (kann den KI-Vorschlag nicht prüfen)
   Resultat: Claims im Paper, die die referenzierte Arbeit gar nicht so aussagt. Verstärkt durch die KI-„Helpfulness-Bias" — sie *will* hilfreich sein und produziert lieber eine Antwort als ein „weiß ich nicht".

Beide Punkte sind retreat-tauglich (methodisch, nicht delivery-prahlerisch — siehe `feedback_retreat_political_framing.md`) und ergänzen die existierenden Retreat-Tasks 13 (Paper-Writing Ethics), 17 (Paper-Writing-as-SE) und 7 (Multi-Tool Reality).

## Subtasks

### T1 — Retreat-Slides: Skills/Layered-Determinism-Story einarbeiten
**Wo:** `C:\repo\soofi\soofi-trainer\retreat\` — natürlicher Anker `task_17_paper_writing_as_software_engineering.md` (vermutlich auch `task_16_stateless_agentic_workflow.md`).

**Was:**
- Ein Slide oder Block: „Skills carry their tool" — als rekursive Anwendung der Layered-Determinism-These auf die Arbeitsweise selbst. Beispiel: `/paper-download` enthält `extract_markdown.py`, nicht nur die Anleitung „rufe es auf".
- Konkrete Beispiele aus dem Repo (4 Skills, 3 bundled Tools, Docker-Digest-Pin).
- Frame: „Vibe Coding → Agentic Engineering" (existiert bereits in der Feedback-Memory).
- Keine Cost-Numbers, kein „selbst bezahlt" (siehe `feedback_retreat_cost_framing.md`).

**Output:** PDF/PPTX-Update in `soofi-trainer/retreat/`, vermutlich 1–2 zusätzliche Slides plus Anpassung an Vortragsskript (`task_15_vortrag_skript.md`).

### T2 — Quellen-Lese-Disziplin als Anti-Pattern verankern
**Hier im aas-hybrid-mcp-Repo:**

- **`/paper-download` SKILL.md** — Anti-Patterns-Sektion ergänzen:
  > ❌ Extrahiertes Markdown an Stelle des Original-PDFs lesen, wenn ein Claim aus dem Paper im eigenen Text landen soll. Markdown ist Discovery-/Navigations-Hilfe, kein Beleg. Vor jedem konkreten Cite: PDF aufmachen, Stelle nachlesen, *dann* zitieren. Begründung: PyMuPDF-Fallback verliert Tabellen/Strukturen; KI füllt Lücken plausibel statt korrekt; Hallu × Schreiber-Unwissenheit = Claim, den die Quelle nicht hergibt.

- **`/paper` SKILL.md** — Querverweis im Claim-Audit-Block: „Bevor ein Cite belegtest wird, muss der menschliche Autor die zitierte Stelle im PDF selbst gesehen haben."

- **Feedback-Memory** — bereits gespeichert in `feedback_source_reading_discipline.md` (auto-memory dir).

### T3 — Retreat-Probevortrag-Check
**Wo:** `task_11_probevortrag.md` im Retreat-Repo. Nach T1: einmal durchgehen ob die Skills-Story in den existierenden Flow passt oder einen eigenen Übergang braucht. Risiko: zu viel Tooling-Innenleben für die Zielgruppe — siehe `task_08_audience_inclusivity.md`.

## Acceptance Criteria

- Retreat-Slides enthalten mindestens einen Block zur Skills/Layered-Determinism-Rekursion mit konkreten Repo-Beispielen
- Vortragsskript-Update reflektiert den neuen Slide
- `/paper-download` und `/paper` SKILL.md tragen das Source-Reading-Anti-Pattern explizit
- Probevortrag-Durchlauf bestätigt: Story passt in 8-Minuten-Slot, keine reine Tool-Schau

## References

- Closed-Task: `memory/tasks/closed/skills_create_done.md`
- Retreat-Anker: `C:\repo\soofi\soofi-trainer\retreat\task_17_paper_writing_as_software_engineering.md`, `task_13_paper_writing_ethics_framing.md`, `task_16_stateless_agentic_workflow.md`, `task_07_multi_tool_reality.md`, `task_15_vortrag_skript.md`, `task_11_probevortrag.md`
- Skill-Files: `.claude/skills/paper-download/SKILL.md`, `.claude/skills/paper/SKILL.md`
- Feedback-Memory: `feedback_source_reading_discipline.md` (auto-memory)
- Verwandte Constraints: `feedback_retreat_cost_framing.md`, `feedback_retreat_political_framing.md`, `feedback_review_and_test_discipline.md`, `feedback_agent_constraint_philosophy.md`
- Verwandte Tasks: `[[task-paper-layered-determinism-thesis]]`, `[[task-paper-style-review]]`
