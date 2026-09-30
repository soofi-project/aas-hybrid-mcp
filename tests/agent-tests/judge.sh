#!/bin/bash
# Usage: ./judge.sh export <model-slug> <T-suffix, e.g. T07> [<repetitions>] [<reasoning-effort>]
#        ./judge.sh merge  <model-slug> <T-suffix, e.g. T07> [<repetitions>] [<reasoning-effort>]
# Example: ./judge.sh export qwen35-27b T07
#          ./judge.sh merge  qwen35-27b T07
#
# Judging is done by Claude Code interactively (judge_claude.py) instead of a
# token-billed LLM API call — stays inside the Claude Code plan budget.
# Two-step because grading happens in the chat session, not in this script:
#
#   1. `export` writes one <suite>_export.jsonl per suite that still needs
#      judging (skips suites whose _judged.json already exists), plus a
#      manifest file. Then STOP and tell Claude: "grade these exports".
#      Claude reads each *_export.jsonl, grades every record against
#      judge.py's JUDGE_PROMPT rubric, and writes a matching
#      *_verdicts.jsonl (one JSON line per idx: answer_correct/reasoning/
#      missing_facts/wrong_claims).
#   2. `merge` reads the manifest, calls judge_claude.py merge for every
#      suite whose verdicts file is now present, and runs analyze_results.py.
#
# Re-running `export` after some suites are already judged only exports the
# remaining ones (same skip-if-output-exists behavior as before).

MODE=$1
MODEL=$2
TEMPERATURE=$3
TEMPERATURE_LOWER=$(echo "$TEMPERATURE" | tr 'A-Z' 'a-z')
N="${4:-10}"
REASONING_EFFORT="${5:-}"
TH_SUFFIX=""
[ -n "$REASONING_EFFORT" ] && TH_SUFFIX="_TH${REASONING_EFFORT}"

if [ "$MODE" != "export" ] && [ "$MODE" != "merge" ]; then
    echo "Usage: $0 export|merge <model-slug> <T-suffix> [N] [reasoning-effort]" >&2
    exit 2
fi

BASE="results/$MODEL/${TEMPERATURE_LOWER}"
MANIFEST="$BASE/_judge_manifest_${MODEL}_${TEMPERATURE}${TH_SUFFIX}.tsv"

# manifest columns: input<TAB>cases(space-joined, may include a leading
# "MAPFROM:<path>" token)<TAB>export<TAB>verdicts<TAB>output

add_suite() {
    local input="$1"
    local cases="$2"        # space-separated case yaml paths, optionally prefixed "MAPFROM:<base.yaml> "
    local name_sub="$3"     # optional "from:to" substring swap applied to output/export/verdicts basenames
    local stem="${input%.json}"
    if [ -n "$name_sub" ]; then
        local from="${name_sub%%:*}"
        local to="${name_sub#*:}"
        stem="${stem/$from/$to}"
    fi
    local output="${stem}_judged.json"
    local export="${stem}_export.jsonl"
    local verdicts="${stem}_verdicts.jsonl"

    if [ -f "$output" ]; then
        echo "SKIP (already judged): $output"
        return
    fi
    if [ ! -f "$input" ]; then
        echo "SKIP (input missing): $input"
        return
    fi
    printf '%s\t%s\t%s\t%s\t%s\n' "$input" "$cases" "$export" "$verdicts" "$output" >> "$MANIFEST"
}

if [ "$MODE" = "export" ]; then
    : > "$MANIFEST"

    add_suite "$BASE/${MODEL}_asset_specs_N${N}_${TEMPERATURE}${TH_SUFFIX}.json" "cases/asset_specs.yaml" ""
    add_suite "$BASE/${MODEL}_asset_specs_N${N}_${TEMPERATURE}${TH_SUFFIX}.json" "MAPFROM:cases/asset_specs.yaml cases/anti_pattern_idShort_lookup.yaml" "asset_specs:anti_pattern"
    add_suite "$BASE/${MODEL}_bench_b_N${N}_${TEMPERATURE}${TH_SUFFIX}.json" "cases/bench_b.yaml" ""
    add_suite "$BASE/${MODEL}_containment_hall4_N${N}_${TEMPERATURE}${TH_SUFFIX}.json" "cases/containment_hall4.yaml" ""
    add_suite "$BASE/${MODEL}_srn_autonomous_N${N}_${TEMPERATURE}${TH_SUFFIX}.json" "cases/srn_autonomous.yaml" ""

    if [ ! -s "$MANIFEST" ]; then
        echo "Nothing to export — all suites already judged, or no raw results found."
        exit 0
    fi

    while IFS=$'\t' read -r input cases export verdicts output; do
        mapfrom=""
        case_args="$cases"
        if [[ "$cases" == MAPFROM:* ]]; then
            rest="${cases#MAPFROM:}"
            mapfrom="${rest%% *}"
            case_args="${rest#* }"
        fi
        echo "Exporting: $input ($case_args)"
        if [ -n "$mapfrom" ]; then
            python judge_claude.py export "$input" $case_args --case-mapping-from "$mapfrom" --output "$export"
        else
            python judge_claude.py export "$input" $case_args --output "$export"
        fi
    done < "$MANIFEST"

    echo ""
    echo "Wrote manifest: $MANIFEST"
    echo "Next: Claude grades each *_export.jsonl and writes a matching *_verdicts.jsonl,"
    echo "      then run: $0 merge $MODEL $TEMPERATURE $N $REASONING_EFFORT"
    exit 0
fi

# MODE = merge
if [ ! -f "$MANIFEST" ]; then
    echo "No manifest found ($MANIFEST) — run '$0 export ...' first." >&2
    exit 1
fi

while IFS=$'\t' read -r input cases export verdicts output; do
    mapfrom=""
    case_args="$cases"
    if [[ "$cases" == MAPFROM:* ]]; then
        rest="${cases#MAPFROM:}"
        mapfrom="${rest%% *}"
        case_args="${rest#* }"
    fi
    if [ ! -f "$verdicts" ]; then
        echo "SKIP (no verdicts yet): $verdicts"
        continue
    fi
    echo "Merging: $verdicts -> $output"
    if [ -n "$mapfrom" ]; then
        python judge_claude.py merge "$input" $case_args --case-mapping-from "$mapfrom" --verdicts "$verdicts" --output "$output"
    else
        python judge_claude.py merge "$input" $case_args --verdicts "$verdicts" --output "$output"
    fi
done < "$MANIFEST"

python analyze_results.py ${MODEL} ${TEMPERATURE_LOWER}
