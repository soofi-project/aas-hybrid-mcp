"""query_aas_graph must not return the plugin-internal internalGraphAnchorId."""

import asyncio

from fastmcp import FastMCP

from aas_hybrid_mcp import neo4j_client
from aas_hybrid_mcp.tools import cypher_query
from aas_hybrid_mcp.tools.cypher_query import _strip_internal

KEY = "internalGraphAnchorId"


def test_removes_key_from_node_dict():
    node = {KEY: "abc", "idShort": "MiR100_001"}
    assert _strip_internal({"a": node}) == {"a": {"idShort": "MiR100_001"}}


def test_removes_key_from_nested_list_and_relationship_tuple():
    rows = [
        {
            "nodes": [{KEY: "1", "id": "x"}, {KEY: "2", "id": "y"}],
            "r": ({KEY: "1"}, "HAS_ELEMENT", {KEY: "2", "id": "y"}),
        }
    ]
    assert _strip_internal(rows) == [
        {
            "nodes": [{"id": "x"}, {"id": "y"}],
            "r": ({}, "HAS_ELEMENT", {"id": "y"}),
        }
    ]


def test_removes_default_projection_column():
    assert _strip_internal([{f"a.{KEY}": "abc", "a.idShort": "x"}]) == [
        {"a.idShort": "x"}
    ]


def test_keeps_other_keys_and_explicit_alias():
    row = {"id": "abc", "idShort": "x", "n": 3, "none": None}
    assert _strip_internal([row]) == [row]


def _call_tool(monkeypatch, rows):
    async def fake_read(cypher, params=None):
        return rows, {
            "unknown_names": {"labels": ["Foo"]},
            "notifications": [],
        }

    async def fake_labels():
        return ["Asset"]

    monkeypatch.setattr(neo4j_client, "read_query_with_notices", fake_read)
    monkeypatch.setattr(neo4j_client, "labels", fake_labels)
    mcp = FastMCP("t")
    cypher_query.register(mcp)

    async def call():
        tool = await mcp.get_tool("query_aas_graph")
        return await tool.fn(cypher="MATCH (a:Foo) RETURN a")

    return asyncio.run(call())


def test_tool_strips_key_and_keeps_total_truncated_and_warnings(monkeypatch):
    monkeypatch.setattr(cypher_query, "MAX_ROWS", 2)
    rows = [{"a": {KEY: str(i), "idShort": f"r{i}"}} for i in range(3)]
    result = _call_tool(monkeypatch, rows)
    assert result["rows"] == [{"a": {"idShort": "r0"}}, {"a": {"idShort": "r1"}}]
    assert result["total"] == 3
    assert result["truncated"] is True
    assert result["_warnings"][0]["rule"] == "unknown_label"
