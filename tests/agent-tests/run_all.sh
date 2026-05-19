#!/bin/bash
# Run all test suites for a given model slug.
# Usage: ./run_all.sh <model-slug>
# Example: ./run_all.sh qwen35-27b
#
# $1 = model slug (used in export filenames)
# Results land in tests/agent-tests/results/
# N=20: paper eval uses ReAct only; N=20 gives ~60 obs/suite (20×3 configs or 20×6 queries)
#        sufficient for existence claims and coarse frequency estimates.
# N=10: smoke/regression tests where exact frequencies are not claimed.

set -e

# Load secrets (OPENAI_API_KEY for LLM judge) if available
[ -f "$HOME/.env.secrets" ] && source "$HOME/.env.secrets"

if [ -z "$1" ]; then
    echo "Usage: ./run_all.sh <model-slug>"
    exit 1
fi

MODEL=$1

# --- Paper Eval — Bench B: Retrieval ablation ---
python run_tests.py \
  --cases cases/bench_b.yaml \
  --variants aas-agent:react \
  --repetitions 20 \
  --export results/${MODEL}_bench_b_N20.json

# --- Containment Hall 4 ---
python run_tests.py \
  --cases cases/containment_hall4.yaml \
  --variants aas-agent:react \
  --repetitions 20 \
  --export results/${MODEL}_containment_hall4_N20.json

# --- Asset Specs ---
python run_tests.py \
  --cases cases/asset_specs.yaml \
  --variants aas-agent:react \
  --repetitions 20 \
  --export results/${MODEL}_asset_specs_N20.json

# --- Anti-Pattern idShort Lookup ---
python run_tests.py \
  --cases cases/anti_pattern_idShort_lookup.yaml \
  --variants aas-agent:react \
  --repetitions 20 \
  --export results/${MODEL}_anti_pattern_N20.json

# --- SRN Write-Path Bypass ---
python run_tests.py \
  --cases cases/srn_bypass.yaml \
  --variants aas-agent:react \
  --repetitions 20 \
  --export results/${MODEL}_srn_bypass_N20.json

# --- SRN Autonomous Creation — Variant B (typed tool) ---
python run_tests.py \
  --cases cases/srn_autonomous.yaml \
  --variants aas-agent:react \
  --repetitions 20 \
  --export results/${MODEL}_srn_autonomous_N20.json

# --- SRN Ablation — Variant A (generic tools) ---
python run_tests.py \
  --cases cases/srn_ablation_variant_a.yaml \
  --variants aas-agent:react \
  --repetitions 20 \
  --export results/${MODEL}_srn_ablation_variant_a_N20.json

# --- Naming Stress (requires renamed fixture from task_read_validation_gap T2) ---
# python run_tests.py \
#   --cases cases/naming_stress.yaml \
#   --repetitions 10 \
#   --export results/${MODEL}_naming_stress_N10.json

echo ""
echo "All suites done for model: ${MODEL}"
echo "Results in tests/agent-tests/results/${MODEL}_*.json"
