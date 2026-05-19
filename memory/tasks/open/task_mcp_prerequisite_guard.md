---
name: Task – MCP Prerequisite Guard & Cypher Validator
description: MCP-Endpunkt statt Prompt zwingt Manual/Schema-Aufrufe und blockt idShort-Substring-Queries
type: task
status: open
priority: medium
---

## Summary

Die Agenten ignorieren trotz Prompt-Hinweis häufig die Reihenfolge „Manual → Schema → Templates → Query" und springen direkt zu `query_aas_graph`, inklusive verbotener `toLower(idShort) CONTAINS`-Heuristik. Statt weitere Prompt-Regeln zu stapeln, soll der MCP-Server selbst sicherstellen, dass Pflicht-Tools vor der ersten Graph- oder Dokumentabfrage laufen und ein Regex-Validator unsaubere Cypher-Bodies blockiert bzw. abmahnt. Ziel ist eine generische, promptunabhängige Leitplanke, die auch bei sprechenden (oder chaotisch benannten) `idShort`-Werten greift – ohne unbeabsichtigt einen „plötzlich Session-gebundenen“ Server zu erzeugen. Alternative Überlegung (noch offen): statt Guards die Manual-/Schema-Inhalte beim Agentenstart fest injizieren (`AGENT_INJECT_*`), was wir aber bisher zugunsten eines „coolen“ nackten MCP-Endpunkts vermieden haben.

## Subtasks

### T1 — Session-Prerequisite-Mechanismus entwerfen
- FastMCP-Request-Context prüfen: Welche IDs eignen sich, um den Pflichtstatus (`manual`, `schema`, `templates`) pro Konversation zu speichern?
- Entscheidung für Datenstruktur (z. B. `contextvars`, globales Dict mit TTL) dokumentieren.
- Fehlerpayload definieren (`missing_prerequisite_tool`) und Verhalten für Mehrfach-Calls (z. B. Caching, Neustart einer Session) klären.

### T2 — Toolbeschreibungen & Handler anpassen
- `get_manual_page`, `get_graph_schema`, `get_templates_index`: Hinweis „muss vor erster Graph-/Dokumentsuche aufgerufen werden“ hinterlegen.
- Beim erfolgreichen Aufruf Pflicht-Flag setzen.
- `query_aas_graph` und ggf. `search_aas_documents`: Vor Ausführung prüfen, ob alle Flags gesetzt sind; bei Verstoß Fehler oder Warnung zurückgeben (Mode-Toggle entscheiden).

### T3 — Cypher-Validator implementieren
- Neues Modul `cypher_validator.py` mit den Regex-Regeln aus [[task-read-validation-gap]].
- `STRICT_READ_VALIDATION` (`off|warn|strict`) unterstützen; in `warn` `_warnings`-Feld, in `strict` Fehlerrückgabe.
- Validator in `query_aas_graph` integrieren, ohne `/Submodel`-Normalizer zu beeinträchtigen.

### T4 — Tests & Dokumentation
- Pytest-Coverage für Validator und Pflicht-Guard (Positiv-/Negativfälle).
- Hinweis in Manual/README ergänzen; Task-Status aktualisieren, sobald umgesetzt.

### T5 — Literatur-Baseline
- PDF `Decoding the Mystery: How Can LLMs Turn Text Into Cypher in Complex Knowledge Graphs?` (Mandilara et al., IEEE Access 2025) besorgen und nach Passagen zu Validierungs-/Schutzmechanismen durchsuchen.
- Optional weitere Quellen wie Tran et al. (2024, CoBGT) sichten und in den Task-Notizen festhalten, falls sie konkrete Validator-Empfehlungen liefern.

## Acceptance Criteria
- Pflichttools werden serverseitig erzwungen: Erste `query_aas_graph` ohne vorherige Manual/Schema/Templates-Calls endet mit deterministischem Fehler.
- Toolbeschreibungen machen die Reihenfolge explizit; Agenten sehen sie beim Planen.
- Regex-Validator verhindert `idShort`-/`id`-Substring-Queries gemäß [[task-read-validation-gap]].
- Tests decken sowohl gültige als auch fehlerhafte Queries ab und laufen per `pytest` grün.

