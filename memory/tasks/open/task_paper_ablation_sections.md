---
name: Task – Paper §09/§10/§11 Write-Path Validation Sections
description: Nach SRN-Eval-Runs: §09 Write-Loop korrigieren, §10 Write-Path-Benchmark einfügen, §11.2 auf Daten verweisen. Kein Ablation A/B mehr — nur generischer Pfad + Template-Validator-Bypass.
type: task
status: open
priority: high
---

## Background

Die ursprüngliche Ablation-Studie (Variant A = Prompt-Hint, Variant B = Typed-Only) ist obsolet.
`create_service_request_notification` wurde entfernt. Der Agent hat nur noch den generischen
`put_submodel`-Pfad mit Template-Validierung. Die neue Befund-Landschaft:

1. **Agent nutzt `put_submodel`** mit vollständigem SRN-Payload → Template-Validator prüft Struktur.
2. **Möglicher Bypass:** Agent pusht ein leeres/minimales Submodel (template-konform, weil
   `ServiceRequestNotification` Cardinality ZeroToMany hat) und füllt es dann Element-für-Element
   via `put_submodel_element`. Auf Element-Ebene gibt es keine Template-Validierung.

Die Paper-Story ändert sich von "Prompt reicht nicht vs. Typed Tool schließt Bypass" zu:
"Template-Validierung auf Submodel-Ebene fängt strukturell falsche Payloads ab, aber der
Agent kann den Validator umgehen indem er ein leeres Submodel pushed und dann Element-für-Element
nachbaut — weil auf Element-Ebene keine Template-Konformität geprüft wird."

## Blocker

**Wartet auf Eval-Runs** aus `[[task-srn-eval-rerun-after-typed-tool-removal]]`:
- Neue `srn_autonomous`-Ergebnisse für alle Modelle (6 Cases pro Modell)
- Insbesondere: `srn_empty_submodel_bypass` — nimmt ein Modell den Bypass?

## Subtasks

### T1 — §09 Write-Loop: "Single Tool" → "Layered Validation"

Aktuell: Abschnitt §09.3 beschreibt `put_submodel_element` als Alles-Lösung.

Änderung: Abschnitt ergänzen:
- 6 generische Write-Tools = explorative Writes, volle Flexibilität
- `put_submodel` mit zweistufiger Validierung: SDK-Deserialisierung + Template-Konformität
- Lücke: `put_submodel_element` hat keine Template-Validierung — Element-Ebene ist ungeregelt
- Kein `WRITE_TOOLS_MODE` mehr erwähnen (entfernt)

**Datei:** `paper/etfa2026/content/09-write-loop.tex`

**Status:** ⬜ Open — wartet auf Eval-Daten

### T2 — §10 Write-Path Benchmark

Abschnitt nach Benchmark C in `10-evaluation.tex`:

Setup: alle Modelle, `srn_autonomous.yaml` (6 Cases), `aas-agent:react`, N=10.

Tabelle:
```latex
\subsection{Write-Path Validation}
\textbf{Setup:} ...generic put_submodel + template validator,
6 cases (3 autonomous, 2 spatial/serial disambiguation, 1 empty-submodel bypass),
aas-agent:react, N=10.

| Case | Write-Path | Template valid | Bypass observed |
|... | put_submodel (full) | yes/no | - |
|... | put_submodel (empty) + put_submodel_element | n/a | yes |
```

Existence-Framing: falls ein Modell den empty-submodel-Bypass nimmt, ist das
Evidenz dass Template-Validierung allein nicht reicht.

**Datei:** `paper/etfa2026/content/10-evaluation.tex`

**Status:** ⬜ Open — wartet auf Eval-Daten

### T3 — §11.2 Discussion: Pragmatics-Validation-Gap

Aktuell: unbelegter Claim über typed tool.

Änderung: Satz ersetzen durch Verweis auf Write-Path-Benchmark:
"as confirmed by the Write-Path evaluation (Section~\ref{sec:write-path}), which shows
that agents can bypass template validation by pushing an empty submodel and constructing
it element-by-element."

Falls kein Modell den Bypass nimmt: schwächere Formulierung — "the architectural
possibility exists because put_submodel_element lacks template validation; future
work should close this gap".

**Datei:** `paper/etfa2026/content/11-discussion.tex`

**Status:** ⬜ Open — wartet auf T2

## Entscheidung: Wie Eval-Ergebnisse ins Paper kommen

**Keine vollständige Query-Liste im Paper.** Stattdessen dreistufiger Ansatz:

1. **Struktur-Tabelle** in §10 — beschreibt die Test-Familien auf einer Zeile
   pro Familie (Name, Case-Anzahl, getestete Eigenschaft). Keine einzelnen
   Query-Texte.
2. **Anekdoten-Queries** — 2–3 konkrete Queries eingebettet im Fließtext von
   §10/§11, direkt dort wo sie einen Befund belegen. Diese sind in den YAML-
   Files mit `tags: [paper_anecdote]` markiert.
3. **Vollständige Case-Liste im Repo** — alle YAML-Files unter
   `tests/agent-tests/cases/` werden im Paper als `[repo]` zitiert.

## Acceptance Criteria

- [ ] §09 beschreibt zweistufige Validierung (SDK + Template) + Lücke auf Element-Ebene
- [ ] §10 enthält Write-Path-Benchmark-Tabelle mit echten Daten
- [ ] §11.2 referenziert Write-Path-Benchmark statt unbelegter Aussage
- [ ] Repo-URL als `[repo]`-Cite in §10 vorhanden
- [ ] Paper baut ohne Fehler: `python .claude/skills/paper/build_paper.py`
- [ ] 8-Seiten-Limit eingehalten

## References

- Abhängiger Task: [[task-srn-eval-rerun-after-typed-tool-removal]] (Blocker)
- Write-Loop Section: `paper/etfa2026/content/09-write-loop.tex`
- Evaluation Section: `paper/etfa2026/content/10-evaluation.tex`
- Discussion Section: `paper/etfa2026/content/11-discussion.tex`
- Test-Cases: `tests/agent-tests/cases/srn_autonomous.yaml`
