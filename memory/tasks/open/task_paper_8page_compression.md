---
name: Task – Paper 8-Page Compression (ETFA 2026)
description: Paper von 9 auf 8 Seiten (IEEE-Hardlimit) bringen. Überlauf ist reine Bibliografie (Seite 9). Zwei Hebel — bib-Notes straffen + Body kompaktieren.
type: task
status: open
priority: high
---

## Summary

`conference_etfa_2026.pdf` baut auf **9 Seiten**, IEEE-Hardlimit ist **8**. Konsolidiert
die verstreuten Kompressions-Items: ersetzt [[task_paper_style_review]] T5 und
[[task_paper_style_fixes]] T2 (Caption-Fold).

## Diagnose (2026-05-31, via PyMuPDF gemessen)

- **Seite 9 ist zu 91 % gefüllt und besteht KOMPLETT aus Referenzen** (Einträge ab `[14]`).
- Body endet auf Seite 8 (Future Work → Conclusion → Acknowledgment), dann laufen
  die Referenzen über.
- ⇒ Zwei Hebel: **(A) Referenzliste selbst straffen** (trifft die Überlaufseite direkt)
  und **(B) Body kompaktieren** (zieht die Refs auf Seite 8 hoch).
- Gesamt-Überlauf ≈ 0,9 Seiten ≈ ~10 % Content. Kein Einzeiler-Fix.

## Hebel A — Bibliografie straffen (high-confidence, trifft Überlauf direkt)

Lange **deskriptive** `note=`-Felder kürzen (private Review-Notizen, die in den Druck
lecken). **Citation-Discipline-Notes BEHALTEN** (`arXiv preprint`, `Workshop paper at
<Venue>`, Lizenz wo relevant).

Kandidaten (main.bib):
- [ ] L135 `sclar2024quantifying` — „Shows that prompt formatting … 76\% accuracy variance …" → streichen
- [ ] L146 `qwen35` — „Models: 397B-A17B … No arXiv paper." → auf das Nötige kürzen
- [ ] L332 `docling2024` — „IBM Research Zurich. arXiv preprint (v5 …). No peer-reviewed venue." → auf `arXiv preprint` reduzieren
- [ ] L359 `kurtic2025bf16` — „ACL 2025 Long Paper. Key finding: W8A8-FP …" → nur Venue
- [ ] L367 `pymupdf4llm_doc` — „MIT-licensed extension … Accessed May 2026." → minimal
- [ ] ggf. lange `\url{}`/Accessed-Felder in @misc-Einträgen

## Hebel B — Body kompaktieren (Spar-Liste, mit User priorisieren)

Erst listen → priorisieren → ändern (keine Substanz streichen, nur verdichten):
- [ ] **§06** Caption-Fold (ex-m8): Body-Satz „Solid arrows … dashed arrows …" IN die
      Fig-Caption verschieben → bessere Caption + 1 Body-Zeile gespart
- [ ] **§08** „Graph Traversal as Entry Point" — sehr langer Absatz mit BaSyx-Query-
      Language-Exkurs; verdichtbar
- [ ] **§03** Contribution-Liste (i)–(iv) wiederholt teils Section-Inhalte; Gaps-Absatz straffbar
- [ ] **§10** Bench-B-Prosa (Manuals-first-Effekt, Anti-pattern-compliance) — lange Absätze
- [ ] **§04** Stolze-et-al.-Satz sehr lang
- [ ] **§05** 5-Schritt-Sequenz + R1–R4/C1–C2 leicht straffbar

## Micro-Pass (zuletzt, geringer Hebel)

- [ ] Orphan lines / Schusterjungen aufspüren, Sätze umformulieren um Zeilen zu sparen

## Acceptance Criteria

- PDF baut auf **≤ 8 Seiten** (`=== BUILD SUCCESS ===` + Seitenzahl prüfen via PyMuPDF)
- Keine Substanz gestrichen, nur verdichtet; Layered-Determinism-These unangetastet
- Citation-Discipline-Notes (arXiv/Workshop) bleiben erhalten
- Build ohne neue Fehler/undefined refs

## Vorgehen

1. Hebel A anwenden (high-confidence) → rebuild → Seitenzahl messen
2. Falls noch > 8: Body-Spar-Liste mit User priorisieren, dann anwenden
3. Micro-Pass nur falls am Ende 1–3 Zeilen fehlen

## References

- `paper/etfa2026/main.bib`, `content/03,04,05,06,08,10*.tex`
- Build: `python .claude/skills/paper/build_paper.py`
- Messung Seitenzahl/Füllung: PyMuPDF (`fitz`) auf das gebaute PDF
