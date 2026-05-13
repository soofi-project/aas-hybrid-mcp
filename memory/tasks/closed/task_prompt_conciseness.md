---
name: Task - Prompt & Manual Conciseness Audit
description: Reduziere Systemprompts, Tool Descriptions und Manuals auf generisch, knapp, kein Implementation-Noise
type: task
status: done
priority: medium
---

## Status (2026-05-13)

**Done.** Hauptteil von qwen umgesetzt (~556→180 Zeilen Reduktion über
Tool-Descs + Manuals + Embedded-Prompts), Restarbeiten + ein
architektonischer Bugfix manuell nachgezogen:

**Architektur-Bugfix (vorher: alle manual-Edits waren wirkungslos):**
`server.py` registrierte bislang `manual` aus `tools/manual.py`, das
den **kompletten Manual-Inhalt inline als Python-Strings** trug —
inklusive aller Architektur-Leaks, ZVEI-URIs, "Phase 10", Recipe E.
Toplevel `manual.py` (file-basiert, liest aus `manual_pages/`) war
nirgendwo importiert. Konsequenz: weder qwen's noch meine
`manual_pages/`-Edits haben den Agent zur Laufzeit erreicht. Fix:
- `tools/manual.py` gelöscht.
- `manual.py` (toplevel) auf `_load_page("index")` umgestellt statt
  hardcoded `_build_index()`; unused `import os` entfernt.
- `server.py` Import: `from aas_hybrid_mcp import manual` (toplevel)
  statt `from aas_hybrid_mcp.tools import manual`.

`manual_pages/` ist im docker-compose bereits bind-mounted, daher
`./down.sh && ./up.sh --vllm` reicht — kein Rebuild nötig.

**Conciseness-Restarbeiten:**
- **T13 nachgeholt:** 6 Architektur-Leaks (Neo4j/BaSyx) aus Tool
  Descriptions raus (`query_aas_graph.md`, `get_graph_schema.md` 2×,
  `get_manual_page.md`, `delete_aas.md`, `lookup_semantic_id.md`).
- **Broken Recipe-E-Pointer** in `troubleshooting.md` repariert durch
  Inline-Cypher; "Nameplate" als Beispiel generalisiert auf
  "text-carrying elements".
- **ZVEI-URI-Konkretheit** raus aus `troubleshooting.md` + `index.md`
  (analog `templates.md`-Generalisierung von qwen).
- **"When no template matches"** in `templates.md` als
  Anti-Fabrications-Guardrail wiederhergestellt (5 Zeilen, generisch).
- **Reflexion `_REFLECT_PROMPT`:** 1 generisches mechanistisches
  Beispiel hinzugefügt (Spec-konform).
- **`search_aas_documents.md` Scoping:** Hedge "if you truly have no
  asset context" raus, URI-vs-Label-Guard rein.

`mapping.md` bewusst nicht angefasst — Verluste (BasicEventElement,
AnnotatedRelationshipElement, OperationVariable-Note) im Bench-B-Korpus
irrelevant; Revert würde 90 Zeilen korrekt entfernten Bloat zurückholen.
`cypher.md` Inline-Beispiele (0 statt Spec-2) bleiben weg — `recipes.md`
deckt sie ab.

Acceptance-Criteria erfüllt:
- 0 Architektur-Namen (Weaviate/Kafka/basyx-python/BaSyx/Neo4j) in Tool
  Descriptions oder `manual_pages/` (`grep` clean).
- 0 konkrete IDTA/ZVEI-URIs in agent-sichtbaren Strings.
- 0 konkrete Template-Namen-Aufzählungen.
- Tool Descriptions ≤ ~27 Zeilen (search_aas_documents leicht über 20,
  vertretbar wegen Scoping-Wichtigkeit).
- Manual Pages: cypher 41, mapping 57, recipes 60, templates 43 (mit
  neuem Block), troubleshooting 46, writing 62 — alle ≤ 70.
- Plan-Datei: `~/.claude/plans/effervescent-beaming-sifakis.md`.

## Summary

