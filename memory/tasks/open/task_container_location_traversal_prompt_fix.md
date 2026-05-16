---
name: Task - Container/Location Traversal Pragmatik-Default
description: Bei Containment-Fragen ("was ist in X") MANAGES_ASSET-Selbstreferenz des Containers ausschließen, da Identitäts-Lesart nur Modellierungs-Artefakt ist und vom Werker nicht gemeint sein kann
type: task
status: open
priority: high
---

## Summary

Bei der Frage "Welche Assets sind in Halle 4?" liefern die Varianten unterschiedliche Antworten. Formal kann man zwei Lesarten konstruieren — praktisch ist aber nur eine je gemeint.

- **Container-Lesart (`HAS_SUBMODEL → HAS_ELEMENT* → Entity → REPRESENTS_ASSET`):** Das HierarchicalStructures-Submodel listet die enthaltenen Geräte. Antwort: `[UR3e_002, CRX10iA_001, MiR100_001]`. **Das ist die einzig praktisch sinnvolle Antwort.**
- **Identitäts-Lesart (`MANAGES_ASSET`):** `urn:aas:hall4` managt das Asset `urn:asset:hall4`. Antwort: `[urn:asset:hall4]`. **Modellierungs-Artefakt, nicht physische Realität.** Eine Halle ist nicht "in sich selbst" — die Selbstreferenz existiert nur auf der AAS-Schalen-Ebene.

Ein Werker in der Halle oder Fahrer eines LKW kennt die AAS-Konzepte (Schale, Submodel, Entity, MANAGES_ASSET) nicht und fragt nach physisch enthaltenen Objekten. Wenn die Frage ein Containment-Pattern hat ("in/inside/contained in <Container>") und das Subjekt ein Container ist (Halle, LKW, Raum, Schrank, Anlage), ist die Antwort **immer** "andere Assets, die im Container sind", **nie** "der Container als Asset selbst". Letzteres ist nur eine korrekte Antwort auf eine andere Frage ("was IST Halle 4 / welches Asset repräsentiert die Schale Halle 4").

## Live-Test-Ergebnisse (2026-05-14, ohne vLLM, GPT-5.4-mini)

| Variant | Antwort | Bewertung |
|---|---|---|
| ReAct | `urn:asset:hall4` | Identitäts-Lesart |
| Plan | `urn:asset:hall4`, beruft sich explizit auf `MANAGES_ASSET` | Identitäts-Lesart |
| CRAG | 500 — Parse-Bug `int('E0')` in `crag_nodes.py:335` | separater Bug, eigener Task nötig |
| Reflexion | 4 Assets: 3 Roboter + `hall4`, confidence high | beide Lesarten |

Vorher (2026-05-14, mit Qwen) hatte ReAct die Container-Lesart, Plan die Identitäts-Lesart, CRAG fand `Halle 4` nicht, Reflexion fand die Roboter aber Judge lehnte ab. **Variant-Performance ist also LLM-sensitiv** — das ist auch für Bench B / Test-Framework relevant (siehe [[task-agent-test-framework]]).

## Root Cause

Es fehlt eine **Pragmatik-Regel** in den Prompts und Tool-Descriptions, die dem LLM den Unterschied zwischen Frage-Intention und Modellierungs-Ebene erklärt. Das Manual hat den Container-Traversal-Pfad bereits in `cypher.md` und `recipes.md` (Recipe A) explizit dokumentiert — aber kein Hinweis, dass `MANAGES_ASSET` bei Containment-Fragen die *Frage missversteht*, statt sie nur "weniger pragmatisch" zu beantworten.

Der DEPLOYED_IN-Fix aus [[task-prompt-quality]] T1+T2 hat das Schema bereinigt, aber die Lesart-Wahl bleibt ungeführt.

## Desired Rule

Pragmatik-Regel für Lokalitäts-/Containment-Phrasen — mit *Begründung*, damit das LLM auch in Edge-Cases korrekt entscheidet:

```
"in / inside / installed in / standing in / contained in / located in <container>"
→ Container-Lesart (ausschließlich):
   HAS_SUBMODEL -> HAS_ELEMENT* -> Entity -> REPRESENTS_ASSET -> Asset
→ Das Container-Asset selbst (urn:asset:<container>) gehört NICHT in die Antwort.
  Eine Halle/ein LKW/ein Raum ist nicht "in sich selbst" — die Selbstreferenz
  ist nur ein AAS-Modellierungs-Artefakt (Schale -> Asset), das in der realen
  Welt keine Entsprechung hat. Der fragende Nutzer (Werker, Fahrer, Operator)
  kennt diese Modellierungs-Ebene nicht und meint immer physische Containment.

"is / represents / which asset is <X>" / "was ist <X> für ein Asset"
→ Identitäts-Lesart:
   AssetAdministrationShell -[:MANAGES_ASSET]-> Asset
```

Kein "Default unter Alternativen" — bei Containment-Fragen ist MANAGES_ASSET-Selbstreferenz des gefragten Containers schlicht die **falsche Antwort auf die gestellte Frage**.

## Subtasks

### T1: Tool-Description ergänzen (höchster Hebel)

`mcp-server/src/aas_hybrid_mcp/tool_descriptions/query_aas_graph.md` um eine kurze Pragmatik-Regel ergänzen — Tool-Beschreibungen werden vom LLM immer mitgelesen, betrifft alle 4 Varianten gleichzeitig:

