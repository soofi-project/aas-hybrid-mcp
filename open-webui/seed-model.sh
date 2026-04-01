#!/usr/bin/env sh
# Seed the AAS Assistant workspace model into Open WebUI.
# Idempotent: creates admin user on first run, signs in on subsequent runs,
# then imports/updates the workspace model.
#
# Usage: seed-model.sh <open_webui_base_url>

set -eu

OPEN_WEBUI_URL="${1:-http://open-webui:8080}"
MODEL_JSON="/app/model.json"
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

# --- Import model ---
echo "Importing workspace model..."
import_payload="/tmp/import-payload.json"
jq -c '{models: [.]}' "$MODEL_JSON" > "$import_payload"

import_response=$(curl --silent -w "\n%{http_code}" \
    -X POST "${OPEN_WEBUI_URL}/api/v1/models/import" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${token}" \
    -d @"$import_payload")

import_status=$(echo "$import_response" | tail -1)
import_body=$(echo "$import_response" | sed '$d')

if [ "$import_status" = "200" ]; then
    echo "Model import successful"
else
    echo "ERROR: Model import failed (status=${import_status})"
    echo "$import_body"
    exit 1
fi

echo "Seeding complete"
