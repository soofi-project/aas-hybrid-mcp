---
name: Task – Paper Read-Validation-Gap Anekdote
description: idShort/id-Substring-Lookup als AAS-spezifische Agent-Failure-Mode ins Paper aufnehmen — Manual sagt Anti-Pattern, Agent macht's trotzdem, fällt in unseren Fixtures nicht auf weil Naming zufällig konsistent.
type: task
status: open
priority: medium
---

## Summary

Im Smoke-Run des neuen Test-Frameworks (2026-05-15) verletzte
`aas-agent:react` bei „Wie schnell kann der MiR100 maximal fahren?" zwei
explizite Manual-Anti-Patterns aus `cypher.md`:

- **#3:** `assetType` ist meist `null`, taugt nicht als Lookup.
- **#4:** `idShort` nie für domain reasoning; nur als entry point.

Konkrete Query:

```cypher
WHERE toLower(aas.idShort)    CONTAINS 'mir100'
   OR toLower(asset.assetType) CONTAINS 'mir100'
   OR toLower(aas.id)          CONTAINS 'mir100'
```

**Kern-Befund:** In unseren Fixtures funktioniert die Query trotzdem, weil
die Naming-Konvention strikt ist (`MiR100_001`, `urn:asset:mir100:001`).
In einem realistischen Deployment mit `Roboter_47`, `Cell-3-Mobile-Unit`
oder `urn:fabrik:device:9f2a-7c1` als Identifikator liefert sie null Rows
— und der Agent würde leere oder erfundene Antworten produzieren.

Das ist der **dritte AAS-spezifische Validation-Gap-Befund** und ergänzt
die zwei bereits dokumentierten:

- [[task-paper-modeling-vs-pragmatics-anecdote]] — MANAGES_ASSET-Selbst-
  referenz statt Container-Traversal.
- [[task-write-tool-validation-gap]] — `put_submodel_element` umgeht
  Submodel-Validator.

Gemeinsam motivieren die drei Befunde eine paper-würdige These (siehe
auch [[feedback-agent-constraint-philosophy]]):

> **Layered Determinism.** Industrial-AI-Agenten brauchen einen geschichteten
> Aufbau: der Agent liefert Sprachverständnis und Strategiewahl, MCP/Tool-
> Boundaries erzwingen domänenspezifische Invarianten *deterministisch*.
> Prompts und Manuals sind Hinweise, keine Garantien. Wo Compliance mit
> Domänen-Konventionen sicherheits- oder konsistenz-relevant ist, gehört
> sie in deterministischen Code.

## Voraussetzung (Hard-Block, Reihenfolge ist wichtig)

Drei Vorbedingungen, in dieser Reihenfolge:

1. **[[task-agent-test-framework]] gebaut** ✅ — erledigt 2026-05-15.
2. **MCP-Side Cypher-Validator implementiert** mit Mode-Toggle
   (`STRICT_READ_VALIDATION=off|warn|strict`) und Unit-Tests. Siehe
   [[task-read-validation-gap]] T1.
3. **Naming-Stress-Fixtures vorhanden** im AAS-Repo (mind. 1 künstlich
   umbenanntes Type-Shell). Siehe [[task-read-validation-gap]] T2.
4. **Pre/Post-Bench gefahren** — Naming-Stress + Anti-Pattern-Smoke-Cases
   × 4 Variants × 3 Modes (off/warn/strict) × N≥3 Wiederholungen.
   Rohdaten archiviert.

Ohne diese Kette ist die Anekdote nicht belastbar — wir hätten nur
„ein Agent hat einmal das Falsche getan". Mit der Kette wird's
„unter realistischen Naming-Bedingungen scheitern N von 4 Varianten,
mit deterministischem MCP-Validator scheitern 0 von 4".

## Klammer mit den anderen zwei Anekdoten

Aktuell sind die drei Anekdoten als isolierte Befunde geplant. Empfehlung:
**ein gemeinsamer Einleitungs- oder Discussion-Absatz** der die drei
unter „Layered Determinism" zusammenfasst. Sonst wirken sie wie isolierte
Bug-Reports.

