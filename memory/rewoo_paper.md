# ReWOO (Xu et al. 2024) — Paper & Implementation Notes

## Paper

**"ReWOO: Reasoning without Observation for Efficient Augmented Reasoning"** (NeurIPS 2023, arXiv:2305.18323)

### Core concept

Eliminates the sequential Thought-Action-Observation loop by decoupling reasoning from tool execution:
1. **Planner**: LLM generates ALL tool calls upfront without seeing any results
2. **Workers**: Tools execute in parallel (`asyncio.gather`-style), results stored as `#E` variables
3. **Solver**: LLM synthesizes a single answer from all observations at once

Contrast with ReAct (sequential: Thought-Action-Observation-Thought-Action...), where each step depends on the previous observation.

### Key results

| Method | HotpotQA EM | TriviaQA Acc | GSM8K Acc |
|---|---|---|---|
| ReAct (zero-shot) | 27.4% | 57.7% | 31.6% |
| **ReWOO (zero-shot)** | **34.0%** | **65.6%** | **33.0%** |
| ReWOO (few-shot) | 30.2% | 61.6% | 34.0% |
| ReWOO (Planner 7B IT) | 38.0% | 66.1% | 37.2% |

**Token savings:** ReWOO 16x fewer tokens on HotpotQA (no per-step exemplar repetition, no observation inflation in context).

### Failure analysis (Section A.2, 100 cases each)

| Failure mode | ReAct | ReWOO |
|---|---|---|
| Bad Reasoning | 76 | 51 |
| Tool Inefficacy | 20 | 29 |
| Token Excess | 18 | 0 |
| Answer Miss | 3 | 11 |
| Ambiguous Question | 17 | 17 |

- **Bad Reasoning down:** ReAct fails catastrophically on tool errors (infinite retry loops A-B-A-B... until token limit). ReWOO plans once, is immune to this.
- **Token Excess down from 18 to 0:** No sequential accumulation of observations.
- **Tool Inefficacy up:** Planner doesn't know whether a query returns data before planning.
- **Answer Miss up (3 to 11):** Solver receives all evidence at once, sometimes draws wrong conclusions.

### Critical finding: Few-shot hurts planning quality

Section 4.4: *"When we use few-shot exemplars, the zero-shot ReWOO consistently outperforms the few-shot ReWOO."*

Reason: Few-shot exemplars constrain the planner — it tends to plan all the same tool type (e.g., all Wikipedia), losing the parallel-discovery advantage. Zero-shot ReWOO generates more diverse, adaptive plans.

**Implication for us: Zero-shot is the right choice.** Our zero-shot approach with tool-refs-only for the planner is paper-aligned.

### Why ReWOO outperforms ReAct (A.2)

ReAct: A single bad tool response ruins the entire reasoning trace. Common pattern: toolA fails, try toolB, toolB fails, revert to toolA, infinite loop until token limit. Beyond 4 steps, context becomes too long, reasoning drifts from the original problem.

ReWOO: Plans are generated independently of tool outcomes. Even if individual tools fail, the plan itself is reasonable. Plans can be "ineffective" (wrong expectations about what data a tool returns), but this is less catastrophic than ReAct's cascade failure.

### Why this fits our AAS domain

- **Parallel discovery is ideal for "all assets in Hall 3" type queries** — multiple Cypher strategies in parallel
- **Robust against tool-failure** — one failed graph query doesn't destroy the pipeline
- **Token efficiency** matters with large MCP tool descriptions and verbose AAS schema
- **Zero-shot > few-shot** — our tool calls are too domain-specific for hand-crafted exemplars in the planner

## Our Implementation

### Architecture: `plan → execute → synthesize` (linear, no loop)

Three LLM/tool specializations:
- **Planner** (`plan_node`): `RewooPlan` with `thoughts[]` — each thought has `plan`, `tool_name`, `tool_args`, `ref_id`
- **Execute** (`execute_node`): `asyncio.gather` parallel execution with `REWOO_PARALLEL_BATCH` batch size
- **Synthesizer** (`synthesize_node`): `FinalAnswer` with `answer`, `confidence`, `unresolved`

