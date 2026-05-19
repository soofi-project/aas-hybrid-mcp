#!/bin/bash
# Run all test suites for a given model slug.
# Usage: ./run_all.sh <model-slug>
# Example: ./run_all.sh qwen35-27b
#
# $1 = model slug (used in export filenames)
# Results land in tests/agent-tests/results/
# N=30: sufficient for frequency claims (±16pp CI); existence claims clear at N=10.

set -e

# Load secrets (OPENAI_API_KEY for LLM judge) if available
[ -f "$HOME/.env.secrets" ] && source "$HOME/.env.secrets"

if [ -z "$1" ]; then
    echo "Usage: ./run_all.sh <model-slug>"
    exit 1
fi

MODEL=$1

# --- Paper Eval (N=10, all 3 variants) ---
python run_tests.py \
  --cases cases/bench_b.yaml \
  --variants aas-agent:react aas-agent:plan aas-agent:reflexion \
  --repetitions 10 \
  --export results/${MODEL}_bench_b_N10.json

# --- Containment Hall 4 (N=10) ---
python run_tests.py \
  --cases cases/containment_hall4.yaml \
  --repetitions 10 \
  --export results/${MODEL}_containment_hall4_N10.json

# --- Asset Specs / Smoke Tests (N=10) ---
python run_tests.py \
  --cases cases/asset_specs.yaml \
  --repetitions 10 \
  --export results/${MODEL}_asset_specs_N10.json

# --- Anti-Pattern idShort Lookup (N=10) ---
python run_tests.py \
  --cases cases/anti_pattern_idShort_lookup.yaml \
  --repetitions 10 \
  --export results/${MODEL}_anti_pattern_N10.json

# --- SRN Write-Path Bypass (N=10) ---
python run_tests.py \
  --cases cases/srn_bypass.yaml \
  --repetitions 10 \
  --export results/${MODEL}_srn_bypass_N10.json

# --- SRN Autonomous Creation — Variant B (typed tool, N=10) ---
python run_tests.py \
  --cases cases/srn_autonomous.yaml \
  --repetitions 10 \
  --export results/${MODEL}_srn_autonomous_N10.json

# --- SRN Ablation — Variant A (generic tools, N=10) ---
python run_tests.py \
  --cases cases/srn_ablation_variant_a.yaml \
  --repetitions 10 \
  --export results/${MODEL}_srn_ablation_variant_a_N10.json

# --- Naming Stress (requires renamed fixture from task_read_validation_gap T2) ---
# python run_tests.py \
#   --cases cases/naming_stress.yaml \
#   --repetitions 10 \
#   --export results/${MODEL}_naming_stress_N10.json

echo ""
echo "All suites done for model: ${MODEL}"
echo "Results in tests/agent-tests/results/${MODEL}_*.json"
