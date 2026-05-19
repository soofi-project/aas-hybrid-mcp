"""Shared helpers for verbose / non-verbose streaming across agent variants.

All three runners (react / plan-reflect / reflexion) implement the same
contract on top of an OpenAI-compatible streaming endpoint:

- **Non-verbose**: a single yield carrying the final answer text.
- **Verbose**: ``<think>`` blocks for tool I/O, node transitions, and any
  variant-specific reasoning artefacts.

This module centralises the gate check, final-answer extraction, and the
node-transition formatter so each runner only plugs in its own node-name
set.
"""

from __future__ import annotations

from typing import Iterable

from langchain_core.messages import AIMessage


def is_verbose(extra: dict | None) -> bool:
    """Return True when the caller requested verbose streaming."""
    return bool((extra or {}).get("verbose", False))


def extract_final_text(result: dict) -> str:
    """Return the last non-empty ``AIMessage.content`` from a graph result.

    Walks ``result['messages']`` in reverse and returns the stripped text of
    the most recent AI message. Returns an empty string if none is found.
    """
    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage):
            content = getattr(msg, "content", None)
            if isinstance(content, str) and content.strip():
                return content.strip()
        else:
            content = getattr(msg, "content", None)
            if isinstance(content, str) and content.strip():
                return content.strip()
    return ""


def node_transition_block(event: dict, allowed: Iterable[str]) -> str | None:
    """Render a top-level node entry as a foldable ``<think>`` block.

    Returns the formatted block when ``event`` is an ``on_chain_start`` for a
    langgraph node listed in ``allowed``; otherwise returns ``None``.

    The metadata check (``langgraph_node == name``) guards against inner
    LCEL chains that happen to share a name with a graph node.
    """
    if event.get("event") != "on_chain_start":
        return None
    name = event.get("name", "")
    if name not in allowed:
        return None
    metadata = event.get("metadata") or {}
    if metadata.get("langgraph_node") != name:
        return None
    return f"\n\n<think>\n**Node**: `{name}`\n</think>\n\n"
