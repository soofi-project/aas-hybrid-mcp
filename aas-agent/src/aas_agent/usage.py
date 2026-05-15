"""Token-usage accumulation for the LangGraph agent variants.

Every ``ChatOpenAI`` call reports its prompt / completion / total token
counts via ``AIMessage.usage_metadata`` (returned by ``ainvoke``) and the
``on_chat_model_end`` event in ``astream_events``. Variants with multiple
LLM calls per turn (plan/reflect, CRAG, reflexion) just sum across all
calls — no per-node split, since the API response and the interaction
log only need the per-turn total.

For streaming, vLLM (and OpenAI) only emit usage when the request asks
for it via ``stream_options.include_usage=true`` — every ``ChatOpenAI``
in the runners therefore sets ``stream_usage=True``.
"""

from __future__ import annotations

import json
from typing import Iterable

# Sentinel prefix runners use to channel the accumulated usage dict
# through the ``AsyncIterator[str]`` stream interface back to
# ``api._stream_sse``. The SSE layer filters and converts it into an
# OpenAI-style ``usage`` chunk before ``[DONE]``.
USAGE_SENTINEL = "__usage__:"


def empty_usage() -> dict:
    return {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}


def add_usage(acc: dict, meta: dict | None) -> None:
    """Fold a ``usage_metadata`` dict into the accumulator (in place)."""
    if not meta:
        return
    try:
        acc["input_tokens"] += int(meta.get("input_tokens", 0) or 0)
        acc["output_tokens"] += int(meta.get("output_tokens", 0) or 0)
        acc["total_tokens"] += int(meta.get("total_tokens", 0) or 0)
    except (TypeError, ValueError):
        return


def accumulate_from_event(event: dict, acc: dict) -> bool:
    """Sum ``on_chat_model_end`` usage into *acc*.

    Returns ``True`` when the event was a chat-model-end so the caller can
    short-circuit other event branches.
    """
    if event.get("event") != "on_chat_model_end":
        return False
    data = event.get("data") or {}
    output = data.get("output")
    meta = getattr(output, "usage_metadata", None)
    if meta is None and isinstance(output, dict):
        meta = output.get("usage_metadata")
    add_usage(acc, meta)
    return True


def accumulate_from_messages(messages: Iterable, acc: dict) -> None:
    """Walk an iterable of LangChain messages and sum ``usage_metadata``."""
    for msg in messages:
        meta = getattr(msg, "usage_metadata", None)
        if meta:
            add_usage(acc, meta)


def usage_to_openai(u: dict) -> dict:
    """Map our internal usage dict to the OpenAI ``usage`` field schema."""
    return {
        "prompt_tokens": int(u.get("input_tokens", 0) or 0),
        "completion_tokens": int(u.get("output_tokens", 0) or 0),
        "total_tokens": int(u.get("total_tokens", 0) or 0),
    }


def encode_usage_sentinel(u: dict) -> str:
    return f"{USAGE_SENTINEL}{json.dumps(u, separators=(',', ':'))}"


def try_decode_usage_sentinel(token: str) -> dict | None:
    if not isinstance(token, str) or not token.startswith(USAGE_SENTINEL):
        return None
    try:
        decoded = json.loads(token[len(USAGE_SENTINEL):])
    except (ValueError, TypeError):
        return None
    if not isinstance(decoded, dict):
        return None
    return decoded
