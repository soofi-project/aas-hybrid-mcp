#!/bin/bash
# Judge-only wrapper for the agent test framework.
# Usage: ./judge.sh <results-json>

set -e

# Load secrets (e.g., OPENAI_API_KEY) if available (tolerate CRLF files)
if [ -f "$HOME/.env.secrets" ]; then
    set -o allexport
    # shellcheck disable=SC1090
    source <(tr -d '\r' < "$HOME/.env.secrets")
    set +o allexport
fi

if [ $# -ne 1 ]; then
    echo "Usage: ./judge.sh <results-json>"
    exit 1
fi

INPUT=$1

if [ ! -f "$INPUT" ]; then
    echo "File not found: $INPUT"
    exit 1
fi

INPUT_DIR=$(dirname "$INPUT")
INPUT_BASE=$(basename "$INPUT")

if [[ "$INPUT_BASE" == *.json ]]; then
    STEM=${INPUT_BASE%.json}
    OUTPUT="${STEM}_judged.json"
else
    STEM=$INPUT_BASE
    OUTPUT="${STEM}_judged.json"
fi

if [ -n "$INPUT_DIR" ] && [ "$INPUT_DIR" != "." ]; then
    OUTPUT_PATH="$INPUT_DIR/$OUTPUT"
else
    OUTPUT_PATH="$OUTPUT"
fi

python run_tests.py \
  --llm-judge \
  --judge-only "$INPUT" \
  --export "$OUTPUT_PATH"

echo ""
echo "Judge results written to $OUTPUT_PATH"
