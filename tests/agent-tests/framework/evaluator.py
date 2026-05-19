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
class ToolViolation:
    """Records a tool-call constraint failure."""
    reason: str  # e.g. "required tool 'X' was not called" or "forbidden tool 'Y' was called"


@dataclass
class ValidatorRejection:
    """Records a server-side forbidden_pattern rejection from query_aas_graph."""

    tool_call_index: int
    rules: list[str]          # rule names from the validator's violations list
    self_corrected: bool | None  # True = next qag call had no rejection; None = no follow-up


@dataclass
class WritePathAnalysis:
    """Classifies how the agent handled submodel creation write-path.

    Used to distinguish bypass types for the Layered-Determinism paper finding.
    Only populated when put_submodel or put_submodel_element appear in tool_calls.
    """

    put_submodel_attempted: bool = False
    put_submodel_error: str | None = None   # error text if put_submodel failed
    put_submodel_element_called: bool = False
    bypass_type: str | None = None
    # "direct"   — put_submodel_element used without prior put_submodel attempt
    # "cascade"  — put_submodel failed → put_submodel_element called afterwards
    # "correct"  — put_submodel succeeded, no put_submodel_element for new submodel
    # "surfaced" — put_submodel failed, no put_submodel_element fallback


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
    tool_violations: list[ToolViolation] = field(default_factory=list)
    validator_rejections: list[ValidatorRejection] = field(default_factory=list)
    write_path: WritePathAnalysis | None = None
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
            "tool_violations": [{"reason": v.reason} for v in self.tool_violations],
            "validator_rejections": [
                {
                    "tool_call_index": v.tool_call_index,
                    "rules": v.rules,
                    "self_corrected": v.self_corrected,
                }
                for v in self.validator_rejections
            ],
            "write_path": {
                "put_submodel_attempted": self.write_path.put_submodel_attempted,
                "put_submodel_error": self.write_path.put_submodel_error,
                "put_submodel_element_called": self.write_path.put_submodel_element_called,
                "bypass_type": self.write_path.bypass_type,
            } if self.write_path else None,
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


def _detect_tool_violations(case: Case, result: TResult) -> list[ToolViolation]:
    """Check tool_called, tool_args, and forbidden_tools constraints."""
    violations: list[ToolViolation] = []
    called_names = {tc.name for tc in result.tool_calls}

    # Required tool must have been called.
    if case.expected.tool_called:
        if case.expected.tool_called not in called_names:
            violations.append(ToolViolation(
                reason=f"required tool '{case.expected.tool_called}' was not called "
                       f"(called: {sorted(called_names) or ['none']})"
            ))
        elif case.expected.tool_args:
            # Check that at least one call to tool_called has matching args (partial match).
            for tc in result.tool_calls:
                if tc.name != case.expected.tool_called:
                    continue
                if not isinstance(tc.args, dict):
                    continue
                mismatches = {
                    k: (v, tc.args.get(k))
                    for k, v in case.expected.tool_args.items()
                    if tc.args.get(k) != v
                }
                if not mismatches:
                    break  # found a matching call
            else:
                violations.append(ToolViolation(
                    reason=f"tool '{case.expected.tool_called}' was called but no call matched "
                           f"expected args {case.expected.tool_args}"
                ))

    # Forbidden tools must NOT have been called.
    for forbidden in case.forbidden_tools:
        if forbidden in called_names:
            violations.append(ToolViolation(reason=f"forbidden tool '{forbidden}' was called"))

    return violations


def _analyse_write_path(result: TResult) -> WritePathAnalysis | None:
    """Classify how the agent handled submodel creation.

    Looks at the sequence of put_submodel / put_submodel_element tool calls
    and their results to determine which bypass pattern (if any) occurred.
    Only returns an analysis when at least one write tool was called.
    """
    write_tools = {"put_submodel", "put_submodel_element"}
    relevant = [(i, tc) for i, tc in enumerate(result.tool_calls) if tc.name in write_tools]
    if not relevant:
        return None

    analysis = WritePathAnalysis()

    # Find put_submodel calls and check if they errored.
    ps_error_indices: set[int] = set()
    for i, tc in relevant:
        if tc.name != "put_submodel":
            continue
        analysis.put_submodel_attempted = True
        result_text = tc.result or ""
        # Tool errors arrive as "Tool error: ..." or contain "error"/"failed" in the result.
        if "error" in result_text.lower() or "failed" in result_text.lower() or "validation" in result_text.lower():
            ps_error_indices.add(i)
            if not analysis.put_submodel_error:
                analysis.put_submodel_error = result_text[:300]

    # Check put_submodel_element calls.
    pse_indices = [i for i, tc in relevant if tc.name == "put_submodel_element"]
    analysis.put_submodel_element_called = bool(pse_indices)

    # Classify.
    if not analysis.put_submodel_attempted and analysis.put_submodel_element_called:
        analysis.bypass_type = "direct"
    elif analysis.put_submodel_attempted and ps_error_indices and analysis.put_submodel_element_called:
        # put_submodel_element must come AFTER a failed put_submodel.
        first_pse = min(pse_indices)
        last_ps_error = max(ps_error_indices)
        if first_pse > last_ps_error:
            analysis.bypass_type = "cascade"
        else:
            analysis.bypass_type = "direct"
    elif analysis.put_submodel_attempted and not analysis.put_submodel_element_called:
        if ps_error_indices:
            analysis.bypass_type = "surfaced"
        else:
            analysis.bypass_type = "correct"

    return analysis


