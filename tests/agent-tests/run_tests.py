"""CLI entry point for the agent test framework."""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import sys
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console

from framework.cases import Case, load_cases, resolve_variants
from framework.evaluator import LLMJudge, evaluate
from framework.reporter import RunRecord, export_json, load_records, print_table
from framework.runner import AgentTester


HERE = Path(__file__).parent


def _load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


async def _run_all(
    cases: list[Case],
    *,
    default_variants: list[str],
    variants_filter: list[str] | None,
    repetitions: int,
    tester: AgentTester,
    judge: LLMJudge | None,
    incremental_path: Path | None = None,
) -> list[RunRecord]:
    console = Console()
    records: list[RunRecord] = []
    for case in cases:
        variants = resolve_variants(case, default_variants)
        if variants_filter:
            variants = [v for v in variants if v in variants_filter]
        if not variants:
            console.print(f"[yellow]skip[/yellow] {case.name}: no matching variants")
            continue
        for variant in variants:
            for rep in range(repetitions):
                console.print(
                    f"-> [cyan]{case.name}[/cyan] | [magenta]{variant}[/magenta] | run {rep + 1}/{repetitions}"
                )
                result = await tester.run_query(case.query, variant)
                evaluation = await evaluate(case, result, judge=judge)
                records.append(RunRecord(case=case, result=result, evaluation=evaluation, repetition=rep))
                if incremental_path:
                    export_json(records, incremental_path)
    return records


async def _judge_existing(
    records: list[RunRecord],
    judge: LLMJudge,
) -> list[RunRecord]:
    """Re-run LLM judge on pre-loaded records; update evaluation in-place."""
    console = Console()
    for i, record in enumerate(records):
        console.print(
            f"-> judging [{i + 1}/{len(records)}] "
            f"[cyan]{record.case.name}[/cyan] | [magenta]{record.result.variant}[/magenta]"
        )
        if not record.case.llm_criteria:
            console.print(f"   [yellow]skip[/yellow] — no llm_criteria defined for this case")
            continue
        llm_score, reasoning = await judge.grade(record.case, record.result)
        ev = record.evaluation
        ev.llm_score = llm_score
        ev.llm_reasoning = reasoning
        if ev.forbidden_hits or ev.cypher_violations or ev.tool_violations:
            ev.score = 0.0
            ev.passed = False
        else:
            ev.score = 0.4 * ev.regex_score + 0.6 * llm_score
            ev.passed = ev.score >= 0.7
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AAS agent test framework")
    parser.add_argument("--cases", nargs="+", default=[str(HERE / "cases" / "*.yaml")])
    parser.add_argument("--variants", nargs="+", default=None)
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--llm-judge", action="store_true")
    parser.add_argument("--judge-only", type=Path, default=None, metavar="RESULTS_JSON",
                        help="Skip agent runs; re-run LLM judge on an existing results JSON. "
                             "Safe two-phase workflow: run without --llm-judge first, "
                             "then judge with --judge-only + --llm-judge.")
    parser.add_argument("--export", type=Path, default=None)
    parser.add_argument("--agent-url", default=None)
    parser.add_argument("--config", type=Path, default=HERE / "config.yaml")
    parser.add_argument("--strict-validation", action="store_true",
                        help="Reject ambiguous queries instead of warning")
    parser.add_argument("--include-tags", nargs="+", default=None,
                        help="Only run cases with at least one of these tags")
    parser.add_argument("--exclude-tags", nargs="+", default=None,
                        help="Skip cases with any of these tags (default: requires_fixture)")
    args = parser.parse_args(argv)

    console = Console()

    if args.judge_only and not args.llm_judge:
        console.print("[red]--judge-only requires --llm-judge[/red]")
        return 2

    cfg = _load_config(args.config)
    agent_url = args.agent_url or cfg.get("agent_url", "http://localhost:8120")
    default_variants = cfg.get("default_variants", [
        "aas-agent:react", "aas-agent:plan", "aas-agent:crag", "aas-agent:reflexion",
    ])
    timeout = float(cfg.get("request_timeout_s", 300))

    include_tags = set(args.include_tags) if args.include_tags else None
    exclude_tags = set(args.exclude_tags) if args.exclude_tags is not None else None
    cases, warnings = load_cases(
        args.cases,
        strict=args.strict_validation,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
    )
    for w in warnings:
        console.print(f"[yellow]warn[/yellow] {w}")
    if not cases:
        console.print("[red]no cases loaded[/red]")
        return 1

    judge: LLMJudge | None = None
    if args.llm_judge:
        judge_cfg = cfg.get("llm_judge") or {}
        try:
            judge = LLMJudge.from_config(judge_cfg)
        except ValueError as e:
            console.print(f"[red]LLM judge disabled — {e}[/red]")
            return 2
        console.print(f"[green]LLM judge enabled[/green] · model={judge._model} · base={judge._base}")

    # --- judge-only mode: load existing results, skip agent calls ---
    if args.judge_only:
        if not args.judge_only.exists():
            console.print(f"[red]file not found: {args.judge_only}[/red]")
            return 2
        console.print(f"[dim]loading records from {args.judge_only}[/dim]")
        records, load_warnings = load_records(args.judge_only, cases)
        for w in load_warnings:
            console.print(f"[yellow]warn[/yellow] {w}")
        if not records:
            console.print("[red]no records loaded — aborting[/red]")
            return 1
        console.print(f"[dim]{len(records)} records loaded[/dim]")
        assert judge is not None  # guaranteed by the check above
        records = asyncio.run(_judge_existing(records, judge))
        print_table(records, llm_judge_used=True)
        if args.export:
            out = args.export
        else:
            src_stem = args.judge_only.stem  # e.g. "run_2026-05-19T10-00-00Z"
            out = args.judge_only.parent / f"judged_{src_stem}.json"
        export_json(records, out)
        console.print(f"[green]wrote[/green] {out}")
        failed = sum(1 for r in records if not r.evaluation.passed)
        return 0 if failed == 0 else 1

    # --- normal mode: run agent, save incrementally, optionally judge inline ---
    tester = AgentTester(agent_url=agent_url, timeout_s=timeout)
    console.print(f"[dim]agent URL: {agent_url}[/dim]")

    ts = dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
    incremental_path: Path = args.export or (HERE / "results" / f"run_{ts}.json")

    records = asyncio.run(_run_all(
        cases,
        default_variants=default_variants,
        variants_filter=args.variants,
        repetitions=args.repetitions,
        tester=tester,
        judge=judge,
        incremental_path=incremental_path,
    ))

    print_table(records, llm_judge_used=judge is not None)
    # incremental_path already written after each record in _run_all()
    console.print(f"[green]wrote[/green] {incremental_path}")

    failed = sum(1 for r in records if not r.evaluation.passed)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
