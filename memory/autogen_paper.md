# AutoGen (Wu et al. 2023) — Paper & Implementation Notes

## Paper

**"AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"** (arXiv:2308.08155)

### Core concept

AutoGen is a framework for building LLM applications through multi-agent conversations. Two key abstractions:

1. **Conversable Agent**: An entity that can send/receive messages and generate replies using a configurable mix of capabilities:
   - LLM-backed (role-playing, tool use, coding)
   - Human-backed (human input at configurable conditions)
   - Tool-backed (code execution, function calls)

2. **Conversation Programming**: Complex workflows expressed as multi-agent conversations with both:
   - **Computation**: actions agents take to generate responses (message passing)
   - **Control flow**: sequence and conditions under which agents communicate (LLM-driven or predefined)

### Conversation patterns

**Two-Agent Chat (sequential/joint)**: Round-robin between two agents until termination.

**Group Chat (hierarchical with manager)**: A `GroupChatManager` orchestrates N agents:
1. Select the next speaker (LLM-based, using conversation history + role definitions)
2. Ask the selected speaker to respond
3. Broadcast the response to all agents

**Hierarchical Chat (nested)**: Demonstrated in the OptiGuide application with a Commander-Writer-Safeguard pattern:
- **Commander**: receives user questions, manages communication flow, handles memory/context
- **Writer**: crafts code, interprets execution output
- **Safeguard**: adversarial checker, reviews for safety

The Commander routes tasks to workers, validates results, loops back on errors, and decides completion.

### Key results

**Math (MATH dataset, Level-5):**
| Method | Accuracy (%) |
|---|---|
| GPT-4 (vanilla) | 45.0 |
| ChatGPT + Code Interpreter | 52.5 |
| LangChain ReAct | 26.7 |
| Multi-Agent Debate | 30.0 |
| **AutoGen (GPT-4)** | **69.5** |

**ALFWorld (decision making):**
| Method | Avg Success (%) | Best of 3 (%) |
|---|---|---|
| ReAct | 54 | 66 |
| AutoGen 2-agent | 69 | 70 |
| **AutoGen 3-agent (+grounding)** | **77** | **80** |

The grounding agent (specialized "knowledge" worker that detects error loops) provides a 15% gain.

**Group Chat — speaker selection:**
| Config | Success (/12 tasks) | Avg LLM Calls | Termination Failures |
|---|---|---|---|
| **Group Chat (role-play prompts)** | **11** | **4.5** | **0** |
| Group Chat (task-based prompts) | 8 | 4.0 | 0 |
| Two-Agent | 9 | 6.8 | 3 |

Role-play prompts significantly outperform task-based routing for dynamic worker selection.

### Design principles (from paper)

1. **Start simple**: Begin with two-agent chat; only add complexity when needed.
2. **Role isolation is critical**: Separate agent memories prevent shortcuts and hallucinations.
3. **Role-play > task-based routing**: Defining who each agent is outperforms listing what tasks need doing.
4. **Supervisor manages memory and termination**: The orchestrator maintains global context, routes to workers, decides completion.
5. **Collaborative + adversarial interactions**: Workers that help + workers that check/challenge each other.
6. **Modularity**: Each agent independently testable with well-defined message interfaces.

### Why this fits Future Work: Specialized Worker vs. Generalist Agent

> **DEPRECATED:** The Supervisor variant (`agent_supervisor.py`) was removed (2026-05-12). The concept lives on as **Future Work**: comparing domain-specialized fine-tuned workers against a single generalist agent. See `memory/future_phases.md`.

The AutoGen Commander pattern remains relevant for this future direction:
- Decompose request → dispatch to specialized workers → synthesize results
- Workers would have role-specific fine-tuned models (not just tool subsets)
- Iterative supervisor loops with multi-turn worker dialogue would address the single-pass limitation
### Key AutoGen features still to implement (Future Work)

| Feature | AutoGen Paper | Future Work Scope | Priority |
|---|---|---|---|
| Iterative supervisor loop | Commander re-dispatches unresolved tasks | Re-dispatch unresolved sub-tasks back to workers | High |
| Domain-specialized models | Shared LLM with role-play prompts | Fine-tuned small models per domain | High |
| Adversarial checking | Safeguard worker reviews output | 4th "critic" worker for consistency checks | Medium |
| Human-in-the-loop | `UserProxyAgent` with human input mode | Not implemented | Low |
| Dynamic worker selection | LLM-based role-play selection | Evaluate: static vs dynamic routing | Medium |
