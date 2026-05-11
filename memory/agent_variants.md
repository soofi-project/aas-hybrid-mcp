---
name: Agent variants
description: Eight LangGraph agent orchestration patterns selectable per-request via model name
type: project
---

## Overview

All variants share a single MCP client connection, tool list, and MCP context at startup. Runners are **lazy-initialized** on first request for their model ID and cached for the process lifetime. Selection via **model name** in the OpenAI-compatible `/v1/chat/completions` request — the user picks their pattern in Open WebUI (or any client). No more global `AGENT_VARIANT` env var.

Each runner implements the same interface: `initialize`, `_lazy_init`, `stream`, `invoke`, `direct_invoke`.

All tool-bearing variants include `get_current_utc_time` as a built-in tool alongside MCP tools. The `aas-agent:passthrough` model is a **passthrough** — single LLM call, no tools, no LangGraph.

**Default model** is `aas-agent:react` (set via `AGENT_DEFAULT_MODEL` env var).

## Model ID → Variant Routing

| Model ID | Variant | Tools? | Graph Topology | Status (2026-05-11) |
|---|---|---|---|---|
| `aas-agent:react` | `AgentRunner` | ✅ | Single LLM loop with tool calls (`create_react_agent`) | ✅ Stable |
| `aas-agent:react-valid` | `AgentRunner` | ✅ | Same as react, prompt adds self-validation (Self-Refine) | ✅ Stable |
| `aas-agent:passthrough` | `PassthroughRunner` | ❌ | Single LLM call, no graph, no tools | ✅ Stable |
| `aas-agent:plan` | `PlanReflectAgentRunner` | ✅ | `planner → executor → reflector → finalizer` | ✅ Stable (since 2026-05-11) |
| `aas-agent:crag` | `CragAgentRunner` | ✅ | `executor → relevance check → (refine → executor) → synthesizer` | ✅ Stable (since 2026-05-11) |
| `aas-agent:reflexion` | `ReflexionAgentRunner` | ✅ | `executor → judge → (reflect → executor) → finalizer` | ✅ Stable (since 2026-05-11) |
| `aas-agent:rewoo` | `RewooAgentRunner` | ✅ | `plan → execute (parallel gather) → synthesize` | ✅ Stable (since 2026-05-11) |
| `aas-agent:supervisor` | `SupervisorAgentRunner` | ✅ | `supervisor → orchestrator (parallel workers) → synthesize` | ✅ Stable (since 2026-05-11) |

## Budget Environment Variables

### Shared
| Variable | Default | Used By |
|---|---|---|
| `AGENT_RECURSION_LIMIT` | `100` | all runners (applied at `ainvoke` config level) |
| `AGENT_STEP_ITERATION_LIMIT` | `5` | plan_reflect executor sub-loop, crag executor sub-loop |
| `AGENT_DEFAULT_THINKING` | `false` | all (controls LLM thinking mode default; ignored in vLLM mode) |
| `AGENT_LOG_DIR` | `""` (disabled) | all (conversation trace logging) |
| `AGENT_INJECT_MANUAL` | `true` | all (inject manual into system prompt at startup) |
| `AGENT_INJECT_SCHEMA` | `true` | all (inject graph schema into system prompt at startup) |
| `AGENT_DEFAULT_MODEL` | required | fallback model for API requests without model field |

### plan_reflect only
| Variable | Default |
|---|---|
| `AGENT_MAX_STEP_ATTEMPTS` | `3` |
| `AGENT_MAX_REPLANS` | `2` |
| `AGENT_MAX_TOTAL_TOOL_CALLS` | `30` |
| `AGENT_SUBLOOP_RECURSION_LIMIT` | `8` |

### crag only
| Variable | Default |
|---|---|
| `CRAG_MAX_REFINEMENTS` | `3` |
| `CRAG_RELEVANCE_THRESHOLD` | `0.7` |

### rewoo only
| Variable | Default |
|---|---|
| `REWOO_MAX_THOUGHTS` | `10` |
| `REWOO_PARALLEL_BATCH` | `5` |

