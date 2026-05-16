# aas-agent-tests

External test framework that drives the AAS Hybrid MCP agent variants over
HTTP, collects metrics, and grades responses.

## Quick start

```powershell
pip install -e .
# Stack must be running with vLLM overlay:
#   ./up.sh --vllm
python run_tests.py --cases cases/containment_hall4.yaml
```

## CLI

```
python run_tests.py [options]

Options:
  --cases PATH...        Case file(s) or glob (default: cases/*.yaml)
  --variants VARIANT...  Filter variants (default: all from config)
  --repetitions N        Repetitions per case × variant (default: 1)
  --llm-judge            Enable LLM-judge evaluator (uses LLM_BASE_URL/LLM_MODEL)
  --export PATH          Write full results to JSON
  --agent-url URL        Override agent URL (default from config)
```

## Layout

```
framework/    # runner, evaluator, reporter, case loader
cases/        # YAML test case files
config.yaml   # defaults (agent URL, variants, LLM-judge endpoint)
run_tests.py  # CLI entry point
```

## Adding cases

See `cases/containment_hall4.yaml` for the schema. The loader rejects cases
that violate the unambiguous-question rule (no AAS jargon like "Welche Assets
sind in X" — see `task_agent_test_framework.md` Frage-Disambiguierung).
