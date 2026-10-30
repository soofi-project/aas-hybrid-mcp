"""Unknown relationship types, labels and property keys come from the Neo4j summary."""

from types import SimpleNamespace

from aas_hybrid_mcp import neo4j_client


def _status(code, description, is_notification=None, position=None):
    return SimpleNamespace(
        gql_status=code,
        status_description=description,
        is_notification=code.startswith(("01N", "03N"))
        if is_notification is None
        else is_notification,
        raw_severity="WARNING" if code.startswith("01N") else "INFORMATION",
        position=position,
    )


def _summary(*statuses):
    return SimpleNamespace(gql_status_objects=list(statuses))


def _rel(name):
    return _status(
        "01N51",
        f"warn: relationship type does not exist. The relationship type `{name}` does not exist. Verify that the spelling is correct.",
    )


def test_groups_names_by_kind_once_and_ignores_other_statuses():
    summary = _summary(
        _status("02000", "note: no data"),
        _rel("CONTAINS"),
        _rel("HAS_COMPONENT"),
        _rel("CONTAINS"),
        _status("01N50", "warn: label does not exist. The label `Foo` does not exist. Verify that the spelling is correct."),
        _status("01N52", "warn: property key does not exist. The property `x` does not exist. Verify that the spelling is correct."),
        _status("03N90", "info: cartesian product."),
    )
    assert neo4j_client.unknown_names(summary) == {
        "relationship_types": ["CONTAINS", "HAS_COMPONENT"],
        "labels": ["Foo"],
        "property_keys": ["x"],
    }


def test_no_unknown_names_when_query_is_clean():
    clean = _summary(_status("00000", "note: successful completion"))
    assert neo4j_client.unknown_names(clean) == {}


def test_unparsable_description_still_reports_the_name():
    summary = _summary(_status("01N50", "warn: reworded"))
    assert neo4j_client.unknown_names(summary) == {"labels": ["<unparsed>"]}


def test_tool_adds_warnings_per_kind(monkeypatch):
    import asyncio

    from fastmcp import FastMCP

    from aas_hybrid_mcp.tools import cypher_query

    async def fake_read(cypher, params=None):
        return [], {
            "unknown_names": {
                "relationship_types": ["CONTAINS"],
                "labels": ["Foo"],
                "property_keys": ["x"],
            },
            "notifications": [{"code": "03N90", "message": "cartesian product", "severity": "INFORMATION"}],
        }

    async def fake_types():
        return ["HAS_ELEMENT", "HAS_SUBMODEL"]

    async def fake_labels():
        return ["Property", "Submodel"]

    monkeypatch.setattr(neo4j_client, "read_query_with_notices", fake_read)
    monkeypatch.setattr(neo4j_client, "relationship_types", fake_types)
    monkeypatch.setattr(neo4j_client, "labels", fake_labels)
    mcp = FastMCP("t")
    cypher_query.register(mcp)

    async def call():
        tool = await mcp.get_tool("query_aas_graph")
        return await tool.fn(cypher="MATCH (s:Foo)-[:CONTAINS]->(x) WHERE x.x = 1 RETURN x")

    by_rule = {w["rule"]: w for w in asyncio.run(call())["_warnings"]}
    assert by_rule["unknown_relationship_type"]["known_relationship_types"] == [
        "HAS_ELEMENT",
        "HAS_SUBMODEL",
    ]
    assert by_rule["unknown_label"]["unknown"] == ["Foo"]
    assert by_rule["unknown_label"]["known_labels"] == ["Property", "Submodel"]
    assert by_rule["unknown_property_key"]["unknown"] == ["x"]
    assert "known_property_keys" not in by_rule["unknown_property_key"]
    notification = by_rule["neo4j_notification"]
    assert (notification["code"], notification["severity"]) == ("03N90", "INFORMATION")


def test_other_notifications_skip_completion_and_unknown_name_statuses():
    pos = SimpleNamespace(line=1, column=7)
    summary = _summary(
        _status("02000", "note: no data"),
        _rel("CONTAINS"),
        _status("03N90", "info: cartesian product.", position=pos),
    )
    assert neo4j_client.other_notifications(summary) == [
        {
            "code": "03N90",
            "message": "info: cartesian product.",
            "severity": "INFORMATION",
            "position": {"line": 1, "column": 7},
        }
    ]


def test_notification_without_position_has_no_position_key():
    summary = _summary(_status("03N90", "info: cartesian product.", position=None))
    (entry,) = neo4j_client.other_notifications(summary)
    assert "position" not in entry