Vorgeschlagene Struktur im Paper:

1. **Einführung** des Layered-Determinism-Arguments (1 Absatz in
   §11-discussion oder §12-limitations).
2. **Drei Anekdoten als Evidenz**, jede 3–5 Sätze, mit Pre/Post-Zahlen:
   - Write-Validation-Gap (Bench-B-Trace 2026-05-15)
   - Modeling-vs-Pragmatics (Pre/Post-Fix-Bench, siehe [[task-paper-modeling-vs-pragmatics-anecdote]])
   - Read-Validation-Gap (Pre/Post-Mode-Bench, dieser Task)
3. **Zusammenfassende These:** Manual ≠ Garantie; deterministischer
   Validator = Garantie.

Wenn Platz knapp ist: einer fliegt raus, aber die Klammer bleibt — sonst
verlieren die anderen zwei ihren Punkt.

## Platzierungs-Optionen

Drei Möglichkeiten, in der Reihenfolge meiner Empfehlung:

### Option 1 (empfohlen): In Bench/Evaluation-Discussion als Layered-Determinism-Trio

Datei: `paper/etfa2026/content/10-evaluation.tex` oder `11-discussion.tex`.

Form: Einleitungsabsatz Layered-Determinism + 3–5 Sätze für diese Anekdote
mit konkreten Pre/Post-Zahlen aus dem Mode-Bench (off / warn / strict).

Pseudo-Wortlaut:

> Während der Eval-Runs traten drei AAS-spezifische Failure-Modes auf,
> die ein gemeinsames Muster teilen: in allen Fällen verbietet das
> Manual die beobachtete Strategie explizit, der Agent wählt sie
> trotzdem. ... Für `query_aas_graph` führte das zu idShort-Substring-
> Lookups statt semanticId-basierter Klassifikation — in unseren
> Fixtures unauffällig, bei Naming-Stress-Tests scheiterten N von 4
> Varianten ohne deterministische Validierung; mit STRICT-Modus 0/4.
> Diese drei Befunde motivieren eine geschichtete Architektur: der
> Agent für Strategiewahl, deterministische Validatoren am Tool-Endpoint
> für Domänen-Invarianten.

Vorteil: schließt alle drei Anekdoten zu einem schlagkräftigen Argument.
Nachteil: ~10–12 Zeilen im 8-Seiten-Budget.

### Option 2: Standalone als Limitations-Lessons-Learned

Datei: `paper/etfa2026/content/12-limitations.tex`.

Form: Eigenständiger Absatz ohne Klammer mit den anderen zwei. Erwähnt
nur: „in stressed-Fixtures versagt idShort-Heuristik, MCP-Validator
hilft".

Vorteil: kompakt, robust gegen Eval-Volatilität.
Nachteil: verliert den Argument-Verbund mit den anderen zwei Anekdoten.

### Option 3 (Fallback): Footnote im Cypher-/MCP-Sektion

Datei: `paper/etfa2026/content/06-mcp-server.tex` oder `08-retrieval-pipeline.tex`.

Form: 1–2 Sätze als Footnote.

Vorteil: extrem kompakt.
Nachteil: verliert den paper-würdigen Punkt fast komplett.

## Subtasks

### T1: Pre/Post-Mode-Bench fahren

- Im Test-Framework Containment-, Anti-Pattern- und Naming-Stress-Cases
  laufen lassen × 4 Varianten × 3 Modes (`off`, `warn`, `strict`) × N≥3
  Wiederholungen.
- Resultate strukturiert speichern (Variant × Case × Mode × Run → Antwort
  + Score + Cypher-Pattern-Hits).
- Auswertung: Per-Variant Erfolgsrate je Mode auf stressed vs. unstressed
  Fixtures.

### T2: Platzierung entscheiden

- Mit Pre/Post-Tabelle in der Hand prüfen ob Option 1 (mit Klammer)
  klappt — braucht Page-Budget für 10–12 Zeilen.
