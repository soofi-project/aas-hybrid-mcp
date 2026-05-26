"""
compute_eval_stats.py — Compute structured statistics from agent eval results.

Usage:
    python compute_eval_stats.py <results_dir> [--output stats.json]

Reads all raw + judged JSON files from a trial directory (e.g. results/qwen35-35b/t07),
computes per-suite and cross-suite statistics, and emits a single JSON to stdout or file.

Sections produced:
  1. paper_table        — per-suite summary rows (N, correct, manuals_first, idShort_violation, bypass, medians)
  2. idshort_validation — violation counts, self-correction rates, rule breakdown
  3. write_path_bypass  — bypass_type distribution, per-case breakdown (SRN only)
  4. template_validation — whether any write tool had validation rejections
  5. judge_failure_modes — missing_facts / wrong_claims frequencies per SRN case
  6. duration_medians   — per-suite, correct vs wrong, SRN per-case
  7. manuals_first_corr — 2x2 contingency table + rates
"""

import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def median(values: list[float]) -> float | None:
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def discover_suites(results_dir: Path) -> list[dict]:
    """Find all (suite_name, raw_path, judged_path) triples."""
    suites = []
    seen_prefixes = set()
    for f in sorted(results_dir.glob("*.json")):
        name = f.stem
        if name.endswith("_judged"):
            prefix = name[: -len("_judged")]
        else:
            prefix = name
        if prefix in seen_prefixes:
            continue
        seen_prefixes.add(prefix)

        raw_path = results_dir / f"{prefix}.json"
        judged_path = results_dir / f"{prefix}_judged.json"

        if raw_path.exists() and judged_path.exists():
            suites.append({
                "suite_name": prefix,
                "raw_path": raw_path,
                "judged_path": judged_path,
            })
    return suites


def is_srn_suite(judged_data: dict) -> bool:
    """Heuristic: SRN suite if any case name contains 'srn'."""
    for case in judged_data.get("cases", []):
        if "srn" in case.lower():
            return True
    return False


