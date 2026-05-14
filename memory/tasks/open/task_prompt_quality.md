---
name: Task - Prompt Quality & Domain Grounding
description: Reduce hallucinations, improve judge/evaluator evidence enforcement, remove misleading schema noise
type: task
status: open
priority: medium
---

## Summary

Nach Prompt-Conciseness-Audit (task_prompt_conciseness.md): die kürzeren Prompts funktionieren,
aber es gibt qualitative Lücken:

1. **DEPLOYED_IN ist Rauschen** — im Graph-Schema als `[:DEPLOYED_IN]->(:Repository)` überall.
   Zeigt nur auf die BaSyx-Server-URL (`http://localhost:8081`). Sieht nach "Location" aus, Agent
   greift darauf zurück bei Standort-Fragen (Hall3-Query → 3 Trials, alle 0.0 score).
2. **Halluzinationen ungeprüft** — reflexion Variant: "MiR100" wird als Biomedizin ("microRNA100 in
   miRBase") interpretiert. Der Judge akzeptiert die Antwort ohne Evidenz-Check.
3. **Reaktiver Reflektor** — driftet in falsche Domänen, hat keine Domänen-Erinnerung.
4. **Synthesizer ohne Evidenz-Verpflichtung** — crag, plan/reflect Finalizer referenzieren
   nicht explizit, dass die Antwort auf Tool-Ergebnissen basieren muss.

## Subtasks

### T1: DEPLOYED_IN aus Graph-Schema entfernen
**Status:** ✅ Done (2026-05-13)
**File:** `mcp-server/src/aas_hybrid_mcp/tools/schema.py`
- `-[:DEPLOYED_IN]->(:Repository)` von AAS, Asset, Submodel Relationship-Listen gelöscht
- `Repository`-Node-Definition entfernt (nichts referenziert ihn mehr)
- `DePLOYED_IN` aus "Other"-Kategorie im Relationship List entfernt
- Anti-Pattern-Sektion "Repository is AAS storage, not a physical location" gelöscht

### T2: DEPLOYED_IN aus cypher.md Anti-Pattern entfernen
**Status:** ✅ Done (2026-05-13)
**File:** `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md`
- Anti-Pattern 1 (`Repository` / `DEPLOYED_IN`) entfernt
- Nummerierung angepasst (ehemalige 2→1, 3→2, etc.)

### T3: Judge-Evidenz-Verpflichtung
**Status:** ✅ Done (2026-05-13)
**File:** `aas-agent/src/aas_agent/reflexion_graph_nodes.py:_JUDGE_PROMPT`
- Neue Regel: "The answer MUST be based on tool-call evidence. Reject answers that sound plausible
  but cite no specific data from tool results, hallucinate domain knowledge (biology, finance, etc.)
  when the domain is industrial automation, or claim data is missing without showing which tools
  were tried and what they returned."
- **Effekt (verifiziert 2026-05-13):** Reflexion-Judge lehnt Antwort ohne Quellenangabe mit
  `score=0.1, verdict=revise` ab → Trial 2 erzwingt explizites Sourcing. Qualität steigt,
  kostet einen zusätzlichen Trial (~15 Tools mehr).

### T4: Reflector-Domänen-Erinnerung
**Status:** ✅ Done (2026-05-13)
**File:** `aas-agent/src/aas_agent/reflexion_graph_nodes.py:_REFLECT_PROMPT`
- Am Anfang eingefügt: "DOMAIN: Stay in the industrial automation / AAS domain. The user asks
  about factory assets (robots, machines, sensors). If previous attempts drifted into unrelated
  domains (biology, finance, etc.), explicitly course-correct."

### T5: System-Prompt — General Knowledge Warning
**Status:** ✅ Done (2026-05-13)
**File:** `aas-agent/src/aas_agent/system-prompt.md`
- Nach dem Key Rule in "Self-validating approach" eingefügt: "If the answer relies on general
  knowledge rather than tool-call evidence, treat it as low confidence and state what data was
  not found."
- Gilt für ALLE 4 Varianten gleichzeitig — günstigster Hebel

### T6: Plan/Reflect Reflector — success_criteria Vollständigkeit
**Status:** ✅ Done (2026-05-13)
**File:** `aas-agent/src/aas_agent/agent_plan_prompts/reflector.md`
Neue Hard-Rule "Complete coverage before done" ergänzt: jeder im `success_criteria`
benannte Datenpunkt muss in `evidence_collected` belegt sein, sonst `step_retry` mit
Hinweis auf den fehlenden Punkt. Paper-Status: domain-neutrale Konsistenzregel, kein
Plan-and-Solve-Konflikt.

### T7: Reflexion Executor — Evidenz-Wiederverwendung
**Status:** ✅ Done (2026-05-13)
**File:** `aas-agent/src/aas_agent/reflexion_graph_nodes.py:_EXECUTOR_PROMPT`
Eine Zeile zu Beginn ergänzt: feedback aus Vortrials als short-term memory behandeln,
keine Re-Calls der dort zitierten Tools, nur fehlende Daten fetchen. Paper-Status:
direkt aus Reflexion §3 abgeleitet (Actor conditions on short- and long-term memory).

### T8: Executor — Tool-Routing für leere Suche
**Status:** ✅ Done (2026-05-13), umgewidmet auf Tool-Ebene
**Paper-Begründung:** ReAct-Paper Table 2 nennt "Search return empty" als 23 % der
ReAct-Fehler ("derails the model reasoning"). Die zwei vom Paper genannten Fixes
(CoT-SC-Fallback bzw. Finetuning) sind für uns nicht anwendbar (Halluzinationsrisiko
bzw. out of scope). Stattdessen wurde der Action-Space des Tools informativer
gemacht — analog zur Wikipedia-API im ReAct-Paper, die bei Fehlsuche "Could not find.
Similar: [...]" liefert. Kein Tool-Routing im Prompt — paper-fremd wäre, dem LLM
die Reihenfolge vorzuschreiben.

**Files:**
- `mcp-server/src/aas_hybrid_mcp/weaviate_client.py`: `_search_templates_sync` liefert
  bei 0 Treffern (Collection fehlt **oder** kein Semantik-Match) ein `hint`-Feld
  *"search_idta_templates returned no results. Call get_templates_index() for the
  complete deterministic catalogue."* Plus Logging für Diagnose.
- `mcp-server/src/aas_hybrid_mcp/tools/template_search.py`: Hint-Feld durch den
  MCP-Wrapper propagieren.

### T9: Test — alle Änderungen verifizieren
Stack restart: `./down.sh && ./up.sh --vllm` (bind-mount, kein rebuild).
Alle 4 Varianten (`react`, `plan`, `crag`, `reflexion`) mit:
1. "Welche Assets stehen in Halle 4 und welche Seriennummern haben diese Assets?"
   → Hierarchische Traversal, kein DEPLOYED_IN, Seriennummern vollständig
2. "Was ist die max. Spindeldrehzahl der MiR100?"
   → Numerischer Lookup, AGV ≠ Spindel, kein Domain-Mismatch
3. "Vergleiche MiR100 und MiR250"
   → Multi-step, kein Biomed-Halluzinations-Pfad

Ergebnisse dokumentieren: Tool-Call-Anzahl, Confidence, korrekte Antwort.

## Config

Keine neuen Umgebungsvariablen.

## Acceptance Criteria

- `DEPLOYED_IN` und `Repository`-Node nicht mehr im Graph-Schema (`get_graph_schema()` output)
- `cypher.md` enthält kein DEPLOYED_IN mehr
- Reflexion-Judge lehnt Antwort ohne Evidenz mit `score < 0.3, verdict=revise` ab
- Reflexion-Reflektor bleibt in industrieller Domäne (kein Biomed-Drift)
- Plan/Reflect-Reflector markiert step_done nur bei vollständigen success_criteria
- Reflexion-Executor reuses evidence von Trial 1 (weniger Tools in Trial 2)
- `get_templates_index` wird vor `search_idta_templates` bevorzugt
- Alle 3 Test-Queries: keine Domain-Mismatch-Antwort
- Bind-mount: kein rebuild, container restart genügt

## References

- Schema: `mcp-server/src/aas_hybrid_mcp/tools/schema.py`
- Reflexion: `aas-agent/src/aas_agent/reflexion_graph_nodes.py`
- Plan/Reflect: `aas-agent/src/aas_agent/agent_plan_prompts/reflector.md`
- System-Prompt: `aas-agent/src/aas_agent/system-prompt.md`
- Cypher-Manual: `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md`
- Vorheriges Audit: `memory/tasks/closed/task_prompt_conciseness.md`
- Through-Runs: `interaction-protocol/2026-05-13T15-01-04Z__6e52ddf1a69d/` (5 Varianten, Halle 4)
