---
name: Bench B — Agent Variant Evaluation
description: 6-question benchmark read-only queries evaluated across 4 agent variants for ETFA 2026 paper
type: project
---

## Purpose

Evaluated agent orchestration variants against 6 industrial queries of increasing complexity. Maps to **Benchmark B (§Benchmark B — Document-Aware Agent Evaluation)** in the ETFA 2026 paper. Assesses correctness, step count, and latency per variant.

## Evaluated Variants

| Variant | Model ID | Graph Topology |
|---|---|---|
| ReAct | `aas-agent:react` | Single LLM loop with tool calls |
| Plan-and-Reflect | `aas-agent:plan` | planner → executor → reflector → finalizer |
| Corrective RAG | `aas-agent:crag` | executor → relevance → (refine → executor) → synthesizer |
| Reflexion | `aas-agent:reflexion` | executor → judge → (reflect → executor) → finalizer |

`supervisor` and `rewoo` are reserved for future work per §3.6.

**Verbose** (`*-verbose` suffix) is available for all tool-bearing variants but is **not an evaluation axis** — used exclusively for debugging and conversation trace inspection.

## Dataset

10 industrial assets (6 instances + 4 type-AASs + 2 halles) across Hall 3 and Hall 4.

All 5 type-AASs carry a `HandoverDocumentation` submodel with a PDF manual.

| AAS | Kind | Hall | Submodel Schema | Payload prop | PDF |
|---|---|---|---|---|---|
| MiR100_001 | instance | **H4** | — | — | MiR100.pdf (via Type) |
| MiR250_001 | instance | **H3** | — | — | MiR250.pdf (via Type) |
| MiR250_002 | instance | **H3** | — | — | MiR250.pdf (via Type) |
| UR3e_001 | instance | **H3** | — | — | UR3e.pdf (via Type) |
| UR3e_002 | instance | **H4** | — | — | UR3e.pdf (via Type) |
| UR20_001 | instance | **H3** | — | — | UR20.pdf (via Type) |
| CRX10iA_001 | instance | **H4** | — | — | CRX10iA.pdf (via Type) |
| MiR100_Type | type | — | TechnicalDataAGV | MaxLoadMass: 100 kg | MiR100.pdf |
| MiR250_Type | type | — | TechnicalDataAGV | MaxLoadMass: 250 kg | MiR250.pdf |
| UR3e_Type | type | — | TechnicalData | Payload: 3 kg | UR3e.pdf |
| UR20_Type | type | — | TechnicalData | Payload: 20 kg | UR20.pdf |
| CRX10iA_Type | type | — | TechnicalData | Payload: 10 kg | CRX10iA.pdf |
| Hall3 | structure | H3 | — | — | — |
| Hall4 | structure | H4 | — | — | — |

**Schema pitfall:** AGV payloads live in `TechnicalDataAGV.SpecificDescriptions.DataSheet.TechnicalParameters.MaxLoadMass`. Cobot payloads live in `TechnicalData.TechnicalProperties.MechanicalProperties.Payload`. Same meaning, different submodel ID and property name — agents must handle both.

## Questions

Each question targets specific requirements from §3.2:

| ID | Question | Complexity | Requirements | Key Challenges | Expected Result (Ground Truth) |
|---|---|---|---|---|---|
| **B1** | "Which assets are located in Hall 3?" | Simple | R1 (Structural Navigation) | Single-hop graph query | MiR250_001, MiR250_002, UR3e_001, UR20_001 |
| **B2** | "Which autonomous transport robots do we have and where are they located?" | Aggregate | R1 | Identify transport robot category across all instances; map to halls | MiR100_001 (H4), MiR250_001 (H3), MiR250_002 (H3) |
| **B3** | "Which transport robot can carry more than 200 kg?" | Property filter | R1 | Query `MaxLoadMass` in `TechnicalDataAGV`; must traverse to Type-AAS first | MiR250_001 (H3), MiR250_002 (H3) |
| **B4** | "What does the MiR250 operator manual say about emergency stops?" | Document retrieval | R2 (Deep Content) | Find HandoverDocumentation submodel ID, then scoped vector search | Emergency stop = category 0 stop (STO contactors + SS1 brake); release sequence: release E-stop button → Resume button flashes blue → press Resume (MiR250.pdf p.83-85) |
| **B5** | "My transport robot in Hall 4 has a red status light — what does it mean and how do I fix it?" | Hybrid: graph + doc | R1 + R2 | Hall 4 → MiR100_001 (not MiR250!) → DERIVED_FROM → MiR100_Type → MiR100.pdf | LED color bar indicates operating status (p.16). Troubleshooting (p.25): if emergency stop, pull to unobstructed area; check destination matches map position; check camera unobstructed; diagnostic menu OK; wheels unobstructed |
| **B6** | "Which of our robots can carry the heaviest load?" | Cross-asset comparison | R1 | Must query **both** `TechnicalDataAGV.MaxLoadMass` (MiR) and `TechnicalData.Payload` (UR/CRX) — two different submodel schemas, two different property names | MiR250 (250 kg) |

## Metrics

Per (question, variant) tuple:

| Metric | Description | Collection |
|---|---|---|
| **Correct** | Binary: does the answer address the question? | Manual grading |
| **Steps** | Total tool calls during the turn | `AGENT_LOG_DIR` trace or verbose stream |
| **Latency** | End-to-end response time (wall clock) | HTTP-level timer |
| **Prec@N** | For B4-B5: are the top-N document chunks relevant? | Manual grading |

## Test Setup

1. Start stack: `./up.sh`
2. Set `AGENT_LOG_DIR=/app/logs/bench-b` in `.env` for conversation traces
3. For each variant × question: send non-streaming POST to `localhost:8120/v1/chat/completions` with `model=aas-agent:<variant>`
4. Save response + trace JSON per run
5. Grade responses manually

## Notes

- Write path (Bench C, §Benchmark C) is evaluated separately with 25 incident scenarios and N=20 repetitions. Not part of this benchmark.
- Questions are in English to match the system prompt language. Worker-facing prompts in production would be multi-lingual (per system-prompt.md: "Respond in the user's language").
- All PDFs are on Type-AAS level — questions requiring document access (B4, B5) must traverse `DERIVED_FROM` from instance to type.
- B6 is the hardest read-only question: it forces the agent to discover two different submodel schemas (`TechnicalDataAGV` vs `TechnicalData`) and two different property names (`MaxLoadMass` vs `Payload`) for the same semantic concept.