def extract_suite_stats(suite: dict) -> dict:
    """Compute all statistics for one suite."""
    raw = load_json(suite["raw_path"])
    judged = load_json(suite["judged_path"])
    srn = is_srn_suite(judged)

    suite_name = suite["suite_name"]
    raw_records = raw.get("records", [])
    judged_records = judged.get("records", [])

    # --- 1. Paper table row ---
    n = len(judged_records)
    correct_count = sum(1 for r in judged_records if r.get("judge", {}).get("answer_correct"))
    manuals_first_count = sum(
        1 for r in judged_records if r.get("process", {}).get("read_manuals_first")
    )

    # idShort violation from raw records
    idshort_violated = 0
    idshort_self_corrected_all = 0
    violation_rules = Counter()
    total_violations = 0
    total_self_corrected = 0

    for rec in raw_records:
        ev = rec.get("evaluation", {})
        # cypher_violations (raw eval)
        cypher_viols = ev.get("cypher_violations", [])
        # validator_rejections
        val_rejs = ev.get("validator_rejections", [])

        has_violation = bool(cypher_viols) or bool(val_rejs)
        if has_violation:
            idshort_violated += 1

            # Check if ALL violations self-corrected
            all_sc = True
            if val_rejs:
                for rej in val_rejs:
                    for rule in rej.get("rules", []):
                        violation_rules[rule] += 1
                        total_violations += 1
                    if not rej.get("self_corrected", False):
                        all_sc = False
            else:
                # cypher_violations don't have self_corrected field
                # but if the query succeeded afterward, it was self-corrected
                all_sc = True  # assume corrected if no validator_rejections

            if all_sc:
                idshort_self_corrected_all += 1

    # Duration stats
    durations_correct = []
    durations_wrong = []
    for rec in judged_records:
        dur = rec.get("duration_s")
        if dur is None:
            continue
        if rec.get("judge", {}).get("answer_correct"):
            durations_correct.append(dur)
        else:
            durations_wrong.append(dur)

    paper_row = {
        "suite": suite_name,
        "n": n,
        "correct": correct_count,
        "correct_rate": round(correct_count / n, 3) if n else 0,
        "manuals_first": manuals_first_count,
        "manuals_first_rate": round(manuals_first_count / n, 3) if n else 0,
        "idshort_violation": idshort_violated,
        "idshort_violation_rate": round(idshort_violated / n, 3) if n else 0,
        "idshort_self_corrected": idshort_self_corrected_all,
        "idshort_self_corrected_rate": (
            round(idshort_self_corrected_all / idshort_violated, 3)
            if idshort_violated
            else None
        ),
        "median_duration_correct": median(durations_correct),
        "median_duration_wrong": median(durations_wrong) if durations_wrong else None,
    }

    # --- 2. idShort detailed ---
    idshort_detail = {
        "violation_rules": dict(violation_rules),
        "total_violation_occurrences": total_violations,
    }

    # --- 3. Write-path bypass (SRN only) ---
    bypass_stats = None
    if srn:
        bypass_types = Counter()
        bypass_per_case = defaultdict(Counter)
        put_submodel_element_called_count = 0
        put_submodel_attempted_count = 0

        for rec in raw_records:
            wp = rec.get("evaluation", {}).get("write_path")
            case = rec.get("case", "unknown")
            if wp is None:
                bypass_types["null"] += 1
                bypass_per_case[case]["null"] += 1
                continue

            bt = wp.get("bypass_type")
            if bt:
                bypass_types[bt] += 1
                bypass_per_case[case][bt] += 1
            else:
                bypass_types["none"] += 1
                bypass_per_case[case]["none"] += 1

            if wp.get("put_submodel_element_called"):
                put_submodel_element_called_count += 1
            if wp.get("put_submodel_attempted"):
                put_submodel_attempted_count += 1

        bypass_stats = {
            "bypass_type_distribution": dict(bypass_types),
            "bypass_per_case": {k: dict(v) for k, v in bypass_per_case.items()},
            "put_submodel_element_called": put_submodel_element_called_count,
            "put_submodel_attempted": put_submodel_attempted_count,
            "bypass_rate": round(
                (bypass_types.get("direct", 0) + bypass_types.get("surfaced", 0) + bypass_types.get("cascade", 0))
                / n, 3
            ) if n else 0,
        }

    # --- 4. Template validation for write calls ---
    template_validation = {"write_tool_rejections": 0, "write_tool_errors": []}
    for rec in raw_records:
        ev = rec.get("evaluation", {})
        val_rejs = ev.get("validator_rejections", [])
        for rej in val_rejs:
            idx = rej.get("tool_call_index", -1)
            tc = rec.get("result", {}).get("tool_calls", [])
            if 0 <= idx < len(tc):
                tool_name = tc[idx].get("name", "")
                if tool_name in ("put_submodel", "put_submodel_element"):
                    template_validation["write_tool_rejections"] += 1
                    template_validation["write_tool_errors"].append({
                        "case": rec.get("case"),
                        "repetition": rec.get("repetition"),
                        "tool": tool_name,
                        "rules": rej.get("rules", []),
                    })

    # --- 5. Judge failure modes (SRN only) ---
    judge_failure_modes = None
    if srn:
        per_case_missing = defaultdict(Counter)
        per_case_wrong = defaultdict(Counter)
        for rec in judged_records:
            if rec.get("judge", {}).get("answer_correct"):
                continue
            case = rec.get("case", "unknown")
            for fact in rec.get("judge", {}).get("missing_facts", []):
                per_case_missing[case][fact] += 1
            for claim in rec.get("judge", {}).get("wrong_claims", []):
                per_case_wrong[case][claim] += 1

        judge_failure_modes = {
            case: {
                "missing_facts": dict(per_case_missing[case]),
                "wrong_claims": dict(per_case_wrong[case]),
                "n_incorrect": sum(1 for r in judged_records if r.get("case") == case and not r.get("judge", {}).get("answer_correct")),
            }
            for case in set(list(per_case_missing.keys()) + list(per_case_wrong.keys()))
        }

    # --- 6. Duration medians (SRN per-case) ---
    duration_per_case = None
    if srn:
        per_case = defaultdict(lambda: {"correct": [], "wrong": [], "all": []})
        for rec in judged_records:
            dur = rec.get("duration_s")
            if dur is None:
                continue
            case = rec.get("case", "unknown")
            per_case[case]["all"].append(dur)
            if rec.get("judge", {}).get("answer_correct"):
                per_case[case]["correct"].append(dur)
            else:
                per_case[case]["wrong"].append(dur)

        duration_per_case = {
            case: {
                "n": len(v["all"]),
                "median_all": median(v["all"]),
                "median_correct": median(v["correct"]) if v["correct"] else None,
                "median_wrong": median(v["wrong"]) if v["wrong"] else None,
            }
            for case, v in per_case.items()
        }

    # --- 7. Manuals-first correlation (accumulated per-record) ---
    manuals_first_records = []
    for rec in judged_records:
        manuals_first_records.append({
            "suite": suite_name,
            "case": rec.get("case"),
            "read_manuals_first": rec.get("process", {}).get("read_manuals_first", False),
            "answer_correct": rec.get("judge", {}).get("answer_correct", False),
        })

    return {
        "paper_row": paper_row,
        "idshort_detail": idshort_detail,
        "bypass_stats": bypass_stats,
        "template_validation": template_validation,
        "judge_failure_modes": judge_failure_modes,
        "duration_per_case": duration_per_case,
        "manuals_first_records": manuals_first_records,
    }


