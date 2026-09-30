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
from langgraph.errors import GraphRecursionError


def is_verbose(extra: dict | None) -> bool:
    """Return True when the caller requested verbose streaming."""
    return bool((extra or {}).get("verbose", False))


def stream_error_message(exc: Exception) -> str:
    """Classify a fatal stream-loop exception for the exported error text.

    A bare ``except Exception`` around the astream loop previously collapsed
    every failure — hitting the recursion-limit cap (``GraphRecursionError``,
    a normal agent-behavior outcome) and genuine backend/network failures
    (dropped connections, proxy timeouts, upstream 5xx) — into the identical
    "[stream error]" string, making the two indistinguishable in eval
    exports. This tags them so downstream analysis (`analyze_eval_run.py`,
    eval reports) doesn't have to infer the cause from tool-call-count
    proximity to the cap as a heuristic.
    """
    if isinstance(exc, GraphRecursionError):
        return "\n\n[stream error: recursion-limit — see server logs]\n"
    return "\n\n[stream error: other — see server logs]\n"


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
