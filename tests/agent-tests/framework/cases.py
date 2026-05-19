"""YAML test case loader with disambiguation validation."""

from __future__ import annotations

import glob
import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator


# Hard-rule pattern from task_agent_test_framework.md "Frage-Disambiguierung".
# Matches queries that ask "what assets/shells/submodels are in/inside <X>"
# using AAS jargon, which is ambiguous between identity-reading and container-
# reading. Loader downgrades these to warnings or rejects them.
_AMBIGUOUS_QUERY_RE = re.compile(
    r"\b(?:welche|which|what)\s+"
    r"(?:assets?|shells?|aas|submodels?|verwaltungsschalen?)"
    r"\s+(?:sind|are|is|stehen|liegen|gibt)\s+(?:in|inside|im|in der)\b",
    re.IGNORECASE,
)


class ExpectedSpec(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    pattern: str | None = None
    forbidden: list[str] = Field(default_factory=list)
    # Tool-call checks: tool that must have been called, and expected args (partial match).
    tool_called: str | None = None
    tool_args: dict[str, Any] | None = None


class Case(BaseModel):
    name: str
    query: str
    asset: str | None = None
    expected: ExpectedSpec = Field(default_factory=ExpectedSpec)
    llm_criteria: str | None = None
    variants: list[str] | None = None
    tags: list[str] = Field(default_factory=list)

    # Tool-call-level Anti-Pattern checks: regex patterns that must NOT
    # appear in any query_aas_graph tool-call's `cypher` argument. A hit
    # zeroes the score and fails the case. Used to enforce manual rules
    # (e.g., cypher.md Anti-Patterns #3 + #4 — no idShort/id substring
    # lookup) deterministically rather than via prompt-engineering.
    forbidden_cypher_patterns: list[str] = Field(default_factory=list)

    # Tools that must NOT have been called at all during the run.
    forbidden_tools: list[str] = Field(default_factory=list)

    @field_validator("name", "query")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must be non-empty")
        return v.strip()


class CaseFile(BaseModel):
    cases: list[Case]


def is_ambiguous(query: str) -> bool:
    """Return True when *query* uses AAS jargon that admits an identity-reading."""
    return bool(_AMBIGUOUS_QUERY_RE.search(query))


def load_cases(
    paths: list[str],
    *,
    strict: bool = False,
    include_tags: set[str] | None = None,
    exclude_tags: set[str] | None = None,
) -> tuple[list[Case], list[str]]:
    """Load + validate cases from one or more YAML files / globs.

    Returns ``(cases, warnings)``. When *strict* is True, ambiguous queries
    raise instead of producing a warning — useful in CI.

    Tag filtering:
      - ``include_tags``: when set, only cases carrying at least one of these tags
        are kept.
      - ``exclude_tags``: default {"requires_fixture"} — cases that depend on
        not-yet-built test fixtures are skipped unless explicitly included.
    """
    if exclude_tags is None:
        exclude_tags = {"requires_fixture"}

    expanded: list[Path] = []
    for p in paths:
        for match in glob.glob(p):
            expanded.append(Path(match))
    if not expanded:
        raise FileNotFoundError(f"No case files matched: {paths}")

    cases: list[Case] = []
    warnings: list[str] = []
    for path in expanded:
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        if isinstance(raw, list):
            raw = {"cases": raw}
        cf = CaseFile.model_validate(raw)
        for case in cf.cases:
            tag_set = set(case.tags)
            if exclude_tags and tag_set & exclude_tags:
                if include_tags and tag_set & include_tags:
                    pass  # explicit include wins over exclude
                else:
                    warnings.append(
                        f"[{path.name}] '{case.name}': skipped due to tags "
                        f"{sorted(tag_set & exclude_tags)} (override with --include-tags)"
                    )
                    continue
            if include_tags and not (tag_set & include_tags):
                continue
            if is_ambiguous(case.query) and "ambiguous_calibration" not in case.tags:
                msg = (
                    f"[{path.name}] '{case.name}': query uses AAS jargon that "
                    f"admits an identity-reading ('{case.query}'). Tag with "
                    f"'ambiguous_calibration' to keep it as a calibration case, "
                    f"or rephrase with domain vocabulary (Roboter/Geräte/...)."
                )
                if strict:
                    raise ValueError(msg)
                warnings.append(msg)
            cases.append(case)
    return cases, warnings


def resolve_variants(case: Case, default_variants: list[str]) -> list[str]:
    return case.variants if case.variants else default_variants
