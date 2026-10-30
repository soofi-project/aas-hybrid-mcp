"""get_graph_schema serves facts in lean mode and facts plus guidance in full mode."""

import re

from aas_hybrid_mcp.tools import schema

GUIDANCE_HEADINGS = ("## Traversal Tips", "## Common Anti-Patterns", "## Example Queries")


class _FakeMCP:
    """Captures the function that ``register`` hands to ``@mcp.tool``."""

    def tool(self, **_kwargs):
        def decorator(fn):
            self.fn = fn
            return fn

        return decorator


def _served(monkeypatch, mode: str) -> str:
    monkeypatch.setenv("DOCS_MODE", mode)
    mcp = _FakeMCP()
    schema.register(mcp)
    return mcp.fn()


def _catalogue(text: str) -> set[str]:
    """Relationship types and backticked property names the text lists."""
    return set(re.findall(r"\[:([A-Z_]+)", text)) | set(re.findall(r"`([A-Za-z]+)`", text))


def test_full_mode_serves_facts_and_guidance(monkeypatch):
    text = _served(monkeypatch, "full")
    assert text == schema._SCHEMA_FACTS + schema._SCHEMA_GUIDANCE
    for heading in GUIDANCE_HEADINGS:
        assert heading in text


def test_lean_mode_serves_facts_only(monkeypatch):
    text = _served(monkeypatch, "lean")
    assert text == schema._SCHEMA_FACTS
    for heading in GUIDANCE_HEADINGS:
        assert heading not in text
    assert "```cypher" not in text
    assert "## Complete Relationship List" in text


# Frozen from the schema before the facts/guidance split: nothing may drop out of lean.
RELATIONSHIPS = {
    "MANAGES_ASSET", "HAS_SUBMODEL", "HAS_ELEMENT", "DERIVED_FROM",
    "HAS_SEMANTIC_ID", "HAS_SUPPLEMENTAL_SEMANTIC_ID", "HAS_SEMANTIC_ID_LIST_ELEMENT",
    "HAS_ADMIN_INFO", "HAS_DESCRIPTION", "HAS_DISPLAY_NAME", "HAS_EXTENSION", "HAS_QUALIFIER",
    "HAS_VALUE", "HAS_VALUE_ID", "HAS_SPECIFIC_ASSET_ID", "REPRESENTS_ASSET",
    "HAS_EXTERNAL_SUBJECT_ID", "HAS_FIRST", "HAS_SECOND", "HAS_ANNOTATION",
    "HAS_INPUT_VARIABLE", "HAS_OUTPUT_VARIABLE", "HAS_INOUTPUT_VARIABLE",
    "OBSERVES", "USES_MESSAGE_BROKER", "HAS_EMBEDDED_DATA_SPECIFICATION",
    "HAS_DATA_SPECIFICATION", "HAS_DEFINITION", "HAS_PREFERRED_NAME", "HAS_SHORT_NAME",
    "HAS_ALLOWED_VALUE", "CREATED_BY", "REFERS_TO",
}
NODE_TYPES = {
    "AssetAdministrationShell", "Asset", "Submodel", "Property", "File", "Blob", "Range",
    "MultiLanguageProperty", "SubmodelElementCollection", "SubmodelElementList",
    "ReferenceElement", "RelationshipElement", "AnnotatedRelationshipElement", "Entity",
    "Operation", "BasicEventElement", "Capability", "SemanticConcept", "ConceptDescription",
    "LangString", "AdminInfo", "SpecificAssetId", "Qualifier", "Extension",
    "DataSpecification", "AllowedValue",
}


def test_lean_mode_keeps_every_relationship_and_node_type(monkeypatch):
    lean = _served(monkeypatch, "lean")
    listed = set(re.findall(r"`([A-Z][A-Z_]+)`", lean.split("## Complete Relationship List")[1]))
    assert listed == RELATIONSHIPS
    assert {h.lstrip("# ") for h in re.findall(r"^### .+$", lean, re.M)} == NODE_TYPES | {
        "Capability"
    }


def test_lean_description_makes_no_promise_about_guidance(monkeypatch):
    from aas_hybrid_mcp.tool_descriptions import load

    monkeypatch.setenv("DOCS_MODE", "lean")
    assert "traversal" not in load("get_graph_schema").lower()


def test_semantic_targets_are_not_restricted_to_one_label():
    for line in schema._SCHEMA_FACTS.splitlines():
        if "HAS_SEMANTIC_ID]->" in line or "HAS_SUPPLEMENTAL_SEMANTIC_ID]->" in line:
            assert ":SemanticConcept" not in line, line


def test_guidance_matches_semantic_targets_without_label():
    assert "->(:SemanticConcept" not in schema._SCHEMA_GUIDANCE
    assert "(sc:SemanticConcept" not in schema._SCHEMA_GUIDANCE


def test_discovery_query_matches_the_target_without_a_label(monkeypatch):
    import asyncio

    from aas_hybrid_mcp import neo4j_client
    from aas_hybrid_mcp.tools import templates

    seen = []

    async def fake_read_query(cypher, params=None):
        seen.append(cypher)
        return [{"graphSemanticId": "urn:x"}]

    monkeypatch.setattr(neo4j_client, "read_query", fake_read_query)
    assert asyncio.run(templates._discover_graph_semantic_ids()) == ["urn:x"]
    assert ":SemanticConcept" not in seen[0]
    assert "-[:HAS_SEMANTIC_ID]->(sc)" in seen[0]
