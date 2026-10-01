#!/bin/bash
# Switch the eval model and restart the stack.
#
# Usage:
#   ./eval-model.sh qwen35-27b
#   ./eval-model.sh qwen35-2b
#   ./eval-model.sh qwen35-397b   # Cortecs — set CORTECSAI_API_KEY in ~/.env.secrets
#   ./eval-model.sh soofi-s-m7    # external LiteLLM (mrk40) — set SOOFI_LLM_API_KEY in ~/.env.secrets
#   ./eval-model.sh nemotron3-ultra-550b   # OpenRouter — set OPENROUTER_API_KEY in ~/.env.secrets
#
# Available slugs:
#   qwen35-2b    qwen35-4b    qwen35-9b    qwen35-27b    qwen35-35b (MoE, ~3B active)
#   qwen35-122b (MoE, ~10B active)    qwen35-397b (Cortecs)
#   qwen36-27b   qwen36-35b (MoE, ~22B active)
#   qwen38-27b-coding (H200, same LiteLLM as the qwen3x aliases above)
#   soofi-s-spree (direct vLLM 10.2.10.44, Soofi-S-Spree-Preview)
#   soofi-s-m7   nemotron3-nano-30b   rlvr-spree-c1-3-hf_step_400 (external LiteLLM proxy at soofi-lite.l3s.de)
#   nemotron3-ultra-550b (OpenRouter)
#
# How it works:
#   Copies .env.model.<slug> to .env.model, then runs docker compose with
#   docker-compose.eval-model-vllm.yml (H200 models),
#   docker-compose.eval-model-cortecs.yml (qwen35-397b),
#   docker-compose.eval-model-litellm.yml (soofi-* models), or
#   docker-compose.eval-model-openrouter.yml (nemotron3-ultra-550b) as final overlay.
#   That overlay appends .env.model as the last env_file entry for each service,
#   so its LLM_MODEL / LLM_BASE_URL / QUERY_REWRITE_* values win over .env.vllm.
#
# Prerequisites:
#   - LiteLLM alias for the chosen model must be configured on the H200.
#     See comments in .env.model.<slug> for the required alias name.
#   - For qwen35-397b: CORTECSAI_API_KEY in ~/.env.secrets must be the Cortecs key.
#   - For soofi-*: SOOFI_LLM_API_KEY in ~/.env.secrets must be the mrk40 LiteLLM key.
#   - For nemotron3-ultra-550b: OPENROUTER_API_KEY in ~/.env.secrets must be the OpenRouter key.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure IDTA templates submodule is present (one-time init; skipped if already populated)
if [ ! -f "idta_templates/README.md" ]; then
    echo "[INFO] Initializing idta_templates submodule..."
    git submodule update --init idta_templates
fi

SLUGS="soofi-s-spree qwen35-2b qwen35-4b qwen35-9b qwen35-27b qwen35-35b qwen35-122b qwen35-397b qwen36-27b qwen36-35b qwen38-27b-coding soofi-s-m7 nemotron3-nano-30b rlvr-spree-c1-3-hf_step_400 nemotron3-ultra-550b"

MODEL=${1:-}
if [ -z "$MODEL" ]; then
    echo "Usage: ./eval-model.sh <model-slug>"
    echo "Available: $SLUGS"
    exit 1
fi

ENV_FILE=".env.model.${MODEL}"
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found."
    echo "Available: $SLUGS"
    exit 1
fi

# .env.model is the temp file loaded by the eval-model overlay
cp "$ENV_FILE" .env.model

case "$MODEL" in
    qwen35-397b)
        EVAL_OVERLAY="docker-compose.eval-model-cortecs.yml"
        ;;
    soofi-s-spree)
        # direct vLLM (10.2.10.44), same shape as the H200 models: no proxy key
        EVAL_OVERLAY="docker-compose.eval-model-vllm.yml"
        ;;
    soofi-*|nemotron3-nano-30b|rlvr-spree-c1-3-hf_step_400)
        EVAL_OVERLAY="docker-compose.eval-model-litellm.yml"
        ;;
    nemotron3-ultra-550b)
        EVAL_OVERLAY="docker-compose.eval-model-openrouter.yml"
        ;;
    *)
        EVAL_OVERLAY="docker-compose.eval-model-vllm.yml"
        ;;
esac

echo "========================================"
echo "  Eval Model: $MODEL"
grep -v '^#' .env.model | grep -v '^$'
echo "========================================"

# Source for compose variable substitution (${VAR} in compose yaml)
source .env 2>/dev/null || true
set -a
source .env.vllm
source .env.model
if [[ "$MODEL" == "qwen35-397b" || "$MODEL" == soofi-* || "$MODEL" == "nemotron3-nano-30b" || "$MODEL" == "rlvr-spree-c1-3-hf_step_400" || "$MODEL" == "nemotron3-ultra-550b" ]]; then
    source ~/.env.secrets 2>/dev/null || true
fi
set +a

docker compose \
  -f docker-compose.yml \
  -f docker-compose.vllm.yml \
  -f "$EVAL_OVERLAY" \
  up -d --wait --build

echo ""
echo "========================================"
echo "  Stack ready — active model: $MODEL"
echo "========================================"
echo ""
echo "Verify:  docker exec aas-agent printenv | grep LLM_MODEL"
echo ""
echo "Run all test suites (from tests/agent-tests/):"
echo "  ./run_all.sh ${MODEL}"
echo ""
echo "Or paper eval only (bench_b, N=10):"
echo "  python run_tests.py --cases cases/bench_b.yaml --repetitions 10 --export results/${MODEL}_bench_b_N10.json"
echo ""
