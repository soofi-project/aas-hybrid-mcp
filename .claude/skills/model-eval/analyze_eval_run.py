#!/usr/bin/env python3
"""Deep-dive analysis for one model's eval run under tests/agent-tests/results/<slug>/<temp>/.

Computes, across all suites for a model+temperature:
  - correct rate (overall and per suite)
  - stream-error rate (agent-side crash/backend failure, distinct from model quality)
  - recursion-limit-hit rate (ran out of tool-call budget without converging)
  - correct rate excluding stream-error runs (with survivorship-bias caveat)
  - tool-call refusal check (did the model ever avoid calling tools?)
  - Cypher query-quality breakdown for query_aas_graph calls:
      validator rejection / syntax error / syntactically-valid-empty-result / returned data

Run from tests/agent-tests/:
  python ../../.claude/skills/model-eval/analyze_eval_run.py <model-slug> [--temp t07]

Requires the raw (non-judged) *_N10_<TEMP>.json files (for tool_calls) and the
*_judged.json files (for judge verdicts) to already exist in results/<slug>/<temp>/.
"""
import argparse
import glob
import json
import os
import sys

REFUSAL_KEYWORDS = [
    "cannot help", "i don't have access", "as an ai", "i'm not able",
    "cannot access", "i am unable", "not authorized", "i can't assist",
]

CAP_FRACTION_WARN = 0.9  # treat tool_call_count >= 90% of the observed max as "hit the cap"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def suite_name(path, model, temp):
    base = os.path.basename(path)
    return base.replace(f"{model}_", "").replace(f"_{temp.upper()}_judged.json", "").replace("_judged.json", "")


