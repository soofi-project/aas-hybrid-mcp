---
name: Task - ReWOO Variant entfernen
description: ReWOO Agent-Variante komplett aus Code, Paper, Doku und Tasks entfernen (performt schlecht, Ansatz passt nicht)
type: task
status: done
priority: medium
depends_on: []
---

## Status

Erledigt (2026-05-14). Alle Code-Dateien, API-Routing, `.env`, Paper, Doku und Task-Referenzen bereinigt.

## Ziel

ReWOO-Variante sauber entfernen — Code, API-Routing, Paper-Text, BibTeX, Doku und alle task-Dateien, die ReWOO noch als aktive Variante referenzieren.

## Subtasks

### T0: Core ReWOO-Dateien löschen

- `aas-agent/src/aas_agent/rewoo.py`
- `aas-agent/src/aas_agent/rewoo_graph.py`
- `aas-agent/src/aas_agent/rewoo_nodes.py`
- `aas-agent/src/aas_agent/rewoo_state.py`
- `memory/rewoo_paper.md`
- `paper/papers_downloaded/xu2024rewoo/` (PDF + rewoo.md + metadata.txt)

### T1: `api.py` bereinigen

- `aas-agent/src/aas_agent/api.py`:
  - `_MODEL_INFO` — `aas-agent:rewoo` Eintrag entfernen
  - `_resolve_runner_class` — `elif variant == "rewoo"` Block entfernen

### T2: `.env` bereinigen

- `REWOO_MAX_THOUGHTS=10` entfernen
- `REWOO_PARALLEL_BATCH=5` entfernen

### T3: Paper — Architektur-Text anpassen

- `paper/etfa2026/content/06-architecture.tex`:
  - ReWOO-Eintrag aus der Agent-Variant-Liste entfernen
  - Falls der Absatz danach kahl aussieht, ggf. den verbleibenden Text für die anderen Varianten entsprechend anpassen
- `paper/etfa2026/main.bib`:
  - `@misc{xu2024rewoo,}` entry entfernen
- Build prüfen: `pdflatex` ohne "citation undefined" oder "bibitem removed" warnings

### T4: Dokumentationen bereinigen

- `memory/agent_variants.md` — alle rewoo-Sektionen entfernen (Routing-Tabelle, env vars, "rewoo only" Section, paper mapping)
- `memory/index.md` — `rewoo_paper.md` Eintrag aus der Tabelle entfernen

### T5: Open Tasks — rewoo Erwähnungen bereinigen

Alle Tasks in `memory/tasks/open/` durchsuchen und rewoo-Referenzen entfernen:
- `task_agent_test_framework.md` — `rewoo` aus variants-Listen entfernen
- `task_token_usage_tracking.md` — `rewoo.py` aus Scope entfernen
- `task_verbose_fix.md` — `rewoo.py` aus Scope entfernen
- `task_prompt_quality.md` — `rewoo` aus variants-Listen entfernen
- `task_bibliography_audit.md` — `xu2024rewoo` aus Status-Liste entfernen (falls relevant)

### T6: Verifizierung

- `grep -r rewoo aas-agent/src/` → nur `rewrites`-Mentions in `cypher_query.py` (falsch-positiv, darf bleiben)
- `grep -r rewoo mcp-server/src/` → nichts
- `grep -r rewoo .env` → nichts
- `grep -r xu2024rewoo paper/` → nichts
- `grep -r rewoo memory/agent_variants.md` → nichts
- Paper compiles: keine ReWOO-Mentions in `.aux` / `.bbl` → nach Neubuild prüfen

## References

- ReWOO-Implementierung: `aas-agent/src/aas_agent/rewoo*.py`
- Agent-Variants-Doku: `memory/agent_variants.md`
- API-Routing: `aas-agent/src/aas_agent/api.py`
- Paper-Architektur: `paper/etfa2026/content/06-architecture.tex`
- BibTeX: `paper/etfa2026/main.bib`
