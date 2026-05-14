# Reflexion (Shinn et al. 2023) — Paper & Implementation Notes

## Paper

**"Reflexion: Language Agents with Verbal Reinforcement Learning"** (arXiv:2303.11366)

### Core concept

Reinforce LLM agents not by updating weights, but through **linguistic feedback**. After each failed attempt:
1. **Actor** (ReAct agent) generates trajectory via tool calls
2. **Evaluator** scores trajectory (binary/skalar)
3. **Self-Reflection** amplifies sparse reward → verbal summary
4. Summary appended to **episodic memory buffer** (`mem`)
5. Actor retries with accumulated past reflections as context
6. Loop until evaluator passes or max trials exhausted

### Key results

| Benchmark | Baseline | +Reflexion | Delta |
|---|---|---|---|
| AlfWorld (decision-making) | 72% | 94% | +22% |
| HotPotQA (CoT+GT, reasoning only) | 61% | 75% | +14% |
| HotPotQA (ReAct, holistic) | 42% | 62% | +20% |
| HumanEval (code, pass@1) | 80% | 91% | +11% |

### Ablation insights (critical for our design)

| Variant | Accuracy (HumanEval Rust) | Insight |
|---|---|---|
| Blind retry (no test, no reflection) | 60% | Pure retry helps slightly |
| Reflection only (no test generation) | 60% | Reflection without evidence is useless |
| Test generation only (no reflection) | 52% | Tests catches errors but doesn't guide fixes |
| **Full Reflexion** | **68%** | Both components are necessary |

**Episodic Memory Ablation (HotPotQA):**
- CoT(GT) + raw prev trajectory (EPM): +8% over baseline
- CoT(GT) + Reflexion (EPM + verbal reflection): +16% over baseline
- Self-reflection adds **8% beyond raw episodic memory** — the verbal amplification step matters

### Why this fits our AAS domain

- Multi-step retrieval across Neo4j + Weaviate benefits from trial-and-error refinement
- Judge has no environment oracle (unlike AlfWorld's "task done?"), so relies on LLM self-evaluation
- Accumulated feedback prevents re-running same failed queries across trials
- Memory bound (≤3 experiences) aligns with our `max_trials=3` to avoid context overflow

## Our Implementation

### Architecture: `executor → judge → (reflect → executor) → finalizer`

Three LLM specializations share the same base model:
- **Executor**: `create_react_agent` subloop with MCP tools (graph, vector, template, manual)
- **Judge**: Scores answer 0.0-1.0, returns `{score, verdict, missing, reason}`
- **Reflection**: Generates `{strategy_hint, common_pitfalls, focus_areas}` in first-person narrative style
- **Finalizer**: Synthesizes final answer from all trial evidence + trial history

### Fixed bugs

| # | Bug | Fix | File |
|---|---|---|---|
| 1 | `feedback_history` replaced instead of appended | Append to existing list | `reflexion_graph_nodes.py:320-325` |
| 2 | Trial number off-by-one in reflect node | Use `completed_trial = current_trial - 1` | `reflexion_graph_nodes.py:266` |
| 3 | `accept_threshold` ignored in routing | `score >= threshold → finalizer` as fallback | `reflexion_graph_nodes.py:495-497` |
| 4 | Reflection prompt too abstract for executor guidance | Added first-person narrative + concrete AAS examples | `reflexion_graph_nodes.py:_REFLECT_PROMPT` |
| 5 | Finalizer only saw best answer, not all trials | Added "All Trial Answers" section with all summaries | `reflexion_graph_nodes.py:383-385` |
| 6 | Shared `synthesizer_rules.md` appended to `_FINALIZER_PROMPT` (2026-05-12) | `reflexion_graph_nodes.py` | **Deliberate addition beyond paper.** Confidence calibration (high/medium/low), empty-result hard rule, forced-termination rule (`REFLEXION_MAX_TRIALS` exhausted with verdict still `revise`), anti-hallucination don'ts. Shared across crag/reflexion finalizers so Bench-B compares loop dynamics, not finalizer-prompt quality. Paper has no confidence dimension — our eval-fair extension. |

### Architectural differences from paper (by design)

| Aspect | Paper | Ours | Rationale |
|---|---|---|---|
| Memory format | Pure narrative prose | Structured JSON → rendered markdown sections | Machine-readable, executor parses fields directly |
| Evaluator | Environment oracle (AlfWorld) or heuristics | LLM judge, no ground truth access | No external oracle in AAS domain; inherent limitation |
| Retry limit | 3 consecutive failures per task | `max_trials=3` hard cap | Comparable; prevents infinite loops, bounded context |
| Actor context | `mem` injected as raw context | `feedback_history` appended to prompt + `trial_records` for EPM | Combines verbal reflection + raw episodic memory |

### Critical limitation we cannot fix

Our judge has **no means to verify factual correctness** — only textual quality against the user query. If the executor hallucinates a plausible-sounding answer, the judge will likely accept it. This is inherent to our architecture (no ground truth oracle for AAS data). The paper's AlfWorld agent benefits from a binary "task done?" signal from the environment. We'd need a verification tool (e.g., "check this claim against the graph") to approximate this — future work.

### Env config

| Var | Default | Purpose |
|---|---|---|
| `REFLEXION_MAX_TRIALS` | `3` | Maximum executor→judge→reflect cycles |
| `REFLEXION_ACCEPT_THRESHOLD` | `0.7` | Score ≥ threshold → accept even if verdict=revise |
