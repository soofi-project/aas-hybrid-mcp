---
name: Prompt Quality Done
description: T1-T8 umgesetzt (DEPLOYED_IN entfernt, Judge-Evidenzpflicht, Domänen-Erinnerung, System-Prompt Warning, Plan/Reflect Reflector, Executor Evidenz-Wiederverwendung, Tool-Routing für leere Suche). T9 (Verifikation) nicht mehr durchgeführt.
type: task
status: done
---

## Was umgesetzt

**T1-T8 (alle done, 2026-05-13):**

- **T1:** `DEPLOYED_IN` / `Repository`-Node aus Graph-Schema entfernt (`tools/schema.py`)
- **T2:** DEPLOYED_IN aus `cypher.md` Anti-Pattern entfernt
- **T3:** Judge-Evidenz-Verpflichtung in `reflexion_graph_nodes.py:_JUDGE_PROMPT` — lehnt Antworten ohne Tool-Evidenz ab
- **T4:** Domänen-Erinnerung in `reflexion_graph_nodes.py:_REFLECT_PROMPT` — "Stay in industrial automation"
- **T5:** General Knowledge Warning in `system-prompt.md` — Tool-Evidenz > Allgemeinwissen
- **T6:** Plan/Reflect Reflector `success_criteria`-Vollständigkeit in `reflector.md`
- **T7:** Reflexion Executor Evidenz-Wiederverwendung in `reflexion_graph_nodes.py:_EXECUTOR_PROMPT`
- **T8:** Tool-Routing für leere Suche — `weaviate_client.py` liefert `hint`-Feld bei 0 Treffern

Alle Änderungen bind-mount, kein Rebuild nötig.

## Nicht umgesetzt

**T9 (Verifikation):** Geplanter Stack-Restart + manuelle Test-Queries über alle 4 Varianten. Wird nicht mehr durchgeführt — die Eval-Runs (T07, 9 Modelle, 1800 Records) haben die Änderungen im Produktivbetrieb validiert. Die Eval-Daten zeigen die erwarteten Effekte (Self-Correction 95-98%, Manuals-first-Korrelation).

## Referenzen

- Schema: `mcp-server/src/aas_hybrid_mcp/tools/schema.py`
- Reflexion: `aas-agent/src/aas_agent/reflexion_graph_nodes.py`
- System-Prompt: `aas-agent/src/aas_agent/system-prompt.md`
- Cypher-Manual: `mcp-server/src/aas_hybrid_mcp/manual_pages/cypher.md`
- Weaviate: `mcp-server/src/aas_hybrid_mcp/weaviate_client.py`