```
For "what is in / inside / installed in / contained in <container>" questions
(hall, truck, room, cabinet, machine), use ONLY the container traversal
(HAS_SUBMODEL -> HAS_ELEMENT* -> Entity -> REPRESENTS_ASSET). Do NOT include
the container's own asset (via MANAGES_ASSET) in the answer — a hall is not
"inside itself"; the shell-to-asset link is a modeling artifact with no real-
world meaning, and the asking user (worker, operator) does not know it.
MANAGES_ASSET only answers identity questions like "which asset IS this shell"
or "what does shell X represent".
```

### T2: Manual-Backstop in cypher.md

Kurze Anti-Verwechslungs-Notiz in `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md` Anti-Patterns-Sektion einfügen — als Backstop für Agenten, die das Manual abrufen:

```
**N. MANAGES_ASSET ≠ contained assets.**
MANAGES_ASSET is the shell-to-asset identity link (modeling layer only). A
container asset is not "inside itself" in the real world. For "what is in /
inside / contained in <container>" questions, traverse the Entity hierarchy
via HAS_SUBMODEL -> HAS_ELEMENT* -> Entity -> REPRESENTS_ASSET and exclude
the container's own asset from the result.
```

### T3: Verifikation mit Roboter-Typ-spezifischen Fragen

Stack mit vLLM neu starten:

```
./down.sh && ./up.sh --vllm
```

Eigentliches Ziel der Frage war Entity→REPRESENTS_ASSET-Traversal **plus** semantische Klassifikation der Roboter-Typen (siehe [[task-agent-test-framework]] Regel "Test-Fragen müssen eindeutig sein"). Daher Test-Queries pro Variant:

1. **Transportroboter:** `Welche Transportroboter sind in Halle 4?`
   → Erwartet: `MiR100_001` (mobile robot).
   Testet: Container-Traversal + AGV-/Mobile-Robot-Klassifikation via TechnicalData/Capability-Submodel.

2. **Greifroboter:** `Welche Greifroboter sind in Halle 4?` oder `Welche kollaborativen Roboter sind in Halle 4?`
   → Erwartet: `UR3e_002`, `CRX10iA_001`.
   Testet: Container-Traversal + Cobot-/Manipulator-Klassifikation.

3. **Optional eindeutiger Sanity-Test:** `Welche Geräte stehen in Halle 4?`
   → Erwartet: alle 3 Roboter, keine Identitäts-Lesart.

Die ursprünglich verwendete Frage `Welche Assets sind in Halle 4?` ist **kein Test-Kandidat** — sie ist semantisch mehrdeutig (Identitäts- vs. Container-Lesart) und verschleiert was eigentlich gemessen wird.

## Out of Scope (separate Tasks nötig)

- **CRAG-Parser-Crash** (`int('E0')` für `item_idx`): Tritt mit nicht-Qwen-LLM-Output auf. Separater Task, da der Parser robuster gegen verschiedene Output-Shapes werden muss.
- **Reflexion-Judge-Strenge** (Qwen-Trace zeigt Score 0.0 trotz korrekter Antwort): Mit GPT-Output funktioniert der Judge — also Qwen-spezifisches Tuning, kein universeller Fix nötig. Falls Bench B mit Qwen weiter läuft, dort kalibrieren — siehe [[task-prompt-quality]] T9.

## Acceptance Criteria

- `query_aas_graph.md` Tool-Description enthält die Pragmatik-Regel für `in/inside/contained` **mit Begründung** (Modellierungs-Artefakt vs. reale Welt, Nutzer kennt Modellierungs-Ebene nicht).
- `cypher.md` Anti-Patterns enthält die `MANAGES_ASSET ≠ contained` Disambiguation mit demselben Begründungs-Kern.
- `Welche Transportroboter sind in Halle 4?` → ReAct, Plan und Reflexion liefern `MiR100_001`, **keine** `urn:asset:hall4`-Antwort.
- `Welche Greifroboter sind in Halle 4?` → ReAct, Plan und Reflexion liefern `UR3e_002` + `CRX10iA_001`, **keine** `urn:asset:hall4`-Antwort.
- `Welche Geräte stehen in Halle 4?` (Sanity) → alle 3 Roboter, **keine** `urn:asset:hall4`-Antwort.
- Die mehrdeutige Frage `Welche Assets sind in Halle 4?` wird **nicht** in das Test-Framework aufgenommen.
- Identitäts-Fragen funktionieren weiterhin: `Welches Asset repräsentiert die Schale Halle 4?` → `urn:asset:hall4` via MANAGES_ASSET (Regression-Check, damit die Verschärfung keine valide Identitäts-Lesart blockiert).
- Paper Alignment bleibt bestehen — keine Variant-Topologie-Änderung, nur Prompt/Manual/Tool-Description.
- Keine Architektur-Leaks, keine harten ZVEI/IDTA-URIs in den Texten.

## References

- Tool-Description: `mcp-server/src/aas_hybrid_mcp/tool_descriptions/query_aas_graph.md`
- Manual: `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md`, `recipes.md`
- Pfad: `(:Entity)-[:REPRESENTS_ASSET]->(:Asset)`, traversiert via `HAS_SUBMODEL → HAS_ELEMENT*`
- Test-Traces: `interaction-protocol/2026-05-14T17-50-30Z__1962b4110f55/` (Qwen) + Live-Curl-Tests am 2026-05-14 (GPT)
- Verwandt: [[task-prompt-quality]] (DEPLOYED_IN-Fix, Judge-Strenge), [[task-agent-test-framework]] (eindeutige Test-Fragen)
