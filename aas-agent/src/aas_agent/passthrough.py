"""Passthrough runner — zero-pattern baseline.

Single LLM call per request, no LangGraph, no tools, no recursion.
System prompt (manual + schema) is injected for grounding. Implements
the same interface as the other runners so that ``api.py`` can route to it.

Used by model ID ``aas:null`` as the "raw LLM" baseline for paper eval.
"""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncIterator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from aas_agent.trace import ConversationLogger

log = logging.getLogger(__name__)


class PassthroughRunner:
    """Zero-pattern baseline — single LLM call with context, no tools, no graph."""

    def __init__(
        self,
        base_system: str,
        llm_base_url: str,
        llm_model: str,
        log_dir: Path | None = None,
    ) -> None:
        self._system_prompt = base_system
        self._llm_base_url = llm_base_url
        self._llm_model = llm_model
        self._log_dir = log_dir
        self._llm: ChatOpenAI | None = None
        self._initialized = False

    @property
    def model_name(self) -> str:
        return self._llm_model

    def _build_llm(self) -> ChatOpenAI:
        """Construct a bare ChatOpenAI (no tools, no streaming for invoke)."""
        extra_body = None
        if self._llm_base_url and "openai.com" not in self._llm_base_url:
            # vLLM — keep thinking off for baseline parity
            extra_body = {"chat_template_kwargs": {"enable_thinking": False}}

        return ChatOpenAI(
            base_url=self._llm_base_url,
            model=self._llm_model,
            streaming=True,
            extra_body=extra_body,
        )

    async def initialize(self) -> None:
        """No resources to load — just construct the LLM."""
        self._llm = self._build_llm()
        self._initialized = True
        log.info(
            "Passthrough agent initialized — %s, system context: %d chars",
            self._llm_model, len(self._system_prompt),
        )

    def _to_langchain_messages(self, messages: list[dict]) -> list:
        lc: list = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                continue
            elif role == "assistant":
                lc.append(AIMessage(content=content))
            else:
                lc.append(HumanMessage(content=content))
        return lc

    async def direct_invoke(self, messages: list[dict]) -> str:
        """Bypass — direct LLM call."""
        if self._llm is None:
            raise RuntimeError("Passthrough agent not initialized")
        lc = self._to_langchain_messages(messages)
        lc_with_system = [SystemMessage(content=self._system_prompt)] + lc
        result = await self._llm.ainvoke(lc_with_system)
        return result.content if isinstance(result.content, str) else str(result.content)

    async def stream(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
        conversation_id: str = "",
        chat_id: str | None = None,
        extra: dict | None = None,
    ) -> AsyncIterator[str]:
        """Stream tokens from a single LLM call (no graph)."""
        if self._llm is None:
            raise RuntimeError("Passthrough agent not initialized")

        lc = self._to_langchain_messages(messages)
        lc_with_system = [SystemMessage(content=self._system_prompt)] + lc
        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)

        try:
            async for chunk in self._llm.astream(lc_with_system):
                content = getattr(chunk, "content", None)
                if isinstance(content, str) and content:
                    trace.append(content)
                    yield content
        except Exception:
            log.exception("Fatal error in passthrough stream")
            err = "\n\n[stream error — see server logs]\n"
            yield err
            trace.append(err)
        finally:
            trace.flush()

    async def invoke(
        self,
        messages: list[dict],
        reasoning_effort: str | None = None,
        conversation_id: str = "",
        chat_id: str | None = None,
        extra: dict | None = None,
    ) -> str:
        """Non-streaming — single LLM call."""
        if self._llm is None:
            raise RuntimeError("Passthrough agent not initialized")

        lc = self._to_langchain_messages(messages)
        lc_with_system = [SystemMessage(content=self._system_prompt)] + lc
        result = await self._llm.ainvoke(lc_with_system)

        response = ""
        content = result.content
        response = content if isinstance(content, str) else str(content)

        trace = ConversationLogger(self._log_dir, conversation_id or "unknown", chat_id=chat_id)
        trace.write_header(messages, self._llm_model, extra=extra)
        trace.append(response)
        trace.flush()
        return response


__all__ = ["PassthroughRunner"]