### reflexion only
| Variable | Default |
|---|---|
| `REFLEXION_MAX_TRIALS` | `3` |
| `REFLEXION_ACCEPT_THRESHOLD` | `0.7` |

## Bind-Mount Strategy (Windows-host)

Full directory bind-mounts sind auf Windows nicht zuverlässig — der docker compose `./aas-agent/src/aas_agent` mount wurde als `C:\134` gemountet (falscher pfad). **Lösung:** einzelne `.py` files explizit in `docker-compose.yml` mounten (Zeile 477-501).

**`api.py`** ist bind-mounted → änderungen greifen sofort nach restart.
**Auch runner-files** (`reflexion.py`, `crag_nodes.py`, `agent_supervisor_nodes.py`, etc.) sind jetzt einzeln gemountet.
**Nicht gemountet:** `__init__.py`, `_smoke_structured.py` — werden nie geändert.

## Changes made on 2026-05-11

### Bug fixes (all variants)
- **`parallel_tool_calls` without tools**: vLLM rejects `parallel_tool_calls=False` when the LLM is called without `bind_tools()`. Fixed by calling `executor_llm.bind_tools(tools)` in `agent_plan_graph.py`, `crag_graph.py`, `reflexion_graph.py` before passing to the executor node.
- **`AGENT_RECURSION_LIMIT` not passed to `ainvoke`**: `reflexion.py`, `crag.py`, `rewoo.py` read the env var but didn't pass it as `config={"recursion_limit": ...}` to `graph.ainvoke()`. Fixed.
- **Missing `BaseMessage` import in `crag_nodes.py`**: Added to langchain import.
- **Missing `BaseTool` import in `agent_supervisor.py`**: Added to langchain import.
- **f-string backslash in `crag_nodes.py` line 381**: Python 3.11 rejects `\n` inside f-string `{...}` expressions. Replaced with `separator` variable + explicit join.

### Pydantic coercion fixes (LLM returns wrong types)
The vLLM Qwen model often returns:
- `unresolved`/`common_pitfalls`/`missing` as **string** instead of `list[str]`
- `evidence` items with `{fact, source}` instead of `{source, tool, summary}`
- `evidence[source]` as `"other/step-1"` instead of `"other"` (invalid Literal)
- `confidence` as **float** (0.05) instead of `"high"/"medium"/"low"`

**Fixes applied:**
- `reflexion_graph_nodes.py`: coerce `missing: str → list`, `common_pitfalls: str → list` in parse functions
- `agent_supervisor_state.py`: `expected_output` field now has `default="graph_query_result"` (LLM often omits it)
- `agent_supervisor_nodes.py`: coerce `unresolved: str → list` in `_parse_final_answer`
- `agent_plan_nodes.py`: central `_coerce_and_validate()` function handles all common coercions — `unresolved`, `common_pitfalls`, `evidence` schema mismatch, `evidence[source]` literal normalization. Brute-force JSON extraction fallback for mixed text output.
- `crag_nodes.py`: coerce `unresolved: str → list` and `confidence: float → "high"/"medium"/"low"` in `_parse_final_answer`
- `rewoo_nodes.py`: `_PLAN_PROMPT_SUFFIX.format(...)` → `.replace('{max_thoughts}', ...)` (other `{}` in prompt collide with `.format()`)
- `agent_supervisor_nodes.py`: fixed `_to_lc_messages(task_prompt, task)` → `_to_lc_messages(task, task_prompt)` argument swap

