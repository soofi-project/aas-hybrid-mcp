# aas-agent-tests

External test framework that drives AAS agent variants over HTTP, collects
metrics, and grades responses.

## Quick start

```bash
cd tests/agent-tests
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .

# Stack must be running:
#   ./up.sh --vllm  (repo root)

python run_tests.py --cases cases/containment_hall4.yaml
```

## Eval workflow (Paper: Pattern × Model size)

Two phases — agent runs and judge are separate scripts.

```bash
# 1 — Switch model (repo root)
./eval-model.sh qwen35-27b

# 2 — Run all 5 suites for a model (from tests/agent-tests/)

# Blocking (foreground):
cd tests/agent-tests
source .venv/bin/activate
./run_all.sh qwen35-27b 0.7

# Greedy decoding (recommended for MoE models and reproducible scaling study):
./run_all.sh qwen35-122b 0.0

# Async via SSH with nohup (session can be closed afterwards):
nohup ./run_all.sh qwen35-27b 0.7 > logs/run_all_qwen35-27b_T07.out 2>&1 &
echo $!   # note the PID

# Follow progress:
tail -f logs/run_all_qwen35-27b_T07.out

# Abort:
kill <PID>

# 3 — Grade all 5 suites (skips already-judged files)
# judge.sh is graded interactively by Claude Code (judge_claude.py), not an
# external LLM API — no token cost, stays in the Claude Code plan budget.
./judge.sh export qwen35-27b T07
# ... Claude reads results/qwen35-27b/t07/*_export.jsonl, grades each record,
#     writes matching *_verdicts.jsonl ...
./judge.sh merge qwen35-27b T07

# 4 — Analyse results
python analyze_results.py qwen35-27b t07
```

> **Temperature in filenames:** The script encodes the temperature as a suffix
> `_T<digits>` in the JSON filename (`0.7` → `_T07`, `0.0` → `_T00`, `0.1` → `_T01`).
> Runs at different temperatures coexist in `results/` without overwriting each other.
>
> For the scaling study (all models comparable) `0.0` (greedy decoding) is recommended
> — reduces sampling noise and ensures MoE models like `qwen35-122b` reliably use
> function calling.

### Model run order (H200 reload overhead minimized)

```
qwen35-2b → qwen35-4b → qwen35-9b → qwen35-27b → qwen35-122b
→ qwen36-27b → qwen36-35b → qwen38-27b-coding
→ soofi-s-m7 (external mrk40 LiteLLM, no H200 reload)
→ qwen35-397b (Cortecs, last)
```

## Results structure

```
results/
  analysis.md                          ← cross-model aggregate
  {model}/
    t00/                               ← temperature 0.0 (greedy decoding)
    t07/                               ← temperature 0.7 (sampling)
      {model}_{suite}_N10_{T}.json           ← raw output (run_tests.py)
      {model}_{suite}_N10_{T}_judged.json    ← graded (judge_claude.py)
      analysis_{model}_{T}.md               ← per-model analysis (analyze_results.py)
```

### Temperature choice

| Suffix | Temperature | When to use |
|--------|-------------|-------------|
| `_T00` | 0.0 | Greedy decoding — reproducible; recommended for MoE models (qwen35-122b, qwen35-397b) where T=0.7 can suppress function-calling |
| `_T07` | 0.7 | Sampling — default for dense models |

### Suites

| Name | Content |
|------|---------|
| `bench_b` | B1–B6 retrieval queries (Benchmark B) |
| `containment_hall4` | Containment checks Hall 4 |
| `asset_specs` | Asset specification queries |
| `anti_pattern` | Anti-pattern detection (validator gates) |
| `srn_autonomous` | SRN write-path: atomic put_submodel, bypass detection, empty-submodel bypass |

## What the judge measures

| Field | Source | Meaning |
|-------|--------|---------|
| `judge.answer_correct` | Claude (interactive) | Final answer satisfies `ground_truth:` |
| `process.read_manuals_first` | programmatic | A manual/schema tool was called before the first query |
| `process.tool_errors` | programmatic | Validator/syntax/tool errors during the run |
| `all_good` | derived | All three signals satisfied |

## CLI

```
python run_tests.py [options]
  --cases PATH...        Case files or glob
  --variants VARIANT...  Variant filter (default: all from config)
  --repetitions N        Repetitions per case × variant (default: 1)
  --export PATH          JSON export (default: results/run_<ts>.json)
  --temperature T        Sampling temperature (default: 0.7)
  --include-tags TAGS    Only run cases with matching tag
  --exclude-tags TAGS    Skip cases with matching tag (default: none)
  --agent-url URL        Agent endpoint (default: agent_url from config.yaml)
  --config PATH          Config file (default: config.yaml)
  --strict-validation    Fail the run on case schema issues

python judge_claude.py export <raw.json> <cases.yaml> [<cases2.yaml> ...] \
    [--case-mapping-from <base.yaml>] --output <export>.jsonl
  # Claude reads the export and writes a matching verdicts .jsonl by hand,
  # grading against judge.py's JUDGE_PROMPT rubric.

python judge_claude.py merge <raw.json> <cases.yaml> [<cases2.yaml> ...] \
    [--case-mapping-from <base.yaml>] --verdicts <verdicts>.jsonl --output <out>_judged.json
```

`judge.py` (the original cortecs/gpt-5.4-based LLM judge) is still present and
usable stand-alone (`python judge.py --input ... --cases ... --base-url ... --model ...`)
for a fully-automated, non-interactive judge run — e.g. pointed at a local
vLLM endpoint instead of cortecs. `judge.sh` no longer calls it by default.

## Layout

```
framework/          # runner, evaluator, reporter, case loader
cases/              # YAML test cases with ground_truth: blocks
results/            # JSON exports + analyses (gitignored)
config.yaml         # defaults (agent URL, variants)
run_tests.py        # Phase 1: run agents, save raw results
judge.py            # strict bool judge against ground_truth — LLM API version (cortecs/vLLM), not used by judge.sh by default
judge_claude.py      # export/merge halves of the Claude-graded judge (imports judge.py's rubric + process checks)
analyze_results.py  # Phase 3: Markdown analysis per model
run_all.sh          # Run all 5 suites for one model in one go
judge.sh            # export|merge all 5 suites for one model (skips already-judged files)
```

## Adding cases

See `cases/bench_b.yaml` for the full schema. Relevant fields:

- `name`, `query` — required
- `ground_truth.required_facts` — facts the answer must support (LLM judge)
- `ground_truth.must_not_claim` — claims the answer must not positively assert
- `ground_truth.notes` — clarifications and edge cases for the judge
- `tags` — e.g. `bench_b`, `paper_eval`, `requires_fixture`
- `variants` — optional override; default: `default_variants` from config
