"""Unknown relationship types are read from the Neo4j result summary."""

from types import SimpleNamespace

from aas_hybrid_mcp import neo4j_client


def _status(code, description):
    return SimpleNamespace(gql_status=code, status_description=description)


def test_extracts_each_unknown_type_once_and_ignores_other_statuses():
    summary = SimpleNamespace(
        gql_status_objects=[
            _status("02000", "note: no data"),
            _status(
                "01N51",
                "warn: relationship type does not exist. "
                "The relationship type `CONTAINS` does not exist. Verify that the spelling is correct.",
            ),
            _status(
                "01N51",
                "warn: relationship type does not exist. "
                "The relationship type `HAS_COMPONENT` does not exist. Verify that the spelling is correct.",
            ),
            _status(
                "01N51",
                "warn: relationship type does not exist. "
                "The relationship type `CONTAINS` does not exist. Verify that the spelling is correct.",
            ),
            _status("01N52", "warn: property key does not exist. The property `x` does not exist."),
        ]
    )
    assert neo4j_client.unknown_relationship_types(summary) == ["CONTAINS", "HAS_COMPONENT"]


def test_no_unknown_types_when_query_is_clean():
    summary = SimpleNamespace(gql_status_objects=[_status("00000", "note: successful completion")])
    assert neo4j_client.unknown_relationship_types(summary) == []
