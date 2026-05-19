---
name: Task - Write-Path Validation Defense (Paper + Code)
description: Fault-injection matrix to ground the validation argument empirically; reframe MCP-side validator as implementation-independence shim + Producer-vs-Write-Path-Side framework; explicit validation reporting in put_submodel response
type: task
status: open
priority: high
---

## Summary

Unsere 6 Write-Tools machen heute ungleich viel Validierung — das ist im Paper
bisher nicht sauber ausdifferenziert. Reviewer-Risiko: **Torben Miny** (RWTH,
Co-Autor Garmaev et al. 2023), **Marko Ristin** (`aas-core3.0`), **IDTA /
`aas-test-engines`-Maintainer**.

**Linie nach Diskussion (2026-05-14):** drei zusammenhängende Reframes,
empirisch durch kleine 2-Kanal Fault-Injection gestützt:

1. **MCP-Layer als Agent-side Validation Shim**, motiviert durch zwei
   Komplementärgründe: (a) **Implementierungsheterogenität** — Eclipse
   BaSyx Java ≠ basyx-dotnet ≠ FA³ST ≠ AASX Server haben unterschiedliche
   Strict-Levels und Error-Schemata; (b) **Operational Mode** — die
   produzierende Seite ist eine LLM-Inference, kein IDE-gestützter
   Entwickler, was die Voraussetzungen der existierenden Tooling-
   Landschaft verschiebt. Konkret arbeitet der Shim in zwei Stufen:
   - Metamodel: `read_aas_json_file(..., failsafe=False)` aus `basyx-
     python-sdk` — implementierungsunabhängig, strict, läuft auf
     jedem Write
   - Template Conformance: **`aas-submodel-template-to-py` von Garmaev
     et al. (2023) im Write-Mode** (siehe Reframe 2)
2. **Wir reuse das Tool von Garmaev et al. (2023) im Write-Mode statt
   Producer-Mode.** Das ist die saubere Garmaev-Positionierung:
   - **Producer-Mode (Garmaev 2023):** Generator → Submodel-spezifische
     Python-Klassen → Entwickler instanziiert Klasse beim Code-Schreiben.
     Mandatory/Cardinality-Constraints werden im Konstruktor erzwungen,
     IDE unterstützt mit Type-Hints.
   - **Write-Mode (wir):** **Selbes** Generator-Output → bei eingehendem
     JSON-Submodel via `put_submodel` versuchen wir, die generierte
     Klasse zur Laufzeit zu instanziieren (nach SDK-Strict-Deserialise).
     Exception aus dem Konstruktor = Template-Conformance-Verletzung.
   - Beziehung ist **Adoption + Modus-Erweiterung**, nicht Konkurrenz
     oder „Baseline". Miny als Reviewer sieht sein Tool korrekt zitiert
     und in neuem Kontext genutzt.
