"""Strict bool judge for agent test results.

Three orthogonal signals per run:

* ``answer_correct`` (bool, LLM-judged) — does the final answer match the
  structured ``ground_truth`` block from the case YAML?
* ``read_manuals_first`` (bool, programmatic) — did the agent call one of
  the manual / schema tools BEFORE its first real query/write tool?
* ``tool_errors`` (list, programmatic) — every tool call whose result is a
  JSON object with a top-level ``"error"`` key (validator rejection, neo4j
  syntax error, BaSyx HTTP error, etc.).

``all_good`` is the conjunction of all three.

Inputs:
  --input  results/<slug>_N10.json   (raw output from run_tests.py)
  --cases  cases/bench_b.yaml

Output:
  results/<slug>_N10_judged.json with one record per input record plus a
  per-(variant, case) and per-variant summary.

Environment:
  Pass --base-url + --model + (--api-key-env) for the judge endpoint, or
  rely on LLM_BASE_URL / LLM_MODEL / OPENAI_API_KEY env vars.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import yaml

# Tools that count as "reading the manual / schema before querying".
# get_graph_schema and get_manual_page are explicit guidance hooks; the
# template introspection tools also count because they teach the agent which
# semanticIds exist before composing queries.
MANUAL_TOOLS = {
    "get_manual_page",
    "get_graph_schema",
    "get_templates_index",
    "get_template",
    "list_resources",
}

# Tools that count as a "real" query/write step (the thing the agent should
# only do AFTER consulting at least one manual tool).
QUERY_TOOLS = {
    "query_aas_graph",
    "search_aas_documents",
    "search_aas_templates",
    "put_submodel",
    "put_submodel_element",
    "delete_submodel",
    "delete_submodel_element",
    "put_concept_description",
    "delete_concept_description",
}


@dataclass
class GroundTruth:
    required_facts: list[str]
    must_not_claim: list[str]
    notes: str
    llm_criteria: str | None  # fallback context

    def render(self) -> str:
        parts = []
        if self.required_facts:
            parts.append("REQUIRED FACTS (every one must be supported by the answer):")
            for f in self.required_facts:
                parts.append(f"  - {f}")
        if self.must_not_claim:
            parts.append("")
            parts.append("MUST NOT CLAIM (the answer must not assert any of these):")
            for f in self.must_not_claim:
                parts.append(f"  - {f}")
        if self.notes:
            parts.append("")
            parts.append(f"NOTES: {self.notes.strip()}")
        if self.llm_criteria and not self.required_facts:
            parts.append("")
            parts.append(f"FALLBACK CRITERION: {self.llm_criteria.strip()}")
        return "\n".join(parts)


def load_ground_truth(cases_paths: list[str]) -> dict[str, GroundTruth]:
    """Read structured ground_truth blocks from one or more case YAML files."""
    out: dict[str, GroundTruth] = {}
    for path in cases_paths:
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        cases = raw["cases"] if isinstance(raw, dict) else raw
        for c in cases:
            name = c.get("name")
            if not name:
                continue
            gt = c.get("ground_truth") or {}
            out[name] = GroundTruth(
                required_facts=list(gt.get("required_facts") or []),
                must_not_claim=list(gt.get("must_not_claim") or []),
                notes=str(gt.get("notes") or "").strip(),
                llm_criteria=c.get("llm_criteria"),
            )
    return out


# ---------- programmatic checks --------------------------------------------


def _parse_first_json_object(s: str) -> dict[str, Any] | None:
    """Return the JSON object at the start of *s*, or None.

    Tool ``result_preview`` strings are truncated, so we only need a parse of
    the leading object enough to read its top-level keys.
    """
    if not s:
        return None
    s = s.lstrip()
    if not s.startswith("{"):
        return None
    # Try full parse; on failure, walk the brace depth and try to close it.
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    depth = 0
    in_str = False
    esc = False
    for i, ch in enumerate(s):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(s[: i + 1])
                except json.JSONDecodeError:
                    return None
    return None


# Pattern: a result_preview that starts with `{"error":` (allow whitespace
# variations). result_preview is usually truncated to ~200 chars, so we
# cannot reliably json.loads() the whole thing — we just need to recognise
# the leading shape.
_ERROR_PREFIX_RE = re.compile(r'^\s*\{\s*"error"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.DOTALL)
# Validator rejection has a fixed sub-shape we can pluck rule names from.
_VALIDATOR_RULE_RE = re.compile(r'"rule"\s*:\s*"([^"]+)"')


def classify_tool_error(tc: dict[str, Any]) -> dict[str, Any] | None:
    """Return a structured tool-error record, or None if the call succeeded.

    Robust against truncated result_preview strings: relies on regex over the
    leading characters rather than a full JSON parse.
    """
    preview = tc.get("result_preview") or ""
    # 1. Explicit "Tool error: ..." prefix used by the agent harness.
    if preview.startswith("Tool error") or preview.lower().startswith("error:"):
        return {
            "kind": "agent_harness",
            "snippet": preview[:200],
        }
    # 2. Leading shape `{"error": "<value>"...` — recognise without full parse.
    m = _ERROR_PREFIX_RE.match(preview)
    if not m:
        return None
    err_value = m.group(1)
    if err_value == "forbidden_pattern":
        rules = _VALIDATOR_RULE_RE.findall(preview)
        return {
            "kind": "validator_rejection",
            "rules": rules,
            "snippet": preview[:200],
        }
    if "Neo.ClientError" in err_value or "SyntaxError" in err_value:
        return {
            "kind": "cypher_syntax_error",
            "snippet": err_value[:200],
        }
    return {
        "kind": "tool_error",
        "snippet": err_value[:200] if err_value else preview[:200],
    }


def analyse_process(tool_calls: list[dict[str, Any]]) -> dict[str, Any]:
    """Programmatic process checks over the tool-call sequence."""
    first_manual_idx: int | None = None
    first_query_idx: int | None = None
    manuals_called: list[str] = []
    errors: list[dict[str, Any]] = []
    for i, tc in enumerate(tool_calls):
        name = tc.get("name", "")
        if name in MANUAL_TOOLS:
            if first_manual_idx is None:
                first_manual_idx = i
            manuals_called.append(name)
        if name in QUERY_TOOLS and first_query_idx is None:
            first_query_idx = i
        err = classify_tool_error(tc)
        if err is not None:
            errors.append({"index": i, "tool": name, **err})

    if first_query_idx is None and first_manual_idx is None:
        # No tool calls at all — cannot determine manual-first; treat as False.
        read_manuals_first = False
    elif first_query_idx is None:
        # Read manuals but never queried — trivially satisfied.
        read_manuals_first = True
    elif first_manual_idx is None:
        read_manuals_first = False
    else:
        read_manuals_first = first_manual_idx < first_query_idx

    return {
        "read_manuals_first": read_manuals_first,
        "first_manual_idx": first_manual_idx,
        "first_query_idx": first_query_idx,
        "manual_tools_called": manuals_called,
        "tool_error_count": len(errors),
        "tool_errors": errors,
    }


# ---------- LLM judge -------------------------------------------------------


JUDGE_PROMPT = """\
You are a strict pass/fail grader for an industrial-AI agent's answer.

