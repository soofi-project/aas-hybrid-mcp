---
name: Task - Future Work — AAS Query IR: Between JSON and Cypher
description: Paper Future-Work-Hypothese: Lohnt sich eine Zwischensprache (IR/DSL)
  zwischen AAS-JSON und Neo4j-Cypher — oder reicht direktes JSON-Traversal wie
  match_submodel? Drei Ansaetze vergleichen (pre-compiled snippets, DSL, JSON-only),
  Read + Write abdecken, kleinere LLMs entlasten.
type: task
status: open
priority: medium
---

## Kernfrage

Das LLM muss heute einen konzeptuellen Sprung leisten:

```
IDTA-Template (JSON) --> Agent-Reasoning --> Cypher-Query --> Neo4j
```

Dieser Sprung ist fuer grosse Modelle (120B) handhabbar. Fuer kleine Modelle
(7B-30B) und fuer den Write-Pfad (put_*/delete_*) ist er fehleranfaelliger.

**Fragestellung fuer den Paper-Ausblick:** Welche Abstraktionsebene ist die
richtige Zwischenschicht?

---

## Drei Loesungsrichtungen (Hypothesen)

### Richtung A — Pre-compiled Cypher-Snippets (bestehende Idee)

**Was:** Beim Einlesen der Templates (`get_templates_index()`) werden die
Template-Felder auf Cypher-Beispiele gemappt. Das LLM sieht nicht
`SubmodelElement MaxRotationSpeed in AGV-TechnicalData` sondern direkt
das fertige Cypher-Pattern zum Lesen des Werts.

**Wichtige Präzisierung (2026-05-18):** Das Mapping muss **deterministisch**
erfolgen, nicht per LLM. IDTA-Templates sind standardisiert — jedes Feld hat
einen bekannten idShort und semanticId. Ein LLM das die Snippets generiert
verlagert das Halluzinationsproblem nur von Inference-Zeit auf Ingest-Zeit;
der Index könnte falsche Beispiel-Queries enthalten. Deterministisches
Regel-Mapping (Template-Feld → Cypher-Pattern) ist einmal verifizierbar
und danach zuverlässig. LLM-Generierung nur als Fallback für proprietäre
Custom-Templates ohne bekannte Feldstruktur.

**Dreistufige Progression — direktes Learning aus dem aktuellen Ansatz:**

1. *Jetzt:* Prompts/Manuals als Laufzeit-Hinweise → Validator fängt Fehler auf
   (gemessen: CONTAINS-Fehlerquote vor/nach Validator)
2. *Nächste Version:* Deterministisch generierte Snippets aus Template-Index →
   weniger Laufzeit-Halluzination, kein Runtime-Validator nötig für bekannte Muster
3. *Danach:* Snippets als **Supervised-Fine-Tuning-Daten** → das Modell lernt
   korrekte AAS-Cypher-Muster direkt, braucht weniger Laufzeit-Guidance.
   Trainingsdaten entstehen deterministisch (Template-Mapping), nicht per LLM →
   verifizierbare Provenienz, kein Hallu-Risiko im Trainingssatz.
   Passt zur SOOFI-Story: transparente Trainingsdaten-Herkunft für
   domänenspezifische Feinabstimmung.

**Zweiter SFT-Ansatz — Observation-based (komplementär):**
Statt schema-getriebener Positive-Beispiele werden *beobachtete Fehler* als
Trainingssignal genutzt: Validator-Rejections liefern `(falsche_Query, Kontext)`-
Paare automatisch. Mit korrekten Rewrite-Queries ergeben sich DPO-Paare
(Direct Preference Optimization) — das Modell lernt direkt aus seinen eigenen
Failure-Modes. Nicht deterministisch (Trainingsdaten hängen von tatsächlichem
Modellverhalten ab), aber sehr zielgenau für bekannte Schwachstellen.
Validator-Rejection-Log ist damit nicht nur Paper-Messung sondern potentielle
Trainingsdatenquelle.

