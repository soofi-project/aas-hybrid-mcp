---
name: Task - Token Usage Tracking
description: Track und expose Token-Usage (prompt/completion/total) in Agent-API Responses
type: task
status: open
priority: medium
---

## Summary

Token counts sind hardcoded `0` in `api.py:334` (invoke) und fehlen komplett im
SSE stream (`api.py:393-401`). Keiner der runner trackt Metriken.

vLLM liefert `usage` nur im **non-streaming** Pfad. Streaming (SSE) sendet
kein usage-chunk — geprüft an `10.2.10.33:4000`, LiteLLM proxy, Modell `qwen36-27b`.

LangChain `ChatOpenAI` liefert pro call `AIMessage.usage_metadata` mit
`{input_tokens, output_tokens, total_tokens}`. Jede `ainvoke()` im Graph
(Planner, Reflector, Executor, Finalizer, Judge, etc.) hat separate usage.

Ein einziger Turn kann viele parallele LLM-Aufrufe beinhalten:
- CRAG: executor → relevance → (refine/uncorrect) → synthesizer
- Reflexion: N×(executor → judge → reflect) → finalizer
- Plan/Reflect: planner → N×(executor + reflector) → finalizer

Tokens müssen also aus allen Calls **akkumuliert** werden.

## Current State

| Pfad | Usage | Quelle |
|---|---|---|
| `api.py` invoke | Hardcoded `{prompt_tokens: 0, ...}` | `api.py:334` |
| `api.py` SSE | Kein usage-chunk | `api.py:393-401` |
| vLLM non-stream | ✅ `usage` im top-level body | Getestet OK |
| vLLM streaming | ❌ Kein usage-chunk im SSE | Getestet, nicht vorhanden |
| LangChain `ainvoke` | ✅ `AIMessage.usage_metadata` | Pro call |
| LangGraph `astream_events` | ✅ `on_chat_model_end` events | `data.chunk.usage_metadata` |

## Tracking Approach: `on_chat_model_end` Akkumulation

Jeder graph-basierte runner verwendet `astream_events()` im stream-loop.
In diesem loop fängt man `on_chat_model_end` events ab und summiert
`usage_metadata` über alle modelle/nodes hinweg.

```python
usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
async for event in graph.astream_events(...):
    kind = event.get("event")
    if kind == "on_chat_model_end":
        chunk = event.get("data", {}).get("chunk")
        meta = getattr(chunk, "usage_metadata", None)
        if meta:
            usage["input_tokens"] += meta.get("input_tokens", 0)
            usage["output_tokens"] += meta.get("output_tokens", 0)
            usage["total_tokens"] += meta.get("total_tokens", 0)
    # ... existing event handling
```

**Invoke-Pfad:** `result["messages"]` durchgehen, `AIMessage.usage_metadata`
extrahieren und summieren.

## Architecture Decision: Usage-Return-Pfad

```
api.py: _stream_sse()
  → runner.stream() (AsyncIterator[str], kann kein usage zurückgeben)
  → trace object wird vom runner erstellt, usage darin sammelt
  → nach generator ends, trace.flush() → dann trace._usage lesen
  → usage als finales SSE-chunk senden
```

**Problem:** `_stream_sse()` in `api.py:353-400` referenziert `trace` nicht —
das trace-objekt lebt nur im runner. Der Generator hat keinen Zugriff darauf
nachdem er endet.

**Lösung:** `ConversationLogger` um `_usage` dict + `.set_usage()` + `.get_usage()`
erweitern. Im runner: `trace` wird erstellt (am anfang von `stream()`),
usage im loop gesammelt, im `finally` block `trace.set_usage(usage)` aufgerufen.
Da `trace` per referenz weiterlebt, kann `_stream_sse` _nicht_ darauf zugreifen —
es sei denn wir ändern die signatur.

**Bessere Lösung:** Ein module-level / thread-local dict pro request, key'd by
`conversation_id`. Oder: `_stream_sse` bekommt usage als zweiten parameter und
der runner übergibt es via dem letzten yield. Am pragmatischsten: **den usage-wert
in das SSE stream selbst als internes chunk packen**, z.B. `__usage__:{...}`.
Dann kann es direkt im loop parsen und am ende als usage-chunk ausgeben.

**Noch bessere Lösung (empfohlen):** Einfache closure-variable `_stream_sse`:

```python
async def _stream_sse(...):
    usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    try:
        async for token in runner.stream(...):
            if token.startswith("__usage__:"):
                usage = json.loads(token[10:])
                continue
            # ... normal chunk yield
    finally:
        yield usage_chunk(usage)
```

Der runner yieldet bei `on_chat_model_end` einen `__usage__`-token mit
der akkumulierten usage. Oder noch besser: im `finally` block den letzten
usage-wert als `__usage__`-token yielden.

## Subtasks

