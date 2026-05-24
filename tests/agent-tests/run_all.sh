#!/bin/bash
# Run all test suites for a given model slug.
# Usage: ./run_all.sh <model-slug> [<temperature>]
# Example: ./run_all.sh qwen35-27b 0.7
#          ./run_all.sh qwen35-122b 0.0
#
# $1 = model slug (used in export filenames)
# $2 = sampling temperature (default: 0.7)
#
# Temperature is encoded in the output filename as _T<digits>, e.g.:
#   0.7 → _T07   0.0 → _T00   0.1 → _T01
#
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
    echo "Usage: ./run_all.sh <model-slug> [<temperature>]"
    exit 1
fi

MODEL=$1
TEMPERATURE="${2:-0.7}"
T_SUFFIX="T$(echo "$TEMPERATURE" | tr -d '.')"
T_DIR="$(echo "${T_SUFFIX}" | tr 'A-Z' 'a-z')"

VARIANTS="aas-agent:react"
N=10

# Output directory: results/{model}/{t_dir}/  (matches judge.sh + analyze_results.py)
OUT="results/${MODEL}/${T_DIR}"
mkdir -p "$OUT"

# --- Paper Eval — Bench B: Retrieval ablation ---
python3 run_tests.py \
  --cases cases/bench_b.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --temperature $TEMPERATURE \
  --export ${OUT}/${MODEL}_bench_b_N${N}_${T_SUFFIX}.json

# --- Containment Hall 4 ---
python3 run_tests.py \
  --cases cases/containment_hall4.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --temperature $TEMPERATURE \
  --export ${OUT}/${MODEL}_containment_hall4_N${N}_${T_SUFFIX}.json

# --- Asset Specs ---
python3 run_tests.py \
  --cases cases/asset_specs.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --temperature $TEMPERATURE \
  --export ${OUT}/${MODEL}_asset_specs_N${N}_${T_SUFFIX}.json

# --- Anti-Pattern idShort Lookup ---
python3 run_tests.py \
  --cases cases/anti_pattern_idShort_lookup.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --temperature $TEMPERATURE \
  --export ${OUT}/${MODEL}_anti_pattern_N${N}_${T_SUFFIX}.json

# --- SRN Autonomous Creation (generic put_submodel path) ---
python3 run_tests.py \
  --cases cases/srn_autonomous.yaml \
  --variants $VARIANTS \
  --repetitions $N \
  --temperature $TEMPERATURE \
  --export ${OUT}/${MODEL}_srn_autonomous_N${N}_${T_SUFFIX}.json

# --- Naming Stress (requires renamed fixture from task_read_validation_gap T2) ---
# python run_tests.py \
#   --cases cases/naming_stress.yaml \
#   --variants $VARIANTS \
#   --repetitions $N \
#   --export ${OUT}/${MODEL}_naming_stress_N${N}.json

echo ""
echo "All suites done for model: ${MODEL} (temperature: ${TEMPERATURE})"
echo "Results in ${OUT}/"
