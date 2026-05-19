"""Unit tests for cypher_validator — pure regex, no Neo4j needed."""

import pytest
from aas_hybrid_mcp.cypher_validator import validate


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _forbidden(cypher: str, mode: str = "strict") -> bool:
    """Return True if the query is blocked in the given mode."""
    vr = validate(cypher, mode=mode)
    return not vr.allowed or bool(vr.violations)


def _violations(cypher: str, mode: str = "warn") -> list[str]:
    return [v.rule for v in validate(cypher, mode=mode).violations]


# ---------------------------------------------------------------------------
# Positive cases — must be caught
# ---------------------------------------------------------------------------

class TestForbiddenPatterns:
    def test_toLower_idShort_contains(self):
        q = "WHERE toLower(aas.idShort) CONTAINS 'mir100'"
        assert _forbidden(q)

    def test_toLower_id_contains(self):
        q = "WHERE toLower(aas.id) CONTAINS 'mir100'"
        assert _forbidden(q)

    def test_toLower_with_alias(self):
        q = "WHERE toLower(a.idShort) CONTAINS 'agv'"
        assert _forbidden(q)

    def test_direct_idShort_contains(self):
        q = "WHERE aas.idShort CONTAINS 'MiR'"
        assert _forbidden(q)

    def test_direct_idShort_regex(self):
        q = "WHERE aas.idShort =~ '.*mir.*'"
        assert _forbidden(q)

    def test_direct_idShort_contains_on_property(self):
        # From Run 3 trace: p.idShort CONTAINS 'speed'
        q = "WHERE toLower(p.idShort) CONTAINS 'speed'"
        assert _forbidden(q)

    def test_direct_id_contains(self):
        q = "WHERE aas.id CONTAINS 'mir100'"
        assert _forbidden(q)

    def test_direct_id_regex(self):
        q = "WHERE sm.id =~ '.*techdata.*'"
        assert _forbidden(q)

    def test_assetType_contains(self):
        q = "WHERE a.assetType CONTAINS 'AGV'"
        assert _forbidden(q)

    def test_assetType_equals(self):
        # assetType = 'X' is also forbidden (often null)
        q = "WHERE a.assetType = 'Type'"
        assert _forbidden(q)

    def test_assetType_regex(self):
        q = "WHERE a.assetType =~ '.*Robot.*'"
        assert _forbidden(q)

    def test_multi_violation_single_query(self):
        # Exactly the query from the traces
        q = (
            "MATCH (aas:AssetAdministrationShell)-[:MANAGES_ASSET]->(a:Asset)\n"
            "WHERE toLower(aas.idShort) CONTAINS 'mir100'\n"
            "   OR toLower(a.idShort) CONTAINS 'mir100'\n"
            "   OR toLower(aas.id) CONTAINS 'mir100'\n"
            "RETURN aas.idShort"
        )
        vr = validate(q, mode="strict")
        assert not vr.allowed
        assert len(vr.violations) >= 3


# ---------------------------------------------------------------------------
# Negative cases — must NOT be caught
# ---------------------------------------------------------------------------

class TestAllowedPatterns:
    def test_exact_idShort_equals(self):
        q = "WHERE aas.idShort = 'MiR100_Type'"
        assert not _forbidden(q)

    def test_exact_id_equals(self):
        q = "WHERE aas.id = 'urn:aas:mir100:001'"
        assert not _forbidden(q)

    def test_property_idShort_equals(self):
        q = "WHERE p.idShort = 'SpeedMaxWithMaxLoadAsSpecified'"
        assert not _forbidden(q)

    def test_idShort_in_list(self):
        q = "WHERE p.idShort IN ['SpeedMaxWithMaxLoadAsSpecified', 'SpeedMaxEmptyAsSpecified']"
        assert not _forbidden(q)

    def test_recipe_c_case1(self):
        # The correct pattern from recipes.md Recipe C
        q = (
            "MATCH (aas:AssetAdministrationShell {idShort: $idShort})\n"
            "      -[:HAS_SUBMODEL]->(sm:Submodel)\n"
            "      -[:HAS_SEMANTIC_ID]->(sc:SemanticConcept {id: $templateSemanticId})\n"
            "MATCH (sm)-[:HAS_ELEMENT*]->(p:Property)\n"
            "WHERE p.idShort IN $propertyIdShorts\n"
            "RETURN aas.idShort, p.idShort, p.value, p.valueType"
        )
        assert not _forbidden(q)

    def test_semanticId_id_equals(self):
        # sc.id = '...' is a standard pattern — must not be blocked
        q = "MATCH (sm)-[:HAS_SEMANTIC_ID]->(sc:SemanticConcept {id: 'https://admin-shell.io/...'})"
        assert not _forbidden(q)

    def test_return_idShort(self):
        # RETURN clause mentioning idShort must not be flagged
        q = "RETURN aas.idShort, p.value"
        assert not _forbidden(q)


# ---------------------------------------------------------------------------
# Mode behaviour
# ---------------------------------------------------------------------------

class TestModes:
    _FORBIDDEN_QUERY = "WHERE toLower(aas.idShort) CONTAINS 'mir100'"
    _CLEAN_QUERY = "WHERE aas.idShort = 'MiR100_Type'"

    def test_off_passes_everything(self):
        vr = validate(self._FORBIDDEN_QUERY, mode="off")
        assert vr.allowed is True
        assert vr.violations == []

    def test_warn_allowed_but_has_violations(self):
        vr = validate(self._FORBIDDEN_QUERY, mode="warn")
        assert vr.allowed is True
        assert len(vr.violations) > 0

    def test_strict_blocks_forbidden(self):
        vr = validate(self._FORBIDDEN_QUERY, mode="strict")
        assert vr.allowed is False
        assert len(vr.violations) > 0

    def test_strict_passes_clean(self):
        vr = validate(self._CLEAN_QUERY, mode="strict")
        assert vr.allowed is True
        assert vr.violations == []

    def test_violation_fields_present(self):
        vr = validate(self._FORBIDDEN_QUERY, mode="warn")
        v = vr.violations[0]
        assert v.rule
        assert v.hint
        assert v.match
