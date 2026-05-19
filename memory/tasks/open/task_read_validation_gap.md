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

### T1 — MCP-Side Cypher-Validator ✅ DONE (2026-05-18)

`mcp-server/src/aas_hybrid_mcp/cypher_validator.py` implementiert:

- Regex-basierter Pre-Check vor Cypher-Execution in `query_aas_graph`.
- 4 Regeln: `toLower_id_contains`, `idShort_contains_or_regex`, `id_contains_or_regex`, `assetType_match`
- Mode toggle via env `STRICT_READ_VALIDATION` (default `off`):
  - `off` → no-op
  - `warn` → query runs, `_warnings` im Response
  - `strict` → `{"error": "forbidden_pattern", "violations": [...], "hint": "..."}`, kein Neo4j-Call
- 24 Unit-Tests in `mcp-server/src/tests/test_cypher_validator.py` — alle grün
- `docker-compose.yml` trägt `STRICT_READ_VALIDATION: "off"` (kommentiert als Eval-Hebel)

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

### T4 — Eval-Strategie: Validator-Rejection-Log als Messung

**Pre-Validator-Zustand ist bereits dokumentiert** (kein separater Baseline-Run nötig):

| Run | Zeitstempel | Variante | Erster Lookup | CONTAINS? |
|-----|------------|----------|--------------|-----------|
| 1 | 2026-05-18T11:59 | react | direkt query_aas_graph | ✗ |
| 2 | 2026-05-18T12:18 | react | query nach get_graph_schema + get_templates_index | ✗ |
| 3 | 2026-05-18T12:33 | react | direkt query_aas_graph | ✗ |

3/3 Runs, 100% CONTAINS-Rate auf dem ersten Asset-Lookup. Existence-Claim ist belegt.

**Der Validator ist selbst die Messung.** `STRICT_READ_VALIDATION=strict` ist
deterministisch — jede Rejection ist ein harter Befund, kein stochastisches Ergebnis.

Eval-Plan:
1. Validator implementieren (T1), `STRICT_READ_VALIDATION=strict` setzen
2. Dieselbe Query ("Wie schnell kann der MiR100 maximal fahren?") N=3 × react laufen lassen
3. Rejection-Log auswerten: wie viele Queries wurden geblockt? Hat sich der Agent danach selbst korrigiert?
4. Optional: `naming_stress`-Fixture (T2) zeigen dass `STRICT_READ_VALIDATION=off` dort lautlos falsch antwortet

Auswertung für Paper (2 Sätze + Tabelle):

| Mode | Anti-Pattern-Queries | Geblockt | Agent korrigiert |
|------|---------------------|----------|-----------------|
| off  | x/N                 | 0/N      | —               |
| strict | x/N              | x/N      | y/N             |

**Kein Multi-Modell-Sweep hier** — der gehört zu `task_paper_pattern_modelsize_eval`
(Qwen 3.5: 2B/9B/27B/122B/397B). Der Validator-Befund gilt mit 27B als Existenz-Beleg;
Modellgrößen-Abhängigkeit ist eine separate Frage.

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
