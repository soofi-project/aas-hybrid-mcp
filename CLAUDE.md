@AGENTS.md




# CLAUDE.md

**Canonical operations guide: `AGENTS.md`.** Read it first — it covers stack
commands (`./up.sh --vllm`, `./down.sh`), service ports, secrets, embedding-model
swaps, agent variants, bind-mount strategy, Neo4j schema, and common gotchas.
This file holds only the few things `AGENTS.md` deliberately omits.


## Memory entry point

`memory/index.md` is the authoritative table of contents for all project memory
files. Load on demand — covers architecture, AAS modeling decisions, template
compliance, paper-summary digests (react / plan-and-solve / reflexion /
crag / multiagent-debate / autogen / self-refine), Bench-B protocol, and paper
build setup.

## Off-limits directories (unless explicitly asked)

Do **not** read files under `interaction-protocol/` or raw test-result JSONs under
`tests/agent-tests/results/*/` unless the user explicitly requests it. These are
large archived logs; browsing them unsolicited wastes context. Derived
`analysis.md` and `stats.json` files in those directories are fine to read.

## Language

All files written to the filesystem (docs, comments, READMEs, YAML, scripts)
must be in **English**. Conversation with the user is in **German**.
