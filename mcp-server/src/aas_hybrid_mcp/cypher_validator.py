"""Regex-based pre-validator for Cypher queries sent to query_aas_graph.

Mode is controlled by the STRICT_READ_VALIDATION environment variable:
  off    (default) — validator is a no-op; all queries pass through
  warn   — query executes; forbidden patterns surfaced in _warnings
  strict — query is blocked; structured error returned, no Neo4j call

The four forbidden patterns guard against the two most common anti-patterns
documented in cypher.md (#3 assetType null-lookup, #4 idShort/id substring):
  1. toLower(x.idShort/x.id) CONTAINS — substring match via toLowerCase wrapper
  2. x.idShort CONTAINS or =~        — direct substring / regex on idShort
  3. x.id CONTAINS or =~             — substring / regex on id (URN)
  4. x.assetType CONTAINS / = / =~   — assetType is often null, unreliable lookup

Legitimate use of idShort with exact equality (=) is intentionally NOT flagged.
"""

import os
import re
from dataclasses import dataclass, field


@dataclass
class Violation:
    rule: str
    hint: str
    match: str


@dataclass
class ValidationResult:
    allowed: bool
    violations: list[Violation] = field(default_factory=list)


@dataclass
class _Rule:
    name: str
    pattern: re.Pattern
    hint: str


_RULES: list[_Rule] = [
    _Rule(
        name="toLower_id_contains",
        pattern=re.compile(r"\btoLower\([^)]*\.id(?:Short)?\)\s+CONTAINS\b", re.IGNORECASE),
        hint=(
            "Use exact match instead: WHERE aas.idShort = 'ExactName'. "
            "See cypher.md anti-pattern #4."
        ),
    ),
    _Rule(
        name="idShort_contains_or_regex",
        # trailing \b omitted: =~ ends with non-word char, so \b would fail
        pattern=re.compile(r"\b\w+\.idShort\s+(CONTAINS\b|=~)", re.IGNORECASE),
        hint=(
            "Use exact match instead: WHERE aas.idShort = 'ExactName'. "
            "See cypher.md anti-pattern #4."
        ),
    ),
    _Rule(
        name="id_contains_or_regex",
        pattern=re.compile(r"\b\w+\.id\s+(CONTAINS\b|=~)", re.IGNORECASE),
        hint=(
            "Use exact match instead: WHERE aas.id = 'urn:...'. "
            "See cypher.md anti-pattern #4."
        ),
    ),
    _Rule(
        name="assetType_match",
        # = / =~ / CONTAINS — assetType is often null, unreliable as lookup
        pattern=re.compile(r"\b\w+\.assetType\s+(CONTAINS\b|=~|=)", re.IGNORECASE),
        hint=(
            "assetType is often null and unreliable as a lookup. "
            "Use semanticId-based submodel traversal instead. "
            "See cypher.md anti-pattern #3."
        ),
    ),
]


def validate(cypher: str, mode: str | None = None) -> ValidationResult:
    """Validate *cypher* against forbidden patterns.

    ``mode`` overrides STRICT_READ_VALIDATION env var — useful in tests.
    """
    effective_mode = mode or os.environ.get("STRICT_READ_VALIDATION", "off")
    if effective_mode == "off":
        return ValidationResult(allowed=True)

    violations: list[Violation] = []
    for rule in _RULES:
        for m in rule.pattern.finditer(cypher):
            violations.append(Violation(rule=rule.name, hint=rule.hint, match=m.group(0)))

    if effective_mode == "strict":
        return ValidationResult(allowed=len(violations) == 0, violations=violations)

    # warn: query runs, but violations are reported
    return ValidationResult(allowed=True, violations=violations)
