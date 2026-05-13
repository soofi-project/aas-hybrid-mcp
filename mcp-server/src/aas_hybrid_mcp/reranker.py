"""Two-phase retrieval reranker — Cohere-compatible /rerank over httpx.

`RERANKER_MODE=distance` (default): no reranker, score = 1 - vector distance.
`RERANKER_MODE=vllm`: real reranker (Qwen3-Reranker-4b on H200 via vLLM).
    Requires `RERANKER_URL` + `RERANKER_CANDIDATE_LIMIT`.

Ported from soofi-trainer/vector-mcp/src/vector_mcp/server.py:60-126.
"""

import logging
import os
import time
from typing import Any

import httpx

log = logging.getLogger(__name__)

RERANKER_MODE: str = os.getenv("RERANKER_MODE", "").lower()
RERANKER_URL: str = ""
RERANKER_CANDIDATE_LIMIT: int = 0
RERANKER_MODEL: str = os.getenv("RERANKER_MODEL", "qwen3-reranker-4b")

if RERANKER_MODE == "vllm":
    RERANKER_URL = os.getenv("RERANKER_URL", "")
    if not RERANKER_URL:
        raise RuntimeError("RERANKER_URL env var required when RERANKER_MODE=vllm")
    _candidate_limit = os.getenv("RERANKER_CANDIDATE_LIMIT", "")
    if not _candidate_limit:
        raise RuntimeError("RERANKER_CANDIDATE_LIMIT env var required when RERANKER_MODE=vllm")
    RERANKER_CANDIDATE_LIMIT = int(_candidate_limit)
    log.info(
        "Reranker: vllm mode, url=%s candidate_limit=%d model=%s",
        RERANKER_URL, RERANKER_CANDIDATE_LIMIT, RERANKER_MODEL,
    )
elif RERANKER_MODE == "distance":
    log.info("Reranker: distance mode (score = 1 - vector distance)")
else:
    raise RuntimeError(
        f"RERANKER_MODE must be 'distance' or 'vllm', got: {RERANKER_MODE!r}"
    )

_client: httpx.Client | None = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(base_url=RERANKER_URL, timeout=5.0)
    return _client


def rerank(query: str, texts: list[str]) -> list[dict[str, Any]] | None:
    """Call vLLM reranker. Returns sorted [{"index": int, "score": float}] or None on failure."""
    if not texts:
        return []
    log.info("Reranking %d candidates for query=%r", len(texts), query[:80])
    try:
        t0 = time.perf_counter()
        resp = _get_client().post(
            "/rerank",
            json={"model": RERANKER_MODEL, "query": query, "documents": texts},
        )
        resp.raise_for_status()
        elapsed_ms = (time.perf_counter() - t0) * 1000
        results = resp.json()["results"]
        ranked = [
            {"index": r["index"], "score": r["relevance_score"]}
            for r in results
        ]
        if not ranked:
            log.warning("Reranker returned empty results")
            return []
        log.info(
            "Reranking done in %.0fms: top score=%.4f, bottom score=%.4f",
            elapsed_ms, ranked[0]["score"], ranked[-1]["score"],
        )
        return ranked
    except Exception:
        log.warning("Reranker unavailable, falling back to vector-only ranking", exc_info=True)
        return None


def close() -> None:
    """Close the httpx client connection."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
