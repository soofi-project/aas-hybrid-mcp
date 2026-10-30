"""query_aas_graph warns when the plugin-internal internalGraphAnchorId is in the result."""

import asyncio

from fastmcp import FastMCP
from neo4j.time import Duration

from aas_hybrid_mcp import neo4j_client
from aas_hybrid_mcp.tools import cypher_query

KEY = "internalGraphAnchorId"


def _call_tool(monkeypatch, rows, unknown_names=None):
    async def fake_read(cypher, params=None):
        return rows, {"unknown_names": unknown_names or {}, "notifications": []}

    async def fake_labels():
        return ["Asset"]

    monkeypatch.setattr(neo4j_client, "read_query_with_notices", fake_read)
    monkeypatch.setattr(neo4j_client, "labels", fake_labels)
    mcp = FastMCP("t")
    cypher_query.register(mcp)

    async def call():
        tool = await mcp.get_tool("query_aas_graph")
        return await tool.fn(cypher="MATCH (a:Asset) RETURN a")

    return asyncio.run(call())


def _rules(result):
    return [w["rule"] for w in result.get("_warnings", [])]


def test_rows_are_returned_unchanged_and_warned_about(monkeypatch):
    rows = [{"a": {KEY: "abc", "idShort": "MiR100_001"}}]
    result = _call_tool(monkeypatch, rows)
    assert result["rows"] == rows
    (warning,) = result["_warnings"]
    assert warning["rule"] == "internal_property"
    assert warning["keys"] == [KEY]
    assert "not an AAS identifier" in warning["hint"]


def test_warns_for_key_in_list_tuple_projection_column_and_value(monkeypatch):
    for rows in (
        [{"ns": [{KEY: "1"}, {KEY: "2"}]}],
        [{"r": ({KEY: "1"}, "HAS_ELEMENT", {"id": "y"})}],
        [{f"a.{KEY}": "abc"}],
        [{"k": KEY}],
    ):
        assert _rules(_call_tool(monkeypatch, rows)) == ["internal_property"]


def test_one_warning_for_many_occurrences(monkeypatch):
    rows = [{"a": {KEY: str(i)}} for i in range(5)]
    assert _rules(_call_tool(monkeypatch, rows)) == ["internal_property"]


def test_no_warning_without_the_key(monkeypatch):
    result = _call_tool(monkeypatch, [{"a": {"idShort": "x"}}])
    assert "_warnings" not in result


def test_neo4j_time_values_pass_through(monkeypatch):
    rows = [{"d": Duration(days=1)}]
    result = _call_tool(monkeypatch, rows)
    assert result["rows"] == rows
    assert "_warnings" not in result


def test_total_truncated_and_other_warnings_unchanged(monkeypatch):
    monkeypatch.setattr(cypher_query, "MAX_ROWS", 2)
    rows = [{"a": {KEY: str(i)}} for i in range(3)]
    result = _call_tool(monkeypatch, rows, {"labels": ["Foo"]})
    assert result["rows"] == rows[:2]
    assert result["total"] == 3
    assert result["truncated"] is True
    assert sorted(_rules(result)) == ["internal_property", "unknown_label"]


def test_key_only_in_truncated_rows_does_not_warn(monkeypatch):
    monkeypatch.setattr(cypher_query, "MAX_ROWS", 1)
    rows = [{"a": {"idShort": "x"}}, {"a": {KEY: "hidden-by-truncation"}}]
    assert "_warnings" not in _call_tool(monkeypatch, rows)
