---
name: Task – FP8-Quantisierung im Paper zitieren
description: kurtic2025bf16 (ACL 2025) an den richtigen Stellen im Paper einbauen — Methodik-Satz + Limitations-Caveat für alle Eval-Modelle
type: task
status: open
priority: medium
---

## Background

Für die Pattern × Modellgröße-Eval laufen alle lokalen Modelle in FP8-Quantisierung
(W8A8-FP). Das muss im Paper methodisch begründet werden. Das Paper

> Kurtic et al., "Give Me BF16 or Give Me Death?" ACL 2025, DOI 10.18653/v1/2025.acl-long.1304

liefert die Belege: **W8A8-FP ist im Wesentlichen verlustfrei gegenüber BF16**,
innerhalb der Messunsicherheit der Benchmarks. Bib-Key: `kurtic2025bf16`.

PDF + Markdown: `paper/papers_downloaded/kurtic2025bf16/paper.md`

## Subtasks

### T1 — Methodik-Satz in der Eval-Sektion einfügen

In der Eval-Sektion (Pattern × Modellgröße, voraussichtlich §5 oder §6) einen
Satz ergänzen, der FP8 als Deployment-Entscheidung begründet:

> "All locally hosted models were served using W8A8-FP8 quantization via vLLM.
> Prior work has shown that W8A8-FP quantization is essentially lossless compared
> to BF16, preserving accuracy within the evaluation's margin of error across
> diverse benchmarks \cite{kurtic2025bf16}."

Anpassungen an Stil und Länge der Sektion sind erlaubt — Kernaussage und Cite
müssen erhalten bleiben.

**Wo:** `paper/etfa2026/content/` — die Sektion mit dem Eval-Setup.
Genaue Section-Datei prüfen, bevor Änderung gemacht wird (erst `/paper`-Skill
aufrufen oder Section-Layout lesen).

### T2 — Limitations-Caveat prüfen

Nachsehen ob in der Limitations-Sektion oder einem Methodik-Caveat-Paragraph
etwas über Quantisierung steht. Falls ja: `\cite{kurtic2025bf16}` als Beleg
ergänzen. Falls nein: keinen neuen Absatz anlegen — T1-Satz reicht.

### T3 — Bib-Key-Verifikation beim Paper-Build

Beim nächsten LaTeX-Build prüfen, ob `kurtic2025bf16` ohne Warnung auflöst.
Entry steht schon in `paper/etfa2026/main.bib` (Abschnitt `% === Quantization ===`).

## Acceptance Criteria

- Mindestens ein `\cite{kurtic2025bf16}` im Fließtext der Eval-Sektion
- Der Satz macht klar: FP8 ist methodisch vertretbar, nicht nur pragmatisch gewählt
- LaTeX-Build läuft ohne undefined-reference-Warnung für den Key
- Kein neuer Absatz in Limitations nötig, wenn T2 nichts Passendes findet

## References

- Bib-Entry: `paper/etfa2026/main.bib` → Abschnitt `% === Quantization ===`
- Paper-Markdown: `paper/papers_downloaded/kurtic2025bf16/paper.md`
- Verwandte Tasks: [[task-paper-pattern-modelsize-eval]] (Eval-Sektion, in der T1 landet)
- Verwandte Tasks: [[task-paper-claim-audit]] (Claim-Audit muss diesen Cite kennen)
