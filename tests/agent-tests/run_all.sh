#!/bin/bash
# Run all test suites for a given model slug.
# Usage: ./run_all.sh <model-slug>
# Example: ./run_all.sh qwen35-27b
#
# $1 = model slug (used in export filenames)
# Results land in tests/agent-tests/results/
# N=10: existence claims; 6 cases × 10 reps = 60 obs/suite — sufficient for the
#        model-size sweep. Results land in JSON regardless of pass/fail exit codes.

# Load secrets (OPENAI_API_KEY for LLM judge) if available (tolerate CRLF files)
if [ -f "$HOME/.env.secrets" ]; then
    set -o allexport
    # shellcheck disable=SC1090
    source <(tr -d '\r' < "$HOME/.env.secrets")
    set +o allexport
fi

if [ -z "$1" ]; then
    echo "Usage: ./run_all.sh <model-slug>"
    exit 1
fi

MODEL=$1
VARIANTS="aas-agent:react"
N=10

# --- Paper Eval — Bench B: Retrieval ablation ---
python run_tests.py \
  --cases cases/bench_b.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --export results/${MODEL}_bench_b_N${N}.json

# --- Containment Hall 4 ---
python run_tests.py \
  --cases cases/containment_hall4.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --export results/${MODEL}_containment_hall4_N${N}.json

# --- Asset Specs ---
python run_tests.py \
  --cases cases/asset_specs.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --export results/${MODEL}_asset_specs_N${N}.json

# --- Anti-Pattern idShort Lookup ---
python run_tests.py \
  --cases cases/anti_pattern_idShort_lookup.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --export results/${MODEL}_anti_pattern_N${N}.json

# --- SRN Write-Path Bypass ---
python run_tests.py \
  --cases cases/srn_bypass.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --export results/${MODEL}_srn_bypass_N${N}.json

# --- SRN Autonomous Creation — Variant B (typed tool) ---
python run_tests.py \
  --cases cases/srn_autonomous.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --export results/${MODEL}_srn_autonomous_N${N}.json

# --- SRN Ablation — Variant A (generic tools) ---
python run_tests.py \
  --cases cases/srn_ablation_variant_a.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --export results/${MODEL}_srn_ablation_variant_a_N${N}.json

# --- Naming Stress (requires renamed fixture from task_read_validation_gap T2) ---
# python run_tests.py \
#   --cases cases/naming_stress.yaml \
#   --variants $VARIANTS \
#   --repetitions $N \
#   --export results/${MODEL}_naming_stress_N${N}.json

echo ""
echo "All suites done for model: ${MODEL}"
echo "Results in tests/agent-tests/results/${MODEL}_*.json"