def classify_cypher(result_preview: str) -> str:
    rp = result_preview or ""
    if '"error":"forbidden_pattern"' in rp:
        return "validator_rejection"
    if "Neo.ClientError" in rp or "neo4j.exceptions" in rp or '"error":"{neo' in rp:
        return "syntax_error"
    if '"rows":[]' in rp or '"total":0' in rp:
        return "empty_result"
    return "returned_data"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model", help="model slug, e.g. soofi-s-m7")
    ap.add_argument("--temp", default="t07", help="temperature subdir (default: t07)")
    ap.add_argument("--results-dir", default="results", help="base results dir (default: results)")
    args = ap.parse_args()

    base = os.path.join(args.results_dir, args.model, args.temp)
    judged_files = sorted(glob.glob(os.path.join(base, "*_judged.json")))
    if not judged_files:
        print(f"No *_judged.json found under {base}", file=sys.stderr)
        sys.exit(1)

    all_records = []  # (suite, record_from_judged, raw_record_or_None)
    raw_by_suite = {}
    for jf in judged_files:
        raw_path = jf.replace("_judged.json", ".json")
        raw = load(raw_path) if os.path.exists(raw_path) else None
        raw_records_by_key = {}
        if raw:
            for r in raw["records"]:
                raw_records_by_key[(r["case"], r["repetition"])] = r["result"]
        suite = suite_name(jf, args.model, args.temp)
        d = load(jf)
        for r in d["records"]:
            key = (r["case"], r["repetition"])
            all_records.append((suite, r, raw_records_by_key.get(key)))

    # observed max tool_call_count = the effective step cap
    tcc = [r.get("tool_call_count", 0) for _, r, _ in all_records]
    cap = max(tcc) if tcc else 0

    print(f"# Eval-run analysis: {args.model} ({args.temp})\n")
    print(f"Suites: {len(judged_files)} · Records: {len(all_records)} · Observed step cap: {cap} tool calls\n")

    # per-suite table
    print("## Per-suite: correct / stream-error / cap-hit\n")
    print("| Suite | N | Correct | Stream-err | Cap-hit | Correct (clean) |")
    print("|---|--:|--:|--:|--:|--:|")
    by_suite = {}
    for suite, r, raw in all_records:
        by_suite.setdefault(suite, []).append((r, raw))

    tot_n = tot_correct = tot_stream = tot_cap = tot_clean = tot_clean_correct = 0
    for suite, items in by_suite.items():
        n = len(items)
        correct = sum(1 for r, _ in items if r["judge"].get("answer_correct"))
        stream = sum(1 for r, _ in items if "stream error" in (r.get("final_answer") or ""))
        cap_hit = sum(1 for r, _ in items if r.get("tool_call_count", 0) >= cap)
        clean = [(r, raw) for r, raw in items if "stream error" not in (r.get("final_answer") or "")]
        clean_correct = sum(1 for r, _ in clean if r["judge"].get("answer_correct"))
        tot_n += n; tot_correct += correct; tot_stream += stream; tot_cap += cap_hit
        tot_clean += len(clean); tot_clean_correct += clean_correct
        clean_rate = f"{clean_correct}/{len(clean)} ({100*clean_correct/len(clean):.0f}%)" if clean else "n/a"
        print(f"| {suite} | {n} | {correct} ({100*correct/n:.0f}%) | {stream} ({100*stream/n:.0f}%) | "
              f"{cap_hit} ({100*cap_hit/n:.0f}%) | {clean_rate} |")

    clean_rate_tot = f"{tot_clean_correct}/{tot_clean} ({100*tot_clean_correct/tot_clean:.0f}%)" if tot_clean else "n/a"
    print(f"| **Total** | **{tot_n}** | **{tot_correct} ({100*tot_correct/tot_n:.0f}%)** | "
          f"**{tot_stream} ({100*tot_stream/tot_n:.0f}%)** | **{tot_cap} ({100*tot_cap/tot_n:.0f}%)** | "
          f"**{clean_rate_tot}** |\n")

    if tot_stream and tot_clean < tot_n:
        surviving_frac = tot_clean / tot_n
        print(f"> Note: the \"Correct (clean)\" column drops {tot_stream} stream-error runs "
              f"({100*(1-surviving_frac):.0f}% of all runs). This is *not* a random subsample — "
              "stream errors correlate with longer/harder runs — so treat clean-only rates as an "
              "optimistic upper bound, not a like-for-like comparison at full statistical power.\n")

    # tool-call refusal check
    print("## Tool-call refusal check\n")
    min_tcc = min(tcc) if tcc else None
    refusals = []
    for suite, r, raw in all_records:
        fa = (r.get("final_answer") or "").lower()
        if any(k in fa for k in REFUSAL_KEYWORDS):
            refusals.append((suite, r.get("repetition")))
    print(f"Minimum tool_call_count across all runs: **{min_tcc}**")
    print(f"Refusal-style final answers found: **{len(refusals)}**")
    if refusals:
        for s, rep in refusals[:10]:
            print(f"  - {s} rep {rep}")
    print()

    # Cypher query-quality breakdown
    print("## Cypher (`query_aas_graph`) query-quality breakdown\n")
    counts = {"validator_rejection": 0, "syntax_error": 0, "empty_result": 0, "returned_data": 0}
    total_calls = 0
    for suite, r, raw in all_records:
        if not raw:
            continue
        for tc in raw.get("tool_calls", []):
            if tc.get("name") != "query_aas_graph":
                continue
            total_calls += 1
            counts[classify_cypher(tc.get("result_preview", ""))] += 1

    if total_calls:
        print("| Outcome | Count | Share |")
        print("|---|--:|--:|")
        labels = {
            "validator_rejection": "Validator rejection (forbidden anti-pattern)",
            "syntax_error": "Cypher syntax error (Neo4j exception)",
            "empty_result": "Syntactically valid, zero rows",
            "returned_data": "Syntactically valid, returned data",
        }
        for key in ["validator_rejection", "syntax_error", "empty_result", "returned_data"]:
            c = counts[key]
            print(f"| {labels[key]} | {c} | {100*c/total_calls:.0f}% |")
        print(f"\nTotal `query_aas_graph` calls analyzed: {total_calls}\n")
    else:
        print("No raw (non-judged) result files with tool_calls found — skipping Cypher breakdown. "
              "(Need results/<model>/<temp>/*_N10_<TEMP>.json alongside the *_judged.json files.)\n")


if __name__ == "__main__":
    main()
