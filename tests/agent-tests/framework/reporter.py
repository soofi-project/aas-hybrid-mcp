"""Console table + JSON export/import for evaluation runs."""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

from framework.cases import Case
from framework.evaluator import (
    CypherViolation,
    Evaluation,
    ToolViolation,
    ValidatorRejection,
    WritePathAnalysis,
)
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

    rejections = [
        (r.case.name, r.result.variant, v)
        for r in records
        for v in r.evaluation.validator_rejections
    ]
    if rejections:
        rej_tbl = Table(
            title="Validator Rejections (server-side forbidden_pattern)",
            show_lines=False,
            border_style="red",
        )
        rej_tbl.add_column("Case", style="cyan")
        rej_tbl.add_column("Variant", style="magenta")
        rej_tbl.add_column("Rules")
        rej_tbl.add_column("Self-corrected", justify="center")
        for case_name, variant, v in rejections:
            corrected = (
                "[green]yes[/green]" if v.self_corrected is True
                else "[red]no[/red]" if v.self_corrected is False
                else "—"
            )
            rej_tbl.add_row(case_name, variant, ", ".join(v.rules), corrected)
        console.print(rej_tbl)

    summary = _aggregate(records)
    summary_tbl = Table(title="Per-Variant Summary", show_lines=False)
    summary_tbl.add_column("Variant", style="magenta")
    summary_tbl.add_column("Runs", justify="right")
    summary_tbl.add_column("Pass %", justify="right")
    summary_tbl.add_column("Avg score", justify="right")
    summary_tbl.add_column("Avg dur (s)", justify="right")
    summary_tbl.add_column("Val.rej.", justify="right")
    summary_tbl.add_column("Self-corr.", justify="right")
    for variant, stats in summary.items():
        rej_count = stats["total_validator_rejections"]
        sc_pct = stats["self_corrected_pct"]
        summary_tbl.add_row(
            variant,
            str(stats["runs"]),
            f"{stats['pass_pct']:.0f}%",
            f"{stats['avg_score']:.2f}",
            f"{stats['avg_dur']:.1f}",
            str(int(rej_count)),
            f"{sc_pct:.0f}%" if rej_count > 0 else "—",
        )
    console.print(summary_tbl)

    bypass_records = [r for r in records if r.evaluation.write_path is not None]
    if bypass_records:
        bp_tbl = Table(title="Write-Path Bypass Analysis", show_lines=False)
        bp_tbl.add_column("Case", style="cyan", overflow="fold")
        bp_tbl.add_column("Variant", style="magenta")
        bp_tbl.add_column("Run", justify="right")
        bp_tbl.add_column("put_submodel", justify="center")
        bp_tbl.add_column("Error", overflow="fold")
        bp_tbl.add_column("Bypass type", justify="center")
        for r in bypass_records:
            wp = r.evaluation.write_path
            ps = "[green]yes[/green]" if wp.put_submodel_attempted else "[red]no[/red]"
            btype_colors = {
                "correct":  "[green]correct[/green]",
                "surfaced": "[yellow]surfaced[/yellow]",
                "cascade":  "[red]cascade[/red]",
                "direct":   "[red]direct[/red]",
            }
            btype = btype_colors.get(wp.bypass_type or "", wp.bypass_type or "—")
            err = (wp.put_submodel_error or "")[:80]
            bp_tbl.add_row(
                r.case.name, r.result.variant, str(r.repetition + 1),
                ps, err, btype,
            )
        console.print(bp_tbl)


def _aggregate(records: list[RunRecord]) -> dict[str, dict[str, float]]:
    by_variant: dict[str, list[RunRecord]] = {}
    for r in records:
        by_variant.setdefault(r.result.variant, []).append(r)
    out: dict[str, dict[str, float]] = {}
    for variant, items in by_variant.items():
        passes = sum(1 for it in items if it.evaluation.passed)
        scores = [it.evaluation.score for it in items]
        durs = [it.result.duration_s for it in items]
        all_rejections = [
            v for it in items for v in it.evaluation.validator_rejections
        ]
        self_corrected = [v for v in all_rejections if v.self_corrected is True]
        out[variant] = {
            "runs": len(items),
            "pass_pct": 100.0 * passes / max(1, len(items)),
            "avg_score": statistics.mean(scores) if scores else 0.0,
            "avg_dur": statistics.mean(durs) if durs else 0.0,
            "total_validator_rejections": len(all_rejections),
            "self_corrected_pct": (
                100.0 * len(self_corrected) / len(all_rejections)
                if all_rejections else 0.0
            ),
        }
    return out


def export_json(records: list[RunRecord], path: Path) -> None:
    payload = {
        "records": [r.to_dict() for r in records],
        "summary_by_variant": _aggregate(records),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _evaluation_from_dict(d: dict[str, Any]) -> Evaluation:
    cypher_violations = [
        CypherViolation(
            pattern=v["pattern"],
            tool_call_index=v["tool_call_index"],
            cypher_excerpt=v["cypher_excerpt"],
        )
        for v in d.get("cypher_violations", [])
    ]
    validator_rejections = [
        ValidatorRejection(
            tool_call_index=v["tool_call_index"],
            rules=v["rules"],
            self_corrected=v["self_corrected"],
        )
        for v in d.get("validator_rejections", [])
    ]
    wp_d = d.get("write_path")
    write_path: WritePathAnalysis | None = None
    if wp_d is not None:
        write_path = WritePathAnalysis(
            put_submodel_attempted=wp_d.get("put_submodel_attempted", False),
            put_submodel_error=wp_d.get("put_submodel_error"),
            put_submodel_element_called=wp_d.get("put_submodel_element_called", False),
            bypass_type=wp_d.get("bypass_type"),
        )
    tool_violations = [ToolViolation(reason=v["reason"]) for v in d.get("tool_violations", [])]
    return Evaluation(
        score=d.get("score", 0.0),
        passed=d.get("passed", False),
        regex_score=d.get("regex_score", 0.0),
        llm_score=d.get("llm_score"),
        keyword_hits=d.get("keyword_hits", []),
        keyword_misses=d.get("keyword_misses", []),
        forbidden_hits=d.get("forbidden_hits", []),
        pattern_matched=d.get("pattern_matched"),
        llm_reasoning=d.get("llm_reasoning"),
        cypher_violations=cypher_violations,
        tool_violations=tool_violations,
        validator_rejections=validator_rejections,
        write_path=write_path,
        notes=d.get("notes", []),
    )


def load_records(path: Path, cases: list[Case]) -> tuple[list[RunRecord], list[str]]:
    """Load RunRecords from a JSON file previously written by export_json.

    Returns (records, warnings). Cases missing from the YAML files are skipped
    and reported as warnings so the caller can surface them.
    """
    cases_by_name = {c.name: c for c in cases}
    data = json.loads(path.read_text(encoding="utf-8"))
    records: list[RunRecord] = []
    warnings: list[str] = []
    for d in data.get("records", []):
        case_name = d.get("case", "")
        case = cases_by_name.get(case_name)
        if case is None:
            warnings.append(f"case '{case_name}' not found in loaded YAML files — skipped")
            continue
        result = TResult.from_dict(d["result"])
        evaluation = _evaluation_from_dict(d["evaluation"])
        records.append(RunRecord(
            case=case,
            result=result,
            evaluation=evaluation,
            repetition=d.get("repetition", 0),
        ))
    return records, warnings
