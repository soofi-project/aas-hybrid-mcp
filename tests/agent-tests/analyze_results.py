"""Analyse judged result files and write a Markdown report.

Usage:
    python analyze_results.py qwen36-27b
    python analyze_results.py qwen35-2b

The argument is a model prefix.  The script globs
``results/{prefix}_*_judged.json``, analyses all records, and writes
``results/analysis_{prefix}.md``.
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _had_antipattern(record: dict) -> bool:
    return any(
        e.get("kind") == "validator_rejection"
        for e in record.get("process", {}).get("tool_errors", [])
    )


def load_records(prefix: str, results_dir: Path) -> tuple[list[dict], list[str]]:
    """Return (flat list of annotated records, list of short file labels)."""
    files = sorted(results_dir.glob(f"{prefix}_*_judged.json"))
    if not files:
        print(f"No files matching '{prefix}_*_judged.json' in {results_dir}", file=sys.stderr)
        sys.exit(1)

    all_records: list[dict] = []
    labels: list[str] = []

    for path in files:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        raw = data.get("records", [])
        # strip prefix and suffix to get a short label
        label = path.stem.removeprefix(f"{prefix}_").removesuffix("_judged")
        labels.append(label)
        for r in raw:
            all_records.append({
                "file_label": label,
                "case": r.get("case", ""),
                "variant": r.get("variant", ""),
                "correct": r.get("judge", {}).get("answer_correct", False),
                "read_manuals_first": r.get("process", {}).get("read_manuals_first", False),
                "had_antipattern": _had_antipattern(r),
                "had_any_error": r.get("process", {}).get("tool_error_count", 0) > 0,
                "all_good": r.get("all_good", False),
                "duration_s": r.get("duration_s", 0.0),
            })

    return all_records, labels


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------

def _pct(n: int, total: int) -> str:
    if total == 0:
        return "–"
    return f"{100 * n / total:.0f}%"


def _cell(n: int, total: int) -> str:
    return f"{n} ({_pct(n, total)})"


def per_file_stats(records: list[dict], labels: list[str]) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        buckets[r["file_label"]].append(r)

    rows = []
    for label in labels:
        grp = buckets[label]
        n = len(grp)
        correct = sum(r["correct"] for r in grp)
        manuals = sum(r["read_manuals_first"] for r in grp)
        antipattern = sum(r["had_antipattern"] for r in grp)
        all_good = sum(r["all_good"] for r in grp)
        rows.append({
            "label": label,
            "n": n,
            "correct": correct,
            "incorrect": n - correct,
            "manuals_first": manuals,
            "antipattern_hit": antipattern,
            "all_good": all_good,
        })
    return rows


def duration_stats(records: list[dict], labels: list[str]) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        buckets[r["file_label"]].append(r)
    rows = []
    for label in labels:
        grp = buckets[label]
        all_d = [r["duration_s"] for r in grp]
        correct_d = [r["duration_s"] for r in grp if r["correct"]]
        wrong_d = [r["duration_s"] for r in grp if not r["correct"]]
        rows.append({
            "label": label,
            "n": len(grp),
            "median_all": statistics.median(all_d) if all_d else None,
            "median_correct": statistics.median(correct_d) if correct_d else None,
            "median_wrong": statistics.median(wrong_d) if wrong_d else None,
        })
    return rows


def crosstab(records: list[dict], row_key: str, col_key: str) -> dict:
    """Return counts for a 2×2 cross-tabulation."""
    counts: dict[tuple[bool, bool], int] = defaultdict(int)
    for r in records:
        counts[(r[row_key], r[col_key])] += 1
    return dict(counts)


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def _md_per_file(rows: list[dict]) -> str:
    lines = [
        "| Test suite | N | Correct | Incorrect | Manuals first | Antipattern hit | All good |",
        "|---|--:|--:|--:|--:|--:|--:|",
    ]
    for r in rows:
        n = r["n"]
        lines.append(
            f"| {r['label']} "
            f"| {n} "
            f"| {_cell(r['correct'], n)} "
            f"| {_cell(r['incorrect'], n)} "
            f"| {_cell(r['manuals_first'], n)} "
            f"| {_cell(r['antipattern_hit'], n)} "
            f"| {_cell(r['all_good'], n)} |"
        )
    # totals row
    n_total = sum(r["n"] for r in rows)
    c_total = sum(r["correct"] for r in rows)
    i_total = sum(r["incorrect"] for r in rows)
    m_total = sum(r["manuals_first"] for r in rows)
    a_total = sum(r["antipattern_hit"] for r in rows)
    g_total = sum(r["all_good"] for r in rows)
    lines.append(
        f"| **Total** "
        f"| **{n_total}** "
        f"| **{_cell(c_total, n_total)}** "
        f"| **{_cell(i_total, n_total)}** "
        f"| **{_cell(m_total, n_total)}** "
        f"| **{_cell(a_total, n_total)}** "
        f"| **{_cell(g_total, n_total)}** |"
    )
    return "\n".join(lines)


def _md_crosstab(
    records: list[dict],
    row_key: str,
    col_key: str,
    row_labels: tuple[str, str] = ("True", "False"),
    col_labels: tuple[str, str] = ("True", "False"),
) -> str:
    counts = crosstab(records, row_key, col_key)
    tt = counts.get((True, True), 0)
    tf = counts.get((True, False), 0)
    ft = counts.get((False, True), 0)
    ff = counts.get((False, False), 0)

    row_t = tt + tf
    row_f = ft + ff

    lines = [
        f"| | **{col_key}={col_labels[0]}** | **{col_key}={col_labels[1]}** | Total |",
        "|---|--:|--:|--:|",
        f"| **{row_key}={row_labels[0]}** | {_cell(tt, row_t)} | {_cell(tf, row_t)} | {row_t} |",
        f"| **{row_key}={row_labels[1]}** | {_cell(ft, row_f)} | {_cell(ff, row_f)} | {row_f} |",
    ]
    return "\n".join(lines)


def _fmt_s(v: float | None) -> str:
    return "–" if v is None else f"{v:.1f}s"


def _md_duration(dur_rows: list[dict]) -> str:
    lines = [
        "| Suite | N | Median (all) | Median (correct) | Median (wrong) |",
        "|---|--:|--:|--:|--:|",
    ]
    for r in dur_rows:
        lines.append(
            f"| {r['label']} | {r['n']} "
            f"| {_fmt_s(r['median_all'])} "
            f"| {_fmt_s(r['median_correct'])} "
            f"| {_fmt_s(r['median_wrong'])} |"
        )
    return "\n".join(lines)


def build_markdown(prefix: str, records: list[dict], per_file: list[dict]) -> str:
    n_files = len(per_file)
    n_total = len(records)
    today = date.today().isoformat()

    dur_rows = duration_stats(records, [r["label"] for r in per_file])

    sections = [
        f"# Results analysis: {prefix}",
        f"",
        f"Generated: {today} · {n_files} test suites · {n_total} runs",
        f"",
        f"## Per test suite",
        f"",
        _md_per_file(per_file),
        f"",
        f"## Correct × Manuals first",
        f"",
        f"Did reading the agent manuals before the first graph query correlate with a correct answer?",
        f"",
        _md_crosstab(records, "correct", "read_manuals_first"),
        f"",
        f"## Correct × Antipattern hit",
        f"",
        f"Did triggering a validator rejection (e.g. `idShort_contains` / `toLower_id_contains`) correlate with an incorrect answer?",
        f"",
        _md_crosstab(records, "correct", "had_antipattern"),
        f"",
        f"## Duration (median seconds per suite)",
        f"",
        f"Fairest cross-model comparison: **Median (all)** — same suite = same questions, "
        f"so question difficulty is controlled. Correct-only median is confounded: smaller models "
        f"only solve easier (faster) questions while larger models also solve harder (slower) ones. "
        f"Failed runs are disproportionately long because models exhaust the recursion limit "
        f"rather than giving up quickly.",
        f"",
        _md_duration(dur_rows),
    ]
    return "\n".join(sections) + "\n"


# ---------------------------------------------------------------------------
# Rich terminal output
# ---------------------------------------------------------------------------

def print_rich(prefix: str, records: list[dict], per_file: list[dict]) -> None:
    try:
        from rich.console import Console
        from rich.table import Table
    except ImportError:
        return

    console = Console()

    t1 = Table(title=f"Per test suite — {prefix}", show_lines=False)
    for col in ("Test suite", "N", "Correct", "Incorrect", "Manuals first", "Antipattern hit", "All good"):
        t1.add_column(col, justify="right" if col != "Test suite" else "left")
    for r in per_file:
        n = r["n"]
        t1.add_row(
            r["label"],
            str(n),
            _cell(r["correct"], n),
            _cell(r["incorrect"], n),
            _cell(r["manuals_first"], n),
            _cell(r["antipattern_hit"], n),
            _cell(r["all_good"], n),
        )
    console.print(t1)

    n_total = len(records)
    c_total = sum(r["correct"] for r in records)
    m_total = sum(r["read_manuals_first"] for r in records)
    a_total = sum(r["had_antipattern"] for r in records)
    g_total = sum(r["all_good"] for r in records)
    console.print(
        f"\nTotal: N={n_total}  correct={_cell(c_total, n_total)}  "
        f"manuals_first={_cell(m_total, n_total)}  "
        f"antipattern={_cell(a_total, n_total)}  "
        f"all_good={_cell(g_total, n_total)}"
    )

    def _ct_table(title: str, row_key: str, col_key: str) -> None:
        counts = crosstab(records, row_key, col_key)
        tt = counts.get((True, True), 0)
        tf = counts.get((True, False), 0)
        ft = counts.get((False, True), 0)
        ff = counts.get((False, False), 0)
        t = Table(title=title, show_lines=True)
        t.add_column("", style="bold")
        t.add_column(f"{col_key}=True", justify="right")
        t.add_column(f"{col_key}=False", justify="right")
        row_t = tt + tf
        row_f = ft + ff
        t.add_row(f"{row_key}=True",  _cell(tt, row_t), _cell(tf, row_t))
        t.add_row(f"{row_key}=False", _cell(ft, row_f), _cell(ff, row_f))
        console.print(t)

    _ct_table("Correct × Manuals first", "correct", "read_manuals_first")
    _ct_table("Correct × Antipattern hit", "correct", "had_antipattern")

    dur_rows = duration_stats(records, [r["label"] for r in per_file])
    t_dur = Table(title="Duration (median seconds per suite)", show_lines=False)
    t_dur.add_column("Suite", justify="left")
    t_dur.add_column("N", justify="right")
    t_dur.add_column("Median (all)", justify="right")
    t_dur.add_column("Median (correct)", justify="right")
    t_dur.add_column("Median (wrong)", justify="right")
    for r in dur_rows:
        t_dur.add_row(
            r["label"], str(r["n"]),
            _fmt_s(r["median_all"]),
            _fmt_s(r["median_correct"]),
            _fmt_s(r["median_wrong"]),
        )
    console.print(t_dur)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    prefix = sys.argv[1] if len(sys.argv) > 1 else "qwen36-27b"

    script_dir = Path(__file__).parent
    results_dir = script_dir / "results"

    records, labels = load_records(prefix, results_dir)
    per_file = per_file_stats(records, labels)

    print_rich(prefix, records, per_file)

    md = build_markdown(prefix, records, per_file)
    out_path = results_dir / f"analysis_{prefix}.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"\nReport written to {out_path}")


if __name__ == "__main__":
    main()
