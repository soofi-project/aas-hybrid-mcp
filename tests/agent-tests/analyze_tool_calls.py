"""
analyze_tool_calls.py - Tool-call analysis for agent eval results.

Focus: Paper-ready cross-model comparison of prerequisite compliance,
anti-pattern violations, and self-correction rates.

Usage:
    python analyze_tool_calls.py results/qwen35-9b/t07/
    python analyze_tool_calls.py results/qwen35-9b/t07/qwen35-9b_bench_b_N10_T07.json
    python analyze_tool_calls.py --compare results/qwen35-2b/t07/ results/qwen35-27b/t07/
    python analyze_tool_calls.py results/run_2026-05-26T10-17-25Z.json
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PREREQ_TOOLS = {"get_graph_schema", "get_manual_page", "get_templates_index"}
QUERY_TOOLS = {"query_aas_graph", "search_aas_documents"}


def _extract_model_from_path(p: Path) -> str:
    parts = p.parts
    for i, part in enumerate(parts):
        if part == "results" and i + 1 < len(parts):
            candidate = parts[i + 1]
            if candidate.startswith("run_"):
                return p.stem
            return candidate
    return p.stem


def _extract_suite_from_filename(p: Path) -> str:
    stem = p.stem
    if stem.startswith("run_"):
        return "mixed"
    m = re.match(r".+?_(\w+?)_N\d+", stem)
    if m:
        return m.group(1)
    return stem


def _parse_file(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"  SKIP {path}: {e}", file=sys.stderr)
        return []

    model = _extract_model_from_path(path)
    suite = _extract_suite_from_filename(path)
    records = data.get("records", [])
    out: list[dict] = []

    for rec in records:
        res = rec.get("result", rec)
        variant = res.get("variant", "react")
        if variant != "react":
            continue

        tool_calls = res.get("tool_calls", [])
        tc_count = res.get("tool_call_count", len(tool_calls))
        ev = rec.get("evaluation", {})
        if not ev and "evaluation" in res:
            ev = res["evaluation"]

        cypher_violations = ev.get("cypher_violations", [])
        validator_rejections = ev.get("validator_rejections", [])

        out.append({
            "source": str(path),
            "model": model,
            "suite": suite,
            "case": rec.get("case", ""),
            "repetition": rec.get("repetition", 0),
            "variant": variant,
            "tool_calls": tool_calls,
            "tool_call_count": tc_count,
            "cypher_violations": cypher_violations,
            "validator_rejections": validator_rejections,
            "score": ev.get("score", 0.0),
            "passed": ev.get("passed", False),
            "duration_s": res.get("duration_s", 0.0),
        })

    return out


def _discover_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        p = p.resolve()
        if p.is_file() and p.suffix == ".json":
            files.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*.json")):
                if f.name == "stats.json" or f.name.endswith("_judged.json"):
                    continue
                files.append(f)
    return files


def load_all(paths: list[Path]) -> list[dict]:
    files = _discover_files(paths)
    if not files:
        print("No JSON files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {len(files)} file(s)...", file=sys.stderr)
    all_records: list[dict] = []
    for f in files:
        recs = _parse_file(f)
        if recs:
            print(f"  {f.name}: {len(recs)} react records", file=sys.stderr)
        all_records.extend(recs)

    if not all_records:
        print("No ReAct records found.", file=sys.stderr)
        sys.exit(1)

    print(f"Total: {len(all_records)} records", file=sys.stderr)
    return all_records


# ---------------------------------------------------------------------------
# Per-record analysis
# ---------------------------------------------------------------------------

def _first_query_index(tool_calls: list[dict]) -> int | None:
    for i, tc in enumerate(tool_calls):
        if tc.get("name") in QUERY_TOOLS:
            return i
    return None


def _first_violation_index(validator_rejections: list[dict],
                           cypher_violations: list[dict]) -> int | None:
    indices: list[int] = []
    for vr in validator_rejections:
        idx = vr.get("tool_call_index")
        if idx is not None:
            indices.append(idx)
    for cv in cypher_violations:
        idx = cv.get("tool_call_index")
        if idx is not None:
            indices.append(idx)
    return min(indices) if indices else None


def analyze_record(rec: dict) -> dict:
    tcs = rec["tool_calls"]
    vrs = rec["validator_rejections"]
    cvs = rec["cypher_violations"]
    has_violations = bool(vrs) or bool(cvs)

    # --- Prerequisite timeline (before first query) ---
    first_q = _first_query_index(tcs)
    prereq_names_before: set[str] = set()
    if first_q is not None and first_q > 0:
        for tc in tcs[:first_q]:
            prereq_names_before.add(tc.get("name", ""))

    schema_before = "get_graph_schema" in prereq_names_before
    manual_before = "get_manual_page" in prereq_names_before
    templates_before = "get_templates_index" in prereq_names_before
    all_three_before = schema_before and manual_before and templates_before
    no_prereq_before = first_q is not None and first_q == 0

    # --- Manual-before-violation ---
    first_v = _first_violation_index(vrs, cvs)
    manual_before_violation: bool | None = None
    manual_after_violation: bool = False
    manual_ever = any(tc.get("name") == "get_manual_page" for tc in tcs)

    if has_violations and first_v is not None:
        tools_before_v = [tc.get("name", "") for tc in tcs[:first_v]]
        manual_before_violation = "get_manual_page" in tools_before_v
        tools_after_v = [tc.get("name", "") for tc in tcs[first_v + 1:]]
        manual_after_violation = "get_manual_page" in tools_after_v

    # --- Failure mode ---
    if rec["tool_call_count"] == 0:
        failure_mode = "no_tools"
    elif has_violations and not rec["passed"]:
        failure_mode = "violation_fail"
    elif has_violations and rec["passed"]:
        failure_mode = "violation_pass"
    elif not rec["passed"]:
        failure_mode = "tools_wrong"
    else:
        failure_mode = "pass"

    # --- Self-correction ---
    self_corrected = None
    if vrs:
        self_corrected = all(vr.get("self_corrected", False) for vr in vrs)
    elif cvs:
        self_corrected = rec["passed"]

    # --- Tool frequency ---
    tool_freq: dict[str, int] = Counter(tc.get("name", "") for tc in tcs)

    # --- Violation rule breakdown (prefer clean names from validator_rejections) ---
    violation_rules: list[str] = []
    violation_indices_seen: set[int] = set()
    for vr in vrs:
        violation_rules.extend(vr.get("rules", []))
        violation_indices_seen.add(vr.get("tool_call_index", -1))
    for cv in cvs:
        idx = cv.get("tool_call_index", -1)
        if idx not in violation_indices_seen:
            violation_rules.append(cv.get("pattern", ""))

    return {
        "model": rec["model"],
        "suite": rec["suite"],
        "case": rec["case"],
        "passed": rec["passed"],
        "score": rec["score"],
        "duration_s": rec["duration_s"],
        "tool_call_count": rec["tool_call_count"],
        "failure_mode": failure_mode,
        "has_violations": has_violations,
        "self_corrected": self_corrected,
        "schema_before_query": schema_before,
        "manual_before_query": manual_before,
        "templates_before_query": templates_before,
        "all_three_before_query": all_three_before,
        "no_prereq_before_query": no_prereq_before,
        "manual_ever": manual_ever,
        "manual_before_violation": manual_before_violation,
        "manual_after_violation": manual_after_violation,
        "first_query_index": first_q,
        "first_tool_name": tcs[0].get("name", "") if tcs else "",
        "tool_freq": tool_freq,
        "violation_rules": violation_rules,
    }


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def _pct(n: int, total: int) -> str:
    if total == 0:
        return "-"
    return f"{100 * n / total:.0f}%"


def _pct_f(n: float, total: int) -> str:
    if total == 0:
        return "-"
    return f"{100 * n / total:.0f}%"


def aggregate(records: list[dict], group_key: str = "model") -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        groups[r[group_key]].append(r)

    rows: list[dict] = []
    for key in sorted(groups.keys()):
        grp = groups[key]
        n = len(grp)

        n_pass = sum(1 for r in grp if r["passed"])
        n_violation = sum(1 for r in grp if r["has_violations"])
        n_no_tools = sum(1 for r in grp if r["failure_mode"] == "no_tools")
        n_tools_wrong = sum(1 for r in grp if r["failure_mode"] == "tools_wrong")
        n_violation_pass = sum(1 for r in grp if r["failure_mode"] == "violation_pass")
        n_violation_fail = sum(1 for r in grp if r["failure_mode"] == "violation_fail")

        sc_total = sum(1 for r in grp if r["self_corrected"] is not None)
        sc_yes = sum(1 for r in grp if r["self_corrected"] is True)

        n_schema = sum(1 for r in grp if r["schema_before_query"])
        n_manual = sum(1 for r in grp if r["manual_before_query"])
        n_templates = sum(1 for r in grp if r["templates_before_query"])
        n_all_three = sum(1 for r in grp if r["all_three_before_query"])
        n_no_prereq = sum(1 for r in grp if r["no_prereq_before_query"])

        n_manual_ever = sum(1 for r in grp if r["manual_ever"])

        mv_with = sum(
            1 for r in grp
            if r["has_violations"] and r["manual_before_violation"] is True
        )
        mv_without = sum(
            1 for r in grp
            if r["has_violations"] and r["manual_before_violation"] is False
        )
        mv_never = sum(
            1 for r in grp
            if r["has_violations"] and r["manual_before_violation"] is None
            and not r["manual_ever"]
        )
        manual_read_still_violated = sum(
            1 for r in grp
            if r["manual_before_violation"] is True
        )
        manual_read_no_violation = sum(
            1 for r in grp
            if r["manual_ever"] and not r["has_violations"]
        )
        no_manual_violated = sum(
            1 for r in grp
            if not r["manual_ever"] and r["has_violations"]
        )

        avg_tc = sum(r["tool_call_count"] for r in grp) / n if n else 0

        all_rules: list[str] = []
        for r in grp:
            all_rules.extend(r["violation_rules"])
        rule_counts = Counter(all_rules)

        suites = sorted(set(r["suite"] for r in grp))

        rows.append({
            "key": key,
            "n": n,
            "suites": suites,
            "pass_count": n_pass,
            "pass_pct": _pct(n_pass, n),
            "violation_count": n_violation,
            "violation_pct": _pct(n_violation, n),
            "no_tools_count": n_no_tools,
            "no_tools_pct": _pct(n_no_tools, n),
            "tools_wrong_count": n_tools_wrong,
            "tools_wrong_pct": _pct(n_tools_wrong, n),
            "violation_pass_count": n_violation_pass,
            "violation_pass_pct": _pct(n_violation_pass, n),
            "violation_fail_count": n_violation_fail,
            "violation_fail_pct": _pct(n_violation_fail, n),
            "self_corrected_pct": _pct(sc_yes, sc_total) if sc_total else "-",
            "schema_before_pct": _pct(n_schema, n),
            "manual_before_pct": _pct(n_manual, n),
            "templates_before_pct": _pct(n_templates, n),
            "all_three_before_pct": _pct(n_all_three, n),
            "no_prereq_pct": _pct(n_no_prereq, n),
            "manual_ever_pct": _pct(n_manual_ever, n),
            "manual_before_violation": mv_with,
            "manual_after_violation": mv_without,
            "manual_read_still_violated": manual_read_still_violated,
            "manual_read_no_violation": manual_read_no_violation,
            "no_manual_violated": no_manual_violated,
            "avg_tool_calls": avg_tc,
            "violation_rules": rule_counts,
        })

    return rows


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def _fmt_pct(count: int, total: int) -> str:
    if total == 0:
        return "  - "
    return f"{100 * count / total:4.0f}%"


def print_summary(rows: list[dict]) -> None:
    for row in rows:
        n = row["n"]
        suites = ", ".join(row["suites"])
        print(f"\n{'=' * 80}")
        print(f"Model: {row['key']}  |  N={n}  |  Suites: {suites}")
        print(f"{'=' * 80}")

        print(f"\n  Overall")
        print(f"    Pass rate:           {_fmt_pct(row['pass_count'], n)}  ({row['pass_count']}/{n})")
        print(f"    Anti-pattern hit:    {_fmt_pct(row['violation_count'], n)}  ({row['violation_count']}/{n})")
        print(f"    Self-corrected:      {row['self_corrected_pct']}")

        print(f"\n  Failure modes")
        print(f"    Pass:                {_fmt_pct(row['pass_count'], n)}  ({row['pass_count']}/{n})")
        print(f"    Violation + pass:    {_fmt_pct(row['violation_pass_count'], n)}  ({row['violation_pass_count']}/{n})")
        print(f"    Violation + fail:    {_fmt_pct(row['violation_fail_count'], n)}  ({row['violation_fail_count']}/{n})")
        print(f"    Tools, no violation: {_fmt_pct(row['tools_wrong_count'], n)}  ({row['tools_wrong_count']}/{n})")
        print(f"    No tools at all:     {_fmt_pct(row['no_tools_count'], n)}  ({row['no_tools_count']}/{n})")

        print(f"\n  Prerequisites (before first query)")
        print(f"    Schema:              {_fmt_pct_raw(row['schema_before_pct'])}")
        print(f"    Manual page:         {_fmt_pct_raw(row['manual_before_pct'])}")
        print(f"    Templates index:     {_fmt_pct_raw(row['templates_before_pct'])}")
        print(f"    All three:           {_fmt_pct_raw(row['all_three_before_pct'])}")
        print(f"    None (query first):  {_fmt_pct_raw(row['no_prereq_pct'])}")
        print(f"    Manual ever called:  {_fmt_pct_raw(row['manual_ever_pct'])}")

        nv = row["violation_count"]
        if nv > 0:
            print(f"\n  Manual vs. Violation ({nv} records with violations)")
            mbv = row["manual_before_violation"]
            print(f"    Manual read, still violated: {mbv}/{nv}  ({_pct(mbv, nv)})")
            print(f"    No manual read, violated:    {row['no_manual_violated']}/{nv}  ({_pct(row['no_manual_violated'], nv)})")

        if row["violation_rules"]:
            print(f"\n  Violation rule breakdown")
            for rule, count in row["violation_rules"].most_common():
                print(f"    {rule}: {count}")

        print(f"\n  Avg tool calls: {row['avg_tool_calls']:.1f}")


def _fmt_pct_raw(s: str) -> str:
    return f"{s:>5}"


def print_compare(rows: list[dict]) -> str:
    lines: list[str] = []

    lines.append("| Model | N | Pass% | AP-hit% | Self-corr% | Schema-1st | Manual-1st | All-3-1st | Manual>AP | NoMan>AP | Avg TC |")
    lines.append("|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|")

    for row in rows:
        nv = row["violation_count"]
        manual_ap = row["manual_read_still_violated"]
        no_manual_ap = row["no_manual_violated"]

        lines.append(
            f"| {row['key']} "
            f"| {row['n']} "
            f"| {row['pass_pct']} "
            f"| {row['violation_pct']} "
            f"| {row['self_corrected_pct']} "
            f"| {row['schema_before_pct']} "
            f"| {row['manual_before_pct']} "
            f"| {row['all_three_before_pct']} "
            f"| {_pct(manual_ap, nv) if nv else '-'} "
            f"| {_pct(no_manual_ap, nv) if nv else '-'} "
            f"| {row['avg_tool_calls']:.1f} |"
        )

    md = "\n".join(lines)
    print(md)
    return md


def print_detailed_manual(rows: list[dict]) -> str:
    lines: list[str] = []

    lines.append("")
    lines.append("## Manual vs. Anti-Pattern Compliance")
    lines.append("")
    lines.append("Manual>AP = read manual *before* first violation, still violated.")
    lines.append("NoMan>AP = never read manual, committed violation.")
    lines.append("Manual>OK = read manual at some point, no violations.")
    lines.append("")
    lines.append("| Model | N | Manual>AP | NoMan>AP | Manual>OK |")
    lines.append("|---|--:|--:|--:|--:|")

    for row in rows:
        n = row["n"]
        lines.append(
            f"| {row['key']} "
            f"| {n} "
            f"| {row['manual_read_still_violated']} "
            f"| {row['no_manual_violated']} "
            f"| {row['manual_read_no_violation']} |"
        )

    md = "\n".join(lines)
    print(md)
    return md


def print_failure_modes(rows: list[dict]) -> str:
    lines: list[str] = []

    lines.append("")
    lines.append("## Failure Mode Breakdown")
    lines.append("")
    lines.append("| Model | Pass | Viol+Pass | Viol+Fail | Clean Fail | No Tools |")
    lines.append("|---|--:|--:|--:|--:|--:|")

    for row in rows:
        n = row["n"]
        lines.append(
            f"| {row['key']} "
            f"| {row['pass_pct']} "
            f"| {row['violation_pass_pct']} "
            f"| {row['violation_fail_pct']} "
            f"| {row['tools_wrong_pct']} "
            f"| {row['no_tools_pct']} |"
        )

    md = "\n".join(lines)
    print(md)
    return md


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tool-call analysis for agent eval results"
    )
    parser.add_argument(
        "paths", nargs="+", type=Path,
        help="JSON files or directories to analyze",
    )
    parser.add_argument(
        "--compare", action="store_true",
        help="Cross-model comparison as Markdown table",
    )
    parser.add_argument(
        "--group-by", default="model", choices=["model", "suite", "case"],
        help="Grouping key for aggregation (default: model)",
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=None,
        help="Write Markdown output to file",
    )
    args = parser.parse_args()

    records = load_all(args.paths)

    analyzed = [analyze_record(r) for r in records]

    rows = aggregate(analyzed, group_key=args.group_by)

    if args.compare:
        md_parts: list[str] = []
        md_parts.append(f"# Tool-Call Analysis — Cross-Model Comparison")
        md_parts.append("")
        md_parts.append(f"Records: {len(analyzed)} | Grouped by: {args.group_by}")
        md_parts.append("")

        md_parts.append("## Summary")
        md_parts.append("")
        md_parts.append(print_compare(rows))
        md_parts.append(print_failure_modes(rows))
        md_parts.append(print_detailed_manual(rows))

        md = "\n".join(md_parts)

        if args.output:
            args.output.write_text(md + "\n", encoding="utf-8")
            print(f"\nWritten to {args.output}", file=sys.stderr)
    else:
        print_summary(rows)
        if args.output:
            lines: list[str] = []
            lines.append(f"# Tool-Call Analysis")
            lines.append("")
            for row in rows:
                lines.append(f"## {row['key']}")
                lines.append("")
                lines.append(f"- N: {row['n']}")
                lines.append(f"- Pass: {row['pass_pct']}")
                lines.append(f"- AP-hit: {row['violation_pct']}")
                lines.append(f"- Self-corr: {row['self_corrected_pct']}")
                lines.append(f"- Schema-1st: {row['schema_before_pct']}")
                lines.append(f"- Manual-1st: {row['manual_before_pct']}")
                lines.append(f"- All-3-1st: {row['all_three_before_pct']}")
                lines.append(f"- Avg tools: {row['avg_tool_calls']:.1f}")
                lines.append("")
            args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"\nWritten to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