### Issues resolved on 2026-05-11 (second round)
1. **`reflexion` non-termination**: `current_trial` was never incremented and no `TrialRecord` objects were created — judge routed to `reflect` forever until recursion limit. Fixed by creating `TrialRecord` in `judge_node`, incrementing `current_trial`, and adding a hard trial cap in `route_after_judge`.
2. **`rewoo` cypher arg mismatch**: Plan node generates `{"query": "MATCH..."}` for `query_aas_graph` tool, but the tool expects `{"cypher": "MATCH..."}`. Fixed with arg normalization in `_execute_single`: `query` → `cypher` when tool is `query_aas_graph`.
3. **`crag` confidence float coercion**: `FinalAnswer` pydantic validation fails when LLM returns `confidence` as a float (e.g. `0.05`) instead of `"high"/"medium"/"low"`. The `QwenOutputParser` path and `_normalize_json_from_qwen` path lacked coercion. Added `_coerce_final_answer()` helper that normalizes `confidence` float → literal and `unresolved` string → list.
4. **`crag` relevance not propagated to synthesizer**: Relevance node scored evidence but never updated the evidence entries — they stayed at `relevance=0.0` so the synthesizer saw no high/medium findings. Fixed by propagating the relevance score back into evidence entries.
5. **`reflexion` finalizer missing answer context**: Finalizer received only trial metadata but no actual answer text, so it had to regenerate from scratch. Added `best_answer_text` to ReflexionState, tracked in judge node, and injected into finalizer context.

### Still to do for full stability
- Centralize pydantic coercion into a single module/function used by all parsers


## Graph Details

### plan_reflect
- **Nodes:** `planner`, `execute_step`, `reflector`, `finalizer`
- **Planner** produces structured `Plan` (goal, steps with intent/suggested_tool/success_criteria, fallback_notes)
- **Executor** is a bounded manual ReAct sub-loop (not `create_react_agent`) with `AGENT_STEP_ITERATION_LIMIT` cap
- **Reflector** produces structured `Reflection` (decision: continue/advance/replan/fail, reasoning, evidence, next_action_hint)
- Can replan up to `AGENT_MAX_REPLANS` times; total tool calls capped at `AGENT_MAX_TOTAL_TOOL_CALLS`
- Prompts from: `agent_plan_prompts/planner.md`, `executor.md`, `reflector.md`, `finalizer.md`
- Inspired by plan-and-solve prompting (wang2023plan_solve)

### agent_supervisor
- **Nodes:** `supervisor`, `orchestrator`, `synthesize`
- Supervisor decomposes request into typed worker sub-tasks
- Three workers (run in parallel): `work_graph`, `work_document`, `work_template`
- Each worker is a pre-compiled `create_react_agent` with domain-specific tool subset
- Worker prompts and tool assignments in `agent_supervisor_nodes.py` (`_WORKER_PROMPTS`, `_WORKER_TOOLS`)
- Inspired by AutoGen (wu2023autogen) and multi-agent debate (du2023multiagent_debate)

### crag
- **Nodes:** `executor`, `relevance`, `refine`, `synthesize`
- **Relevance** evaluates retrieved evidence on 0.0–1.0 scale via structured Pydantic schema
- Below `CRAG_RELEVANCE_THRESHOLD`: generates refined query, retries (up to `CRAG_MAX_REFINEMENTS`)
- Based on CRAG (yan2024crag)

### rewoo
- **Nodes:** `plan`, `execute`, `synthesize`
- Plan node produces ALL tool calls upfront (no observation-based branching)
- Execute node runs tool calls in parallel via `asyncio.gather` (batch size: `REWOO_PARALLEL_BATCH`)
- Linear, no feedback loops — fastest but least flexible
- Based on Reasoning Without Observation (xu2024rewoo)

### reflexion
- **Nodes:** `executor`, `judge`, `reflect`, `finalizer`
- Executor is a bounded ReAct sub-loop (recursion: `AGENT_STEP_ITERATION_LIMIT`)
- **Judge** produces structured verdict (score + accept/revise)
- If "revise", **reflect** generates verbal feedback (strategy hints, pitfalls, focus areas)
- Feedback injected into next attempt's prompt — self-correcting loop
- Up to `REFLEXION_MAX_TRIALS` iterations
- Based on Reflexion (shinn2023reflexion)

## Paper Mapping (ETFA 2026)

Section 3.6 "Agent Orchestration and Variants" (`paper/etfa2026/conference_etfa_2026.tex:113-124`):
- Evaluated in Bench B: react, plan_reflect, crag, reflexion
- Reserved: react_validating (Self-Refine, madaan2023self_refine), agent_supervisor (wu2023autogen, du2023multiagent_debate), rewoo (xu2024rewoo)