**Vorteil:** Keine neue Sprache, kein Parseraufwand. Nur Index-Anreicherung.
Progression von Text-Beispielen zu SFT-Daten ist natürlich und ohne
Architekturbruch erweiterbar.

**Nachteil:** Read-only. Schreiben braucht ein analoges Write-Pattern —
entweder ebenfalls vorcompiliert oder generiert. Skaliert schlecht wenn
Templates sich aendern.

**Trigger:** Bench mit einem 7B-30B-Modell zeigt Lift gegenueber JSON-only.

---

### Richtung B — JSON-Result-Traversal (match_submodel-Ansatz)

**Was:** Statt Cypher zu generieren gibt der Agent JSON-Strukturabfragen ab.
Wie `match_submodel` heute: Neo4j gibt JSON zurueck, Agent filtert/traversiert
das Ergebnis im Tool-Result oder per weiterem Tool-Call.

**Vorteil:**
- LLM muss kein Cypher kennen, nur JSON-Strukturen (AAS-nah)
- Write-Pfad analog: statt `SET n.value = x` ein strukturiertes JSON-Patch-
  Objekt — deterministisch validierbar
- Kleinere Modelle koennen AAS-JSON leichter lesen als Cypher-Syntax

**Nachteil:** Komplex bei tiefen Graph-Traversals (CONTAINS->HAS_ELEMENT->
DERIVED_FROM-Ketten). Mehrere Round-Trips statt einem Cypher-Match.

**Offen:** Kann man die Traversal-Tiefe mit einem vorcompilierten
Traversal-Schema begrenzen (Template gibt an: "diese Abfrage braucht max. 3 Hops")?

---

### Richtung C — Dedizierte AAS-Query-DSL

**Was:** Eine schlanke Zwischensprache, die:
- Naeher an AAS-Konzepten liegt als Cypher (SubmodelElement, idShort, ConceptDescription)
- Deterministisch zu Cypher kompilierbar ist (kein LLM im Compile-Schritt)
- Dieselbe Syntax fuer Read und Write nutzt

Beispiel-Sketch:
```
GET AGV-TechnicalData.MaxRotationSpeed WHERE shell.idShort = "MiR100_001"
PUT AGV-TechnicalData.MaxRotationSpeed = 200 WHERE shell.idShort = "MiR100_001"
```

Der DSL-Compiler (deterministisch, Python) erzeugt das passende Cypher / BaSyx-API-Call.

**Vorteil:**
- LLM generiert einfachere Syntax
- Compile-Step ist deterministisch pruefbar (kein Halluzinationsrisiko im Uebertrag)
- Read + Write symmetrisch

**Nachteil:** Neues Sprachdesign + Parser-Implementierung. Expressivitaet begrenzt
(was ist mit Join-Queries, Aggregationen?). Nicht standardisiert — wartungsaufwand.

**Trigger:** Sinnvoll erst wenn A und B empirisch gescheitert sind ODER
wenn die AAS-Community selbst eine solche Query-Syntax standardisiert
(z.B. im Rahmen von IDTA/AAS-Spezifikationen).

---

## Was ins Paper (§13 — Future Work)

Ein Absatz der alle drei Richtungen als offene Hypothesen benennt, motiviert durch
die Beobachtung dass JSON-zu-Cypher-Sprung Komplexitaet auf Inference-Zeit verlagert:

> *The current system requires the agent to bridge two representation layers at
> inference time: IDTA template definitions (JSON) and the Neo4j graph query
> language (Cypher). For our 27B evaluation model this gap is manageable; smaller
> open-weight models may struggle not with reasoning depth but with this implicit
> translation. Three directions are worth exploring. First, pre-compiling templates
> into per-field Cypher examples at ingest time shifts the mapping burden from
> inference to index-build time. Second, exposing AAS data as structured JSON
> objects (analogous to our existing \texttt{match\_submodel} tool) lets the agent
> traverse results without generating graph queries, at the cost of additional
> round-trips for deep traversals. Third, a dedicated AAS query DSL — compiling
> deterministically to Cypher — would provide a symmetric read/write interface
> closer to AAS concepts, though it introduces a new language and parser surface.
> Empirical comparison of these approaches, particularly for sub-10B models and
> write-heavy workloads, remains future work.*

