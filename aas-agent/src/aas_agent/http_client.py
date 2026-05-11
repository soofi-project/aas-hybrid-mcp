"""Shared httpx client factory — prevents vLLM streaming TransferEncodingError.

LangChain's ChatOpenAI uses both sync and async openai clients.  When a
custom ``httpx.Client`` or ``httpx.AsyncClient`` is passed, the underlying
openai SDK inherits its timeout / keep-alive policy.  With vLLM's SSE
engine, the defaults are too aggressive and mid-stream disconnects
(``TransferEncodingError``) occur on longer ReAct loops.
"""

import httpx

# Per-connection idle timeout long enough for multi-step ReAct loops.
_DEFAULT_TIMEOUT = 120  # seconds
_MAX_KEEP_ALIVE_CONNECTIONS = 10
_MAX_KEEP_ALIVE_EXPIRE = 5


def _build_http_client() -> httpx.Client:
    """Return a *sync* ``httpx.Client`` for ``ChatOpenAI(http_client=…)``."""
    return httpx.Client(
        timeout=_DEFAULT_TIMEOUT,
        limits=httpx.Limits(
            max_connections=_MAX_KEEP_ALIVE_CONNECTIONS,
            max_keepalive_connections=_MAX_KEEP_ALIVE_CONNECTIONS,
            keepalive_expiry=_MAX_KEEP_ALIVE_EXPIRE,
        ),
    )


def _build_http_async_client() -> httpx.AsyncClient:
    """Return an *async* ``httpx.AsyncClient`` for ``ChatOpenAI(http_async_client=…)``."""
    return httpx.AsyncClient(
        timeout=_DEFAULT_TIMEOUT,
        limits=httpx.Limits(
            max_connections=_MAX_KEEP_ALIVE_CONNECTIONS,
            max_keepalive_connections=_MAX_KEEP_ALIVE_CONNECTIONS,
            keepalive_expiry=_MAX_KEEP_ALIVE_EXPIRE,
        ),
    )