DECISION RULE:
  Step 1. Identify the answer's CORE LIST — the items the agent positively
          puts forward as its answer to the user's question (typically a
          numbered/bulleted enumeration, table rows, or a short subject line
          like "X can carry 250 kg").
  Step 2. Check every REQUIRED FACT against that core list (and supporting
          prose). All required facts must be supported.
  Step 3. Check every MUST NOT CLAIM. A MUST NOT CLAIM is violated ONLY when
          the agent positively asserts it as part of the answer (e.g.,
          includes the forbidden entity in its enumerated answer list, or
          attributes the required property to it). Mentioning the forbidden
          entity ONLY as background/context/parent-container/exclusion
          ("Hall 3 contains the following 4 devices: ...", "MiR100 only
          carries 100 kg so it does not qualify") is NOT a violation.
  Step 4. answer_correct = (all required facts supported) AND
                           (no must-not-claim positively asserted).

INTERPRETATION HINTS:
- "X contains/has Y" is a claim about Y's location, NOT a claim that X
  itself is one of the answer items.
- Naming an entity to exclude or contrast it is fine and often desirable.
- Vague hand-waving without specifics does not "support" a required fact.
- An empty answer, a refusal, or a raw tool-error trace is always incorrect.

USER QUESTION:
{query}

GROUND TRUTH:
{ground_truth}

AGENT FINAL ANSWER:
{answer}

Respond with ONLY a single JSON object, no prose, no code fence:
{{"answer_correct": true|false, "reasoning": "<one short sentence naming the core list and the verdict>", "missing_facts": ["..."], "wrong_claims": ["..."]}}

Use empty lists for missing_facts / wrong_claims when correct.
"""


@dataclass
class JudgeConfig:
    base_url: str
    model: str
    api_key: str
    timeout_s: float = 90.0


async def judge_one(
    client: httpx.AsyncClient,
    cfg: JudgeConfig,
    query: str,
    gt: GroundTruth,
    final_answer: str,
) -> dict[str, Any]:
    prompt = JUDGE_PROMPT.format(
        query=query.strip(),
        ground_truth=gt.render(),
        answer=(final_answer or "(empty)").strip(),
    )
    payload = {
        "model": cfg.model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "stream": False,
    }
    try:
        resp = await client.post(
            f"{cfg.base_url.rstrip('/')}/v1/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {cfg.api_key}"},
            timeout=cfg.timeout_s,
        )
        resp.raise_for_status()
        data = resp.json()
    except httpx.HTTPStatusError as e:
        body = ""
        try:
            body = e.response.text[:300]
        except Exception:
            pass
        return {
            "answer_correct": False,
            "reasoning": f"judge HTTP error: {e!r} body={body}",
            "missing_facts": [],
            "wrong_claims": [],
            "_judge_error": True,
        }
    except httpx.HTTPError as e:
        return {
            "answer_correct": False,
            "reasoning": f"judge transport error: {e!r}",
            "missing_facts": [],
            "wrong_claims": [],
            "_judge_error": True,
        }

    text = (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    ) or ""
    return parse_judge_json(text)


def parse_judge_json(text: str) -> dict[str, Any]:
    """Tolerant parse: take the first {...} blob, coerce types."""
    if not text:
        return {
            "answer_correct": False,
            "reasoning": "empty judge response",
            "missing_facts": [],
            "wrong_claims": [],
            "_judge_error": True,
        }
    m = re.search(r"\{.*\}", text, re.DOTALL)
    payload = m.group(0) if m else text
    try:
        obj = json.loads(payload)
    except json.JSONDecodeError:
        return {
            "answer_correct": False,
            "reasoning": f"unparseable judge response: {text[:200]!r}",
            "missing_facts": [],
            "wrong_claims": [],
            "_judge_error": True,
        }
    raw = obj.get("answer_correct")
    if isinstance(raw, str):
        correct = raw.strip().lower() in {"true", "yes", "1"}
    else:
        correct = bool(raw)
    return {
        "answer_correct": correct,
        "reasoning": str(obj.get("reasoning", "")).strip(),
        "missing_facts": [str(x) for x in (obj.get("missing_facts") or [])],
        "wrong_claims": [str(x) for x in (obj.get("wrong_claims") or [])],
    }


# ---------- main ------------------------------------------------------------


async def run(
    input_path: Path,
    cases_paths: list[str],
    output_path: Path,
    cfg: JudgeConfig,
    concurrency: int,
    limit: int = 0,
) -> None:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    records = data.get("records") or []
    if limit > 0:
        records = records[:limit]
    gts = load_ground_truth(cases_paths)

    missing_gt = sorted({r["case"] for r in records if r["case"] not in gts})
    if missing_gt:
        sys.stderr.write(
            "WARNING: no ground_truth block for cases: "
            + ", ".join(missing_gt)
            + "\n  (these will be judged against llm_criteria fallback only)\n"
        )

    sem = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient() as client:

        async def process(idx: int, rec: dict[str, Any]) -> dict[str, Any]:
            case = rec["case"]
            query = rec.get("query") or rec.get("result", {}).get("query", "")
            result = rec.get("result") or {}
            tool_calls = result.get("tool_calls") or []
            final_answer = result.get("final_answer") or result.get("response") or ""
            error = result.get("error")

            process_block = analyse_process(tool_calls)

            gt = gts.get(case) or GroundTruth(
                required_facts=[],
                must_not_claim=[],
                notes="",
                llm_criteria=rec.get("llm_criteria")
                or rec.get("evaluation", {}).get("llm_reasoning"),
            )

            if error:
                judge = {
                    "answer_correct": False,
                    "reasoning": f"agent run errored: {error}",
                    "missing_facts": [],
                    "wrong_claims": [],
                    "_judge_error": False,
                }
            else:
                async with sem:
                    judge = await judge_one(client, cfg, query, gt, final_answer)
            return {
                "_idx": idx,
                "case": case,
                "repetition": rec.get("repetition"),
                "variant": result.get("variant"),
                "model_id": result.get("model_id"),
                "query": query,
                "final_answer": final_answer,
                "duration_s": result.get("duration_s"),
                "tool_call_count": result.get("tool_call_count")
                or len(tool_calls),
                "judge": {
                    "answer_correct": judge["answer_correct"],
                    "reasoning": judge.get("reasoning", ""),
                    "missing_facts": judge.get("missing_facts", []),
                    "wrong_claims": judge.get("wrong_claims", []),
                    "judge_error": judge.get("_judge_error", False),
                },
                "process": process_block,
                "all_good": bool(
                    judge["answer_correct"]
                    and process_block["read_manuals_first"]
                    and process_block["tool_error_count"] == 0
                ),
            }

        tasks = [process(i, r) for i, r in enumerate(records)]
        out_records = await asyncio.gather(*tasks)

    out_records.sort(key=lambda r: r["_idx"])
    for r in out_records:
        r.pop("_idx", None)

    summary = summarise(out_records)

    output_path.write_text(
        json.dumps(
            {
                "input": str(input_path),
                "cases": cases_paths,
                "judge_model": cfg.model,
                "judge_base_url": cfg.base_url,
                "summary": summary,
                "records": out_records,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print_summary(summary)
    print(f"\nWrote {output_path}")


def summarise(records: list[dict[str, Any]]) -> dict[str, Any]:
    from collections import defaultdict

    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        buckets[(r.get("variant") or "?", r["case"])].append(r)

    per_bucket = []
    for (variant, case), recs in sorted(buckets.items()):
        n = len(recs)
        correct = sum(1 for r in recs if r["judge"]["answer_correct"])
        manuals_first = sum(1 for r in recs if r["process"]["read_manuals_first"])
        clean = sum(1 for r in recs if r["process"]["tool_error_count"] == 0)
        all_good = sum(1 for r in recs if r["all_good"])
        per_bucket.append(
            {
                "variant": variant,
                "case": case,
                "n": n,
                "correct": correct,
                "correct_rate": round(correct / n, 3) if n else 0.0,
                "manuals_first": manuals_first,
                "manuals_first_rate": round(manuals_first / n, 3) if n else 0.0,
                "tool_error_free": clean,
                "tool_error_free_rate": round(clean / n, 3) if n else 0.0,
                "all_good": all_good,
                "all_good_rate": round(all_good / n, 3) if n else 0.0,
            }
        )

    per_variant_totals: dict[str, dict[str, int]] = defaultdict(
        lambda: {"n": 0, "correct": 0, "manuals_first": 0, "clean": 0, "all_good": 0}
    )
    for b in per_bucket:
        v = b["variant"]
        per_variant_totals[v]["n"] += b["n"]
        per_variant_totals[v]["correct"] += b["correct"]
        per_variant_totals[v]["manuals_first"] += b["manuals_first"]
        per_variant_totals[v]["clean"] += b["tool_error_free"]
        per_variant_totals[v]["all_good"] += b["all_good"]

    per_variant = []
    for variant, t in sorted(per_variant_totals.items()):
        n = t["n"]
        per_variant.append(
            {
                "variant": variant,
                "n": n,
                "correct": t["correct"],
                "correct_rate": round(t["correct"] / n, 3) if n else 0.0,
                "manuals_first": t["manuals_first"],
                "manuals_first_rate": round(t["manuals_first"] / n, 3) if n else 0.0,
                "tool_error_free": t["clean"],
                "tool_error_free_rate": round(t["clean"] / n, 3) if n else 0.0,
                "all_good": t["all_good"],
                "all_good_rate": round(t["all_good"] / n, 3) if n else 0.0,
            }
        )

    grand_n = sum(t["n"] for t in per_variant_totals.values())
    grand_correct = sum(t["correct"] for t in per_variant_totals.values())
    grand_manuals = sum(t["manuals_first"] for t in per_variant_totals.values())
    grand_clean = sum(t["clean"] for t in per_variant_totals.values())
    grand_all_good = sum(t["all_good"] for t in per_variant_totals.values())
    totals = {
        "n": grand_n,
        "correct": grand_correct,
        "correct_rate": round(grand_correct / grand_n, 3) if grand_n else 0.0,
        "manuals_first": grand_manuals,
        "manuals_first_rate": round(grand_manuals / grand_n, 3) if grand_n else 0.0,
        "tool_error_free": grand_clean,
        "tool_error_free_rate": round(grand_clean / grand_n, 3) if grand_n else 0.0,
        "all_good": grand_all_good,
        "all_good_rate": round(grand_all_good / grand_n, 3) if grand_n else 0.0,
    }

    return {"totals": totals, "per_bucket": per_bucket, "per_variant": per_variant}


def print_summary(summary: dict[str, Any]) -> None:
    totals = summary["totals"]
    n = totals["n"]
    print("\n" + "=" * 72)
    print(
        f"  RESULT: {totals['correct']}/{n} tests correct "
        f"({totals['correct_rate'] * 100:.1f}%)  ·  "
        f"all_good: {totals['all_good']}/{n} ({totals['all_good_rate'] * 100:.1f}%)"
    )
    print("=" * 72)

    print("\n=== Per-(variant, case) ===")
    print(
        f"{'variant':<22} {'case':<42} {'n':>3} {'correct':>9} {'manuals1st':>11} {'no_err':>7} {'all_good':>9}"
    )
    for b in summary["per_bucket"]:
        print(
            f"{b['variant']:<22} {b['case']:<42} {b['n']:>3} "
            f"{b['correct']:>3}/{b['n']:<3} ({b['correct_rate']*100:>4.0f}%)  "
            f"{b['manuals_first']:>2}/{b['n']:<3} ({b['manuals_first_rate']*100:>4.0f}%)  "
            f"{b['tool_error_free']:>2}/{b['n']:<3} "
            f"{b['all_good']:>2}/{b['n']:<3} ({b['all_good_rate']*100:>4.0f}%)"
        )
    print("\n=== Per-variant totals ===")
    print(
        f"{'variant':<22} {'n':>4} {'correct':>14} {'manuals1st':>12} {'no_err':>9} {'all_good':>10}"
    )
    for v in summary["per_variant"]:
        print(
            f"{v['variant']:<22} {v['n']:>4}  "
            f"{v['correct']:>3}/{v['n']:<3} ({v['correct_rate']*100:>4.0f}%) "
            f"{v['manuals_first_rate']*100:>9.1f}%  "
            f"{v['tool_error_free_rate']*100:>7.1f}%  "
            f"{v['all_good_rate']*100:>8.1f}%"
        )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--input",
        required=True,
        type=Path,
        help="path to raw run_tests.py output (e.g. results/<slug>_N10.json)",
    )
    p.add_argument(
        "--cases",
        nargs="+",
        default=["cases/bench_b.yaml"],
        help="case YAML file(s) with ground_truth blocks",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="output path; defaults to <input-stem>_judged.json",
    )
    p.add_argument(
        "--base-url",
        default=os.environ.get("LLM_BASE_URL", ""),
        help="LLM endpoint (default: $LLM_BASE_URL)",
    )
    p.add_argument(
        "--model",
        default=os.environ.get("LLM_MODEL", ""),
        help="judge model id (default: $LLM_MODEL)",
    )
    p.add_argument(
        "--api-key-env",
        default="OPENAI_API_KEY",
        help="env var holding bearer token (default: OPENAI_API_KEY)",
    )
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument(
        "--limit",
        type=int,
        default=0,
        help="if >0, only judge the first N records (smoke-test mode)",
    )
    args = p.parse_args()

    if not args.base_url or not args.model:
        sys.stderr.write(
            "ERROR: --base-url and --model are required (or set $LLM_BASE_URL "
            "and $LLM_MODEL).\n"
        )
        return 2

    api_key = os.environ.get(args.api_key_env) or "dummy"
    cfg = JudgeConfig(base_url=args.base_url, model=args.model, api_key=api_key)

    input_path: Path = args.input
    if args.output is None:
        stem = input_path.stem
        # tolerate accidentally passing an already-judged file
        if stem.endswith("_judged"):
            out = input_path
        else:
            out = input_path.with_name(f"{stem}_judged.json")
    else:
        out = args.output

    asyncio.run(
        run(
            input_path=input_path,
            cases_paths=[str(p) for p in args.cases],
            output_path=out,
            cfg=cfg,
            concurrency=args.concurrency,
            limit=args.limit,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
