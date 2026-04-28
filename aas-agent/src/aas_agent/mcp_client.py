"""MCP client — connects to AAS Hybrid MCP server, reads resources, wraps tools."""

import json
import logging
from contextlib import AsyncExitStack
from typing import Any

from langchain_core.tools import StructuredTool
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from pydantic import BaseModel, Field, create_model

log = logging.getLogger(__name__)

_JSON_TYPE_MAP: dict[str, type] = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
}


def _build_args_model(tool_name: str, schema: dict[str, Any]) -> type[BaseModel]:
    """Build a Pydantic model from a JSON Schema properties dict."""
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    fields: dict[str, Any] = {}
    for name, prop in properties.items():
        # Handle type arrays like ["string", "null"]
        raw_type = prop.get("type", "string")
        if isinstance(raw_type, list):
            raw_type = next((t for t in raw_type if t != "null"), "string")
        py_type = _JSON_TYPE_MAP.get(raw_type, str)
        description = prop.get("description", "")
        if name in required:
            fields[name] = (py_type, Field(description=description))
        else:
            fields[name] = (py_type | None, Field(default=None, description=description))
    return create_model(f"{tool_name}_Args", **fields)


class MCPClientManager:
    """Manages a persistent MCP client session over streamable-http."""

    def __init__(self, mcp_url: str) -> None:
        self._url = mcp_url
        self._exit_stack = AsyncExitStack()
        self._session: ClientSession | None = None
        self._context_cache: str | None = None

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

    async def read_resource(self, uri: str) -> str:
        """Read a single MCP resource by URI."""
        result = await self.session.read_resource(uri)
        return result.contents[0].text

    async def load_context(self) -> str:
        """Read graph schema + template index; cache for reuse."""
        if self._context_cache is not None:
            return self._context_cache

        parts: list[str] = []

        try:
            schema = await self.read_resource("aas://schema/graph")
            parts.append("## AAS Graph Schema (auto-injected)\n\n" + schema)
        except Exception:
            log.warning("Failed to load graph schema resource", exc_info=True)

        try:
            index = await self.read_resource("aas://templates/index")
            parts.append("## IDTA Submodel Template Index (auto-injected)\n\n" + index)
        except Exception:
            log.warning("Failed to load template index resource", exc_info=True)

        self._context_cache = "\n\n---\n\n".join(parts) if parts else ""
        return self._context_cache

    def _make_tool_caller(self, tool_name: str):
        """Create an async function that calls an MCP tool."""
        session_ref = self  # capture reference for reconnect support

        async def _call(**kwargs: Any) -> str:
            # Remove None values (optional params not provided)
            args = {k: v for k, v in kwargs.items() if v is not None}
            result = await session_ref.session.call_tool(tool_name, args)
            texts = [c.text for c in result.content if hasattr(c, "text")]
            return "\n".join(texts) if texts else json.dumps({"result": "empty"})

        return _call

    async def get_langchain_tools(self) -> list[StructuredTool]:
        """Convert MCP tools to LangChain StructuredTool objects."""
        result = await self.session.list_tools()
        tools: list[StructuredTool] = []

        for tool_info in result.tools:
            args_model = _build_args_model(tool_info.name, tool_info.inputSchema)
            caller = self._make_tool_caller(tool_info.name)

            lc_tool = StructuredTool.from_function(
                coroutine=caller,
                name=tool_info.name,
                description=tool_info.description or "",
                args_schema=args_model,
            )
            tools.append(lc_tool)
            log.info("Registered MCP tool: %s", tool_info.name)

        return tools
