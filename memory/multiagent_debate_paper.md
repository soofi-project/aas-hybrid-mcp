# Multi-Agent Debate (Du et al. 2023) — Paper & Implementation Notes

## Paper

**"Improving Factuality and Reasoning in Language Models through Multi-Agent Debate"** (arXiv:2305.14325)

### Core concept

N identical LLM instances independently generate candidate answers, then iteratively debate to converge on a common final answer:

1. **Initial responses**: Each agent independently solves the problem
2. **Debate rounds (R)**: Each agent reads all other agents' responses, critiques them, and updates its own answer
3. **Consensus**: Agents typically converge to a single common answer

Two consensus prompt variants:
- **Short**: "Based off the opinion of other agents, can you give an updated response..."
- **Long**: "Using the opinion of other agents as additional advice..." — makes agents more "stubborn", slower convergence but better final answer

Standard setup: **3 agents, 2 debate rounds**.

### Key results

**Reasoning (GSM8K, 3 agents, 2 rounds):**
| Method | GSM8K (%) | Arithmetic (%) | Chess (Pawn Score) |
|---|---|---|---|
| Single Agent | 77.0 | 67.0 | 91.4 |
| Single Agent (Reflection) | 75.0 | 72.1 | 102.1 |
| Multi-Agent (Majority Vote) | 81.0 | 69.0 | 102.2 |
| **Multi-Agent (Debate)** | **85.0** | **81.8** | **122.9** |

Debate outperforms majority vote on GSM8K by 4pp — the iterative debate adds value beyond simple voting.

**Factual accuracy:**
| Method | Biographies | MMLU | Chess Move Validity |
|---|---|---|---|
| Single Agent | 66.0 | 63.9 | 29.3 |
| Single Agent (Reflection) | 68.3 | 57.7 | 38.8 |
| **Multi-Agent (Debate)** | **73.8** | **71.1** | **45.2** |

Critical: Self-reflection **hurts** MMLU (63.9 → 57.7), while debate improves everything. Debate beats self-reflection across all factual tasks.

**Cross-model debate:** ChatGPT (14/20) + Bard (11/20) → joint debate (17/20). Different models debating each other works well.

### Ablation insights

- **More agents → better**: Performance increases monotonically with N (tested 1 through 5+ agents on arithmetic). With 5+ agents, summarization of prior responses is needed (context length).
- **Debate rounds**: Performance plateaus after 4 rounds. 2 rounds is the sweet spot for cost/quality trade-off.
- **Stubborn vs. agreeable**: Long prompts (more stubborn) converge slower but reach higher-quality consensus. RLHF-tuned models are too "agreeable" — they converge on wrong answers easily.
- **Summarization > concatenation**: Summarizing other agents' responses improves debate quality, especially with many agents.
- **Personas**: Different agent personas (professor, doctor, mathematician) on MMLU: 71.1 → 74.2%. Diversity in prompting adds value.

### Critical failure modes

1. **Convergence to wrong consensus**: The most insidious failure mode. Agents converge on a single answer, but the answer is wrong. LLMs express uniformly high confidence even on wrong consensus.
2. **No uncertainty mechanism**: LLMs cannot reliably express "I don't know". "Ease of persuasion" is proposed as a proxy for factual confidence.
3. **Context overflow**: Long debates overwhelm context windows — LLMs only focus on recent generations.

### Why this is NOT our Supervisor

MAD requires **iterative cross-agent critique with feedback loops**. Each agent sees the other agents' outputs and revises. Our supervisor runs workers once in parallel with no cross-talk. The MAD improvement signal (iterative debate) is absent from our architecture. The supervisor is structurally closer to AutoGen's Commander pattern (see `autogen_paper.md`).

## Paper-to-Implementation Audit

| Aspect | MAD Paper | Our Supervisor | Gap |
|---|---|---|---|
| Iterative debate | N rounds of cross-agent critique | Single pass: no iteration | **Gap: No feedback loop** |
| Agent diversity | Identical models or cross-model; personas | 3 specialized workers (different roles/tools) | Partial — role diversity exists, but no iteration |
| Consensus mechanism | Natural-language debate → converge | Synthesizer combines results | **Different: synthesize vs. debate** |
| Cross-talk | Each agent sees all other agents' outputs | Workers run in isolation | **Gap: No cross-critique** |
| Stubbornness control | Prompt-length knob (short vs. long) | Not applicable | N/A |
| Convergence detection | Implicit (agents agree) | Not applicable | N/A |
| Computational model | N × R LLM calls per agent | 1 supervisor + 3 workers + 1 synthesize | Comparable in cost, different in structure |

### Assessment

The Supervisor variant draws nominal inspiration from MAD but does not implement the core MAD mechanism (iterative debate). The cited benefit ("inspired by AutoGen and multi-agent debate" in `agent_variants.md:129`) overstates the MAD connection. The implementation is structurally an AutoGen Commander pattern: decompose → dispatch specialized workers → synthesize. There is no MAD-style debate round.

If MAD-inspired behavior were desired, a plausible addition would be: after initial worker execution, the synthesizer could route results back to workers for critique and revision (1-2 rounds). This would add complexity and cost but would approximate the MAD mechanism.
