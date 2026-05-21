"""CLI entry point for the agent test framework.

Runs the cases against the agent and writes raw results (with deterministic
regex / tool-call evaluation) to ``results/run_<ts>.json``. Authoritative
"is the answer correct?" judging is a separate step — run ``judge.py``
afterwards on the output of this script.
"""

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
from framework.evaluator import evaluate_regex
from framework.reporter import RunRecord, export_json, print_table
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
                evaluation = evaluate_regex(case, result)
                records.append(RunRecord(case=case, result=result, evaluation=evaluation, repetition=rep))
                if incremental_path:
                    export_json(records, incremental_path)
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AAS agent test framework")
    parser.add_argument("--cases", nargs="+", default=[str(HERE / "cases" / "*.yaml")])
    parser.add_argument("--variants", nargs="+", default=None)
    parser.add_argument("--repetitions", type=int, default=1)
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
        incremental_path=incremental_path,
    ))

    print_table(records)
    console.print(f"[green]wrote[/green] {incremental_path}")
    console.print(
        "[dim]Next: run judge.py on this file to compute answer_correct.[/dim]"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
