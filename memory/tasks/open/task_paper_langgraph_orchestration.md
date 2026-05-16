---
name: Task - LangGraph Orchestration Exposition (ETFA 2026)
description: Make the LangGraph agent patterns explicit in the ETFA 2026 paper, including architecture narrative, evaluation evidence, and justification versus alternative orchestrators
type: task
status: open
priority: high
---

## Summary

The current manuscript only states that "we use a LangGraph-based ReAct agent" and lists four variants, but it never shows how those graphs are structured, why LangGraph was chosen, or how the variants impact performance. Section~\ref{sec:bench-b} even promises a comparison without providing data. Reviewers will not understand the orchestration story, leaving our "agentically actionable" claim unsupported. This task produces the missing narrative, figures, and measurements so the LangGraph usage is clear, justified, and evidence-backed.

## Scope

- Paper sources under `paper/etfa2026/`, especially:
  - `content/06-architecture.tex`
  - `content/08-retrieval-pipeline.tex`
  - `content/09-write-loop.tex`
  - `content/10-evaluation.tex`
  - `content/11-discussion.tex`
- LangGraph workflow definitions in `aas-agent/src/aas_agent/`
- Bench-B run logs / configs once generated (store under `memory/bench_b_*.md` or similar)

## Subtasks

### T1: Extract and Document LangGraph Topology

- Read the LangGraph definitions (`agent.py`, `agent_plan.py`, `crag.py`, `reflexion.py`).
- Produce a concise topology description for each variant (nodes, edges, retry/reflect loops, guard conditions).
- Draft a new figure (or update Fig.~\ref{fig:arch}) and a dedicated paragraph for `06-architecture.tex` explaining why LangGraph is the enabling layer (state tracking, deterministic retries, tool sequencing).
- Add a short comparison sentence contrasting LangGraph with baseline orchestrators (LangChain AgentExecutor, ADK) to motivate the choice.

### T2: Instrument and Run Variant Benchmarks

- Define the evaluation protocol promised in §\ref{sec:bench-b}: identical scenarios across the four variants, recording success rate, average tool calls, total tokens, and latency.
- Store raw results (CSV/JSON + short memo) under `memory/` for auditability.
- Replace the `[EVAL]` placeholders in `10-evaluation.tex` with actual numbers and cite the memo/log file.
- Ensure the ablation table highlights per-variant trade-offs (e.g., plan overhead vs. success).

### T3: Update Discussion and Conclusion

- Insert a subsection or paragraph in `11-discussion.tex` that interprets the variant results (when to prefer each pattern, trade-offs for industrial deployment).
- Adjust `14-conclusion.tex` to reference the orchestration insight (e.g., "Plan-and-Reflect reduced retries by X").
- Cross-reference requirements in `05-scenario-requirements.tex` where relevant (e.g., R1–R4 alignment).

### T4: Citations and Task Interlocks

- Add or update BibTeX entries (e.g., LangGraph paper, CRAG/Reflexion sources) in `main.bib` if missing.
- Feed the new quantitative claims through `task_paper_claim_audit.md` once numbers are inserted.
- Trigger `task_paper_style_review.md` for the edited sections after substantive changes.

## Acceptance Criteria

- `06-architecture.tex` contains a clear LangGraph topology explanation (text + figure/table) and the rationale for choosing LangGraph over alternatives.
- `10-evaluation.tex` reports concrete metrics for all four agent variants; placeholders `[EVAL]` are eliminated.
- `11-discussion.tex` and `14-conclusion.tex` interpret the variant results and tie them back to the maintenance scenario.
- Supporting run logs/memos for the variant benchmarks exist under `memory/` with referenced filenames.
- Any new claims are registered in `paper/etfa2026/claim_audit.md` per the audit task, and citations for orchestration papers are present in `main.bib`.

## References

- Agent code: `aas-agent/src/aas_agent/agent.py`, `agent_plan.py`, `crag.py`, `reflexion.py`
- Paper sections: `paper/etfa2026/content/06-architecture.tex`, `08-retrieval-pipeline.tex`, `09-write-loop.tex`, `10-evaluation.tex`, `11-discussion.tex`, `14-conclusion.tex`
- Bench logs: `memory/bench_b_evaluation.md` (baseline) + new variant-specific logs
- Existing tasks: `task_paper_claim_audit.md`, `task_paper_style_review.md`
