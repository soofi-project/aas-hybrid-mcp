---
name: Skills Create Done
description: Vier Claude-Code-Skills (`/task`, `/paper`, `/paper-download`, `/paper-search`) unter .claude/skills/ angelegt, je mit bundled Tooling (Layered-Determinism); Paper-Build via Docker-Digest gepinnt
type: task
status: done
---

## Was umgesetzt

**`/task`** (`.claude/skills/task/SKILL.md`, 3.3 KB): Open→Closed-Workflow für `memory/tasks/`. Frontmatter-Templates (open mit `priority`, closed ohne), Umbenennung `task_<name>.md` → `<name>_done.md`, Subtask-Inline-Status, `[[wiki-link]]`-Cross-Refs, Anti-Patterns + Vorlagen-Pointer (`task_crag_diagnosis.md`, `task_prompt_quality.md`, `retrieval_enhancements_done.md`).

**`/paper`** (`.claude/skills/paper/SKILL.md`, 11 KB): ETFA-2026-Paper-Arbeit. Verzeichnislayout (alle 15 content-Files), Build-Befehl + Erfolgs-Marker, Log-Patterns für gezielte Fehler-Suche. Kern-Constraints: 8 Seiten IEEE, Layered-Determinism, Eval-Modell Qwen3.6-27B-FP8 (statt outdated 120B), SOOFI als Future Work, N=3-Existence-Claims-Caveat, HyDE-Verbot, BaSyx-Version-Pinning, 3-Anekdoten-Klammer Write→Read→Pragmatics.

**`/paper` Cross-cutting-Audit (2026-05-16):** Alle 14 `task_paper_*.md` durchgelesen und 8 Lücken im Skill nachgezogen — neue Sektionen *Claim-Belegbarkeit & Citation-Disziplin* (Belegtypen-Tabelle, Hallu-Verbot, BibTeX-Pflichtfelder), *Reviewer-Bingo „bessere Modelle"-Defense* (3 Gründe + Trained-In-4-Layer-Konsistenz), *Outlook-/Future-Work-Konsistenz* (stärkt vs. bricht These), *Cite-Positioning* (Garmaev als Adoption, ImplAAS-2025-Pflicht-Cites). Anti-Patterns um URN-Verbot, Reviewer-Bait-Phrasen, „due to space"-Ausreden, Garmaev-Baseline-Framing erweitert.

**`/paper-download`** (`.claude/skills/paper-download/SKILL.md`, 5.1 KB): PDF→Markdown via `extract_markdown.py`. Verzeichnis-Convention `<lastname><year><shortid>/` mit 22 Repo-Beispielen, single + bulk Mode, Qualitäts-Check-Liste (Titel/Abstract/References/Page-Count, PyMuPDF-Fallback-Warnung interpretieren), Bib-Key-Format mit Grep-Pflicht gegen Duplikate, optionale `related_work.md`-Regel (nur Cite-Kandidaten).

## Konventionen-Entscheidungen

- **Subfolder + `SKILL.md`** statt flat-file (`.md`) gewählt: Claude Code lädt Skills aus `<name>/SKILL.md`. Original-Task hatte flat-files vorgesehen — bei realer Skill-Lade-Mechanik nicht geladen worden.
- **Repo-lokal** (`.claude/skills/`) statt user-global — alle drei sind projektgebunden (AAS-Hybrid-MCP-Pfade, ETFA-Paper-Konstraints).

## Smoke-Test

Deferred to next session — Claude Code lädt Skills nur beim Session-Start in die Slash-Liste. Wird implizit beim ersten echten Aufruf von `/task`, `/paper`, `/paper-download` validiert. Bei Pfad-/Build-Korrekturen → Follow-up-Task `task_skill_<name>_fix.md`.

## Cost-Charakterisierung (für Kontext)

Pro Session: erste Aktivierung = einmaliger Body-Inject (3–11 KB), Folge-Aktivierungen 0 Kosten (Body bleibt in History, Harness dedupliziert). Verifiziert via claude-code-guide-Agent mit Bezug auf `code.claude.com/docs/en/skills.md` „Skill content lifecycle".

## Nachtrag — Layered-Determinism-Härtung (2026-05-16)

Nach erstem Skill-Wurf wurde die These des Papers („skills carry tools, not just prompt instructions") auf die Skills selbst angewendet:

**`/paper-download` — Script-Move:** `extract_markdown.py` von `paper/papers_downloaded/` nach `.claude/skills/paper-download/extract_markdown.py` verschoben. `_default_base_dir()` walked vom Script-Standort hoch und findet `paper/papers_downloaded/`; `--base-dir` als Override. Verhindert, dass der Agent den Konversions-Code neu zusammenwürfelt.

**`/paper` — Build-Wrapper + Digest-Pin:** `.claude/skills/paper/build_paper.py` als kanonischer Build-Aufruf (resolves repo-root, prüft `=== BUILD SUCCESS ===`-Marker, propagiert exit code). Compose-File `paper/etfa2026/docker-compose.yml` zeigt nicht mehr auf `qmcgaw/latexdevcontainer:latest-full`, sondern auf Content-Digest `sha256:4211ea058ce0…` — reproduzierbarer Build, kein Drift bei Image-Re-pull. Smoke-Test erfolgreich (PDF generiert).

**`/paper-search` (neu):** Vierter Skill — OpenAlex-Suche via `.claude/skills/paper-search/search_openalex.py` (250M Werke, frei, `mailto`-Identifier). Workflow in SKILL.md: Duplikat-Check (`main.bib` + `papers_downloaded/`) → OpenAlex-Suche/DOI-Lookup → Cite-Entscheidung (peer-review / Cites / OA / Cite-Positioning) → PDF + BibTeX-Stub. Smoke-Test 2026-05-16 mit `"asset administration shell agent" --year-from 2023` → 3 relevante Treffer (Xia 2024, Siatras 2023, Sakurada 2023), alle [OA] mit funktionierenden DOIs + PDF-URLs.

Ausgangsfrage des Users: „hätte paper-download nicht eigentlich die python datei gebraucht? […] ein wenig determinismus wäre doch gut oder?" → genau die Layered-Determinism-These des ETFA-Papers, auf die Skill-Architektur selbst übertragen. Skills sind jetzt: Workflow-Doku + bundled Tool, nicht nur Prompt-Hint.

## References

- Skill-Files: `.claude/skills/{task,paper,paper-download,paper-search}/SKILL.md`
- Bundled Tools: `.claude/skills/paper-download/extract_markdown.py`, `.claude/skills/paper/build_paper.py`, `.claude/skills/paper-search/search_openalex.py`
- Build-Pin: `paper/etfa2026/docker-compose.yml` (sha256:4211ea058ce0…)
- Reviewte Task-Files für Cross-cutting-Audit: `memory/tasks/open/task_paper_*.md` (14 Stück)
- Pfad-Referenz-Update: `memory/tasks/open/task_paper_implaas2025_citations.md` (zeigt jetzt auf neuen Script-Pfad)
- Skill-Lade-Mechanik-Recherche: claude-code-guide-Agent 2026-05-16