Tool descriptions und manual pages enthalten zu viele Implementation-Details
(Weaviate, Kafka, BaSyx SDK, Java mapper-Klassen), zu konkrete Template-Namen
als "examples", und sind insgesamt zu lang. Ziel: knapp halten, generisch
bleiben, keine Datenhaltungs-Infos ausleuten.

**Regeln:**
1. Keine Architektur-Details (Weaviate, Kafka, BaSyx-SDK, Java mappers)
2. Keine konkreten Template-Namen als Enumerierung (HandoverDocumentation, Nameplate, etc.)
3. Keine konkreten ZVEI/IDTA URIs — stattdessen generisch "legacy vs current URIs"
4. Tool Descriptions: max ~20 Zeilen, ein Absatz +(INPUT/OUTPUT)
5. Manuals: nur das, was der Agent zum Ausführen braucht; Cypher-Beispiele auf 2-3 pro Seite
6. Kein Element-Type-Aufzählung („Entity, ReferenceElement, …") — statt "inventory what exists"

## Subtasks

### T1: `search_aas_documents.md` — Tool Description auf ~20 Zeilen reduzieren
- HandoverDocumentation / Nameplate Spezifika entfernen → "Dokumentation lebt typischerweise auf dem Type AAS" generisch
- Weaviate Erwähnung entfernen ("not_indexed... in Weaviate")
- Der lange "PICK THE RIGHT SUBMODEL"-Block komprimieren auf 1-2 Sätze
- "DIAGNOSTICS ON EMPTY RESULTS" absichtlich belassen (nützlich), aber Weaviate-Nennung generalisieren

### T2: `search_idta_templates.md` — Template-Namen-Liste entfernen
- Die Aufzählung "Nameplate, HandoverDocumentation, TechnicalData, ServiceRequestNotification, ..." löschen
- Rest ist in Ordnung; max ~20 Zeilen anstreben

### T3: `mapping.md` — drastisch reduzieren (~60 Zeilen Ziel)
- Ganzes Dokument ist zu detailliert: Java-Field-Namen, `AbstractSmeNode`, `*Node mappers`
- Strichen: "Auxiliary nodes" Tabelle, "Shared metadata" Tabelle, "Common labels" (GraphNode/Referable/Identifiable)
- Behalten: Top-level nodes Tabelle, SubmodelElements containment slots (kompakt), SubmodelElement value access Tabelle, Key insight (Entity.statements)
- Konkrete Java/connector-Referenzen ersetzen durch "the connector maps ..." generisch

### T4: `recipes.md` — auf 3 generische Rezepte schneiden (~80 Zeilen Ziel)
- Behalten: Recipe A (container traversal, generisch), Recipe B (instance→type), Recipe D (diagnostics)
- Recipe A-alt (custom templates) in Recipe A integrieren als note
- Recipe C (capabilities) strichen — zu spezifisch
- Recipe E (MultiLanguageProperty) in troubleshooting.md verweisen statt duplizieren
- Recipe F (IRDI lookup) strichen — ist selbsterklärend via `lookup_semantic_id` tool

### T5: `cypher.md` — "Useful traversal recipes" Sektion komprimieren
- 6 Cypher-Beispiele → auf 2 belassen (submodels-of-a-shell, container traversal verweis auf recipes)
- "Key rule: Never use idShort for domain reasoning" behaltenswert, aber kürzer
- ECLASS IRDI Beispiel (`0173-1#02-ABL884#002`) in lookup_semantic_id verweisen

### T6: `templates.md` — ZVEI/IDTA Konkretheit entfernen
- Konkrete URIs (`admin-shell.io/idta/nameplate/3/0`, `zvei/nameplate/2/0`) ersetzen durch generisches "legacy vs current template URIs may diverge"
- Rest ist OK

### T7: `writing.md` — Implementation-Details entfernen
- "basyx-python-sdk" Nennung → generic "client-side SDK validation"
- "Kafka events from BaSyx auto-sync" → "changes propagate automatically"
- "Phase 10" Nennung entfernen
- Ansonsten OK (~50 Zeilen Ziel)

### T8: `executor.md` — Element-Type-Aufzählung generisieren
- Die Liste "Entity, ReferenceElement, RelationshipElement, SubmodelElementCollection, SubmodelElementList, Property" → "AAS submodel elements vary in type" + "inventory what exists"
- Ansonsten Struktur und Regeln sind gut

### T9: `system-prompt.md` — optional straffen
- Momentan 76 Zeilen, akzeptabel aber prüfbar
- "Self-validating approach" Loop (5 Schritte) — gut, aber 1-2 Zeilen straffbar
- Sonst keine Änderungen nötig

### T10: Embedded prompt — reflexion_graph_nodes.py
- `_EXECUTOR_PROMPT` (L39-50): Overlap mit system-prompt.md („cross-reference evidence", "never fabricate", thorough/precise) → auf 3 Zeilen: "retrieve information to answer the user's query using MCP tools"
- `_REFLECT_PROMPT` (L58-80): Die zwei paper-style Beispiele referenzieren idShort/semanticId/Cypher/get_graph_schema — das dupliziert system-prompt.md + executor.md → auf 1 generisches Beispiel kürzen
- `_FINALIZER_PROMPT` (L82-93): OK, variant-spezifisch, keine Redundanz

### T11: Embedded prompt — crag_nodes.py
- `_EXECUTOR_PROMPT` (L42-56): "cross-reference evidence between graph, document, and template sources", "never fabricate" → dupliziert system-prompt.md → auf 3 Zeilen: "retrieve information using MCP tools. Report findings; do not synthesize the final answer."
- `_RELEVANCE_PROMPT` (L58-67): OK, variant-spezifisch
- `_SYNTHESIZER_PROMPT` (L74-85): OK, variant-spezifisch

### T12: Embedded prompt — rewoo_nodes.py
- `_PLAN_PROMPT_SUFFIX` (L50-69): "FIRST-STEP RULE: Most queries need graph structure... Don't skip this — zero-row results almost always come from wrong relationships or missing semanticIds" → dupliziert system-prompt.md + cypher.md → generisch: "Plan structural context discovery before domain queries."
- `_SYNTHESIZER_PROMPT` (L76-95): Das EXAMPLE (L89-94) für E#/E#N Citation ist nützlich und nicht redundant → belassen

### T13: Cross-check — keine verbliebenen Architektur-Leaks + Zeilenlimits
- Grep nach: `Weaviate`, `Kafka`, `kafka`, `basyx`, `basyx-python-sdk`, `AbstractSmeNode`, `Neo4j` (in Tool Descs, nur im manual OK), `Phase 10`
- Sicherstellen: alle Tool Descriptions ≤ ~20 Zeilen, alle Manuals ≤ ~70 Zeilen

## Files Affected

| File | Subtask |
|---|---|
| `mcp-server/src/aas_hybrid_mcp/tool_descriptions/search_aas_documents.md` | T1 |
| `mcp-server/src/aas_hybrid_mcp/tool_descriptions/search_idta_templates.md` | T2 |
| `mcp-server/src/aas_hybrid_mcp/manual_pages/mapping.md` | T3 |
| `mcp-server/src/aas_hybrid_mcp/manual_pages/recipes.md` | T4 |
| `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md` | T5 |
| `mcp-server/src/aas_hybrid_mcp/manual_pages/templates.md` | T6 |
| `mcp-server/src/aas_hybrid_mcp/manual_pages/writing.md` | T7 |
| `aas-agent/src/aas_agent/agent_plan_prompts/executor.md` | T8 |
| `aas-agent/src/aas_agent/reflexion_graph_nodes.py` | T10 |
| `aas-agent/src/aas_agent/crag_nodes.py` | T11 |
| `aas-agent/src/aas_agent/rewoo_nodes.py` | T12 |
| (all above) | T13 |

## Acceptance Criteria

- Keine Architektur-Namen (Weaviate, Kafka, baSyx-SDK) in Tool Descriptions oder Manuals
- Keine konkreten IDTA Template-Namen als Enumerierung
- Keine konkreten ZVEI/IDTA URIs
- Alle Tool Descriptions ≤ 20 Zeilen
- Alle Manual Pages ≤ 70 Zeilen (Ausnahme: mapping.md ≤ 60 wegen Tabellen)
- recipes.md ≤ 80 Zeilen
- Bind-mount → kein rebuild, container restart genügt (`./down.sh && ./up.sh --vllm`)
