# Bench B — Agent Variant Evaluation

## Overview

Evaluate 4 agent orchestration variants against 6 industrial queries of increasing complexity.
Runs are done via `curl` against the agent API in **verbose streaming mode**.
Conversation traces are automatically written to `interaction-protocol/` via `AGENT_LOG_DIR=/logs`.

## Evaluated Variants

| Variant | Model ID |
|---|---|
| ReAct | `aas-agent:react-verbose` |
| Plan-and-Reflect | `aas-agent:plan-verbose` |
| Corrective RAG | `aas-agent:crag-verbose` |
| Reflexion | `aas-agent:reflexion-verbose` |

## Questions

| ID | Question |
|---|---|
| **B1** | `Which assets are located in Hall 3?` |
| **B2** | `Which autonomous transport robots do we have and where are they located?` |
| **B3** | `Which transport robot can carry more than 200 kg?` |
| **B4** | `What does the MiR250 operator manual say about emergency stops?` |
| **B5** | `My transport robot in Hall 4 has a red status light — what does it mean and how do I fix it?` |
| **B6** | `Which of our robots can carry the heaviest load?` |

## Ground Truth

| ID | Correct Answer |
|---|---|
| **B1** | MiR250_001, MiR250_002, UR3e_001, UR20_001 |
| **B2** | MiR100_001 (H4), MiR250_001 (H3), MiR250_002 (H3) |
| **B3** | MiR250_001, MiR250_002 |
| **B4** | Emergency stop = category 0 stop (STO contactors + SS1 brake); release sequence: release E-stop button → Resume button flashes blue → press Resume (MiR250.pdf p.83-85) |
| **B5** | Hall 4 contains MiR100_001 (not MiR250). MiR100 LED bar = operating status (p.16). Troubleshooting (p.25): if emergency stop, pull to unobstructed area; check destination matches map position; check camera unobstructed; diagnostic menu OK; wheels unobstructed |
| **B6** | MiR250 (250 kg) — must scan both `TechnicalDataAGV.MaxLoadMass` and `TechnicalData.Payload` |

## Run Checklist

For each variant × question (24 total):

**CRITICAL: Each run = fresh session.** No context carry-over between questions.
Every `curl` sends only `[{role: "user", content: "..."}]` — no history from prior runs. The API is stateless; each request generates a new `conversation_id` internally.

1. Ensure stack running: `./up.sh`
2. Run curl (non-streaming JSON, `stream: false`):

```bash
curl -s http://localhost:8120/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "aas-agent:react-verbose",
    "messages": [{"role": "user", "content": "Which assets are located in Hall 3?"}],
    "stream": false
  }' 2>&1 | tee interaction-protocol/manual-react-B1.json
```

3. Find matching trace file in `interaction-protocol/` (folder `{ts}__{sid}/turn-01__{ts}.md`) — stays there, no copy needed.
4. Wait 10s before next run (let LLM cool / avoid rate limits)

**After all 24 runs: grade manually against ground truth table above.**

## Grading Rubric

| Score | Criteria |
|---|---|
| **✓✓ Full** | Answer is correct and complete; key facts match ground truth |
| **✓ Partial** | Answer is directionally correct but missing details or slightly off |
| **✗ Fail** | Wrong answer, hallucination, or no relevant retrieval |

### B5 Specific Rubric

| Score | Criteria |
|---|---|
| **✓✓** | Identifies correct robot (MiR100_001) AND finds both Protective stop + Emergency stop causes + resolution steps from manual |
| **✓** | Identifies correct robot but only covers one stop type OR wrong robot but right troubleshooting |
| **✗** | Wrong robot (says MiR250) OR no meaningful retrieval |

## Results Matrix

Fill in after grading:

| | react | plan | crag | reflexion |
|---|---|---|---|---|
| **B1** | | | | |
| **B2** | | | | |
| **B3** | | | | |
| **B4** | | | | |
| **B5** | | | | |
| **B6** | | | | |

---

## Future: Automated Eval Tool

Once manual evals are done, build a proper eval runner (`aas-agent/eval_bench.py`) that:

1. **Runs all variant × question combinations programmatically** via `httpx.AsyncClient`
2. **Captures from the verbose SSE stream:**
   - Tool calls: name, arguments, result
   - Node transitions (planner, executor, judge, reflect, etc.)
   - Total step count
   - Wall-clock latency (start to finish)
3. **Parses `<antml:thinking>` blocks** from the stream to reconstruct the agent's full trace
4. **Outputs per-run JSON:**
   ```json
   {
     "variant": "react",
     "question_id": "B1",
     "question": "Which assets are located in Hall 3?",
     "response_text": "...",
     "steps": 3,
     "tool_calls": [
       {"name": "query_aas_graph", "args": {"cypher": "..."}, "duration_ms": 120}
     ],
     "latency_ms": 4230,
     "grade": "full"
   }
   ```
5. **Generates summary table** matching the Results Matrix above
6. **Parses conversation trace files** (`interaction-protocol/`) as fallback when stream parsing isn't available
7. **Supports multi-run averaging** (N repetitions per tuple for statistical significance)
