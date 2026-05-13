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
- Rewrite metadata: MCP tool response enthält `query_rewritten` und `rewritten_query` (aus `search_aas_documents` tool result)

## Subtasks

### T1: Framework skeleton + runner
**Files:** `tests/agent-tests/` (neu, außerhalb des repos)
- `framework/__init__.py`, `framework/runner.py`
- `runner.AgentTester`: async HTTP client, `pytest` async support
- `run_query(query, model_id, *, rewrite_mode="on" | "off") -> TResult` mit:
  - `response: str`
  - `duration: float`
  - `tool_calls: list[dict]` — parsed from verbose SSE stream
  - `variant: str`
  - `model_id: str`
  - `query_rewritten: bool` — from MCP `search_aas_documents` result
  - `rewritten_query: str | None` — from MCP result (when rewritten)
  - `rewrite_mode: str` — "on" / "off" (for ablation runs)
- Config: `AGENT_URL` (default `http://localhost:8120`), `AGENT_DEFAULT_MODEL`
- SSE parser für verbose stream: extract tool name, args, result aus `<antml:thinking>` blocks
- Rewrite metadata extraction: parse `search_aas_documents` tool result from SSE for `query_rewritten`/`rewritten_query`

### T2: Test-Case loader + YAML schema
- `cases/` directory mit `.yaml` Dateien
- Schema:
  ```yaml
  name: "MiR100 max speed (worker phrasing)"
  query: "Wie schnell kann der MiR100 fahren?"
  asset: "MiR100"
  expected:
    keywords: ["1.5", "maximum speed", "m/s", "5.6 km/hour"]
    pattern: "\\d+\\.?\\d*\\s*(m/s|km/h|ft/s)"
  llm_criteria: "Die Antwort nennt die korrekte max. Geschwindigkeit (1.5 m/s)"
  rewrite_expected:
    should_improve: true
  variants: ["aas-agent:react", "aas-agent:plan", "aas-agent:crag", "aas-agent:reflexion", "aas-agent:rewoo"]
  ```
- `cases.default_variants` in `config.yaml` als fallback wenn nicht pro-case gesetzt
- `rewrite_expected` fields (optional, for ablation cases):
  - `should_improve: bool` — erwartet rewrite on > rewrite off?
  - `rewritten_query_pattern: str` — regex, was rewritten query enthalten sollte
  - `description: str` — kurze Begründung
- Validation: `name` + `query` required; `expected` und `variants` optional
- Separates file `tests/cases_rewrite_ablation.yaml` existiert bereits mit 10 Worker-Phrasing → Manual-Spec Fällen

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
  - `--rewrite-ablation`: run each case twice (on/off), show difference
  - `--ablation-export FILE`: write ablation comparison to JSON
- Normal table output:
  ```
  Query              | Variant  | Duration | Tools | Score | Pass
  -------------------|----------|----------|-------|-------|-----
  MiR100 max speed   | react    | 4.2s     | 2     | 0.9   | ✅
  MiR100 max speed   | plan     | 8.1s     | 4     | 0.7   | ⚠️
  ```
- Ablation table output (`--rewrite-ablation`):
  ```
  Query              | Variant  | Rewrite | Duration | Tools | Score | Δ     | Pass
  -------------------|----------|---------|----------|-------|-------|-------|-----
  MiR100 max speed   | react    | off     | 2.1s     | 2     | 0.5   |       | ❌
  MiR100 max speed   | react    | on      | 4.2s     | 2     | 0.9   | +0.4  | ✅
  UR3e payload       | react    | off     | 2.4s     | 2     | 0.3   |       | ❌
  UR3e payload       | react    | on      | 4.8s     | 2     | 0.8   | +0.5  | ✅
  ```
- JSON export: full results array with all metrics per run (incl. `rewrite_mode`, `rewritten_query`, `Δ`)

