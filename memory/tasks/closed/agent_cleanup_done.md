---
name: Agent Cleanup Done
description: ReWOO entfernt, Verbose Streaming vereinheitlicht, Token Tracking live, Prompt Conciseness
type: task
status: done
---

## Was umgesetzt

**ReWOO entfernt** (2026-05-14): `rewoo*.py` gelöscht, API-Routing bereinigt, `xu2024rewoo` aus `main.bib` entfernt, §06 Architecture-Tex angepasst. Aktive Varianten: **react / plan / crag / reflexion**.

**Verbose Streaming vereinheitlicht**: alle 4 Varianten konsistent — non-verbose gibt nur finale Antwort, verbose gibt Tools + Node-Transitions in `<thinking>`-Blöcken. Gemeinsame Utilities in `verbose_stream_utils.py`. Bugfix: `tools/manual.py` (inline Python-Strings) war aktiv statt toplevel `manual.py` (file-basiert, bind-mounted) — Edits an `manual_pages/` hatten keine Wirkung, jetzt korrekt verdrahtet.

**Token Usage Tracking**: `on_chat_model_end`-Events über alle Graph-Nodes akkumuliert. SSE-Stream erhält finales `__usage__`-Chunk mit echten prompt/completion-Counts. Hardcoded `0` in `api.py` entfernt. Alle 4 Varianten reporten Usage.

**Prompt Conciseness**: Tool Descriptions ≤ 20 Zeilen, Manual Pages ≤ 70 Zeilen, keine Architektur-Namen (Weaviate/Kafka/BaSyx/Neo4j) in agent-sichtbaren Strings, keine konkreten ZVEI/IDTA-URIs hardcodiert.

## Paper-Relevanz

- §06 Architecture: nur noch 4 Varianten (react/plan/crag/reflexion), kein ReWOO
- `xu2024rewoo` nicht in `main.bib` und nicht im Paper
