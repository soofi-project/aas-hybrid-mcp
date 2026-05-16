"""Regex + LLM-judge evaluators. Composite: regex floor, LLM refinement."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

import httpx

from framework.cases import Case
from framework.runner import TResult, extract_final_answer


@dataclass
class CypherViolation:
    """Records that a tool-call's cypher arg matched a forbidden pattern."""

    pattern: str
    tool_call_index: int
    cypher_excerpt: str


@dataclass
class Evaluation:
    score: float                # final composite score in [0, 1]
    passed: bool
    regex_score: float = 0.0
    llm_score: float | None = None
    keyword_hits: list[str] = field(default_factory=list)
    keyword_misses: list[str] = field(default_factory=list)
    forbidden_hits: list[str] = field(default_factory=list)
    pattern_matched: bool | None = None
    llm_reasoning: str | None = None
    cypher_violations: list[CypherViolation] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": round(self.score, 3),
            "passed": self.passed,
            "regex_score": round(self.regex_score, 3),
            "llm_score": round(self.llm_score, 3) if self.llm_score is not None else None,
            "keyword_hits": self.keyword_hits,
            "keyword_misses": self.keyword_misses,
            "forbidden_hits": self.forbidden_hits,
            "pattern_matched": self.pattern_matched,
            "llm_reasoning": self.llm_reasoning,
            "cypher_violations": [
                {
                    "pattern": v.pattern,
                    "tool_call_index": v.tool_call_index,
                    "cypher_excerpt": v.cypher_excerpt,
                }
                for v in self.cypher_violations
            ],
            "notes": self.notes,
        }


def _detect_cypher_violations(case: Case, result: TResult) -> list[CypherViolation]:
    """Scan query_aas_graph tool-call args for forbidden Cypher patterns."""
    if not case.forbidden_cypher_patterns:
        return []
    compiled = [(p, re.compile(p, re.IGNORECASE)) for p in case.forbidden_cypher_patterns]
    violations: list[CypherViolation] = []
    for i, tc in enumerate(result.tool_calls):
        if tc.name != "query_aas_graph":
            continue
        cypher = ""
        if isinstance(tc.args, dict):
            cypher = str(tc.args.get("cypher", ""))
        if not cypher:
            continue
        for pat, rx in compiled:
            m = rx.search(cypher)
            if m:
                start = max(0, m.start() - 30)
                end = min(len(cypher), m.end() + 30)
                excerpt = cypher[start:end].replace("\n", " ").strip()
                violations.append(CypherViolation(
                    pattern=pat,
                    tool_call_index=i,
                    cypher_excerpt=excerpt,
                ))
    return violations


def evaluate_regex(case: Case, result: TResult) -> Evaluation:
    """Score based on keyword presence, regex pattern, forbidden-token absence,
    and absence of forbidden Cypher patterns in tool-call args."""
    response = result.response or ""
    haystack = response.lower()
    spec = case.expected

    hits: list[str] = []
    misses: list[str] = []
    for kw in spec.keywords:
        if kw.lower() in haystack:
            hits.append(kw)
        else:
            misses.append(kw)

    pattern_matched: bool | None = None
    if spec.pattern:
        pattern_matched = bool(re.search(spec.pattern, response, re.IGNORECASE))

    forbidden_hits = [f for f in spec.forbidden if f.lower() in haystack]
    cypher_violations = _detect_cypher_violations(case, result)

    # Score: 70% keywords, 30% pattern (if specified). Forbidden response
    # tokens OR forbidden Cypher patterns zero out — these are hard rules.
    kw_score = (len(hits) / len(spec.keywords)) if spec.keywords else 1.0
    pat_score = 1.0 if (pattern_matched is None or pattern_matched) else 0.0
    weight_kw = 0.7 if spec.pattern else 1.0
    weight_pat = 0.3 if spec.pattern else 0.0
    regex_score = kw_score * weight_kw + pat_score * weight_pat
    if forbidden_hits or cypher_violations:
        regex_score = 0.0

    passed = (
        regex_score >= 0.7
        and not forbidden_hits
        and not cypher_violations
        and not result.error
    )
    return Evaluation(
        score=regex_score,
        passed=passed,
        regex_score=regex_score,
        keyword_hits=hits,
        keyword_misses=misses,
        forbidden_hits=forbidden_hits,
        pattern_matched=pattern_matched,
        cypher_violations=cypher_violations,
    )


