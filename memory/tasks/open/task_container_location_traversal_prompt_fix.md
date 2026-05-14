---
name: Task - Container/Location Traversal Pragmatik-Default
description: Default-Lesart für "in/inside/located in" auf Container-Traversal festlegen, da MANAGES_ASSET ebenfalls eine valide aber unprägmatische Antwort liefert
type: task
status: open
priority: high
---

## Summary

Bei der Frage "Welche Assets sind in Halle4?" liefern die Varianten unterschiedliche Antworten. Eine nähere Analyse zeigt: das ist nicht nur ein Agent-Bug, sondern auch eine **semantische Mehrdeutigkeit** in der Frage selbst.

Beide Lesarten sind formal korrekt:

- **Identitäts-Lesart (`MANAGES_ASSET`):** `urn:aas:hall4` managt das Asset `urn:asset:hall4`. Die Halle als physisches Objekt ist trivialerweise "in" sich selbst. Antwort: `[urn:asset:hall4]`.
- **Container-Lesart (`HAS_SUBMODEL → HAS_ELEMENT* → Entity → REPRESENTS_ASSET`):** Das HierarchicalStructures-Submodel listet die enthaltenen Geräte. Antwort: `[UR3e_002, CRX10iA_001, MiR100_001]`.

Der Nutzer kennt die AAS-Konzepte (Schale, Submodel, Entity) typischerweise nicht und meint pragmatisch die zweite Lesart. Der Agent muss diesen Default kennen.

## Live-Test-Ergebnisse (2026-05-14, ohne vLLM, GPT-5.4-mini)

| Variant | Antwort | Bewertung |
|---|---|---|
| ReAct | `urn:asset:hall4` | Identitäts-Lesart |
| Plan | `urn:asset:hall4`, beruft sich explizit auf `MANAGES_ASSET` | Identitäts-Lesart |
| CRAG | 500 — Parse-Bug `int('E0')` in `crag_nodes.py:335` | separater Bug, eigener Task nötig |
| Reflexion | 4 Assets: 3 Roboter + `hall4`, confidence high | beide Lesarten |

Vorher (2026-05-14, mit Qwen) hatte ReAct die Container-Lesart, Plan die Identitäts-Lesart, CRAG fand `Halle4` nicht, Reflexion fand die Roboter aber Judge lehnte ab. **Variant-Performance ist also LLM-sensitiv** — das ist auch für Bench B / Test-Framework relevant (siehe [[task-agent-test-framework]]).

## Root Cause

Es fehlt eine **Pragmatik-Default-Regel** in den Prompts und Tool-Descriptions. Das Manual hat den Container-Traversal-Pfad bereits in `cypher.md` und `recipes.md` (Recipe A) explizit dokumentiert — aber kein Hinweis, wann diese gegenüber `MANAGES_ASSET` zu bevorzugen ist.

Der DEPLOYED_IN-Fix aus [[task-prompt-quality]] T1+T2 hat das Schema bereinigt, aber die Lesart-Wahl bleibt ungeführt.

## Desired Rule

Pragmatik-Default für Lokalitäts-/Containment-Phrasen:

```
"in / inside / installed in / standing in / contained in / located in <container>"
→ Container-Lesart bevorzugen:
   HAS_SUBMODEL -> HAS_ELEMENT* -> Entity -> REPRESENTS_ASSET -> Asset
→ Wenn der Container selbst auch ein interessantes Asset ist (z.B. die Halle als
  Asset mit Area/PowerConnection), kann es zusätzlich erwähnt werden — aber nicht
  als alleinige Antwort.

"is / represents / which asset is <X>"
→ Identitäts-Lesart:
   AssetAdministrationShell -[:MANAGES_ASSET]-> Asset
```

Wichtig: Beide Pfade sind valide. Es geht nicht darum, MANAGES_ASSET zu verbieten, sondern den **Default für mehrdeutige Lokalitäts-Fragen** festzulegen.

## Subtasks

### T1: Tool-Description ergänzen (höchster Hebel)

`mcp-server/src/aas_hybrid_mcp/tool_descriptions/query_aas_graph.md` um eine kurze Pragmatik-Regel ergänzen — Tool-Beschreibungen werden vom LLM immer mitgelesen, betrifft alle 4 Varianten gleichzeitig:

```
For "what is in / inside / installed in / contained in <container>" questions,
prefer the container traversal (HAS_SUBMODEL -> HAS_ELEMENT* -> Entity ->
REPRESENTS_ASSET) over MANAGES_ASSET. MANAGES_ASSET answers "which asset IS
this shell" — usually not what the user means by "in".
```