## Open Questions
- Wie stellen wir Pflicht-Aufrufe sicher, ohne den MCP-Server dauerhaft sessionspezifisch umzubauen? (Bedenken: zusätzlicher Session-Cache vs. stateless Verhalten)
- Welche Konversations- oder Request-IDs aus FastMCP eignen sich hierfür zuverlässig, und wie räumen wir deren Zustand wieder auf?
- Falls Manual/Schema doch injiziert werden: Welche Ausschnitte reichen (Anti-Pattern vs. Ganzer Inhalt) und wie handhaben wir Tokenkosten?

## Empirische Evidenz (2026-05-18)

### Vorher (ohne Änderungen)
Trace: `interaction-protocol/2026-05-18T11-59-03Z__723aa0690758/turn-01__2026-05-18T11-59-03Z.md`

- Erster Call: direkt `query_aas_graph` mit `idShort CONTAINS 'MiR100'`
- Kein `get_manual_page`, kein `get_graph_schema`, kein `get_templates_index`
- Input-Tokens: 77k
- Antwort zufällig korrekt, weil Fixtures saubere Namen haben

### Nachher (Tool-Descriptions verschärft: Prerequisite-Block + CONTAINS-Verbot mit Beispiel)
Trace: `interaction-protocol/2026-05-18T11-59-03Z__723aa0690758/turn-01__2026-05-18T12-18-36Z.md`

- Ruft jetzt `get_graph_schema` + `get_templates_index` auf ✅
- Ruft `get_template("Technical Data for AGV")` auf, nutzt Template-Wissen für nachfolgende Queries ✅
- `get_manual_page("cypher")` — **nicht aufgerufen**, obwohl explizit gefordert ❌
- Erster Asset-Lookup: **immer noch** `toLower(aas.idShort) CONTAINS 'mir100'` — trotz Gegenbeispiel direkt in der Tool-Description ❌
- Input-Tokens: 128k (+65 %)

### Run 3 (+ Recipe C in recipes.md ergänzt)
Trace: `interaction-protocol/2026-05-18T11-59-03Z__723aa0690758/turn-01__2026-05-18T12-33-32Z.md`

- Kein Prerequisite-Call, kein `get_manual_page("recipes")` → Recipe C nie gesehen ❌
- Erster Lookup: CONTAINS auf `aas.idShort` ❌
- Weiteres CONTAINS auf `p.idShort` für Property-Suche ❌
- 8 Tool-Calls (vs. 4 in Run 1) — Einheiten-Jagd als Seiteneffekt
- Input-Tokens: 150k

### Schlussfolgerung

Drei Runs, drei verschiedene Verhaltensweisen, alle ignorierten die Manual-Pflicht konsistent. Prompt-Hints (Tool-Description-Verschärfung, Recipe C) haben keinen verlässlichen Effekt auf das erste Lookup-Pattern. Die Varianz zwischen Runs ist hoch — das macht das Verhalten nicht reproduzierbar. Das ist dreifache empirische Motivation für den serverseitigen Prerequisite-Guard (T1+T2) und den Cypher-Validator (T3): **Prompt ist Hint, Enforcement ist Architektur.**

Eval-Strategie (abgestimmt mit [[task-read-validation-gap]] T4): kein separater Pre-Validator-Run nötig, die drei Traces sind der Baseline. Nach Validator-Implementierung: N=3 mit `STRICT_READ_VALIDATION=strict`, Rejection-Log als Messung.

## References
- `interaction-protocol/2026-05-18T11-59-03Z__723aa0690758/turn-01__2026-05-18T11-59-03Z.md` (Vorher)
- `interaction-protocol/2026-05-18T11-59-03Z__723aa0690758/turn-01__2026-05-18T12-18-36Z.md` (Nachher)
- `mcp-server/src/aas_hybrid_mcp/tool_descriptions/query_aas_graph.md`
- `mcp-server/src/aas_hybrid_mcp/tool_descriptions/get_manual_page.md`
- `mcp-server/src/aas_hybrid_mcp/tools/cypher_query.py`
- [[task-read-validation-gap]]
