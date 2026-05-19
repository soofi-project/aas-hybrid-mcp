"""HTTP client + SSE parser that drives the AAS agent and extracts metrics."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import Any

import httpx


_VERBOSE_SUFFIX = "-verbose"

# Tool-call block emitted by the agent's verbose stream (see
# aas_agent/agent.py::_format_tool_start / _format_tool_end).
# Opening: "<think>\n**Tool** `<name>`\n\n```json\n<args>\n```"
# Closing: "**Result**\n\n```\n<result>\n```\n</think>"
_TOOL_BLOCK_RE = re.compile(
    r"<think>\s*\*\*Tool\*\*\s*`(?P<name>[^`]+)`\s*"
    r"```json\s*(?P<args>.*?)\s*```\s*"
    r"\*\*Result\*\*\s*```\s*(?P<result>.*?)\s*```\s*</think>",
    re.DOTALL,
)


@dataclass
class ToolCall:
    name: str
    args: dict[str, Any]
    result: str


@dataclass
class TResult:
    """Outcome of a single agent run."""

    query: str
    variant: str
    model_id: str
    response: str = ""
    duration_s: float = 0.0
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    raw_stream: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "variant": self.variant,
            "model_id": self.model_id,
            "response": self.response,
            "final_answer": extract_final_answer(self.raw_stream) if self.raw_stream else (self.response or ""),
            "duration_s": round(self.duration_s, 3),
            "tool_calls": [
                {"name": t.name, "args": t.args, "result_preview": t.result[:200]}
                for t in self.tool_calls
            ],
            "tool_call_count": len(self.tool_calls),
            "usage": self.usage,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "TResult":
        tool_calls = [
            ToolCall(name=t["name"], args=t.get("args", {}), result=t.get("result_preview", ""))
            for t in d.get("tool_calls", [])
        ]
        obj = cls(
            query=d["query"],
            variant=d["variant"],
            model_id=d["model_id"],
            response=d.get("response", ""),
            duration_s=d.get("duration_s", 0.0),
            tool_calls=tool_calls,
            usage=d.get("usage", {}),
            error=d.get("error"),
        )
        # Restore raw_stream from final_answer so LLMJudge.grade() works correctly.
        # extract_final_answer() on a string without </think> blocks returns it unchanged.
        obj.raw_stream = d.get("final_answer", d.get("response", ""))
        return obj


class AgentTester:
    """Async HTTP client that runs queries against the agent's /v1/chat/completions endpoint."""

    def __init__(self, agent_url: str, timeout_s: float = 300.0) -> None:
        self._base = agent_url.rstrip("/")
        self._timeout = timeout_s

    async def run_query(
        self,
        query: str,
        model_id: str,
        *,
        system_prompt: str | None = None,
    ) -> TResult:
        """Run *query* against *model_id* (verbose suffix is added automatically).

        Streams the response, accumulates content + usage, parses tool calls
        from <think> blocks. Returns a TResult.
        """
        variant = model_id.split(":", 1)[-1] if ":" in model_id else model_id
        verbose_model = (
            model_id if model_id.endswith(_VERBOSE_SUFFIX) else model_id + _VERBOSE_SUFFIX
        )

        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})

        payload = {
            "model": verbose_model,
            "messages": messages,
            "stream": True,
        }

        start = time.perf_counter()
        result = TResult(
            query=query,
            variant=variant,
            model_id=model_id,
        )

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self._base}/v1/chat/completions",
                    json=payload,
                ) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        body = line[len("data: "):]
                        if body == "[DONE]":
                            break
                        try:
                            chunk = json.loads(body)
                        except json.JSONDecodeError:
                            continue
                        _accumulate_chunk(chunk, result)
        except httpx.HTTPError as e:
            result.error = f"HTTP error: {e!r}"
        except Exception as e:  # noqa: BLE001 — surface everything to the result
            result.error = f"Unexpected error: {e!r}"
        finally:
            result.duration_s = time.perf_counter() - start

        if result.raw_stream and not result.error:
            result.tool_calls = _parse_tool_calls(result.raw_stream)
            result.response = _strip_think_blocks(result.raw_stream).strip()

        return result


def _accumulate_chunk(chunk: dict[str, Any], result: TResult) -> None:
    """Append delta content to result.raw_stream; capture usage when present."""
    choices = chunk.get("choices") or []
    for ch in choices:
        delta = ch.get("delta") or {}
        content = delta.get("content")
        if isinstance(content, str):
            result.raw_stream += content
    usage = chunk.get("usage")
    if isinstance(usage, dict):
        result.usage = usage


def _parse_tool_calls(stream: str) -> list[ToolCall]:
    calls: list[ToolCall] = []
    for m in _TOOL_BLOCK_RE.finditer(stream):
        name = m.group("name")
        args_raw = m.group("args")
        result = m.group("result")
        try:
            args = json.loads(args_raw)
        except json.JSONDecodeError:
            args = {"_raw": args_raw}
        calls.append(ToolCall(name=name, args=args, result=result))
    return calls


def _strip_think_blocks(stream: str) -> str:
    """Remove all <think>...</think> sections so only the final answer remains."""
    return re.sub(r"<think>.*?</think>", "", stream, flags=re.DOTALL)


def extract_final_answer(stream: str) -> str:
    """Return only the text after the last </think> block.

    Used by the LLM judge to avoid evaluating reasoning text — only the
    agent's actual final answer is relevant for grading.
    """
    last = stream.rfind("</think>")
    if last == -1:
        return stream
    return stream[last + len("</think>"):].strip()
