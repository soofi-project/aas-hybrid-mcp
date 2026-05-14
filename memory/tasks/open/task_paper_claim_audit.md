---
name: Task - Paper Claim Audit (ETFA 2026)
description: Verify every claim in conference_etfa_2026.tex is backed by either own measurement (Bench A/B/C) or a peer-reviewed reference
type: task
status: open
priority: high
---

## Summary

Vor Einreichung muss jede sachliche Behauptung im Paper einen Beleg haben — entweder
**eigene Messung** (Bench A retrieval, Bench B end-to-end, Bench C write-path) oder
eine **peer-reviewte Referenz** in `main.bib`. Workshop-Paper / arXiv-only Quellen sind
zu markieren, aber nicht automatisch disqualifiziert (Einzelfallentscheidung).

Ziel ist eine zeilengenaue Checkliste, an der wir vor Submission jeden Claim abhaken
können. Halluzinierte Zahlen, „gefühlte" Performance-Aussagen, und nicht belegte
Vergleiche zu anderen Systemen sind die häufigsten Risiken.

## Scope

Alle Section-Files in `paper/etfa2026/content/`:

- `02-abstract-keywords.tex`
- `03-introduction.tex`
- `04-related-work.tex`
- `05-scenario-requirements.tex`
- `06-architecture.tex`
- `07-ingestion-plugin.tex`
- `08-retrieval-pipeline.tex`
- `09-write-loop.tex`
- `10-evaluation.tex`
- `11-discussion.tex`
- `12-limitations.tex`
- `13-future-work.tex`
- `14-conclusion.tex`

## Subtasks

### T1: Claim-Extraktion pro Section

Pro `.tex`-Datei: alle Aussagen extrahieren, die einen Beleg brauchen. Kategorien:

- **Quantitativ:** Zahlen, Prozente, Latenzen, Token-Counts, Recall/Precision, Tool-Call-Anzahl
- **Komparativ:** „better than X", „faster than Y", „outperforms Z"
- **Kausal:** „because of X, we observe Y"
- **Existenz-Behauptung:** „X exists / is standard / is widely used"
- **Negation:** „no existing system does X", „prior work cannot Y"

Ausgabe: `paper/etfa2026/claim_audit.md` mit Tabelle:

| Section | Line | Claim (zitiert) | Belegtyp | Beleg | Status |
|---------|------|-----------------|----------|-------|--------|
| 08-retrieval-pipeline | 42 | „rewriting verbessert recall um 12%" | Bench A | `bench_a_results.json` row 7 | ✅ |
| 04-related-work | 18 | „kein bestehendes System unterstützt write-back" | Survey | `related_work.md` §3 | ⚠ unbelegt |

### T2: Belegtypen pro Claim festlegen

Pro extrahiertem Claim entscheiden:

- **Own measurement** → Datei + Zeile/Row im Bench-Ordner zitieren
- **Peer-reviewed reference** → BibTeX-Key in `main.bib` (Venue muss peer-reviewed sein — IEEE/ACM/Springer-Konferenz/Journal). Workshop/Preprint mit `[W]`/`[P]` flaggen.
- **Common knowledge** → nur für wirklich unstrittiges (z. B. „AAS ist ein I4.0-Standard"). Defensiv anwenden.
- **Architectural decision** → kein externer Beleg, aber muss klar als Designentscheidung formuliert sein („we chose X because Y" statt „X is the right approach")

### T3: Lücken-Liste

Aus T1+T2: alle Claims mit Status `⚠ unbelegt` oder `❌ widersprochen` in einer
Priority-List sortiert nach Risiko:

1. **Block (vor Submission fixen):** quantitative Claims ohne Messung, Vergleiche ohne Referenz
2. **Soften (Formulierung abschwächen):** Existenz-/Negationsclaims ohne Survey-Beleg
3. **Future Work (verschieben):** Claims über Features die wir nicht evaluieren

### T4: bib-Hygiene

- Jeder in T2 zitierte Key muss in `main.bib` existieren
- Venue-Feld auf peer-reviewed prüfen (kein „arXiv preprint" für Block-Claims)
- Doppelte Einträge mergen
- Workshop-Paper als `@inproceedings` mit `note={Workshop}` markieren

### T5: Re-Audit nach jeder größeren Überarbeitung

Wenn `.tex`-Dateien substantiell geändert werden (nicht: typo fixes), Audit wiederholen
für die geänderten Sections. Diff-Modus: nur neue/geänderte Claims durchgehen.

## Acceptance Criteria

- `paper/etfa2026/claim_audit.md` existiert und deckt alle 13 Content-Sections ab
- Jede Zeile mit Status `✅` hat einen klickbaren Beleg (File + Zeile oder BibKey)
- Block-Claims (T3 Priorität 1) sind 0 vor Submission
- Soften-Claims (T3 Priorität 2) sind im `.tex` umformuliert oder ein Beleg ist nachgereicht
- `main.bib`: keine arXiv-only Quellen mehr als Beleg für quantitative Claims

## Non-Goals

- **Keine** Stilkorrektur (Grammatik, Klarheit) — separates Task wenn nötig
- **Keine** Reviewer-Antizipation („würde Reviewer X kritisieren?") — fokussiert auf
  Belegbarkeit, nicht Überzeugungskraft
- **Keine** Bench-Erweiterung — falls ein Claim keinen Beleg hat, entweder softening
  oder entfernen; neue Messungen brauchen ein eigenes Task

## References

- Paper-Quelle: `paper/etfa2026/content/*.tex`
- Bibliography: `paper/etfa2026/main.bib`
- Bench-Daten: `memory/bench_b_evaluation.md`, `interaction-protocol/`
- Related-Work-Memory: `~/.claude/projects/.../memory/related_work.md`
- Paper-Plan: `~/.claude/projects/.../memory/paper_etfa2026.md`
