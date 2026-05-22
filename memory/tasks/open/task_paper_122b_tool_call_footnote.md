---
name: Task – 122b Tool-Call-Anomalie im Paper beschreiben
description: Qwen3.5-122b schreibt Tool-Calls als Plaintext in den Chat statt strukturierte Function-Calls; Tabelleneintrag raus, Fußnote/Erklärung rein.
type: task
status: open
priority: medium
---

## Background

Bei der Benchmark-B-Auswertung (T=0.0 und T=0.7) zeigt Qwen3.5-122b-A10B
systematisch `tool_call_count=0` — nicht weil das Modell keine Tools nutzen
wollte, sondern weil es die Aufrufe als Plaintext in den Chat-Output schreibt
(z.B. `query_aas_graph({"cypher": "MATCH..."})`), statt strukturierte
Function-Calls zu erzeugen.

Konsequenz: Der Agent-Harness führt die Tools nie aus. Das Modell "antwortet"
entweder aus Trainingswissen (<3s, Sofortantwort) oder läuft in einen Timeout
(~88-90s). Echte Cypher- oder Weaviate-Ergebnisse fließen nie ein.

Betroffene Dateien:
- `tests/agent-tests/results/qwen35-122b/t00/qwen35-122b_bench_b_N10_T00.json`
- `tests/agent-tests/results/qwen35-122b/t07/qwen35-122b_bench_b_N10_T07.json`
- analog alle anderen Bench-B/Containment/SRN-Dateien für 122b

## Subtasks

### T1 — 122b-Zeile aus Paper-Eval-Tabelle entfernen

Bench-B-Ergebnistabelle in `paper/etfa2026/` enthält oder würde enthalten:
Zeile für 122b (A10B). Diese Zeile rausnehmen oder mit „–" markieren.

### T2 — Fußnote / Inline-Erklärung formulieren

In der Eval-Sektion (§ Experiments o.ä.) eine kurze Erklärung hinzufügen:

> Qwen3.5-122B-A10B was excluded from the quantitative comparison because the
> model consistently emitted tool invocations as plain chat text rather than
> structured function calls, preventing the agent harness from executing any
> MCP tool. This behaviour was observed at both evaluated temperatures (0.0 and
> 0.7). The root cause is a known incompatibility between the model's
> instruction-following and the OpenAI function-calling wire format.

Alternativ als Fußnote, je nach verfügbarem Platz.

### T3 — Skalierungs-Achse ohne 122b dokumentieren

Die Modellgrößen-Achse lautet dann: 2B → 4B → 8B → 9B → 27B → 35B → 397B
(ohne 122B-A10B). Im Paper darauf hinweisen dass 122b kein Lücke in der
Skalierungsaussage erzeugt, weil es sich um ein MoE-Modell handelt das
architektonisch nicht zwischen 35B und 397B einzuordnen ist.

## Acceptance Criteria

- 122b-Zeile ist aus der Bench-B-Tabelle entfernt (oder klar als „n/a" markiert)
- Paper-Text enthält mindestens einen Satz der die Exklusion begründet
- Kein Reviewer-Einwand möglich: „warum fehlt das größte Modell?"

## References

- Eval-Daten: `tests/agent-tests/results/qwen35-122b/`
- Paper: `paper/etfa2026/`
- Verwandte Tasks: [[task-paper-pattern-modelsize-eval]]
