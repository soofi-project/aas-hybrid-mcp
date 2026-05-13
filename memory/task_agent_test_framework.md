---
name: Task - Agent Test Framework
description: Externes Python-Framework zum messen und vergleichen von Agent-Variants
type: task
status: open
priority: medium
---

## Summary

Kein formelles test framework existiert. Token counts sind hardcoded `0` in `api.py`,
die runner tracken keine Metriken, und die bestehenden Scripts in `mcp-server/src/test_*.py`
sind nur low-level Cypher-Checks — nicht agent-level.

Ziel: Externes Python-Tool (außerhalb des repos) das gegen die Agent-API (`/v1/chat/completions`, port 8120)
spricht, Test-Cases durchläuft, und quantitative Metriken sammelt um Agent-Variants
vergleichbar zu machen.

**Hybrid evaluation:** Test-Cases statisch in YAML definiert, Metriken (dauer, tool calls, quality)
teilweise automatisiert (regex/keyword), optional LLM-judge für qualitative Bewertung.

## Architecture

Framework spricht ausschließlich über HTTP gegen den Agent — keine Code-Änderungen
am Agent selbst nötig. Metriken kommen aus:
- Wall-clock time: `time.perf_counter()` um HTTP request
- Tool calls: `stream: true` + `*-verbose` suffix am model name → `<antml:thinking>` events parsen
- Response text: für evaluation (regex + optional LLM-judge)
- Token usage: vLLM response headers (falls available), sonst nicht trackbar über OpenAI-API

## Subtasks

### T1: Framework skeleton + runner
**Files:** `tests/agent-tests/` (neu, außerhalb des repos)
- `framework/__init__.py`, `framework/runner.py`
- `runner.AgentTester`: async HTTP client, `pytest` async support
- `run_query(query, model_id) -> TResult` mit:
  - `response: str`
  - `duration: float`
  - `tool_calls: list[dict]` — parsed from verbose SSE stream
  - `variant: str`
  - `model_id: str`
- Config: `AGENT_URL` (default `http://localhost:8120`), `AGENT_DEFAULT_MODEL`
- SSE parser für verbose stream: extract tool name, args, result aus `<antml:thinking>` blocks

### T2: Test-Case loader + YAML schema
- `cases/` directory mit `.yaml` Dateien
- Schema:
  ```yaml
  name: "MiR100 spindle speed lookup"
  query: "Was ist die max. Spindeldrehzahl der MiR100?"
  expected:
    keywords: ["9000", "rpm", "Spindle"]
    pattern: "\\d{4,}.*rpm"
  llm_criteria: "Die Antwort nennt die korrekte max. Spindeldrehzahl (9000 rpm)"
  variants: ["aas-agent:react", "aas-agent:plan", "aas-agent:crag", "aas-agent:reflexion", "aas-agent:rewoo"]
  ```
- `cases.default_variants` in `config.yaml` als fallback wenn nicht pro-case gesetzt
- Validation: `name` + `query` required; `expected` und `variants` optional

### T3: Evaluator
- `framework/evaluator.py`
- `RegexEvaluator`: keywords (all must match), pattern (regex search) → pass/fail + score 0-1
- Score formula: `(keyword_matches / total_keywords) * 0.7 + (1.0 if pattern else 0.0) * 0.3`
- `LLMJudgeEvaluator` (optional, behind `--llm-judge`):
  - Second LLM call (direkt an vLLM, nicht durch agent) mit `llm_criteria` + response + query
  - Structured output: score 0-1 + brief reasoning
  - Needs `LLM_BASE_URL` + `LLM_MODEL` from env
- Composite evaluator: regex score als hard floor, LLM score als refinement

### T4: Reporter + entry point
- `framework/reporter.py`: CLI table + JSON export
- `run_tests.py`: argparse entry point
  - `--variants`: filter specific variants (default: all from config)
  - `--cases`: specific case file(s) or glob (default: all in `cases/`)
  - `--llm-judge`: enable LLM-based evaluation
  - `--export FILE`: write results to JSON
  - `--parallel N`: concurrent queries per variant (default: 1)
- Table output:
  ```
  Query              | Variant  | Duration | Tools | Score | Pass
  -------------------|----------|----------|-------|-------|-----
  MiR100 spindle     | react    | 4.2s     | 2     | 0.9   | ✅
  MiR100 spindle     | plan     | 8.1s     | 4     | 0.7   | ⚠️
  ```
- JSON export: full results array with all metrics per run

### T5: Beispiel-Test-Cases (5-10 queries)
- Cover: AAS lookup, submodel traversal, document search, hierarchical query, write operation
- Queries basierend auf typischen Nutzernutzung + existierende Cypher-Tests als inspiration
- Minimal:
  1. MiR100 Spindeldrehzahl (numeric lookup via graph)
  2. UR3e payload capacity (numeric lookup via graph)
  3. Hall3 enthaltenen Assets (hierarchical traversal)
  4. PDF document: Safety instructions (vector search)
  5. IDTA template lookup (template search)
  6. Multi-step: Vergleiche zwei Roboter (multiple tool calls needed)

### T6: Config + README
- `config.yaml` mit defaults:
  ```yaml
  agent_url: "http://localhost:8120"
  default_variants:
    - "aas-agent:react"
    - "aas-agent:plan"
    - "aas-agent:crag"
    - "aas-agent:reflexion"
    - "aas-agent:rewoo"
  llm_judge:
    enabled: false
    base_url: ""
    model: ""
  ```
- Kurzes README im `tests/agent-tests/` Verzeichnis mit usage examples

## Config

| Variable | Default | Description |
|---|---|---|
| `AGENT_URL` | `http://localhost:8120` | Agent API endpoint |
| `LLM_BASE_URL` | — | LLM-judge endpoint (vLLM) |
| `LLM_MODEL` | — | LLM-judge model |

## Acceptance Criteria

- `python run_tests.py` läuft gegen live Agent, sammelt Metriken, zeigt Tabelle
- Pro run: duration, tool call count, response quality score, pass/fail
- Results exportierbar als JSON für weiterverarbeitung
- LLM-judge optional: mit/ohne `--llm-judge` flag funktionieren beide
- Kein hard dependency auf repo-Code: standalone ausführbar
- Mindestens 5 sinnvolle Test-Cases die reale Queries repräsentieren
- Alle 5 Agent-Variants testbar (react, plan, crag, reflexion, rewoo)

## References

- Agent API: `aas-agent/src/aas_agent/api.py` — `/v1/chat/completions`
- Agent variants: `memory/agent_variants.md` — 5 variants + verbose suffix behavior
- Existing ad-hoc tests: `mcp-server/src/test_hierarchical.py`, `test_hierarchical_final.py`
