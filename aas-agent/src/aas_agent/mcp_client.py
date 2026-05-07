"""MCP client — connects to AAS Hybrid MCP server and wraps tools."""

import logging
from contextlib import AsyncExitStack

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

log = logging.getLogger(__name__)


class MCPClientManager:
    """Manages a persistent MCP client session over streamable-http."""

    def __init__(
        self,
        mcp_url: str,
        *,
        inject_manual: bool = True,
        inject_schema: bool = True,
    ) -> None:
        self._url = mcp_url
        self._exit_stack = AsyncExitStack()
        self._session: ClientSession | None = None
        self._context_cache: str | None = None
        self._inject_manual = inject_manual
        self._inject_schema = inject_schema

    async def connect(self) -> None:
        """Establish MCP session (survives across requests via AsyncExitStack)."""
        log.info("Connecting to MCP server at %s", self._url)
        transport = await self._exit_stack.enter_async_context(
            streamablehttp_client(url=self._url)
        )
        read_stream, write_stream = transport[0], transport[1]
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self._session.initialize()
        tools = await self._session.list_tools()
        log.info("MCP connected — %d tools available", len(tools.tools))

    async def disconnect(self) -> None:
        """Close the MCP session."""
        await self._exit_stack.aclose()
        self._session = None
        self._context_cache = None
        log.info("MCP session closed")

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            raise RuntimeError("MCP client not connected — call connect() first")
        return self._session

    async def _call_tool_text(self, name: str) -> str:
        """Invoke a parameterless MCP tool and return its text content."""
        result = await self.session.call_tool(name, arguments={})
        return result.content[0].text

    async def load_context(self) -> str:
        """Pre-fetch the manual index and graph schema for the system prompt.

        Both come from MCP tools (``get_manual_index``, ``get_graph_schema``)
        on the server side; the corresponding ``inject_*`` flags decide
        whether they get baked into the agent's system message at startup.
        With the flags off, the agent has to call those tools itself when
        it needs the content — useful for comparing prompted-context vs.
        tool-driven retrieval.
        """
        if self._context_cache is not None:
            return self._context_cache

        sources: list[tuple[str, str]] = []
        if self._inject_manual:
            sources.append(("get_manual_index", "AAS Hybrid MCP — Manual (auto-injected)"))
        if self._inject_schema:
            sources.append(("get_graph_schema", "AAS Graph Schema (auto-injected)"))

        parts: list[str] = []
        for tool_name, header in sources:
            try:
                content = await self._call_tool_text(tool_name)
                parts.append(f"## {header}\n\n{content}")
            except Exception:
                log.warning("Failed to call tool %s", tool_name, exc_info=True)

        self._context_cache = "\n\n---\n\n".join(parts)
        return self._context_cache

    async def get_langchain_tools(self) -> list[BaseTool]:
        """Load all MCP tools via langchain-mcp-adapters.

        Templates, manual sub-pages, and schema are all exposed as MCP tools
        on the server side, so load_mcp_tools picks them up automatically.
        No client-side resource wrapper needed.
        """
        tools: list[BaseTool] = await load_mcp_tools(self.session)
        log.info("Loaded %d MCP tools via langchain-mcp-adapters", len(tools))
        return tools
