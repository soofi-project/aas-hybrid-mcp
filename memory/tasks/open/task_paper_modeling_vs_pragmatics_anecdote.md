---
name: Task – Paper Modeling-vs-Pragmatics Anekdote
description: Container/MANAGES_ASSET-Ambiguität als kompakte AAS-spezifische Agent-Failure-Mode ins Paper aufnehmen — Modellierungs-Layer-Selbstreferenz vs. reale Welt aus Werker-Sicht
type: task
status: open
priority: medium
---

## Summary

Während Bench B trat eine AAS-spezifische Failure-Mode auf, die andere RAG-Paper *nicht* haben können, weil sie nicht auf einem Datenmodell mit Schalen↔Asset-Identitätsrelation operieren:

Auf die Frage „Welche Assets sind in Halle 4?" antworteten mehrere Varianten mit `urn:asset:hall4` (Identitäts-Lesart via `MANAGES_ASSET`) statt mit den enthaltenen Geräten (Container-Lesart via `HAS_SUBMODEL → HAS_ELEMENT* → Entity → REPRESENTS_ASSET`). Formal sind beide Cypher-Pfade korrekt — die MANAGES_ASSET-Selbstreferenz hat aber keine reale Entsprechung: eine Halle ist nicht „in sich selbst", das ist ein reines AAS-Modellierungs-Artefakt. Der fragende Nutzer (Werker, Fahrer, Operator) kennt diese Modellierungs-Ebene nicht und meint immer physische Containment.

Behebung nicht via Topologie-Änderung oder Retrieval-Tuning, sondern via Pragmatik-Regel in Tool-Description + Manual (siehe [[task-container-location-traversal-prompt-fix]]). Das ist ein eigenständiger, paper-werter Befund: **AAS-Agenten brauchen Pragmatik-Prompts, die die Lücke zwischen formaler Modell-Korrektheit und Nutzer-Mentalmodell schließen — Schema-Korrektheit allein reicht nicht.**

## Voraussetzung (Hard-Block, Reihenfolge ist wichtig)

Drei Vorbedingungen, in dieser Reihenfolge:

1. **[[task-agent-test-framework]] ist gebaut** — wir brauchen einen reproduzierbaren Test-Harness, der Fragen × Varianten × Wiederholungen läuft und Ergebnisse strukturiert ablegt. T3 im Fix-Task ist nur manueller Augenmaß-Check und reicht **nicht** für Paper-Material.
2. **Containment-Pattern als Test-Familie im Framework** — mehrere Fragen mit dem Muster „was ist in/inside/contained in <Container>" über mindestens den Halle-4-Container (später erweiterbar auf LKW, Schrank, Anlage). Die ursprünglich aussortierte mehrdeutige Frage `Welche Assets sind in Halle 4?` darf explizit *als* Containment-Test mit klarer Erwartung (Container-Lesart, keine Selbstreferenz) wieder aufgenommen werden — sie ist ja gerade der Grenzfall der den Fix motiviert.
3. **Pre/Post-Fix-Vergleich gefahren** — Baseline-Run *vor* Fix-Deployment, dann [[task-container-location-traversal-prompt-fix]] T1+T2 anwenden, dann identischer Post-Run. Beides über alle 4 Varianten × N Wiederholungen (N≥3, gegen LLM-Sampling-Noise). Erst diese Tabelle ist Paper-Material.

Ohne diese Kette gibt es keine belastbaren Zahlen — und „N von 4 Varianten falsch, nach Fix alle korrekt" wird Anekdote statt Befund.

## Platzierungs-Optionen

Drei Möglichkeiten, in der Reihenfolge meiner Empfehlung:

### Option 1 (empfohlen): In Bench-B Discussion verankern

Datei: `paper/etfa2026/content/10-evaluation.tex` oder `11-discussion.tex` (je nachdem wo Bench-B-Discussion sitzt).

Form: 3–5 Sätze als Eval-Befund. Pseudo-Wortlaut:

> Während Bench B beobachteten wir eine semantische Ambiguität, die spezifisch
> für AAS-Datenmodelle ist: formal valide MANAGES_ASSET-Selbstreferenzen vs.
> pragmatisch gemeintes Entity-Hierarchie-Traversal. Vor dem Fix lieferten N
> von 4 Varianten die Modellierungs-Antwort statt der vom Werker gemeinten
> Container-Antwort. Wir adressieren das nicht durch Topologie-Änderungen am
> Agenten, sondern durch eine Pragmatik-Regel in Tool-Description und Cypher-
> Manual, die die Modellierungs-Layer-Lücke explizit macht. Nach Fix: alle
> Varianten korrekt.

Vorteil: Eval-verankert, konkrete Zahlen, schärft den Punkt „Prompt-Engineering ist Eval-relevant, nicht nur Retrieval".
Nachteil: kostet 4–6 Zeilen im 8-Seiten-Budget.

### Option 2: In Discussion / Limitations als „Lessons Learned"

Datei: `paper/etfa2026/content/11-discussion.tex` oder `12-limitations.tex`.

Form: generischer formuliert, weniger an konkrete Bench-B-Zahlen gekoppelt. Funktioniert auch ohne Eval-Numbers.

Vorteil: robuster gegen Eval-Volatilität, leichter unterzubringen.
Nachteil: weniger schlagkräftig — wirkt eher als Reflexion denn als Befund.

### Option 3 (Fallback bei Kompression): Footnote im Retrieval- oder Agent-Kapitel

