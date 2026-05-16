---
name: Task – Read Tool Validation Gap (idShort/id Substring Lookup)
description: Quantify and mitigate the agent's habit of using `idShort`/`id` substring matches as a semantic lookup mechanism, despite the manual explicitly forbidding it (cypher.md Anti-Patterns #3 + #4). Capture the finding for the paper.
type: task
status: open
priority: high
---

## Background

Bei der Frage „Wie schnell kann der MiR100 maximal fahren?" (2026-05-15,
Smoke-Run aus dem neuen Test-Framework) generierte `aas-agent:react` folgende
Cypher-Query als ersten Schritt:

```cypher
MATCH (aas:AssetAdministrationShell)-[:MANAGES_ASSET]->(asset:Asset)
WHERE toLower(aas.idShort)    CONTAINS 'mir100'
   OR toLower(asset.assetType) CONTAINS 'mir100'
   OR toLower(aas.id)          CONTAINS 'mir100'
```

Das verletzt zwei explizite Manual-Regeln in `cypher.md` Anti-Patterns:

- **#3** — `assetType` ist oft `null`, taugt nicht als Lookup.
- **#4** — `idShort` nie für domain reasoning; nur als entry point wenn der
  Nutzer das Asset explizit beim Namen nennt. Struktur/Zweck immer via
  Submodels und ihre semanticIds verifizieren.

Der eigentliche Befund: **in unseren Fixtures funktioniert die falsche Query
trotzdem**, weil unsere Naming-Konvention strikt ist (`MiR100_001`,
`urn:asset:mir100:001`). Im realen Deployment mit `Roboter_47` oder
`Cell-3-Mobile-Unit` als idShort liefert die Query null Rows — und der Agent
gibt entweder leere Antworten zurück oder erfindet etwas.

Das ist analog zu den anderen Validation-Gap-Befunden:

- [[task-write-tool-validation-gap]] — Element-Writes umgehen den Submodel-
  Validator. Lösung: MCP-Side-Validation / Slot-Filling.
- [[task-container-location-traversal-prompt-fix]] — MANAGES_ASSET-Selbst-
  referenz statt Container-Traversal. Lösung: Prompt-Regel.
- **NEU (dieser Task)** — Cypher-Read mit `idShort/id CONTAINS` umgeht
  semantische Disziplin. Lösung: MCP-Side-Validation des Cypher-Body am
  Read-Endpoint.

## Goals

- Belastbar belegen, wie häufig Varianten beim Read die idShort-/id-Substring-
  Heuristik nutzen statt semanticId-basiertes Lookup.
- Zeigen, dass die Heuristik in „messy" Daten (umbenannte idShort) bricht,
  in unseren Fixtures aber zufällig funktioniert.
- MCP-Side-Validator als optionalen Safety-Net implementieren und Pre/Post-
  Bench fahren.
- Befund ins Paper aufnehmen (siehe [[task-paper-read-validation-anecdote]]).

## Subtasks

### T1 — MCP-Side Cypher-Validator

`mcp-server/src/aas_hybrid_mcp/cypher_validator.py` (neu):

- Regex-basierter Pre-Check vor Cypher-Execution in `query_aas_graph`.
- Verbotene Patterns (default):
  - `\btoLower\([^)]*\.id(Short)?\)\s+CONTAINS\b`
  - `\b[a-zA-Z_]\w*\.idShort\s+(CONTAINS|=~)\b`
  - `\b[a-zA-Z_]\w*\.id\s+(CONTAINS|=~)\b` (URN substring lookup — same problem)
  - `\b[a-zA-Z_]\w*\.assetType\s+(CONTAINS|=)\b`
- Mode toggle via env `STRICT_READ_VALIDATION` (default `off`):
  - `off` → silent, query runs as-is (current behavior)
  - `warn` → query runs, response carries `_warnings: [{rule, line, ...}]`
  - `strict` → response is a structured error: `{"error": "forbidden_pattern", "rule": "...", "hint": "see cypher.md #4"}`, no Cypher execution
- Test-Coverage: unit tests in `mcp-server/src/tests/test_cypher_validator.py`
  mit positive + negative samples (legitimate `idShort` as entry point
  must NOT be flagged: e.g. `WHERE aas.idShort = 'MiR100_Type'` is fine,
  it's the CONTAINS / regex form that's forbidden).

### T2 — Naming-Stress-Fixtures

Künstlich umbenannte Variante eines bestehenden Type-Shells, um zu zeigen
dass die idShort-Heuristik bricht:

- `aasx/MiR100_Type_stressed.aasx` — Kopie von `MiR100_Type.aasx` mit:
  - `idShort` ≠ enthält "MiR100"  (z.B. `MobilePlatformV3`)
  - `id` ≠ enthält "mir100"        (z.B. `urn:fabrik:device:9f2a-7c1`)
  - **Asset-Properties bleiben unverändert** — semanticId für
    `MaxLinearSpeed` ist nach wie vor da, der „echte" Lookup-Pfad
    funktioniert weiter.
