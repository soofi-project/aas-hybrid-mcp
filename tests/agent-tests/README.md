# aas-agent-tests

External test framework that drives the AAS Hybrid MCP agent variants over
HTTP, collects metrics, and grades responses.

## Quick start

```bash
# 1 — Create and activate a venv (once per machine)
cd tests/agent-tests
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .

# 2 — Stack must be running with vLLM overlay:
#   ./up.sh --vllm  (from repo root)

# 3 — Run a smoke test
python run_tests.py --cases cases/containment_hall4.yaml
```

For subsequent sessions just re-activate: `source .venv/bin/activate`.

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

Two-phase workflow — agent runs and judge are separate scripts so an aborted
run never wastes judge budget and the judge model can be swapped without
re-running agents.

```bash
# Phase 1: agent runs — results saved incrementally after each test.
python run_tests.py \
  --cases cases/bench_b.yaml \
  --variants aas-agent:react aas-agent:plan aas-agent:reflexion \
  --repetitions 10 \
  --export results/qwen35-27b_bench_b_N10.json

# Phase 2: strict bool judge on the finished JSON (no agent calls).
# Per-case `ground_truth:` blocks in the YAML drive the judgement.
source ~/.env.secrets    # for OPENAI_API_KEY
python judge.py \
  --input results/qwen35-27b_bench_b_N10.json \
  --cases cases/bench_b.yaml \
  --base-url https://api.openai.com \
  --model gpt-5.4-mini
# → results/qwen35-27b_bench_b_N10_judged.json
```

For a local judge (vLLM/Cortecs/LiteLLM) pass the appropriate `--base-url`
and `--model`, e.g. `--base-url http://10.2.10.33:4000 --model qwen36-27b`.

Repeat Phase 1 + 2 for each model slug.

### Model run order (H200 reload overhead minimized)

```
qwen35-08b → qwen35-2b → qwen35-4b → qwen35-9b → qwen35-27b → qwen35-122b
→ qwen36-27b → qwen36-35b → qwen35-397b (Cortecs, last)
```

### 3 — Alle Suites auf einmal (run_all.sh)

`run_all.sh` führt alle 7 Suites für ein Modell durch (N=10 je Suite). Es sourct
automatisch `~/.env.secrets` für den Judge-API-Key.

```bash
# Direkt (blockierend):
cd tests/agent-tests
source .venv/bin/activate
./run_all.sh qwen35-27b

# Async über SSH mit nohup (Session kann danach geschlossen werden):
cd tests/agent-tests
source .venv/bin/activate
nohup ./run_all.sh qwen35-27b > logs/run_all_qwen35-27b.out 2>&1 &
echo $!   # PID merken

# Fortschritt verfolgen:
tail -f logs/run_all_qwen35-27b.out

# Abbrechen:
kill <PID>
```

### Prerequisites

- LiteLLM aliases configured on H200 for all local models
  (see comments in `.env.model.*` files for alias → HuggingFace model mapping)
- Cortecs API key in `~/.env.secrets` as `OPENAI_API_KEY`

## What the judge measures

`judge.py` emits three orthogonal signals per run, plus an `all_good`
conjunction:

| Field                       | Source       | Meaning                                                |
|-----------------------------|--------------|--------------------------------------------------------|
| `judge.answer_correct`      | LLM judge    | Final answer matches the structured `ground_truth:`    |
| `process.read_manuals_first`| programmatic | A manual/schema tool was called before the first query |
| `process.tool_errors`       | programmatic | List of validator/syntax/tool errors during the run    |
| `all_good`                  | derived      | All three signals satisfied                            |

Per-case `ground_truth:` blocks in the YAML drive the LLM judgement
(`required_facts`, `must_not_claim`, `notes`). The judge response is
constrained to a single JSON object — no free prose, no regex matching.

The legacy composite (regex + LLM blended into a 0..1 score) has been
removed. `run_tests.py` still runs the deterministic regex / tool-call
checks (`evaluator.evaluate_regex`) for at-a-glance terminal output, but
those numbers no longer affect the authoritative correctness verdict.

## CLI

```
python run_tests.py [options]

Options:
  --cases PATH...        Case file(s) or glob (default: cases/*.yaml)
  --variants VARIANT...  Filter variants (default: all from config)
  --repetitions N        Repetitions per case × variant (default: 1)
  --export PATH          Write full results to JSON (default: results/run_<ts>.json)
  --agent-url URL        Override agent URL (default from config)
  --include-tags TAGS    Only run cases with at least one matching tag
  --exclude-tags TAGS    Skip cases with any matching tag (default: requires_fixture)
```

```
python judge.py [options]

Options:
  --input PATH           Raw run output (results/<slug>_N10.json)
  --cases PATH...        Case YAML files with `ground_truth:` blocks
  --output PATH          Output path (default: <input-stem>_judged.json)
  --base-url URL         Judge LLM endpoint (default: $LLM_BASE_URL)
  --model NAME           Judge model id (default: $LLM_MODEL)
  --api-key-env VAR      Env var holding bearer token (default: OPENAI_API_KEY)
  --concurrency N        Parallel judge calls (default: 4)
  --limit N              Smoke-test mode: only judge the first N records
```

### 4 — Ergebnisse analysieren

Nach dem Judge-Lauf erzeugt `analyze_results.py` eine Markdown-Auswertung pro Modell:

```bash
cd tests/agent-tests
python analyze_results.py qwen36-27b
# → results/analysis_qwen36-27b.md
```

Das Argument ist der Modell-Prefix. Das Skript lädt alle `results/{prefix}_*_judged.json`-Dateien
und gibt aus:

- **Per-Suite-Tabelle** — N, Correct, Incorrect, Manuals-first, Antipattern-hit, All-good (je als `n (xx%)`)
- **Cross-Tab Correct × Manuals-first** — hat das vorherige Lesen der Agent-Manuals die Korrektheit beeinflusst?
- **Cross-Tab Correct × Antipattern-hit** — korrelieren Validator-Rejections mit falschen Antworten?

Die Tabellen werden sowohl im Terminal (via `rich`) als auch in die Markdown-Datei geschrieben.

## Layout

```
framework/          # runner, evaluator (regex/tool-call), reporter, case loader
cases/              # YAML test case files with ground_truth: blocks
  bench_b.yaml      # B1-B6 Bench B queries for Paper eval
  containment_hall4.yaml
  asset_specs.yaml
  ...
results/            # JSON exports (gitignored)
config.yaml         # defaults (agent URL, default variants)
run_tests.py        # Phase 1: run agents, save raw results
judge.py            # Phase 2: strict bool judge against ground_truth
analyze_results.py  # Phase 3: Markdown analysis per model prefix
```

## Adding cases

See `cases/bench_b.yaml` for the full schema including the `ground_truth:`
block. The loader rejects cases that violate the unambiguous-question rule
(no AAS jargon like "Welche Assets sind in X" — see
`task_agent_test_framework.md` Frage-Disambiguierung).

Case fields:
- `name`, `query` — required
- `expected.keywords` — strings that must appear (informational, no longer a hard pass-rule)
- `expected.forbidden` — strings that must NOT appear (informational)
- `llm_criteria` — fallback natural-language criterion when no `ground_truth:` block exists
- `ground_truth.required_facts` — facts that the answer must support (judge LLM)
- `ground_truth.must_not_claim` — claims the answer must not assert positively
- `ground_truth.notes` — clarifications, edge cases, valid wordings for the judge
- `tags` — use `bench_b`, `paper_eval`, `requires_fixture`, etc.
- `variants` — optional override; defaults to config `default_variants`
