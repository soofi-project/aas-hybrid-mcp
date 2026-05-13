---
name: Task - Prompt & Manual Conciseness Audit
description: Reduziere Systemprompts, Tool Descriptions und Manuals auf generisch, knapp, kein Implementation-Noise
type: task
status: open
priority: medium
---

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

### T10: Cross-check — keine verbliebenen Architektur-Leaks
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
| `aas-agent/src/aas_agent/system-prompt.md` | T9 |
| (all above) | T10 |

## Acceptance Criteria

- Keine Architektur-Namen (Weaviate, Kafka, baSyx-SDK) in Tool Descriptions oder Manuals
- Keine konkreten IDTA Template-Namen als Enumerierung
- Keine konkreten ZVEI/IDTA URIs
- Alle Tool Descriptions ≤ 20 Zeilen
- Alle Manual Pages ≤ 70 Zeilen (Ausnahme: mapping.md ≤ 60 wegen Tabellen)
- recipes.md ≤ 80 Zeilen
- Bind-mount → kein rebuild, container restart genügt (`./down.sh && ./up.sh --vllm`)