Linear graph: `START → plan → execute → synthesize → END` (no conditional edges, no retry loop)

### Changes applied (paper-aligned)

| # | Change | File | Rationale |
|---|---|---|---|
| 1 | `base_system` removed from plan node | `rewoo_nodes.py` + `rewoo_graph.py` | Paper: planner is lightweight, only tool definitions + instructions. Domain context in the plan prompt is expensive and not needed. |
| 2 | `base_system` injected into synthesize node | `rewoo_nodes.py` | Solver needs domain context to interpret observations correctly. |
| 3 | Generic exemplar added to synthesizer prompt | `rewoo_nodes.py:_SYNTHESIZER_PROMPT` | Paper (A.2): "providing a simple exemplar could mitigate Answer Miss issue." Single exemplar for the solver only, NOT the planner. |
| 4 | Failed/empty observations split into separate section | `rewoo_nodes.py:synthesize_node` | Explicit categorization helps solver recognize gaps and populate `unresolved`. |
| 5 | `REWOO_MAX_THOUGHTS`, `REWOO_PARALLEL_BATCH` env defaults | `.env` | Reproducibility, aligned with `rewoo.py` env reading. |
| 6 | Shared `synthesizer_rules.md` appended to `_SYNTHESIZER_PROMPT` (2026-05-12) | `rewoo_nodes.py` | **Deliberate addition beyond paper.** Confidence calibration (high/medium/low), empty-result hard rule, forced-termination rule, anti-hallucination don'ts. Shared across rewoo/crag/reflexion finalizers so Bench-B compares retrieval/planning mechanisms, not synthesizer-prompt quality. Paper has no confidence dimension — this is our eval-fair extension. |

### Architectural differences from paper (by design)

| Aspect | Paper | Ours | Rationale |
|---|---|---|---|
| Planner context | Tool defs only | Tool defs + arg schemas | Our MCP tools have complex args; schema helps the planner emit valid calls |
| `#E` as variable refs | `#E1` used as input to subsequent tools | Not applicable (no sequential dependencies) | ReWOO's linear execution doesn't pass outputs between workers |
| LLM as a tool | `LLM[input]` is a first-class tool | No — we don't have an "LLM as tool" MCP endpoint | Our tools are graph/vector/manual/template; internal reasoning happens in the planner |
| Solver exemplar | Paper recommends single exemplar | Generic exemplar added (no domain knowledge) | Paper-aligned, avoids hardcoding AAS-specific patterns |
| Retry loop | None (single-shot) | None (single-shot) | Correct — adding retry would defeat ReWOO's cost advantage |
| Confidence scoring | Not in paper | `high/medium/low` + `unresolved[]` | Useful for evaluation; no paper equivalent, our extension |

### Critical limitations we cannot fix

1. **No adaptive behavior:** If the planner's assumptions about data structure are wrong, there's no feedback loop. This is inherent to ReWOO and intentional.
2. **Sequential reasoning queries (B5):** Queries that require discovering X, then using X to find Y are weak points for ReWOO **by design** — the planner must plan both steps without knowing X exists. Our plan prompt instructs parallel-hypothesis planning to mitigate this, but the weakness is architecture-inherent and is expected to surface as a Bench-B finding rather than as a bug. ReWOO is reserved (not in Bench B's evaluated variants) precisely because this trade-off makes it less suitable for sequential AAS queries; it remains available for parallel-discovery queries where it shines.
3. **Observation truncation at 3000 chars** (`rewoo_nodes.py:316-321`): Necessary to prevent solver context overflow, but may lose data for large graph result sets.

### Env config

| Var | Default | Purpose |
|---|---|---|
| `REWOO_MAX_THOUGHTS` | `10` | Maximum tool calls the planner can generate in one plan |
| `REWOO_PARALLEL_BATCH` | `5` | Batch size for `asyncio.gather` parallel execution |
