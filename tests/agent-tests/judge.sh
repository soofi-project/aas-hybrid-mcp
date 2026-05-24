#!/bin/bash

source ~/.env.secrets
export CORTECSAI_API_KEY

MODEL=$1
TEMPERATURE=$2
TEMPERATURE_LOWER=$(echo "$TEMPERATURE" | tr 'A-Z' 'a-z')

BASE="results/$MODEL/${TEMPERATURE_LOWER}"

judge_if_needed() {
    local input="$1"
    local cases="$2"
    local output="${input%.json}_judged.json"

    if [ -f "$output" ]; then
        echo "SKIP (already judged): $output"
        return
    fi

    if [ ! -f "$input" ]; then
        echo "SKIP (input missing): $input"
        return
    fi

    echo "Judging: $input"
    python judge.py \
        --input "$input" \
        --cases "$cases" \
        --base-url https://api.cortecs.ai \
        --model gpt-5.4 \
        --api-key-env CORTECSAI_API_KEY
}

judge_if_needed "$BASE/${MODEL}_anti_pattern_N10_${TEMPERATURE}.json"           cases/anti_pattern_idShort_lookup.yaml
judge_if_needed "$BASE/${MODEL}_asset_specs_N10_${TEMPERATURE}.json"            cases/asset_specs.yaml
judge_if_needed "$BASE/${MODEL}_bench_b_N10_${TEMPERATURE}.json"                cases/bench_b.yaml
judge_if_needed "$BASE/${MODEL}_containment_hall4_N10_${TEMPERATURE}.json"      cases/containment_hall4.yaml
judge_if_needed "$BASE/${MODEL}_srn_autonomous_N10_${TEMPERATURE}.json"         cases/srn_autonomous.yaml

python analyze_results.py ${MODEL} ${TEMPERATURE_LOWER}