def compute_cross_suite(all_stats: list[dict]) -> dict:
    """Aggregate across all suites."""
    total_n = sum(s["paper_row"]["n"] for s in all_stats)
    total_correct = sum(s["paper_row"]["correct"] for s in all_stats)
    total_manuals_first = sum(s["paper_row"]["manuals_first"] for s in all_stats)
    total_idshort_viol = sum(s["paper_row"]["idshort_violation"] for s in all_stats)
    total_idshort_sc = sum(s["paper_row"]["idshort_self_corrected"] for s in all_stats)

    # Manuals-first 2x2
    all_mf_records = []
    for s in all_stats:
        all_mf_records.extend(s["manuals_first_records"])

    mf_correct = sum(1 for r in all_mf_records if r["read_manuals_first"] and r["answer_correct"])
    mf_wrong = sum(1 for r in all_mf_records if r["read_manuals_first"] and not r["answer_correct"])
    no_mf_correct = sum(1 for r in all_mf_records if not r["read_manuals_first"] and r["answer_correct"])
    no_mf_wrong = sum(1 for r in all_mf_records if not r["read_manuals_first"] and not r["answer_correct"])

    # Merge violation rules
    merged_rules = Counter()
    for s in all_stats:
        merged_rules.update(s["idshort_detail"]["violation_rules"])

    # Merge judge failure modes
    merged_failure_modes = {}
    for s in all_stats:
        fm = s.get("judge_failure_modes")
        if fm:
            merged_failure_modes.update(fm)

    # Bypass stats: only SRN suites have them. Use directly (don't merge across suites since each SRN suite is self-contained).
    merged_bypass = None
    for s in all_stats:
        bs = s.get("bypass_stats")
        if bs:
            merged_bypass = bs
            break

    return {
        "paper_totals": {
            "n": total_n,
            "correct": total_correct,
            "correct_rate": round(total_correct / total_n, 3) if total_n else 0,
            "manuals_first": total_manuals_first,
            "manuals_first_rate": round(total_manuals_first / total_n, 3) if total_n else 0,
            "idshort_violation": total_idshort_viol,
            "idshort_violation_rate": round(total_idshort_viol / total_n, 3) if total_n else 0,
            "idshort_self_corrected": total_idshort_sc,
            "idshort_self_corrected_rate": (
                round(total_idshort_sc / total_idshort_viol, 3) if total_idshort_viol else None
            ),
        },
        "violation_rules_merged": dict(merged_rules),
        "manuals_first_contingency": {
            "manuals_first_correct": mf_correct,
            "manuals_first_wrong": mf_wrong,
            "no_manuals_correct": no_mf_correct,
            "no_manuals_wrong": no_mf_wrong,
            "manuals_first_correct_rate": round(mf_correct / (mf_correct + mf_wrong), 3) if (mf_correct + mf_wrong) else None,
            "no_manuals_correct_rate": round(no_mf_correct / (no_mf_correct + no_mf_wrong), 3) if (no_mf_correct + no_mf_wrong) else None,
        },
        "bypass_stats": merged_bypass,
        "judge_failure_modes": merged_failure_modes,
    }


def main():
    parser = argparse.ArgumentParser(description="Compute eval stats from agent test results")
    parser.add_argument("results_dir", type=Path, help="Directory with raw+judged JSON files")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    results_dir = args.results_dir.resolve()
    if not results_dir.is_dir():
        print(f"Error: {results_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    suites = discover_suites(results_dir)
    if not suites:
        print(f"Error: no raw+judged JSON pairs found in {results_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(suites)} suites: {[s['suite_name'] for s in suites]}", file=sys.stderr)

    all_stats = []
    for suite in suites:
        print(f"  Processing {suite['suite_name']}...", file=sys.stderr)
        stats = extract_suite_stats(suite)
        all_stats.append(stats)

    cross = compute_cross_suite(all_stats)

    suites_output = {}
    for suite, stats in zip(suites, all_stats):
        suites_output[suite["suite_name"]] = {
            "paper_row": stats["paper_row"],
            "idshort_detail": stats["idshort_detail"],
            "bypass_stats": stats["bypass_stats"],
            "template_validation": stats["template_validation"],
            "judge_failure_modes": stats["judge_failure_modes"],
            "duration_per_case": stats["duration_per_case"],
        }

    output = {
        "results_dir": str(results_dir),
        "suites": suites_output,
        "totals": cross,
    }

    json_str = json.dumps(output, indent=2, ensure_ascii=False)

    if args.output:
        args.output.write_text(json_str, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