Formulierung muss durch [[task_paper_claim_audit]] (kein Overclaim) und
[[task_paper_style_review]] (keine Marketing-Sprache) durchkommen.

---

## Subtasks

### T1: §13-Absatz formulieren und einfügen

- Datei: `paper/etfa2026/content/13-future-work.tex`
- Absatz-Entwurf oben als Ausgangspunkt
- Alle drei Richtungen als Hypothesen kennzeichnen (nicht als Plan)
- Max. ~12 Zeilen — kein eigener Subsection-Header noetig

### T2: Memo zur technischen Tiefe (separat vom Paper)

- Memory-Doc: `memory/research_idea_aas_query_ir.md`
- Skizziert: Was Richtung A (Snippet-Index) technisch aendert, was Richtung B
  (JSON-Traversal) an neuem Tool braucht, was Richtung C (DSL-Parser) kosten wuerde
- Grobe Aufwandsschaetzung pro Richtung
- Empirische Trigger-Bedingungen fuer jede Richtung (was muss Bench zeigen?)

### T3: Trigger-Bedingungen dokumentieren

Wann lohnt sich ein Follow-up-Paper zu einer der Richtungen?

- **A (Snippets):** Bench mit 7B-30B zeigt >15 Prozentpunkte Lift mit Snippets vs. ohne
- **B (JSON-Traversal):** CRAG-/ReAct-Fehlerklassen zeigen Cypher-Generierungsfehler
  als dominante Fehlerursache (nicht: Reasoning, nicht: Tool-Reihenfolge)
- **C (DSL):** IDTA startet Standardisierungsarbeit fuer AAS-Query-Language ODER
  Richtungen A + B scheitern empirisch

Dokumentation im Memo (T2), damit spaetere Entscheidung kriterienbasiert ist.

### T4 (optional): Quick Probe fuer Richtung A

- 1-2 Templates (AGV-TechnicalData, HierarchicalStructures) handgepflegt mit
  Cypher-Snippets in `get_templates_index()` anreichern
- Mit einem 7B-14B-Modell gegen aktuelle JSON-only-Baseline messen
- Ergebnis im Memo (T2) dokumentieren

T4 nur wenn H200 + Zeit nach ETFA-Submission verfuegbar.

---

## Acceptance Criteria

- `13-future-work.tex` enthaelt den Absatz mit allen drei Richtungen
- Formulierung passt durch Claim-Audit und Style-Review
- Memo (T2) existiert mit Trigger-Kriterien

## Non-Goals

- Keine Implementierung einer DSL oder eines JSON-Traversal-Frameworks im aktuellen Scope
- Keine vollstaendige Multi-Modell-Auswertung — waere ein eigenes Paper
- Kein Refactoring der Template-Pipeline "auf Verdacht"

## References

- IDTA-Templates: `mcp-server/src/aas_hybrid_mcp/idta_templates/`
- Templates-Index: `mcp-server/src/aas_hybrid_mcp/tools/template_search.py`, `get_templates_index()`
- `match_submodel` als Referenz fuer Richtung B: `mcp-server/src/aas_hybrid_mcp/tools/`
- Bench-B-Protokoll: `memory/bench_b_evaluation.md`
- Schwester-Tasks: [[task_paper_claim_audit]], [[task_paper_style_review]]
- Uebergeordnet: [[task_paper_layered_determinism_thesis]] — DSL/IR-Idee ist
  logische Konsequenz von "Komplexitaet deterministisch nach unten schieben"