- AAS-Environment-Bind-Mount in `docker-compose.yml` ergänzen.
- Neo4j + Weaviate reindexieren (Kafka-Replay).
- Dokumentieren in `memory/aas_test_data_fixtures.md`.

### T3 — Test-Cases im Framework

`tests/agent-tests/cases/naming_stress.yaml` (neu):

- 3–5 Queries die nach dem stressed Asset fragen, *ohne* den künstlichen
  Namen zu erwähnen — der Agent muss über semanticId / DERIVED_FROM
  routen. Beispiele:
  - „Wie schnell ist der MobilePlatformV3?" (nennt den korrekten Namen → Agent muss `idShort = ...` als entry-point benutzen, NICHT substring CONTAINS auf "mir100")
  - „Welche mobilen Roboter haben mehr als 100kg Nutzlast?" (kein Name → reine semanticId-Klassifikation)
  - „Wie schnell kann der Roboter mit Asset-ID `urn:fabrik:device:9f2a-7c1` fahren?" (id explizit → `MATCH ... {id: $id}` ist erlaubt, `CONTAINS` nicht)
- `forbidden_cypher_patterns` pro Case mit den Anti-Pattern-Regexen.
- `llm_criteria` formuliert: „Antwort liefert korrekte Spec-Werte und
  Agent hat semanticId / DERIVED_FROM / direkten id-Match benutzt,
  keinen idShort-substring-Lookup."

`tests/agent-tests/cases/anti_pattern_idShort_lookup.yaml` (neu, sofort):

- Der konkrete Befund vom 2026-05-15 als Smoke-Case mit
  `forbidden_cypher_patterns` und expliziter Doku in Kommentaren.

### T4 — Pre/Post-Bench fahren

- Baseline: `STRICT_READ_VALIDATION=off`, alle Naming-Stress + Anti-Pattern
  Cases × 4 Variants × N≥3 Wiederholungen. Erwartung: in unseren
  unstressed Fixtures läufts trotz Anti-Pattern; in stressed Fixtures
  scheitert es.
- Mode `warn`: Erwartung wie Baseline, aber `_warnings` im Response → Agent
  sollte (idealerweise) bei der zweiten Iteration korrigieren.
- Mode `strict`: Erwartung — Agent muss von Anfang an semanticId-Path
  nehmen; Erfolgsrate auf stressed Fixtures sollte steigen.
- Rohdaten in `tests/agent-tests/results/` archivieren.
- Auswerten: Per-Variant Erfolgsrate × Mode × Fixture-Set.

### T5 — Paper-Einbindung

Siehe [[task-paper-read-validation-anecdote]].

## Open Questions

- **Granularität des Pre-Checks** — reicht Regex, oder brauchen wir
  AST-Parsing der Cypher-Query? Regex hat false positives bei Property-
  Namen wie `assetTypeText` (würde von `\.assetType\b` getroffen). Für
  Paper-Run reicht Regex; für Production wäre AST sauberer.
- **Was tun mit legitimen `idShort CONTAINS '_Type'` Cases?** Z.B. der
  Wunsch „liste alle Type-Shells". Argument: dafür gibts ConceptDescriptions
  oder `assetKind`. Wenn die nicht greifen → das ist genau die Datenqualitäts-
  Annahme aus [[task-paper-data-quality-assumption]].
- **Slot-Filling-Variante** — analog zu write_tool: könnten wir ein
  `find_assets_by_semantic_class(class_uri)` Tool anbieten, das den
  Cypher intern baut? Schöner aber größerer Eingriff.

## Acceptance Criteria

- `cypher_validator.py` existiert mit Mode-Toggle + Unit-Tests.
- Naming-Stress-Fixture (mind. 1 umbenanntes Asset) im AAS-Repo verfügbar
  und reproduzierbar via `./up.sh --vllm`.
- Test-Cases (anti_pattern_idShort_lookup + naming_stress) im Framework.
- Pre/Post-Bench-Rohdaten archiviert (4 Variants × N≥3 × 3 Modes).
- Tabelle: Erfolgsrate je Variant × Mode auf stressed vs. unstressed.
- Paper-Anekdote-Task ([[task-paper-read-validation-anecdote]]) referenziert
  diese Zahlen.
- Mode `off` ist Default, kein Regression-Risiko für bestehende Deployments.

## References

- Manual: `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md` Anti-Patterns #3 + #4
- Trace mit Anti-Pattern: `tests/agent-tests/results/run_2026-05-15T18-06-32Z.json` (mir100_max_speed, ReAct)
- Verwandt: [[task-write-tool-validation-gap]], [[task-container-location-traversal-prompt-fix]], [[task-paper-read-validation-anecdote]]
- Test-Framework: `tests/agent-tests/`