### T2: Manual-Backstop in cypher.md

Kurze Anti-Verwechslungs-Notiz in `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md` Anti-Patterns-Sektion einfügen — als Backstop für Agenten, die das Manual abrufen:

```
**N. MANAGES_ASSET ≠ contained assets.**
MANAGES_ASSET answers which Asset this AAS represents (the shell's identity).
For "what is in / inside / contained in" questions, traverse the Entity
hierarchy via HAS_SUBMODEL -> HAS_ELEMENT* -> Entity -> REPRESENTS_ASSET.
```

### T3: Verifikation mit Roboter-Typ-spezifischen Fragen

Stack mit vLLM neu starten:

```
./down.sh && ./up.sh --vllm
```

Eigentliches Ziel der Frage war Entity→REPRESENTS_ASSET-Traversal **plus** semantische Klassifikation der Roboter-Typen (siehe [[task-agent-test-framework]] Regel "Test-Fragen müssen eindeutig sein"). Daher Test-Queries pro Variant:

1. **Transportroboter:** `Welche Transportroboter sind in Halle4?`
   → Erwartet: `MiR100_001` (mobile robot).
   Testet: Container-Traversal + AGV-/Mobile-Robot-Klassifikation via TechnicalData/Capability-Submodel.

2. **Greifroboter:** `Welche Greifroboter sind in Halle4?` oder `Welche kollaborativen Roboter sind in Halle4?`
   → Erwartet: `UR3e_002`, `CRX10iA_001`.
   Testet: Container-Traversal + Cobot-/Manipulator-Klassifikation.

3. **Optional eindeutiger Sanity-Test:** `Welche Geräte stehen in Halle4?`
   → Erwartet: alle 3 Roboter, keine Identitäts-Lesart.

Die ursprünglich verwendete Frage `Welche Assets sind in Halle4?` ist **kein Test-Kandidat** — sie ist semantisch mehrdeutig (Identitäts- vs. Container-Lesart) und verschleiert was eigentlich gemessen wird.

## Out of Scope (separate Tasks nötig)

- **CRAG-Parser-Crash** (`int('E0')` für `item_idx`): Tritt mit nicht-Qwen-LLM-Output auf. Separater Task, da der Parser robuster gegen verschiedene Output-Shapes werden muss.
- **Reflexion-Judge-Strenge** (Qwen-Trace zeigt Score 0.0 trotz korrekter Antwort): Mit GPT-Output funktioniert der Judge — also Qwen-spezifisches Tuning, kein universeller Fix nötig. Falls Bench B mit Qwen weiter läuft, dort kalibrieren — siehe [[task-prompt-quality]] T9.

## Acceptance Criteria

- `query_aas_graph.md` Tool-Description enthält Pragmatik-Default für `in/inside/contained`.
- `cypher.md` Anti-Patterns enthält die `MANAGES_ASSET ≠ contained` Disambiguation.
- `Welche Transportroboter sind in Halle4?` → ReAct, Plan und Reflexion liefern `MiR100_001`.
- `Welche Greifroboter sind in Halle4?` → ReAct, Plan und Reflexion liefern `UR3e_002` + `CRX10iA_001`.
- `Welche Geräte stehen in Halle4?` (Sanity) → alle 3 Roboter, keine `urn:asset:hall4`-Antwort.
- Die mehrdeutige Frage `Welche Assets sind in Halle4?` wird **nicht** in das Test-Framework aufgenommen.
- Paper Alignment bleibt bestehen — keine Variant-Topologie-Änderung, nur Prompt/Manual/Tool-Description.
- Keine Architektur-Leaks, keine harten ZVEI/IDTA-URIs in den Texten.

## References

- Tool-Description: `mcp-server/src/aas_hybrid_mcp/tool_descriptions/query_aas_graph.md`
- Manual: `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md`, `recipes.md`
- Pfad: `(:Entity)-[:REPRESENTS_ASSET]->(:Asset)`, traversiert via `HAS_SUBMODEL → HAS_ELEMENT*`
- Test-Traces: `interaction-protocol/2026-05-14T17-50-30Z__1962b4110f55/` (Qwen) + Live-Curl-Tests am 2026-05-14 (GPT)
- Verwandt: [[task-prompt-quality]] (DEPLOYED_IN-Fix, Judge-Strenge), [[task-agent-test-framework]] (eindeutige Test-Fragen)
