---
name: Task – Paper §09/§10/§11 Ablation Section Updates
description: Nach T6-Eval-Runs (Ablation Variant A/B): §09 Write-Loop korrigieren, §10 Benchmark D einfügen, §11.2 auf Daten verweisen.
type: task
status: open
priority: high
---

## Background

Die Ablation-Studie (Variant A = Prompt-Hint, Variant B = Typed-Only) ist implementiert
und die Test-Cases sind fertig — aber die Eval-Runs (T6 aus [[task-write-tools-ablation-study]])
fehlen noch. Erst danach können die Paper-Sections mit echten Daten befüllt werden.

Drei konkrete Probleme im aktuellen Paper-Stand:

1. **§09 beschreibt 6 generische Tools** — `create_service_request_notification`
   taucht nur als Nachgedanke in §11 auf, nicht als bewusste Architekturentscheidung.
2. **§11.2 ist ein unbelegter Claim** — "typed tool closes bypass" steht ohne Daten.
3. **§10 hat kein Benchmark D** — die Ablation-Tabelle fehlt komplett.

## Blocker

**Wartet auf T6** aus `[[task-write-tools-ablation-study]]`:
- Eval-Run Variant A (`WRITE_TOOLS_MODE=generic`, N=3, `srn_ablation_variant_a.yaml`)
- Eval-Run Variant B (`WRITE_TOOLS_MODE=typed`, N=3, `srn_autonomous.yaml`)
- BaSyx-Verifikation via `verify_srn.py` für alle Runs

## Subtasks

### T1 — §09 Write-Loop: "Single Tool" → "Layered Tool Surface"

Aktuell: Abschnitt §09.3 "Single Tool for SubmodelElement Subtypes" — beschreibt
`put_submodel_element` als Alles-Lösung.

Änderung: Abschnitt umbenennen und ergänzen:
- 6 generische Tools = explorative Writes, volle Flexibilität
- `create_service_request_notification` = Typed Tool für SRN als Existence-Proof
- Expliziter Trade-off: generisch = flexibel, typed = garantiert korrekt
- `WRITE_TOOLS_MODE`-Env-Var kurz erwähnen als Eval-Hebel

**Datei:** `paper/etfa2026/content/09-write-loop.tex`

**Größe:** Mittel (Absatz-Reformulierung + 1–2 neue Sätze)

**Status:** ⬜ Open — wartet auf T6

### T2 — §10 Benchmark D: Write-Path Enforcement Ablation

Neuer Abschnitt nach Benchmark C in `10-evaluation.tex`:

```latex
\subsection{Benchmark D --- Write-Path Enforcement Ablation}
\textbf{Setup:} ...Variant A (WRITE_TOOLS_MODE=generic + prompt-hint)
vs. Variant B (WRITE_TOOLS_MODE=typed, create_srn only), N=3 each,
aas-agent:react, post-hoc BaSyx verification via verify_srn.py.

\begin{table}[h]
\caption{Write-Path Enforcement Ablation (N=3)}
...
| Variant | Write-Path | SRN valid in BaSyx | Bypass observed |
| A (prompt-hint) | put_submodel | x/3 | y/3 |
| B (typed-only)  | create_srn   | 3/3 | 0/3 |
\end{table}

Existence-Framing: N=3 establishes that prompt guidance alone is
insufficient to prevent bypass; the typed tool eliminates the path
entirely.
```

**Datei:** `paper/etfa2026/content/10-evaluation.tex`

**Größe:** Mittel (neuer Abschnitt, ~15 Zeilen LaTeX)

**Größencheck:** §10 Benchmark C hat noch `[EVAL]`-Platzhalter — nach Befüllung
Seitenzahl prüfen, ggf. Benchmark D kürzen.

**Status:** ⬜ Open — wartet auf T6-Daten

### T3 — §11.2 Agentic Reads vs. Workflow Writes: Claim → Referenz

Aktuell: "A typed `create_service_request_notification` tool…closes this bypass path"
— Behauptung ohne Daten.

Änderung: Satz ersetzen durch Verweis auf Benchmark D:
`"as confirmed by Benchmark D (Section~\ref{sec:bench-d}), which shows…"`

**Datei:** `paper/etfa2026/content/11-discussion.tex`

**Größe:** Klein (1–2 Sätze)

**Status:** ⬜ Open — wartet auf T2

## Entscheidung: Wie Eval-Ergebnisse ins Paper kommen

**Keine vollständige Query-Liste im Paper.** 22 Cases über 6 Test-Familien
würden das Paper füllen. Stattdessen dreistufiger Ansatz:

1. **Struktur-Tabelle** in §10 — beschreibt die Test-Familien auf einer Zeile
   pro Familie (Name, Case-Anzahl, getestete Eigenschaft). Keine einzelnen
   Query-Texte.
2. **Anekdoten-Queries** — 2–3 konkrete Queries eingebettet im Fließtext von
   §10/§11, direkt dort wo sie einen Befund belegen. Diese sind in den YAML-
   Files mit `tags: [paper_anecdote]` markiert.
3. **Vollständige Case-Liste im Repo** — alle YAML-Files unter
   `tests/agent-tests/cases/` werden im Paper als `[repo]` zitiert.
   Kein Supplementary-Appendix nötig.

**Post-hoc-Selektion der Anekdoten ist legitim**, solange im Paper transparent
gemacht wird wie viele Cases insgesamt liefen und wie viele bestanden haben —
sonst wirkt es wie Cherry-Picking.

## Acceptance Criteria

- [ ] §09 nennt `create_service_request_notification` als explizite Architekturentscheidung
      (nicht nur §11-Erwähnung)
- [ ] §10 enthält Struktur-Tabelle der Test-Familien (keine einzelnen Query-Texte)
- [ ] §10 enthält Benchmark-D-Tabelle mit echten Daten aus T6
- [ ] §11.2 referenziert Benchmark D statt unbelegter Aussage
- [ ] Repo-URL als `[repo]`-Cite in §10 vorhanden
- [ ] Paper baut ohne Fehler: `python .claude/skills/paper/build_paper.py`
- [ ] 8-Seiten-Limit eingehalten (nach §10-Befüllung mit echten Bench-C-Daten prüfen)

## References

- Abhängiger Task: [[task-write-tools-ablation-study]] (T6 = Blocker)
- Write-Loop Section: `paper/etfa2026/content/09-write-loop.tex`
- Evaluation Section: `paper/etfa2026/content/10-evaluation.tex`
- Discussion Section: `paper/etfa2026/content/11-discussion.tex`
- Verify-Script: `tests/agent-tests/verify_srn.py`
- Test-Cases: `tests/agent-tests/cases/srn_ablation_variant_a.yaml`
