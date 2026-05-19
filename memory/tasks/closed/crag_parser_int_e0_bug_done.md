---
name: CRAG-Parser-Bug Done — Out of Paper Scope nach Pivot 2026-05-16
description: `int('E0')`-Parser-Crash in crag_nodes.py:335 nicht weiter gefixt; CRAG aus Paper raus, Cortecs-Frontier-Eval für CRAG entfällt.
type: task
status: done
---

## Outcome

Der Parser-Bug war primär kritisch, weil er den Cortecs-Frontier-Eval für
die CRAG-Variant geblockt hätte (GPT-5.4, Claude-Opus-4.6 liefern nicht im
Qwen-Output-Format). Mit dem Paper-Pivot 2026-05-16 ist CRAG aus der Eval
rausgenommen — der Bug ist damit nicht mehr blockierend.

## Was nicht passiert ist

- Keine Bug-Lokalisierung mit aktueller Zeilennummer (T1)
- Kein robustes Parsing implementiert (T2)
- Keine Unit-Tests für Multi-Format-Parser (T3)
- Kein Smoke-Run gegen GPT/Claude für CRAG (T4)

## Verbleibende Risiken

Der Bug bleibt im Code (`aas-agent/src/aas_agent/crag_nodes.py`). Falls
jemand die CRAG-Variante reaktiviert (z.B. für die in Paper-Future-Work
erwähnte Node-Decomposed-CRAG-Idee), muss der Bug vorher gefixt werden.
Notiz dazu in den Future-Work-Block des Papers oder im Code als Kommentar
sinnvoll, aber out of scope für aktuelle Submission.

## Verwandte Stelle für ähnliche Parser-Lücken

Plan und Reflexion haben eigene Custom-Parser
(`agent_plan_nodes.py`, `reflexion_graph_nodes.py`). Die Robustheits-Lücke
dort wird durch den Pivot ebenfalls weniger akut, sollte aber beim
Cortecs-Multi-Modell-Test (`task_paper_pattern_modelsize_eval.md` T2/T3)
mit-geprüft werden, weil die Eval explizit nicht-Qwen-Modelle... nein,
streichen — der Pivot bleibt innerhalb der Qwen-Familie. Damit ist auch
das Plan/Reflexion-Parser-Risiko gering.

## References

- Pivot-Kontext: `task_paper_crag_removal_and_reframe.md`, `paper_etfa2026.md` Pivot-Sektion
- Ursprünglicher Befund: `interaction-protocol/2026-05-14T17-50-30Z__1962b4110f55/`
