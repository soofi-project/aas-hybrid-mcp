#!/bin/bash
# Switch the eval model and restart the stack.
#
# Usage:
#   ./eval-model.sh qwen35-27b
#   ./eval-model.sh qwen35-2b
#   ./eval-model.sh qwen35-397b   # Cortecs — set OPENAI_API_KEY in ~/.env.secrets
#
# Available slugs:
#   qwen35-08b   qwen35-2b    qwen35-4b    qwen35-9b    qwen35-27b    qwen35-122b    qwen35-397b (Cortecs)
#   qwen36-27b   qwen36-35b
#
# How it works:
#   Copies .env.model.<slug> to .env.model, then runs docker compose with
#   docker-compose.eval-model.yml as final overlay. That overlay appends
#   .env.model as the last env_file entry for each service, so its LLM_MODEL /
#   LLM_BASE_URL / QUERY_REWRITE_* values win over .env.vllm.
#
# Prerequisites:
#   - LiteLLM alias for the chosen model must be configured on the H200.
#     See comments in .env.model.<slug> for the required alias name.
#   - For qwen35-397b: OPENAI_API_KEY in ~/.env.secrets must be the Cortecs key.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure IDTA templates submodule is present (one-time init; skipped if already populated)
if [ ! -f "idta_templates/README.md" ]; then
    echo "[INFO] Initializing idta_templates submodule..."
    git submodule update --init idta_templates
fi

SLUGS="qwen35-08b qwen35-2b qwen35-4b qwen35-9b qwen35-27b qwen35-122b qwen35-397b qwen36-27b qwen36-35b"

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

# .env.model is the temp file loaded by docker-compose.eval-model.yml
cp "$ENV_FILE" .env.model

echo "========================================"
echo "  Eval Model: $MODEL"
grep -v '^#' .env.model | grep -v '^$'
echo "========================================"

# Source for compose variable substitution (${VAR} in compose yaml)
source .env 2>/dev/null || true
set -a
source .env.vllm
source .env.model
set +a

docker compose \
  -f docker-compose.yml \
  -f docker-compose.vllm.yml \
  -f docker-compose.eval-model.yml \
  up -d --wait --build

echo ""
echo "========================================"
echo "  Stack ready — active model: $MODEL"
echo "========================================"
echo ""
echo "Verify:  docker exec aas-agent printenv | grep LLM_MODEL"
echo "Eval:    python tests/agent-tests/run_tests.py"
echo ""
