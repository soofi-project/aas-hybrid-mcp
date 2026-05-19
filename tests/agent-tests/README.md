# aas-agent-tests

External test framework that drives the AAS Hybrid MCP agent variants over
HTTP, collects metrics, and grades responses.

## Quick start

```bash
pip install -e .
# Stack must be running with vLLM overlay:
#   ./up.sh --vllm
python run_tests.py --cases cases/containment_hall4.yaml
```

## Paper eval — Pattern × Modellgröße

The ETFA 2026 eval runs 3 patterns × 9 models × 6 Bench-B queries × N=10.
Use `eval-model.sh` (repo root) to switch the active model, then run the
test framework per model.

### 1 — Switch model (from repo root)

```bash
./eval-model.sh qwen35-27b   # or: qwen35-08b | qwen35-2b | qwen35-4b |
                              #       qwen35-9b | qwen35-122b | qwen35-397b |
                              #       qwen36-27b | qwen36-35b
```

The script copies `.env.model.<slug>` to `.env.model` and restarts the stack
with `docker-compose.eval-model.yml` as override. Verify:

```bash
docker exec aas-agent printenv | grep LLM_MODEL
```

### 2 — Run Bench B (from tests/agent-tests/)

Two-phase workflow — agent runs and LLM judge are kept separate so an abort never
wastes judge budget and the judge model can be swapped without re-running agents.

```bash
# Phase 1: agent runs only — results saved incrementally after each test
python run_tests.py \
  --cases cases/bench_b.yaml \
  --variants aas-agent:react aas-agent:plan aas-agent:reflexion \
  --repetitions 10 \
  --export results/qwen35-27b_bench_b_N10.json

# Phase 2: LLM judge on the finished JSON (no agent calls)
# LLM_BASE_URL must NOT include /v1 — the framework appends /v1/chat/completions.
# For OpenAI: set LLM_BASE_URL=https://api.openai.com and OPENAI_API_KEY.
# For local H200: set LLM_BASE_URL=http://<host>:<port> and LLM_MODEL=<alias>.
LLM_BASE_URL=https://api.openai.com LLM_MODEL=gpt-4o-2024-11-20 \
python run_tests.py \
  --judge-only results/qwen35-27b_bench_b_N10.json \
  --llm-judge \
  --export results/qwen35-27b_bench_b_N10_judged.json
```

Repeat Phase 1 + 2 for each model slug.

### Model run order (H200 reload overhead minimized)

```
qwen35-08b → qwen35-2b → qwen35-4b → qwen35-9b → qwen35-27b → qwen35-122b
→ qwen36-27b → qwen36-35b → qwen35-397b (Cortecs, last)
```

### Prerequisites

- LiteLLM aliases configured on H200 for all local models
  (see comments in `.env.model.*` files for alias → HuggingFace model mapping)
- Cortecs API key in `~/.env.secrets` as `OPENAI_API_KEY` for `qwen35-397b`
- `--llm-judge` requires `LLM_BASE_URL` / `LLM_MODEL` to be set in the active stack

## CLI

```
python run_tests.py [options]

Options:
  --cases PATH...        Case file(s) or glob (default: cases/*.yaml)
  --variants VARIANT...  Filter variants (default: all from config)
  --repetitions N        Repetitions per case × variant (default: 1)
  --llm-judge            Enable LLM-judge evaluator (uses LLM_BASE_URL/LLM_MODEL)
  --judge-only PATH      Skip agent runs; re-run LLM judge on an existing results JSON.
                         Requires --llm-judge. Output: results/judged_<original>.json
                         (or --export). Recommended two-phase workflow:
                           1. run_tests.py              → agent runs, no judge cost
                           2. run_tests.py --judge-only → judge only, no agent cost
  --export PATH          Write full results to JSON (default: results/run_<ts>.json)
  --agent-url URL        Override agent URL (default from config)
  --include-tags TAGS    Only run cases with at least one matching tag
  --exclude-tags TAGS    Skip cases with any matching tag (default: requires_fixture)
```

## Layout

```
framework/          # runner, evaluator, reporter, case loader
cases/              # YAML test case files
  bench_b.yaml      # B1-B6 Bench B queries for Paper eval
  containment_hall4.yaml
  asset_specs.yaml
  ...
results/            # JSON exports (gitignored)
config.yaml         # defaults (agent URL, variants, LLM-judge endpoint)
run_tests.py        # CLI entry point
```

## Adding cases

See `cases/containment_hall4.yaml` for the schema. The loader rejects cases
that violate the unambiguous-question rule (no AAS jargon like "Welche Assets
sind in X" — see `task_agent_test_framework.md` Frage-Disambiguierung).

Case fields:
- `name`, `query` — required
- `expected.keywords` — strings that must appear in the response
- `expected.forbidden` — strings that must NOT appear
- `llm_criteria` — natural-language pass/fail criterion for the LLM judge
- `tags` — use `bench_b`, `paper_eval`, `requires_fixture`, etc.
- `variants` — optional override; defaults to config `default_variants`
