---
name: MCP Prerequisite Guard Done
description: Cypher-Validator live in cypher_query.py (forbidden_pattern). Session-Prerequisite-Guard nicht umgesetzt — stattdessen empirisch belegt via task_eval_tool_call_analysis dass Prompt-only nicht reicht.
type: task
status: done
---

## Was umgesetzt

**Cypher-Validator (T3):** Implementiert in `mcp-server/src/aas_hybrid_mcp/cypher_validator.py`, integriert in `tools/cypher_query.py`. Blockt `idShort CONTAINS`, `toLower(id) CONTAINS`, `assetType MATCH` etc. mit strukturiertem Error-Response. Läuft produktiv seit 2026-05-15.

**Empirische Evidenz:** Die Tool-Call-Analyse (`task_eval_tool_call_analysis`) zeigt: AP-hit 13-76% über alle Modelle, Self-Correction 95-98%, Manual>AP > 0 bei allen Modellen. Ergebnisse in §10 und §11 des Papers eingearbeitet.

## Nicht umgesetzt (bewusst)

**Session-Prerequisite-Guard (T1/T2):** Wurde nicht gebaut. Begründung:
- Der Validator-Output (`forbidden_pattern` mit `violations` und `hint`) liefert bereits strukturiertes Feedback
- Self-Correction-Rate von 95-98% zeigt dass das Feedback funktioniert
- Die eval-Daten zeigen dass das Problem nicht "fehlendes Enforcement" sondern "Prompt wird ignoriert" ist — belegt durch Manual>AP > 0
- Statt serverseitigem Session-State lieber die Validator-Evidenz ins Paper nehmen

## Referenzen

- Validator: `mcp-server/src/aas_hybrid_mcp/cypher_validator.py`
- Integration: `mcp-server/src/aas_hybrid_mcp/tools/cypher_query.py:97`
- Eval-Nachweis: `memory/tasks/closed/eval_tool_call_analysis_done.md`
