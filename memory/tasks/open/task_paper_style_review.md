---
name: Task - Paper Style Review (Reviewer Perspective)
description: Critical reviewer-style evaluation of conference_etfa_2026.tex — written by an agent acting as a skeptical IEEE/ETFA reviewer
type: task
status: open
priority: medium
---

## Summary

Nach dem Claim-Audit ([[task_paper_claim_audit]]) eine zweite, **stilistische** Runde:
ein Agent liest das gebaute PDF (oder die `.tex`-Sektionen) und bewertet es aus der
Sicht eines kritischen Reviewers — nicht freundlich, nicht ermutigend, sondern so wie
ein typischer ETFA/IEEE-Reviewer eine zu lange, zu vage oder zu marketing-lastige
Einreichung in der zweiten Review-Runde zerlegen würde.

Ziel ist keine Stilpolitur per Diff, sondern eine **Schwachstellen-Liste** die wir
selbst priorisieren und umsetzen.

## Reviewer Persona (für den Agent-Prompt)

> You are reviewer #2 for an ETFA workshop submission. You have read ~30 industrial-AI
> papers this year and are tired of vague claims, narrative filler, marketing language,
> and "we built X and it works" without rigorous evaluation. You read this paper
> looking for reasons to reject. Be specific (cite section + sentence), be harsh,
> but stay technical — no personal attacks, no style preferences disguised as bugs.

## Was zu prüfen ist

1. **Vague claims** — „significantly improves", „state of the art", „efficient",
   „scalable" ohne Zahlen oder Vergleich
2. **Marketing language** — „novel", „innovative", „cutting-edge", „groundbreaking"
   in einem technischen Paper
3. **Missing baselines** — Behauptungen, die einen Vergleich nahelegen, aber keinen
   liefern („our approach handles X" — gegen was?)
4. **Causality vs. correlation** — „after introducing X, we see Y" ohne Ablation
5. **Overclaiming scope** — Generalisierungen jenseits dessen, was Bench A/B/C tatsächlich gezeigt hat
6. **Hand-waving** — „due to space constraints", „details omitted", „future work"
   als Ausrede für fehlende Substanz
7. **Inkonsistente Terminologie** — gleicher Begriff mit verschiedenen Bedeutungen,
   oder verschiedene Begriffe für dasselbe (z. B. „agent" / „LLM" / „assistant" wild gemischt)
8. **Figure/Table-Verweise** — wird jede Figure/Table referenziert? Steht der Text
   *vor* der Figure?
9. **Related Work als Liste vs. Kontrast** — werden andere Arbeiten nur aufgezählt
   oder wirklich abgegrenzt? Wo ist der Unterschied?
10. **Abstract vs. Body** — verspricht das Abstract Dinge, die der Body nicht hält?
11. **Conclusion vs. Body** — wiederholt die Conclusion nur das Abstract oder zieht
    sie eine echte Schlussfolgerung?
12. **Reproducibility** — kann ein Leser die Methodik nachvollziehen? Sind Modell-IDs,
    Versionen, Hyperparameter, Prompts dokumentiert (oder Link auf Repo)?

## Subtasks

### T1: Reviewer-Pass über das gebaute PDF

Agent (Opus oder vergleichbar) liest `paper/etfa2026/conference_etfa_2026.pdf` (oder
die `.tex`-Quellen) und schreibt einen Review-Report:
- Tabelle: Section | Issue Type | Citation | Severity (major/minor) | Suggested fix
- Severity-Schwelle: nur was ein echter Reviewer auch wirklich anmerken würde —
  keine Mikro-Stiltipps

Ausgabe: `paper/etfa2026/style_review.md`

### T2: Selbst-Review der drei kritischsten Sections

Nach T1: die drei vom Agent als „weakest" markierten Sections noch einmal manuell
durchgehen — Agent kann übersehen, was wir aus eigenem Bench-Wissen besser einschätzen.

### T3: Priorisierung + Fix-Liste

Aus T1+T2: drei Buckets:
1. **Block** — Major issues, die ein Reviewer auf Reject schreiben würde → vor Submission fixen
2. **Soften** — Formulierungen, die zu viel versprechen → abschwächen
3. **Defer** — Nice-to-have, wenn Zeit bleibt

### T4: Diff-Pass nach jedem größeren Edit

Bei substantieller Überarbeitung einer Section: lokaler Reviewer-Pass auf das Diff,
damit neue Schwächen nicht durchrutschen.

### T5: 8-Seiten-Compliance-Pass (nach Fertigstellung des Inhalts)

**Erst wenn der Inhalt stabil ist** — kein Sinn vorher, da Sections noch wachsen.

**Content-Analyse (größter Hebel):**
Alle `.tex`-Dateien sequentiell lesen; pro Section schätzen wie viel
eingespart werden kann (in % / Zeilen) durch:
- Redundanz zwischen Introduction, Related Work und Conclusion
- Füllphrasen mit niedriger Informationsdichte
  (z. B. „It is important to emphasize", „As mentioned above", „In this paper we")
- Abbildungen/Tabellen zu groß für ihren Informationsgehalt

Ausgabe: priorisierte Sparliste (Section | Schätzung | Beispiel) — erst listen, dann mit User priorisieren, dann ändern.

**LaTeX-Micro-Pass (geringer Hebel, Feinschliff):**
Orphan Lines ("Schusterjungen") aufspüren — einzelne Wörter oder Satzenden
die alleine eine neue Zeile belegen. Sätze umformulieren um die Zeile einzusparen.
Kann 3–8 Zeilen bringen, also letzter Schritt vor Submission.

**Template-Check (Einmalcheck, trivial):**
Sicherstellen dass `IEEEtran.cls` korrekt eingebunden ist:
- Referenzen in 8pt (statt 10pt Haupttext) — automatisch via Template
- Vornamen als Initialen + „et al." ab dem 4. Autor — automatisch via IEEEtran
Falls das bereits stimmt: kein Handlungsbedarf.

## Acceptance Criteria

- `paper/etfa2026/style_review.md` existiert mit zeilengenauen Kommentaren
- Block-Issues (T3 Bucket 1) sind vor Submission auf 0
- Soften-Issues (T3 Bucket 2) sind im `.tex` umformuliert *oder* explizit als
  akzeptiert markiert mit Begründung
- Reviewer-Perspektive bleibt skeptisch — kein „looks good overall" als Fazit

## Non-Goals

- **Keine** Grammatik-/Typo-Korrektur — separat (Sprachtool reicht)
- **Keine** Belegprüfung — das ist [[task_paper_claim_audit]]
- **Keine** Reviewer-Antwort-Vorbereitung („rebuttal") — passiert erst nach Submission

## References

- Paper: `paper/etfa2026/conference_etfa_2026.tex` + `content/*.tex`
- Schwester-Task: [[task_paper_claim_audit]]
- Stilguide (falls vorhanden): `paper/guideline.md`