- Wenn Budget knapp und der andere Pragmatik-Task ([[task-paper-modeling-vs-pragmatics-anecdote]])
  schon platziert ist: in dessen Absatz mit-andocken.
- Wenn Budget extrem knapp: Option 3 (Footnote) als Fallback.

### T3: Absatz schreiben

- 3–5 Sätze (Option 1/2) bzw. 1–2 Sätze (Option 3).
- Konkrete Pre/Post-Zahlen aus T1 zitieren.
- Anti-Pattern-Beispiel-Cypher als Listing in einer Beispiel-Box
  (kein URN-Leak im Fließtext).
- Keine harten IDTA-URIs.

### T4: §13 Future-Work-Erweiterung (optional, falls Platz)

Falls Budget es erlaubt: in §13 erwähnen, dass das Read-Validator-System
prinzipiell weitere Regeln unterstützen kann — zwei konkrete Beispiele:

- **LIMIT-Enforcement:** MATCH auf Top-Level-Knoten (z. B.
  `AssetAdministrationShell`, `Submodel`) ohne ID-/semanticId-Filter und
  ohne LIMIT erzeugt bei großen Datenbeständen Full-Graph-Scans. Eine
  zusätzliche Validator-Regel würde solche Queries abfangen.
- **Cursor-basiertes Paginieren:** statt `SKIP N` (O(n)) den Cursor-Ansatz
  (`WHERE id > $last_id ORDER BY id ASC LIMIT N`) als Manual-Rezept und
  optional als Validator-Empfehlung verankern.

Zeigt Erweiterbarkeit ohne Implementierungsverpflichtung. Passt als 2–3
Sätze ans Ende der §13-Validator-Passage aus
[[task-paper-write-validation-defense]].

### T5: Cross-Refs & Konsistenz

- Konsistenz mit [[task-paper-modeling-vs-pragmatics-anecdote]] und
  Write-Validation-Befund prüfen — gemeinsame Klammer „Layered Determinism"
  konsistent durchziehen.
- Bench-B-Tabelle/Zahlen ggf. nachziehen.
- Pre/Post-Rohdaten in `tests/agent-tests/results/` archivieren.

## Acceptance Criteria

- Pre/Post-Mode-Bench gefahren, Rohdaten archiviert, Tabelle Variant ×
  Case × Mode erzeugt.
- Stressed-Fixture-Bench zeigt klare Verbesserung von `off` → `strict`
  (oder dokumentierter Grund warum nicht).
- Paper enthält den Read-Validation-Befund an einer der drei Stellen.
- Bei Option 1: Layered-Determinism-Klammer mit den anderen zwei
  Anekdoten ist explizit gemacht.
- Absatz nennt konkret: (a) AAS-spezifische Failure-Mode (idShort-Sub-
  string-Lookup statt semanticId), (b) Manual-Disziplin reicht nicht,
  (c) deterministischer Validator als Fix, (d) Pre/Post-Zahlen.
- Keine Architektur-Leaks, keine harten IDTA-URIs im Fließtext.
- Konsistenz mit Bench-B-Zahlen und Retrieval-Sektion geprüft.

## References

- Quellen-Task: [[task-read-validation-gap]] — liefert Validator + Stress-Fixtures.
- Verwandte Anekdoten: [[task-paper-modeling-vs-pragmatics-anecdote]], [[task-write-tool-validation-gap]].
- Engineering-Philosophie: [[feedback-agent-constraint-philosophy]] (auto-memory).
- Paper-Dateien (Kandidaten): `paper/etfa2026/content/10-evaluation.tex`, `11-discussion.tex`, `12-limitations.tex`, `06-mcp-server.tex`, `08-retrieval-pipeline.tex`.
- Live-Test-Befund: `tests/agent-tests/results/run_2026-05-15T18-06-32Z.json` (mir100_max_speed, ReAct).
- Hintergrund: `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md` Anti-Patterns #3 + #4.
