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


def test_unparsable_description_still_reports_the_type():
    summary = SimpleNamespace(gql_status_objects=[_status("01N51", "warn: reworded")])
    assert neo4j_client.unknown_relationship_types(summary) == ["<unparsed>"]


def test_tool_adds_warning_with_known_types(monkeypatch):
    import asyncio

    from fastmcp import FastMCP

    from aas_hybrid_mcp.tools import cypher_query

    async def fake_read(cypher, params=None):
        return [], ["CONTAINS"]

    async def fake_types():
        return ["HAS_ELEMENT", "HAS_SUBMODEL"]

    monkeypatch.setattr(neo4j_client, "read_query_with_unknown_types", fake_read)
    monkeypatch.setattr(neo4j_client, "relationship_types", fake_types)
    mcp = FastMCP("t")
    cypher_query.register(mcp)

    async def call():
        tool = await mcp.get_tool("query_aas_graph")
        return await tool.fn(cypher="MATCH (s:Submodel)-[:CONTAINS]->(x) RETURN x")

    result = asyncio.run(call())
    warning = result["_warnings"][0]
    assert warning["rule"] == "unknown_relationship_type"
    assert warning["unknown"] == ["CONTAINS"]
    assert warning["known_relationship_types"] == ["HAS_ELEMENT", "HAS_SUBMODEL"]