### T1: Usage-extract helper + trace extension
**Files:** `aas-agent/src/aas_agent/trace.py` (oder neues `usage.py`)
- `_sum_usage_metadata(messages: list) -> dict` — iteriert alle messages,
  extrahiert `usage_metadata`, summiert
- `ConversationLogger` um `.set_usage(usage: dict)` + `.get_usage() -> dict`
  erweitern, `_usage` als instance var

### T1b: React runner usage
**File:** `aas-agent/src/aas_agent/agent.py`
- `stream()`: `on_chat_model_end` events im loop sammeln; im `finally` block
  `trace.set_usage(usage)` aufrufen
- `invoke()`: `result["messages"]` — jedes `AIMessage.usage_metadata`
  extrahieren und summieren

### T2: Plan/reflect runner usage
**File:** `aas-agent/src/aas_agent/agent_plan.py`
- `stream()`: `on_chat_model_end` branch im bestehenden `astream_events`
  loop einfügen + `trace.set_usage(usage)` im `finally`
- `invoke()`: `usage_metadata` aus allen `AIMessage` im result summieren

### T3: CRAG runner usage
**File:** `aas-agent/src/aas_agent/crag.py`
- `_stream_crag_verbose()`: `on_chat_model_end` branch einfügen +
  `trace.set_usage(usage)` im `finally`
- Nicht-verbose branch: `graph.ainvoke` → usage aus result messages,
  `trace.set_usage()` aufrufen
- `invoke()`: `usage_metadata` aus result extrahieren

### T4: Reflexion runner usage
**File:** `aas-agent/src/aas_agent/reflexion.py`
- Gleiches pattern wie T3

### T6: API-Layer usage in `_stream_sse`
**File:** `aas-agent/src/aas_agent/api.py:353-401`
- Problem: `_stream_sse` hat keinen access zum `trace` objekt vom runner
- Lösung: Das trace-objekt aus dem runner zugänglich machen.
  **Option A:** `__usage__` token im SSE stream (elegant, kein signatur-change)
  **Option B:** `stream()` returnt NamedTuple mit `.usage` (breaking, aber klarer)
- Empfehlung: Option A — runner yieldet `__usage__:{...}` im finally-block,
  `_stream_sse` parst und sendet als usage-chunk
- Finales chunk (vor `[DONE]`) mit usage:
  ```json
  {"id": "...", "object": "chat.completion.chunk", "usage": {
    "prompt_tokens": 123, "completion_tokens": 456, "total_tokens": 579}}
  ```

### T7: API-Layer usage im invoke-pfad
**File:** `api.py:321-335`
- Hardcoded `0` → aus runner's `invoke()` zurückgegebenes usage verwenden
- Runner `invoke()` muss usage als zweiter return-wert liefern, oder
  trace.get_usage() aufrufen (wenn trace referenzierbar)

## LLM Calls pro Variant (für token-tracking validation)

| Variant | Nodes mit LLM-Call | Calls pro Turn (typisch) |
|---|---|---|
| React | executor (ReAct loop) | 1-4 |
| Plan/Reflect | planner, executor (loop), reflector, finalizer | 4-8 |
| CRAG | executor, relevance, refine/uncorrect, synthesizer | 3-5 |
| Reflexion | executor (loop), judge, reflect, finalizer | 4-7 |

## Files Affected

| File | Subtask | Change |
|---|---|---|
| `aas-agent/src/aas_agent/trace.py` | T1 | `_usage` dict + `.set_usage()` + `.get_usage()` |
| `aas-agent/src/aas_agent/agent.py` | T1b | Usage akkumulieren (stream + invoke) |
| `aas-agent/src/aas_agent/agent_plan.py` | T2 | Usage akkumulieren (stream + invoke) |
| `aas-agent/src/aas_agent/crag.py` | T3 | Usage akkumulieren (stream + invoke) |
| `aas-agent/src/aas_agent/reflexion.py` | T4 | Usage akkumulieren (stream + invoke) |
| `aas-agent/src/aas_agent/api.py` | T6, T7 | Hardcoded `0` → real usage, SSE final chunk |

## Acceptance Criteria

- `/v1/chat/completions` (no stream) → response `usage` hat echte token counts
- `stream: true` SSE → letztes chunk hat `usage` field (OpenAI-Schema)
- Alle 4 variants (react, plan, crag, reflexion) reporten usage
- Non-verbose + verbose streams gleichermaßen mit usage
- `api.py:334` hardcoded `0` entfernt
- `on_chat_model_end` in allen `astream_events` loops gesammelt
- Token counts plausibel: prompt > 0, completion > 0
- Mehrere LLM-Calls pro Turn korrekt akkumuliert (nicht nur letzter call)
- Bind-mount → kein rebuild, container restart genügt

## References

- vLLM test: Non-streaming `usage` top-level OK, streaming SSE kein usage-chunk
- LangChain docs: `AIMessage.usage_metadata` = `{input_tokens, output_tokens, total_tokens}`
- OpenAI streaming: last non-`[DONE]` chunk has `usage` object