class LLMJudge:
    """Calls a second LLM (vLLM / OpenAI-compatible) to grade the agent response.

    The judge does NOT see the agent's reasoning — only the user query, the
    grading criterion, and the agent's final answer. This keeps the judge
    focused on outcome quality rather than process quality.
    """

    _PROMPT = (
        "You are an evaluator for an industrial-AI agent. Grade the assistant's "
        "answer against the criterion. Be strict: a partially correct answer "
        "with omissions or extra wrong items scores lower.\n\n"
        "User question:\n{query}\n\n"
        "Grading criterion:\n{criterion}\n\n"
        "Assistant answer:\n{answer}\n\n"
        "Respond with ONLY a JSON object: "
        '{{"score": <float 0..1>, "reasoning": "<one sentence>"}}'
    )

    def __init__(self, base_url: str, model: str, timeout_s: float = 60.0) -> None:
        if not base_url or not model:
            raise ValueError("LLMJudge requires base_url and model")
        self._base = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout_s

    @classmethod
    def from_config(cls, cfg: dict[str, Any]) -> "LLMJudge":
        base = cfg.get("base_url") or os.environ.get("LLM_BASE_URL", "")
        model = cfg.get("model") or os.environ.get("LLM_MODEL", "")
        return cls(base_url=base, model=model)

    async def grade(self, case: Case, result: TResult) -> tuple[float, str]:
        criterion = case.llm_criteria or "The answer must directly address the user's question with correct, complete information."
        final_answer = extract_final_answer(result.raw_stream) if result.raw_stream else result.response or ""
        prompt = self._PROMPT.format(
            query=case.query,
            criterion=criterion,
            answer=final_answer or "(empty)",
        )
        payload = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "stream": False,
        }
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(
                    f"{self._base}/v1/chat/completions",
                    json=payload,
                    headers={"Authorization": "Bearer dummy"},
                )
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPError as e:
            return 0.0, f"LLM judge HTTP error: {e!r}"

        text = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )
        score, reasoning = _parse_judge_response(text)
        return score, reasoning


def _parse_judge_response(text: str) -> tuple[float, str]:
    if not text:
        return 0.0, "empty judge response"
    # Tolerate leading prose / code fences.
    m = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    payload = m.group(0) if m else text
    try:
        obj = json.loads(payload)
        score = float(obj.get("score", 0.0))
        reasoning = str(obj.get("reasoning", "")).strip()
        return max(0.0, min(1.0, score)), reasoning
    except (json.JSONDecodeError, ValueError, TypeError):
        return 0.0, f"unparseable judge response: {text[:200]!r}"


async def evaluate(
    case: Case,
    result: TResult,
    *,
    judge: LLMJudge | None = None,
) -> Evaluation:
    """Composite evaluation: regex is the hard floor, LLM refines the score."""
    ev = evaluate_regex(case, result)
    if result.error:
        ev.notes.append(f"agent error: {result.error}")
        ev.passed = False
        ev.score = 0.0
        return ev

    if judge is None or not case.llm_criteria:
        return ev

    llm_score, reasoning = await judge.grade(case, result)
    ev.llm_score = llm_score
    ev.llm_reasoning = reasoning
    # Composite: weight 0.4 regex + 0.6 LLM, but hard-rule violations
    # (forbidden response tokens OR forbidden Cypher patterns) still zero out.
    if ev.forbidden_hits or ev.cypher_violations:
        ev.score = 0.0
        ev.passed = False
    else:
        ev.score = 0.4 * ev.regex_score + 0.6 * llm_score
        ev.passed = ev.score >= 0.7
    return ev
