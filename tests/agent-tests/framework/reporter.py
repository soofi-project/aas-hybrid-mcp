"""Console table + JSON export for evaluation runs."""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

from framework.cases import Case
from framework.evaluator import Evaluation
from framework.runner import TResult


@dataclass
class RunRecord:
    case: Case
    result: TResult
    evaluation: Evaluation
    repetition: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "case": self.case.name,
            "query": self.case.query,
            "repetition": self.repetition,
            "result": self.result.to_dict(),
            "evaluation": self.evaluation.to_dict(),
        }


def print_table(records: list[RunRecord], *, llm_judge_used: bool) -> None:
    console = Console()
    table = Table(title="Agent Test Results", show_lines=False)
    table.add_column("Case", style="cyan", overflow="fold")
    table.add_column("Variant", style="magenta")
    table.add_column("Run", justify="right")
    table.add_column("Dur (s)", justify="right")
    table.add_column("Tools", justify="right")
    table.add_column("Regex", justify="right")
    if llm_judge_used:
        table.add_column("LLM", justify="right")
    table.add_column("Score", justify="right")
    table.add_column("Pass", justify="center")

    for r in records:
        ev = r.evaluation
        if ev.passed:
            passed = "[green]ok[/green]"
        elif ev.cypher_violations:
            passed = "[red]fail[/red] [yellow]Cy![/yellow]"
        elif ev.forbidden_hits:
            passed = "[red]fail[/red] [yellow]Fb![/yellow]"
        else:
            passed = "[red]fail[/red]"
        row = [
            r.case.name,
            r.result.variant,
            str(r.repetition + 1),
            f"{r.result.duration_s:.1f}",
            str(len(r.result.tool_calls)),
            f"{ev.regex_score:.2f}",
        ]
        if llm_judge_used:
            row.append(f"{ev.llm_score:.2f}" if ev.llm_score is not None else "—")
        row.append(f"{ev.score:.2f}")
        row.append(passed)
        table.add_row(*row)
    console.print(table)

    violations = [
        (r.case.name, r.result.variant, v)
        for r in records
        for v in r.evaluation.cypher_violations
    ]
    if violations:
        viol_tbl = Table(
            title="Cypher Anti-Pattern Violations",
            show_lines=False,
            border_style="yellow",
        )
        viol_tbl.add_column("Case", style="cyan")
        viol_tbl.add_column("Variant", style="magenta")
        viol_tbl.add_column("Pattern")
        viol_tbl.add_column("Cypher excerpt", overflow="fold")
        for case_name, variant, v in violations:
            viol_tbl.add_row(case_name, variant, v.pattern, v.cypher_excerpt)
        console.print(viol_tbl)

    summary = _aggregate(records)
    summary_tbl = Table(title="Per-Variant Summary", show_lines=False)
    summary_tbl.add_column("Variant", style="magenta")
    summary_tbl.add_column("Runs", justify="right")
    summary_tbl.add_column("Pass %", justify="right")
    summary_tbl.add_column("Avg score", justify="right")
    summary_tbl.add_column("Avg dur (s)", justify="right")
    for variant, stats in summary.items():
        summary_tbl.add_row(
            variant,
            str(stats["runs"]),
            f"{stats['pass_pct']:.0f}%",
            f"{stats['avg_score']:.2f}",
            f"{stats['avg_dur']:.1f}",
        )
    console.print(summary_tbl)


def _aggregate(records: list[RunRecord]) -> dict[str, dict[str, float]]:
    by_variant: dict[str, list[RunRecord]] = {}
    for r in records:
        by_variant.setdefault(r.result.variant, []).append(r)
    out: dict[str, dict[str, float]] = {}
    for variant, items in by_variant.items():
        passes = sum(1 for it in items if it.evaluation.passed)
        scores = [it.evaluation.score for it in items]
        durs = [it.result.duration_s for it in items]
        out[variant] = {
            "runs": len(items),
            "pass_pct": 100.0 * passes / max(1, len(items)),
            "avg_score": statistics.mean(scores) if scores else 0.0,
            "avg_dur": statistics.mean(durs) if durs else 0.0,
        }
    return out


def export_json(records: list[RunRecord], path: Path) -> None:
    payload = {
        "records": [r.to_dict() for r in records],
        "summary_by_variant": _aggregate(records),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