### T5: Beispiel-Test-Cases (5-10 queries)
- Cover: AAS lookup, submodel traversal, document search, hierarchical query, write operation
- Queries basierend auf typischen Nutzernutzung + existierende Cypher-Tests als inspiration
- **Document search cases:** Basierend auf extrahierten Manuals (`docs/*.md`).
  Worker-Phrasen vs. Manual-Vokabular → rewrite benefit messbar.
- **Rewrite ablation cases:** `tests/cases_rewrite_ablation.yaml` — 10 cases mit Worker-Queries,
  expected keywords/patterns aus Manuals, `rewrite_expected` blocks für ablation.
  Basierend auf extrahiertem Content: MiR100.md (30p), UR3e.md (238p), UR20.md (217p),
  CRX10iA.md (122p), MiR250.md (213p).

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

## Ablation: `--rewrite-ablation` mode

`--rewrite-ablation` führt jeden Case zweimal pro Variant aus:
1. `QUERY_REWRITE_MODE=off` — um die Umgebungsvariable vor/durch den Test zu setzen
   (MCP-Server muss restarten **odder** der Agent übergibt den rewrite mode via tool call param).
   Da wir gegen den live Agent sprechen: der Runner spricht MCP direkt (`http://localhost:8110`)
   und toggelt `QUERY_REWRITE_MODE` **vor dem Test** durch kill + env-overwrite + restart des
   MCP Containers. Alternativ: der Runner setzt `QUERY_REWRITE_MODE` nur im MCP-Server-Prozess,
   was ein restart erfordert.
2. `QUERY_REWRITE_MODE=on`

**Einfacherer Ansatz:** Der runner setzt `QUERY_REWRITE_MODE` via docker-compose env
und nutzt `docker compose restart aas-hybrid-mcp` zwischen den zwei Durchläufen.
Oder: der Runner macht zwei separate docker-compose Aufrufe mit unterschiedlichen env overlays.

**Noch einfacher:** Falls `QUERY_REWRITE_MODE` vom MCP-Server live gelesen wird (on-each-call),
könnte ein `POST /health?rewrite=on|off` endpoint den mode toggeln.
Das wäre ein kleiner feature-request an den MCP Server, aber optional.

**Empfohlen:** `QUERY_REWRITE_MODE` bleibt env-basiert. Der runner macht zwei vollständige
runs (once mit `on`, once mit `off`), MCP-Server restartet zwischen den Läufen durch
`docker compose restart aas-hybrid-mcp`.

## Acceptance Criteria

- `python run_tests.py` läuft gegen live Agent, sammelt Metriken, zeigt Tabelle
- Pro run: duration, tool call count, response quality score, pass/fail
- Results exportierbar als JSON für weiterverarbeitung
- LLM-judge optional: mit/ohne `--llm-judge` flag funktionieren beide
- Kein hard dependency auf repo-Code: standalone ausführbar
- Mindestens 5 sinnvolle Test-Cases die reale Queries repräsentieren
- Alle 5 Agent-Variants testbar (react, plan, crag, reflexion, rewoo)
- `--rewrite-ablation` läuft zwei Durchläufe (on/off), zeigt Δ-Score pro case
- `query_rewritten` und `rewritten_query` im TResult für rewrite-tracing
- `cases_rewrite_ablation.yaml` als separates file mit 10 Worker-Query Cases

## References

- Agent API: `aas-agent/src/aas_agent/api.py` — `/v1/chat/completions`
- Agent variants: `memory/agent_variants.md` — 5 variants + verbose suffix behavior
- Existing ad-hoc tests: `mcp-server/src/test_hierarchical.py`, `test_hierarchical_final.py`
- Rewrite module: `mcp-server/src/aas_hybrid_mcp/query_rewriter.py`
- Rewrite ablation cases: `tests/cases_rewrite_ablation.yaml`
- Extracted manuals: `docs/MiR100.md`, `docs/UR3e.md`, `docs/UR20.md`, `docs/CRX10iA.md`, `docs/MiR250.md`
