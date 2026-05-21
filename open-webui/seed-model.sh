#!/usr/bin/env sh
# Seed the AAS Assistant workspace model into Open WebUI.
# Idempotent: creates admin user on first run, signs in on subsequent runs,
# then imports/updates the workspace model.
#
# Usage: seed-model.sh <open_webui_base_url>

set -eu

OPEN_WEBUI_URL="${1:-http://open-web-ui:8080}"
HEALTH_URL="${OPEN_WEBUI_URL}/health"

SEED_EMAIL="${SEED_EMAIL:-admin@aas-hybrid-mcp.local}"
SEED_PASSWORD="${SEED_PASSWORD:-admin}"
SEED_NAME="${SEED_NAME:-Admin}"

TIMEOUT="${SEED_TIMEOUT:-120}"
RETRY_INTERVAL=5

# --- Wait for Open WebUI ---
echo "Waiting for Open WebUI at ${HEALTH_URL}..."
deadline=$(($(date +%s) + TIMEOUT))
while true; do
    if curl --silent --fail "$HEALTH_URL" | jq -e '.status == true' > /dev/null 2>&1; then
        echo "Open WebUI is ready"
        break
    fi
    now=$(date +%s)
    if [ "$now" -ge "$deadline" ]; then
        echo "ERROR: Open WebUI not ready after ${TIMEOUT}s"
        exit 1
    fi
    sleep "$RETRY_INTERVAL"
done

# --- Authenticate (signup on first run, signin after) ---
echo "Authenticating..."
token=""

# Try signup first (works only when no users exist yet)
signup_response=$(curl --silent -w "\n%{http_code}" \
    -X POST "${OPEN_WEBUI_URL}/api/v1/auths/signup" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"${SEED_EMAIL}\",\"password\":\"${SEED_PASSWORD}\",\"name\":\"${SEED_NAME}\"}")

signup_status=$(echo "$signup_response" | tail -1)
signup_body=$(echo "$signup_response" | sed '$d')

if [ "$signup_status" = "200" ]; then
    token=$(echo "$signup_body" | jq -r '.token')
    echo "Created admin user"
else
    # Signup failed (user exists) — sign in instead
    signin_response=$(curl --silent -w "\n%{http_code}" \
        -X POST "${OPEN_WEBUI_URL}/api/v1/auths/signin" \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"${SEED_EMAIL}\",\"password\":\"${SEED_PASSWORD}\"}")

    signin_status=$(echo "$signin_response" | tail -1)
    signin_body=$(echo "$signin_response" | sed '$d')

    if [ "$signin_status" = "200" ]; then
        token=$(echo "$signin_body" | jq -r '.token')
        echo "Signed in as existing user"
    else
        echo "ERROR: Could not authenticate (signup=${signup_status}, signin=${signin_status})"
        echo "$signin_body"
        exit 1
    fi
fi

if [ -z "$token" ] || [ "$token" = "null" ]; then
    echo "ERROR: No token received"
    exit 1
fi

# --- Restrict vLLM connection to a single model ID ---
# Open WebUI is configured with two OPENAI_API_BASE_URLS:
#   index 0 → aas-agent (agentic chat)
#   index 1 → vLLM (LiteLLM proxy on H200, used for TASK_MODEL_EXTERNAL)
#
# Without a filter, Open WebUI lists every model the LiteLLM proxy exposes
# (potentially many). We pin connection 1 to the single model that
# TASK_MODEL_EXTERNAL needs (${TASK_MODEL_EXTERNAL:-}). This keeps the
# user dropdown tidy — five aas-agent:* entries + one ${LLM_MODEL} entry
# — without breaking title/tag/follow-up generation.
#
# model_ids in OPENAI_API_CONFIGS is a *synthesis* list (not an allowlist):
# Open WebUI renders each entry as-is without checking the upstream. The
# entry MUST be a real model on the upstream proxy or chat completions
# will 404. OPENAI_API_CONFIGS is a PersistentConfig, so we apply this via
# API on every restart (idempotent).
TASK_MODEL_ID="${TASK_MODEL_ID:-qwen36-27b}"
echo "Pinning vLLM connection to model_id=${TASK_MODEL_ID}..."
current_config=$(curl --silent --fail \
    -H "Authorization: Bearer ${token}" \
    "${OPEN_WEBUI_URL}/openai/config" || echo "")

if [ -z "$current_config" ]; then
    echo "WARN: Could not read /openai/config; skipping filter"
else
    filter_payload=$(echo "$current_config" \
        | jq --arg mid "$TASK_MODEL_ID" '.OPENAI_API_CONFIGS["1"] = {
            "enable": true,
            "model_ids": [$mid],
            "connection_type": "external",
            "prefix_id": "",
            "tags": []
        }')

    filter_status=$(curl --silent -o /dev/null -w "%{http_code}" \
        -X POST "${OPEN_WEBUI_URL}/openai/config/update" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${token}" \
        -d "$filter_payload")

    if [ "$filter_status" = "200" ]; then
        echo "vLLM connection pinned to single model"
    else
        echo "WARN: /openai/config/update returned ${filter_status}"
    fi
fi

echo "Seeding complete"