3. **Validation implicit in `put_submodel`, explicit im Response.** Status-
   Feld unterscheidet `passed` / `failed: <details>` / `skipped: no class
   for <semanticId>` — kein silent fallback mehr. Element- und AAS-Writes
   melden nur `metamodel`-Status (Template-Conformance ist strukturell
   n/a, nicht „passed").

Empirische Grundlage: **2-Kanal Fault-Injection (BaSyx-Java direkt vs.
Python-SDK strict)**, 3–4 Faults, ~2 Stunden Aufwand. Kein Agent, keine
Happy-Path-Ablation, keine 3×8-Matrix.

*Interne Motivation (nicht ins Paper):* ein Kollege hatte sich beschwert,
dass er über das Python SDK keine kaputten Objekte ablegen kann — das war
der Hinweis, dass die SDK-Strictness selbst der Hauptdefensiv-Layer ist.
Im Paper steht **nur** das empirisch belegte Resultat aus T0+T1, nicht
die Anekdote.

## Reframe 1 (Detail): Agent-side Validation Shim

Beide Motivationen zusammengezogen — Implementierungsheterogenität +
LLM-als-Producer:

**Implementierungs-Spread:** „BaSyx-Fehlerfeedback" ist kein definiertes
Konzept. Eclipse BaSyx Java, basyx-dotnet, FA³ST Service, AASX Server,
basyx-python-sdk Reference-Repo haben:
- unterschiedliche Error-Response-Schemas
- unterschiedliche Strict-Levels bei Deserialisierung
- unterschiedliche Template-Awareness (meist: keine)
- ggf. unterschiedliche Spec-Versionen

**Operational Mode shift:** wenn der Producer kein IDE-gestützter
Entwickler ist sondern ein LLM, das JSON erzeugt, dann verschiebt sich
die Voraussetzung der existierenden Tooling-Landschaft. Garmaev's
Klassen-API + IDE-Support wirken nicht beim Coden (es gibt keinen
Coding-Step), sondern müssen zur Laufzeit gegen erzeugtes JSON greifen.

Konsequenzen für §6/§9/§11/§12:
- **§6/§12 muss BaSyx-Version pinnen**: „We evaluate against Eclipse
  BaSyx Java Server vX.Y.Z (commit ...). Error behavior is
  implementation-specific."
- **Paper-Argument für §11**: „The MCP layer applies the BaSyx Python
  SDK's strict metamodel deserialisation to every write, together with
  the submodel-class generator of Garmaev et al. (2023) applied in
  write-mode, providing the agent with implementation-independent
  diagnostics that are strictly stronger than what the underlying AAS
  server enforces at receive time."

## Reframe 2 (Detail): Producer-Mode vs. Write-Mode mit demselben Generator

Garmaev et al. 2023 stellen den **Generator**
(`aas-submodel-template-to-py`) bereit und nutzen ihn im **Producer-Mode**:

```
template.xml → generator → SubmodelClass.py → Entwickler instanziiert in Code
                                              IDE prüft Mandatory + Cardinality
```

Wir nutzen **denselben Generator-Output** im **Write-Mode**:

```
incoming JSON → SDK strict deserialize → versuch Konstruktor-Instantiation
                                          der generierten Klasse mit JSON-Inhalt
                                          Exception → Template-Conformance-Verletzung
```

Out-of-scope ihres Papers (von uns geerbt):
- `AllowedRange`/`AllowedValue`-Qualifier (ihr Future Work §VI)
- Templates mit Extension-Points wie TechnicalData (ihr Validation-Gap §V)

Diese Grenzen erben sich automatisch in unseren Write-Mode-Validator und
werden in §12 ehrlich benannt.

**Saubere Garmaev-Positionierung**: Adoption + Modus-Erweiterung, **kein
Vergleich**, **kein „surpass"**, **keine „Baseline"**.

## Reframe 3 (Detail): Explicit Validation Reporting

`put_submodel` validiert **immer** intern (kein opt-in vom Agent) und gibt
das Ergebnis strukturiert im Response zurück:

```json
{
  "stored": true,
  "validation": {
    "metamodel": "passed",
    "template_conformance": "passed"
                          | "failed: <reason>"
                          | "skipped: no template class for <semanticId>"
  }
}
```

Bei `template_conformance: failed` → kein Store, Fehler-Response. Bei
`skipped` → Store findet statt, Agent sieht aber dass keine Template-
Verifikation lief (kein silent pass).

`put_aas` und `put_submodel_element`: nur `metamodel` im Response,
`template_conformance` nicht vorhanden (nicht „passed", sondern strukturell
nicht anwendbar). Im Paper §6 explizit benennen.

`delete_*`: gar keine Validation. §12 als Limitation.

## Heutige Lage (Code-Audit `mcp-server/src/aas_hybrid_mcp/`)

| Tool | Metamodel | Template Conformance | Reporting heute |
|------|-----------|----------------------|------------------|
| `put_aas` | ✅ | ❌ (strukturell n/a) | implizit, kein Status-Feld |
| `put_submodel` | ✅ | ✅ via `aas-submodel-to-py`; **silent fallback** | implizit, kein Status-Feld |
| `put_submodel_element` | ✅ (Wrapper) | ❌ (Kontext fehlt) | implizit |
| `delete_*` | nur non-empty | ❌ | — |

## Subtasks

### T0: BaSyx Java Coverage Audit (Hauptbeleg)

**Hauptpfad der Argumentation.** Bevor wir behaupten „BaSyx fängt X nicht":
**im Source belegen**, nicht raten.

- Source-Read: `basyx-java-server-sdk` (Spring Boot, AAS Repository
  Component) — was prüft die Deserialisierung-Pipeline, welche
  Constraints sind im ObjectMapper, gibt es nach Deserialize einen
  Validator-Hook, was passiert bei strict vs. lenient JSON-Mapping?
- Spec-Read: IDTA OpenAPI für AAS Repository v3 — welche Constraints sind
  als Pflicht-HTTP-Statuscodes formuliert, welche nur als Prosa, welche
  delegieren an „implementation-defined behavior"?
- Output: Memo `memory/basyx_java_validation_audit.md` mit Klassen,
  Pfaden, ObjectMapper-Konfig, Test-Coverage-Beobachtungen
- BaSyx-Version + Commit pinnen, die in `docker-compose.yml` läuft (für
  §6/§12 Versionspinning)

### T1: 2-Kanal Fault Injection (Anker, klein)

**Decoration zu T0, kein Hauptbeleg.** Drei bis vier Fault-Klassen, zwei
Kanäle, ~2 Stunden Aufwand. Reine Existenzbeweise im Paper, keine
Coverage-Matrix.

**Fault-Klassen (Pick 3–4):**

| ID | Fehler | Erwartung |
|----|--------|-----------|
| F1 | mandatory SME fehlt | A: accept (BaSyx hat keine Template-Registry); B: accept (SDK prüft Metamodel, nicht Template) → motiviert Template-Validator |
| F3 | falscher `valueType` (`xs:string` für `xs:int`-Property) | A: ?; B: reject → belegt SDK > BaSyx im Metamodel |
| F4 | extra SME im Submodel, im Template nicht vorgesehen | beide accept → belegt Template-Closure-Gap (Garmaev V) |
| F7 | Property mit `value` aber ohne `valueType` | A: ?; B: reject → SDK-Strict-Punkt |

**Zwei Kanäle:**

- **A — direkt gegen BaSyx Java:**
  ```bash
  curl -X PUT http://basyx:8081/submodels/<id> \
    -H "Content-Type: application/json" \
    -d @broken_submodel.json
  ```
  → HTTP-Statuscode + Body protokollieren

- **B — Python SDK strict (ohne HTTP, ohne MCP, ohne Agent):**
  ```python
  from basyx.aas.adapter.json import read_aas_json_file
  read_aas_json_file(io.StringIO(broken_json), failsafe=False)
  ```
  → Exception-Typ + Message protokollieren

Den **dritten Kanal** (MCP `put_submodel`) sparen wir — der ist tautologisch
= Python SDK strict + Template-Validator obendrauf; Mehrwert lässt sich aus
`template_validator.py`-Read herleiten, nicht empirisch.

**Output:** `memory/fault_injection_matrix.md` als kleine Tabelle:

| Fault | BaSyx direct (curl) | Python SDK strict | Reading |
|-------|---------------------|-------------------|---------|
| F1 | … | … | beide accept → Template-Gap |
| F3 | … | … | SDK strenger als BaSyx |
| F4 | … | … | beide accept → Template-Closure-Gap |

**Auswertung — was wir paperseitig konkret behaupten:**
- Existenz von Fällen, wo SDK rejects + BaSyx accepts → empirischer Beleg
  für „Python-SDK-Strict als Portabilitäts-Shim" (Reframe 1)
- Existenz von Fällen, wo beide accepten → empirischer Beleg für
  „Template-Validator hat eigene Coverage" (Reframe 4)
- Eine kleine Tabelle in §11 oder §12 mit den 3–4 Faults zeigt
  konkret-anschaulich, was sonst nur abstrakt argumentiert wäre

### T2: Code-Änderungen — Response-Schema + Cleanup

**Stand 2026-05-18 (teilweise umgesetzt):**

`REQUIRE_TEMPLATE_VALIDATOR`-Flag in `template_validator.py` eingebaut:
- Gesetzt: kein semanticId → Error; semanticId ohne Validator → Error mit supported-Liste
- Nicht gesetzt: Runtime-Error (kein Default, muss explizit konfiguriert sein)
- Fehlermeldungen sind agenten-tauglich: verweisen auf `get_templates_index()` und listen registrierte semanticIds auf

**Semantik-Änderung gegenüber ursprünglichem Plan:**
`skipped: no class for <semanticId>` existiert bei `REQUIRE_TEMPLATE_VALIDATOR=true` nicht mehr —
stattdessen harter Fehler. `skipped` bleibt nur bei `REQUIRE_TEMPLATE_VALIDATOR=false` (permissiver Mode).
In §9/§12 muss das klar unterschieden werden: permissiver Mode für generische Deployments,
strikter Mode für bekannte Use-Cases.

**Noch offen:**
- `put_submodel` Response gibt noch kein strukturiertes `validation`-Feld zurück
  (`{"stored": true, "validation": {"metamodel": "passed", "template_conformance": "..."}}`)
- `template_validator.validate_conformance` gibt noch `Optional[str]` zurück, kein typisiertes Result-Objekt
- `put_aas` und `put_submodel_element` haben noch kein explizites Metamodel-Status-Feld im Response

Diese drei Punkte sind für Paper-Reframe 3 (Explicit Validation Reporting) noch zu implementieren.

Cleanup-Entscheidung **nach T1**:
- Falls T1 zeigt „Validator fängt Klassen, die BaSyx nicht fängt": Code
  bleibt, Paper sagt empirisch wieso
- Falls T1 zeigt „Validator deckt nichts Zusätzliches ab": Code kann zu
  **Dry-Run-Tool** umgewidmet werden (`validate_submodel_against_template`),
  Write-Pfad ruft nur Metamodel-SDK

### T3: Error-Enrichment-Layer

Aus T1-Spalte „Fehlermeldungs-Qualität" abgeleitet:
- Wrapper um `basyx_client.put_*` / `delete_*`: HTTP-Fehler parsen, Felder
  extrahieren (Property, Constraint-Typ, semanticId-Stelle)
- Strukturiertes JSON zurück, nicht raw text
- Klein, ehrlich, benchmarkbar (Variante mit/ohne via Bench-B)
- Paper: legitimer MCP-Beitrag unabhängig von Template-Conformance-Diskussion

### T4: Paper-Sektionen umschreiben

- **§6 (Architecture):**
  - Zwei Validation-Stufen explizit (metamodel + template conformance)
  - Tabelle: welches Tool hat welche Stufe; explicit reporting im Response
  - BaSyx-Versionspinning
- **§9 (Write-Loop):**
  - Write-Loop = PUT → strukturierte Antwort (stored/validation/error) →
    Agent self-correction
- **§11 (Discussion):**
  - Producer-Side vs. Write-Path-Side mit `garmaev2023submodel` zitiert
  - Implementation-Independence-Argument für MCP-Layer
  - Fault-Injection-Matrix-Ergebnis referenziert
- **§12 (Limitations):**
  - Element-Write- und Delete-Tool-Disclaimer (Template-Conformance
    strukturell n/a)
  - Implementierungsabhängigkeit (gepinnt auf konkrete BaSyx-Version)
  - Bekannte Validator-Lücken (z. B. `AllowedRange` aus Garmaev FW
    übernommen — was wir auch nicht prüfen)
- **§13 (Future Work):**
  - Server-side Validating Plugin (analog Neo4j-Kafka-Plugin)
  - Validating Proxy mit ETag/If-Match Optimistic Concurrency Control
  - `aas-test-engines`-Integration als zusätzliche Stage
  - White Spaces aus T6

### T5: References einbauen (`main.bib`)

```bibtex
@inproceedings{garmaev2023submodel,
  author={Garmaev, Igor and Miny, Torben and Kleinert, Tobias},
  title={Automatic Generation of Submodel-Specific Classes with Predefined
         Meta-Information Based on Submodel Templates},
  booktitle={IEEE ETFA},
  year={2023},
  doi={10.1109/ETFA54631.2023.10275464}
}

@inproceedings{miny2024deployment,
  author={Miny, Torben and others},
  title={Deployment of Asset Administration Shell Submodels},
  booktitle={IEEE ETFA},
  year={2024}
}

@inproceedings{eichelberger2024modeldriven,
  author={Eichelberger, Holger and Weber, Alexander},
  title={Model-driven Realization of IDTA Submodel Specifications:
         The Good, the Bad, the Incompatible?},
  booktitle={IEEE ETFA},
  year={2024},
  eprint={2406.14470},
  archivePrefix={arXiv}
}

@software{idta_aastest,
  author={{Industrial Digital Twin Association}},
  title={aas-test-engines},
  url={https://github.com/admin-shell-io/aas-test-engines},
  year={2024}
}

@software{aascore3python,
  author={Ristin, Marko and others},
  title={aas-core3.0-python — Verification module (AASd-129, AASd-119)},
  url={https://github.com/aas-core-works/aas-core3.0-python},
  year={2024}
}
```

Paper-Sätze, die jetzt belegbar sind:
- *„We adopt the submodel-class generator of Garmaev et al. (2023,
  `aas-submodel-template-to-py`) and apply it in write-mode: where the
  original work uses the generated classes to support developer-time
  submodel construction in an IDE, we instantiate them at write-time
  against incoming JSON, treating constructor exceptions as template-
  conformance violations. The constraint coverage we inherit therefore
  matches theirs — Multiplicity/Cardinality qualifiers — and we share
  their open limitations on `AllowedRange`/`AllowedValue` and on
  templates with extension points such as TechnicalData."*
- *„Backend-side enforcement could leverage `aas-test-engines` (IDTA) or
  the verification module of `aas-core3.0-python` (AASd-129, AASd-119);
  to our knowledge neither has been integrated into the BaSyx write path
  in peer-reviewed work."*
- *„BaSyx error reporting is implementation-specific; we pin our
  evaluation to Eclipse BaSyx Java Server vX.Y.Z. A client-side
  validation shim normalises diagnostic shape across heterogeneous AAS
  server implementations, which a server-side plugin cannot do."*

### T6: White-Space-Belegung (für §13)

Aus dem 2026-05-14 Lit-Scan bewusst genutzte Lücken:
1. Kein peer-reviewed Paper zu `aas-test-engines` oder `aas-core3.0-python
   verification` als BaSyx-Write-Path-Stage
2. Keine AAS-spezifische Plugin-/Proxy-Architektur für Write-Path-
   Constraint-Enforcement
3. Keine Behandlung von ETag/Optimistic Concurrency Control auf
   AAS-REST-APIs

## Empfehlung — wie wir damit umgehen

**Phase A (vor Submission, ~2 Tage Gesamtaufwand):**

1. **T0 BaSyx-Coverage-Audit (~halber Tag)** — Source-Lesen + Spec-Lesen +
   Memo. **Hauptbeleg.** Liefert die paper-zitierbare Aussage.
2. **T1 2-Kanal Fault Injection (~2 Stunden)** — 3–4 Faults, curl direct
   vs. Python SDK strict. Reine Decoration mit konkreten Beispielen für
   §11/§12, kein Hauptbeleg.
3. **T2 Response-Schema-Refactor (~halber Tag)** — auf jeden Fall machen,
   unabhängig vom T1-Ausgang. Macht heutiges Silent-Fallback explizit.
4. **T5 References + T4 Paper-Reframe (~Tag)** — kann parallel zu T0/T1
   laufen, weil Argumentation robust gegen T1-Ausgang ist.

**Phase B (nach T1, vor Submission):**

- T3 Error-Enrichment: aktivieren wenn T1 zeigt, dass rohe BaSyx-Fehler
  unzureichend sind (sehr wahrscheinlicher Pfad)
- Endgültige Code-Entscheidung in T2 (Cleanup vs. behalten) anhand
  T1-Daten

**Phase C (nach Submission):**

- BaSyx-Validating-Plugin als Open-Source-Side-Project
- Beitrag an `aas-test-engines` als Write-Path-Modul
- Beides explizit außerhalb ETFA-2026 Scope

## Acceptance Criteria

- T0 BaSyx-Audit-Memo existiert mit gepinnter Version + Source-Belegen
- T1 2-Kanal Fault-Tabelle existiert, 3–4 Faults dokumentiert
- `put_submodel` Response enthält strukturiertes `validation`-Feld;
  `put_aas` und `put_submodel_element` analog (nur metamodel)
- Silent fallback in `template_validator.py` durch explizites `skipped:
  no class`-Reporting ersetzt
- `main.bib` enthält die 5 Stubs
- §6, §9, §11, §12, §13 reformuliert + BaSyx-Version explizit gepinnt
- White Spaces aus T6 in §13 sichtbar adressiert

## Non-Goals

- **Kein** Server-Plugin im aktuellen Paper-Scope
- **Kein** `AllowedRange`/`AllowedValue`-Check (übernehmen die Garmaev-
  Future-Work-Limitation)
- **Keine** ETag-Implementation
- **Keine** Behauptung „wir integrieren `aas-test-engines`" ohne dass
  das wirklich geschieht
- **Keine** Multi-Implementation-Eval (kein FA³ST, kein basyx-dotnet)
  — nur Eclipse BaSyx Java mit klarer Versionspinning

## Paper-Diff-Plan

Konkret pro `.tex`-Datei, was wo eingefügt/geändert wird:

**`content/06-architecture.tex`**
- Neuer Absatz/Subsection nach der MCP-Server-Beschreibung: *„Validation
  layers"* — listet die zwei Stufen (Metamodel via Python SDK strict;
  Template Conformance via Garmaev's generator in write-mode). Tabelle
  3 Spalten × 4 Zeilen: Tool / Metamodel / Template Conformance.
- Fußnote zur BaSyx-Version: `eclipse-basyx/basyx-java-server-sdk` vX.Y.Z.

**`content/09-write-loop.tex`**
- Write-Loop-Beschreibung umstellen: PUT → strukturierte Response mit
  `validation`-Feld → Agent self-correction. JSON-Snippet einfügen
  (`stored` + `validation.metamodel` + `validation.template_conformance`).

**`content/11-discussion.tex`**
- Neuer Absatz „Where validation lives": (a) Producer-Mode vs.
  Write-Mode mit demselben Generator, Garmaev zitiert; (b) Agent-side
  Shim wegen Implementierungsheterogenität; (c) Hinweis dass
  Server-side Plugin architektonisch sauberer aber nicht
  implementierungs-übergreifend wäre.
- Kleine Tabelle aus T1 (3–4 Faults × 2 Kanäle) — Existenzbeweis.

**`content/12-limitations.tex`**
- Element-/AAS-Write-Disclaimer (Template-Conformance strukturell n/a
  bei diesen Tools).
- Delete-Tool-Disclaimer (gar keine Validierung).
- Geerbte Garmaev-Limits explizit nennen
  (AllowedRange/AllowedValue, TechnicalData-style extension points).
- Implementation-Specificity-Disclaimer (gepinnt auf BaSyx-Java vX.Y.Z).

**`content/13-future-work.tex`**
- Subsection „Server-side validation": Plugin-Variante (analog Neo4j-
  Kafka-Plugin), Proxy-Variante mit ETag/Optimistic Concurrency,
  `aas-test-engines`-Integration. Mit den drei White-Spaces aus T6 als
  Belegen.

**`main.bib`**
- Fünf Stubs aus T5 einfügen: `garmaev2023submodel`,
  `miny2024deployment`, `eichelberger2024modeldriven`, `idta_aastest`,
  `aascore3python`.

## References

- Code: `mcp-server/src/aas_hybrid_mcp/tools/write_tools.py`,
  `mcp-server/src/aas_hybrid_mcp/template_validator.py`
- Generator (extern): `aas-submodel-template-to-py`
  (https://github.com/rwth-iat/aas-submodel-template-to-py)
- BaSyx Java: `https://github.com/eclipse-basyx/basyx-java-server-sdk`
- Paper-Sections: `paper/etfa2026/content/06-architecture.tex`,
  `09-write-loop.tex`, `11-discussion.tex`, `12-limitations.tex`,
  `13-future-work.tex`
- Bibliography: `paper/etfa2026/main.bib`
- Bench-B-Protokoll: `memory/bench_b_evaluation.md`
- Schwester-Tasks: [[task_paper_claim_audit]], [[task_paper_style_review]],
  [[task_paper_future_work_template_cypher]]
- Lit-Scan-Output: 2026-05-14 (Explore-Agent-Run)
