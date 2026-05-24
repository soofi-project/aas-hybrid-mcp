"""LLM-based query rewriting for scoped technical documentation search.

Adapted from Ma et al. (2023) "Query Rewriting for Retrieval-Augmented Large
Language Models" (EMNLP 2023). Our scoped variant strips asset-name references
when `submodel_id` filters the search already.

`QUERY_REWRITE_MODE=off`: no rewrite, returns original query.
`QUERY_REWRITE_MODE=on`: LLM expands query with synonyms / domain terminology.
"""

import logging
import os
import time

import httpx

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config (all required, no defaults)
# ---------------------------------------------------------------------------

QUERY_REWRITE_MODE: str = os.environ.get("QUERY_REWRITE_MODE", "").lower()
QUERY_REWRITE_URL: str = os.environ.get("QUERY_REWRITE_URL", "")
QUERY_REWRITE_MODEL: str = os.environ.get("QUERY_REWRITE_MODEL", "")
QUERY_REWRITE_TIMEOUT: int = int(os.environ.get("QUERY_REWRITE_TIMEOUT", "30"))

if QUERY_REWRITE_MODE not in ("on", "off"):
    raise RuntimeError(
        f"QUERY_REWRITE_MODE must be 'on' or 'off', got: {QUERY_REWRITE_MODE!r}"
    )
if QUERY_REWRITE_MODE == "off":
    if QUERY_REWRITE_URL or QUERY_REWRITE_MODEL:
        log.debug("Query rewriter disabled (mode=off)")
else:
    if not QUERY_REWRITE_URL:
        raise RuntimeError("QUERY_REWRITE_URL required when QUERY_REWRITE_MODE=on")
    if not QUERY_REWRITE_MODEL:
        raise RuntimeError("QUERY_REWRITE_MODEL required when QUERY_REWRITE_MODE=on")
    log.info(
        "Query rewriter: url=%s model=%s timeout=%ds",
        QUERY_REWRITE_URL, QUERY_REWRITE_MODEL, QUERY_REWRITE_TIMEOUT,
    )

# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

_client: httpx.Client | None = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        headers = {}
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        _client = httpx.Client(
            base_url=QUERY_REWRITE_URL,
            timeout=QUERY_REWRITE_TIMEOUT,
            headers=headers,
        )
    return _client


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a query rewriting engine for technical documentation search. \
Expand the user's query with technical synonyms, domain terminology, and \
alternative phrasings that match industrial equipment manuals.

Examples:
  "max speed" -> "maximum speed velocity performance limit"
  "how heavy can it lift" -> "payload capacity weight limit lifting specification"
  "error on display" -> "fault error code display alarm diagnostic troubleshooting"
  "where to find the serial number" -> "serial number type rating plate identification label location"

{scope_block}

Focus on technical terms an equipment manual would use. Expand informal \
worker phrasing into datasheet vocabulary.

Output only the rewritten query, nothing else.\
""".lstrip()


def _build_system_prompt(*, asset_name: str | None, doc_language: str | None) -> str:
    parts = []
    if asset_name:
        parts.append(
            f'The user is searching within the manual for "{asset_name}". This '
            "asset name is already covered by the document filter. Do NOT "
            f'include "{asset_name}" or any variant of it in the rewritten '
            "query — the search is already scoped to this asset's documentation. "
            "Focus on the technical intent and vocabulary expansion instead."
        )
    if doc_language:
        parts.append(
            f"The documentation is in {doc_language}. Rewrite the query in "
            f"{doc_language}."
        )
    scope_block = ("\n\n" + "\n".join(parts) + "\n") if parts else ""
    return SYSTEM_PROMPT.format(scope_block=scope_block)


# ---------------------------------------------------------------------------
# Rewrite
# ---------------------------------------------------------------------------


def rewrite(
    query: str,
    *,
    asset_name: str | None = None,
    submodel_id: str | None = None,
    doc_language: str | None = None,
) -> str:
    """Rewrite a user query with technical synonyms.

    Returns the rewritten query string, or the original query on failure.
    """
    if QUERY_REWRITE_MODE != "on":
        return query

    system = _build_system_prompt(asset_name=asset_name, doc_language=doc_language)

    try:
        t0 = time.perf_counter()
        resp = _get_client().post(
            "/chat/completions",
            json={
                "model": QUERY_REWRITE_MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": query},
                ],
            },
        )
        resp.raise_for_status()
        elapsed_ms = (time.perf_counter() - t0) * 1000
        rewritten = resp.json()["choices"][0]["message"]["content"].strip()
        log.info(
            "Query rewritten in %.0fms: %r -> %r",
            elapsed_ms, query[:80], rewritten[:80],
        )
        return rewritten
    except Exception:
        log.warning("Query rewriter unavailable, using original query", exc_info=True)
        return query


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------


def close() -> None:
    """Close the httpx client connection."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
