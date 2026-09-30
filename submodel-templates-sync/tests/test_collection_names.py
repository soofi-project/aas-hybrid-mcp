"""The template sync and the MCP server must derive the same collection name.

They are separate sub-projects with separate packages, so the slug algorithm
exists three times. These tests pin the expected output *and* the parity with
the two existing implementations, because a mismatch is invisible at runtime:
the writer fills a collection nobody reads and every search comes back empty.
"""

import ast
import os
import re
from pathlib import Path

import pytest

from collection_names import collection_name

REPO = Path(__file__).resolve().parents[2]

PARITY_HELPERS = [
    REPO / "embedding-service" / "vectorstore.py",
    REPO / "mcp-server" / "src" / "aas_hybrid_mcp" / "weaviate_client.py",
]


def load_helper(path: Path, name: str):
    """Extract one module-level function and run it on its own.

    Compiling just the function def avoids importing weaviate / the embedding
    clients and skips the module-level config reads. Only ``os`` and ``re`` are
    injected — if a helper ever needs more, the test fails with a NameError
    instead of silently comparing against different behaviour.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    (func,) = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    namespace = {"os": os, "re": re}
    exec(compile(ast.Module(body=[func], type_ignores=[]), str(path), "exec"), namespace)
    return namespace[name]


@pytest.mark.parametrize(
    "model,expected",
    [
        ("openai:qwen3-embedding-8b", "IdtaTemplateSpecQwen3Embedding8B"),
        ("openai:text-embedding-3-small", "IdtaTemplateSpecTextEmbedding3Small"),
        ("ollama:bge-m3", "IdtaTemplateSpecBgeM3"),
        ("voyageai:voyage-3", "IdtaTemplateSpecVoyage3"),
    ],
)
def test_slug_is_model_aware(model, expected):
    assert collection_name("IdtaTemplateSpec", model) == expected


def test_reads_embedding_model_from_env(monkeypatch):
    monkeypatch.setenv("EMBEDDING_MODEL", "openai:qwen3-embedding-8b")
    assert collection_name("IdtaTemplateSpec") == "IdtaTemplateSpecQwen3Embedding8B"


@pytest.mark.parametrize("raw", ["", "no-colon"])
def test_missing_or_malformed_model_is_rejected(raw, monkeypatch):
    monkeypatch.setenv("EMBEDDING_MODEL", raw)
    with pytest.raises(ValueError, match="provider:model"):
        collection_name("IdtaTemplateSpec")


def test_unset_model_is_rejected(monkeypatch):
    monkeypatch.delenv("EMBEDDING_MODEL", raising=False)
    with pytest.raises(ValueError, match="provider:model"):
        collection_name("IdtaTemplateSpec")


def test_empty_model_part_is_rejected(monkeypatch):
    monkeypatch.setenv("EMBEDDING_MODEL", "openai:")
    with pytest.raises(ValueError, match="after the colon"):
        collection_name("IdtaTemplateSpec")


def test_base_first_letter_is_upper_cased():
    assert collection_name("aas_documents", "openai:qwen3-embedding-8b") == (
        "Aas_documentsQwen3Embedding8B"
    )


@pytest.mark.parametrize("path", PARITY_HELPERS, ids=lambda p: p.parent.name)
@pytest.mark.parametrize(
    "model",
    ["openai:qwen3-embedding-8b", "openai:text-embedding-3-small", "ollama:bge-m3"],
)
def test_parity_with_existing_implementations(path, model, monkeypatch):
    monkeypatch.setenv("EMBEDDING_MODEL", model)
    existing = load_helper(path, "_get_collection_name")
    assert collection_name("IdtaTemplateSpec") == existing("IdtaTemplateSpec")


@pytest.mark.parametrize("path", PARITY_HELPERS, ids=lambda p: p.parent.name)
def test_parity_on_rejected_models_too(path, monkeypatch):
    monkeypatch.setenv("EMBEDDING_MODEL", "openai:")
    existing = load_helper(path, "_get_collection_name")
    with pytest.raises(ValueError):
        existing("IdtaTemplateSpec")
    with pytest.raises(ValueError):
        collection_name("IdtaTemplateSpec")