Datei: `paper/etfa2026/content/08-retrieval-pipeline.tex` oder `09-write-loop.tex` (bzw. wo der Agent beschrieben wird).

Form: 1–2 Sätze als Footnote, minimal-invasiv.

Vorteil: extrem kompakt, fällt bei Page-Budget-Druck als erstes raus ohne Sektion zu beschädigen.
Nachteil: leicht zu übersehen, schwächt den Punkt deutlich.

## Subtasks

### T1: Pre/Post-Benchmark fahren

- Im Test-Framework eine Containment-Test-Suite definieren mit mindestens diesen Fragen über Halle 4:
  - `Welche Assets sind in Halle 4?` (mehrdeutige Original-Frage — Erwartung: nur enthaltene Geräte, **kein** `urn:asset:hall4`)
  - `Welche Geräte stehen in Halle 4?`
  - `Welche Transportroboter sind in Halle 4?`
  - `Welche Greifroboter sind in Halle 4?` / `Welche kollaborativen Roboter sind in Halle 4?`
  - Mindestens 1 Identitäts-Regression: `Welches Asset repräsentiert die Schale Halle 4?` (Erwartung: `urn:asset:hall4` via MANAGES_ASSET — darf durch den Fix **nicht** kaputtgehen)
- **Baseline-Run** (Pre-Fix) über alle 4 Varianten × N≥3 Wiederholungen. Resultate strukturiert speichern (Variant × Frage × Run → Antwort + Score).
- [[task-container-location-traversal-prompt-fix]] T1+T2 anwenden (Tool-Description + Cypher-Manual).
- **Post-Fix-Run** identisch wiederholen, gleiche N, gleiche Modelle/Temperaturen.
- Auswertung: Per-Variant-Trefferquote vor vs. nach Fix, Identitäts-Regression intakt? Sampling-Streuung dokumentieren.

### T2: Platzierung entscheiden

- Mit Pre/Post-Tabelle in der Hand prüfen, ob die Zahlen schlagkräftig genug für Option 1 sind (deutliche Verbesserung, klare Story).
- Wenn Verbesserung deutlich + Page-Budget reicht → Option 1 (Bench-B Discussion).
- Wenn Verbesserung nur teilweise oder Zahlen verrauscht → Option 2 (Limitations / Lessons Learned, weniger zahlen-abhängig).
- Wenn Page-Budget extrem knapp → Option 3 (Footnote).

### T3: Absatz schreiben

- 3–5 Sätze (Option 1/2) bzw. 1–2 Sätze (Option 3) in die gewählte `.tex`-Datei einfügen.
- Sprache: deutsche oder englische Paper-Sprache (je nachdem was die übrigen Sektionen verwenden — vermutlich Englisch).
- Keine harten ZVEI/IDTA-URIs im Wortlaut, keine konkreten URN-Strings im Paper-Text (allenfalls in einer Beispiel-Box).
- Connection zu existierenden Sektionen: kurz auf Tool-Description-Regel verweisen, ohne den Wortlaut zu duplizieren.
- Bei Option 1: konkrete Pre/Post-Zahlen aus T1 zitieren (z. B. „3/4 Varianten lieferten vor Fix die Modellierungs-Antwort, nach Fix 0/4").

### T4: Cross-Refs & Konsistenz

- Sicherstellen dass kein anderer Paper-Abschnitt der Beobachtung widerspricht (besonders `08-retrieval-pipeline.tex` „Retrieval Enhancements" und `09-write-loop.tex` Agent-Beschreibung).
- Bench-B-Tabelle/Zahlen falls vorhanden konsistent halten — falls die Zahlen sich durch Fix verschieben, Tabelle nachziehen.
- Pre/Post-Rohdaten in `interaction-protocol/` oder Eval-Output-Verzeichnis aufbewahren, im Paper als „data available on request / in repo" referenzierbar.

## Acceptance Criteria

- Pre/Post-Benchmark im Test-Framework gefahren, Rohdaten archiviert, Tabelle Variant × Frage × Pre/Post erzeugt.
- Identitäts-Regression-Frage zeigt **keinen** negativen Effekt durch den Fix (`urn:asset:hall4` via MANAGES_ASSET funktioniert weiter).
- Paper enthält den Modeling-vs-Pragmatics-Befund an einer der drei genannten Stellen.
- Absatz nennt konkret: (a) AAS-spezifische Failure-Mode (Schalen-Selbstreferenz vs. physische Containment), (b) Werker-Mentalmodell-Argument, (c) Fix-Stelle (Prompt/Tool-Description statt Topologie).
- Eval-Verankerung vorhanden (Option 1: konkrete Pre/Post-Zahlen im Absatz) oder bewusst weggelassen (Option 2/3) — Entscheidung dokumentiert.
- Keine Architektur-Leaks, keine harten IDTA-URIs im Fließtext.
- Konsistenz mit Bench-B-Zahlen und Retrieval-Sektion geprüft.

## References

- Quellen-Task: [[task-container-location-traversal-prompt-fix]] — liefert die Eval-Numbers und Tool-Description-Texte.
- Paper-Dateien (Kandidaten): `paper/etfa2026/content/10-evaluation.tex`, `11-discussion.tex`, `12-limitations.tex`, `08-retrieval-pipeline.tex`, `09-write-loop.tex`.
- Live-Test-Befund: `interaction-protocol/2026-05-14T17-50-30Z__1962b4110f55/` (Qwen) + Curl-Tests am 2026-05-14 (GPT).
- Hintergrund-Memory: repo `memory/bench_b_evaluation.md`.