def _detect_validator_rejections(result: TResult) -> list[ValidatorRejection]:
    """Scan query_aas_graph tool results for server-side forbidden_pattern rejections."""
    qag_calls = [(i, tc) for i, tc in enumerate(result.tool_calls) if tc.name == "query_aas_graph"]

    rejected_positions: set[int] = set()
    raw: list[tuple[int, int, list[str]]] = []  # (qag_pos, tool_call_index, rules)

    for pos, (i, tc) in enumerate(qag_calls):
        try:
            data = json.loads(tc.result) if isinstance(tc.result, str) else {}
        except (json.JSONDecodeError, AttributeError, TypeError):
            continue
        if not isinstance(data, dict) or data.get("error") != "forbidden_pattern":
            continue
        rules = [
            v.get("rule", "unknown")
            for v in data.get("violations", [])
            if isinstance(v, dict)
        ]
        raw.append((pos, i, rules))
        rejected_positions.add(pos)

    rejections: list[ValidatorRejection] = []
    for pos, tc_index, rules in raw:
        next_pos = pos + 1
        if next_pos < len(qag_calls):
            self_corrected = next_pos not in rejected_positions
        else:
            self_corrected = None
        rejections.append(ValidatorRejection(
            tool_call_index=tc_index,
            rules=rules,
            self_corrected=self_corrected,
        ))
    return rejections


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
    tool_violations = _detect_tool_violations(case, result)
    validator_rejections = _detect_validator_rejections(result)
    write_path = _analyse_write_path(result)

    # Score: 70% keywords, 30% pattern (if specified). Forbidden response
    # tokens, forbidden Cypher patterns, or tool violations zero out — hard rules.
    # Validator rejections are purely informational and do not affect the score.
    kw_score = (len(hits) / len(spec.keywords)) if spec.keywords else 1.0
    pat_score = 1.0 if (pattern_matched is None or pattern_matched) else 0.0
    weight_kw = 0.7 if spec.pattern else 1.0
    weight_pat = 0.3 if spec.pattern else 0.0
    regex_score = kw_score * weight_kw + pat_score * weight_pat
    if forbidden_hits or cypher_violations or tool_violations:
        regex_score = 0.0

    passed = (
        regex_score >= 0.7
        and not forbidden_hits
        and not cypher_violations
        and not tool_violations
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
        tool_violations=tool_violations,
        validator_rejections=validator_rejections,
        write_path=write_path,
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

    def __init__(self, base_url: str, model: str, timeout_s: float = 60.0, api_key: str = "") -> None:
        if not base_url or not model:
            raise ValueError("LLMJudge requires base_url and model")
        self._base = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout_s
        self._api_key = api_key or "dummy"

    @classmethod
    def from_config(cls, cfg: dict[str, Any]) -> "LLMJudge":
        base = cfg.get("base_url") or os.environ.get("LLM_BASE_URL", "")
        model = cfg.get("model") or os.environ.get("LLM_MODEL", "")
        api_key = os.environ.get("OPENAI_API_KEY", "")
        return cls(base_url=base, model=model, api_key=api_key)

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
                    headers={"Authorization": f"Bearer {self._api_key}"},
                )
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPStatusError as e:
            body = ""
            try:
                body = e.response.text[:500]
            except Exception:
                pass
            msg = f"LLM judge HTTP error: {e!r} (body: {body})"
            raise RuntimeError(msg) from e
        except httpx.HTTPError as e:
            raise RuntimeError(f"LLM judge transport error: {e!r}") from e

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
    if ev.forbidden_hits or ev.cypher_violations or ev.tool_violations:
        ev.score = 0.0
        ev.passed = False
    else:
        ev.score = 0.4 * ev.regex_score + 0.6 * llm_score
        ev.passed = ev.score >= 0.7
    return ev
