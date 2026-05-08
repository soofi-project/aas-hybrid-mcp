"""Custom output parser for Qwen models that output non-JSON format.

Qwen via vLLM + LiteLLM sometimes outputs structured data as plain text
(e.g., bullet lists, XML-like blocks) instead of pure JSON. This parser
tries multiple strategies to extract valid structured output.
"""

import json
import re
from typing import Type, Any

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.outputs import ChatResult
from pydantic import BaseModel, Field

log = __import__("logging").getLogger(__name__)

# Common key-name mismatches between what Qwen produces and what the Pydantic
# models expect.  The parser normalises keys after JSON extraction so the
# downstream Pydantic validation passes.
_KEY_ALIASES = {
    # Plan.step → Plan.steps element
    "step": "id",
    # Reflection aliases
    "dec": "decision",
    # FinalAnswer aliases (if any)
}


def _normalize_keys(obj: Any, *, parent_key: str = "") -> Any:
    """Recursively normalise known key aliases in a parsed JSON object.

    Also converts ``None`` values to ``""`` (empty string) because Qwen
    sometimes omits optional fields.

    Evidence dicts are normalised to Pydantic-compatible form:
    - Already has ``source``/``tool``/``summary`` → keep as-is
    - Has ``type``/``content`` → map to ``{source: <type>, tool: "finalizer", summary: <content>}``
    - Is a plain string → wrap as Evidence dict
    - Other dicts → stringify for ``list[str]`` fields
    """
    _EVIDENCE_KEYS = {"source", "tool", "summary"}
    _EVIDENCE_LIST_KEYS = {"evidence"}

    def _is_evidence_dict(d: dict) -> bool:
        return bool(_EVIDENCE_KEYS & set(d.keys()))

    def _is_type_content_dict(d: dict) -> bool:
        return "type" in d and "content" in d

    def _to_evidence_dict(d: dict) -> dict:
        """Map Qwen's {type, content} → Pydantic's {source, tool, summary}."""
        return {
            "source": d.get("type", "other"),
            "tool": d.get("tool", "finalizer"),
            "summary": d.get("content", str(d)),
        }

    if isinstance(obj, dict):
        # Normalize Qwen's {type, content} → {source, tool, summary}
        if _is_type_content_dict(obj) and not _is_evidence_dict(obj):
            obj = _to_evidence_dict(obj)
        new_dict = {}
        for k, v in obj.items():
            norm_key = _KEY_ALIASES.get(k, k)
            new_dict[norm_key] = _normalize_keys(v, parent_key=norm_key)
        return new_dict
    if isinstance(obj, list):
        # If parent field expects Evidence dicts and items are plain strings,
        # wrap each string as an Evidence dict
        if parent_key in _EVIDENCE_LIST_KEYS and obj and all(isinstance(item, str) for item in obj):
            return [{"source": "other", "tool": "finalizer", "summary": item} for item in obj]
        return [_normalize_keys(item, parent_key=parent_key) for item in obj]
    # Dict that is NOT an evidence dict → stringify for list[str] fields
    if isinstance(obj, dict) and not _is_evidence_dict(obj):
        return str(obj)
    if obj is None:
        return ""
    return obj


def _normalize_json_from_qwen(text: str) -> dict | None:
    """Convenience helper: extract JSON from Qwen output and normalise keys.

    Used by ``agent_plan_nodes.py`` so the fallback path in
    ``_qwen_structured_invoke`` also benefits from key normalisation
    (e.g. Qwen's ``"step"`` → Pydantic's ``"id"``).
    """
    try:
        data = QwenOutputParser.try_parse_json(text)
    except Exception:
        data = None
    if data is not None:
        return _normalize_keys(data)

    md_json = QwenOutputParser.try_parse_markdown_json(text)
    if md_json:
        try:
            return _normalize_keys(json.loads(md_json))
        except (json.JSONDecodeError, TypeError):
            pass

    xml_json = QwenOutputParser.try_parse_qwen_xml(text)
    if xml_json:
        try:
            return _normalize_keys(json.loads(xml_json))
        except (json.JSONDecodeError, TypeError):
            pass

    extracted = QwenOutputParser.try_extract_json_from_text(text)
    if extracted:
        try:
            return _normalize_keys(json.loads(extracted))
        except (json.JSONDecodeError, TypeError):
            pass

    return None


class QwenOutputParser(BaseOutputParser):
    """Output parser that handles multiple Qwen output formats."""

    pydantic_model: Type[BaseModel] = Field(default=None, exclude=True)

    def __init__(self, pydantic_model: Type[BaseModel], **kwargs: Any):
        super().__init__(**kwargs)
        self.pydantic_model = pydantic_model

    @staticmethod
    def try_parse_json(text: str) -> dict | None:
        """Try to parse text as pure JSON (OpenAI format or direct model data)."""
        try:
            data = json.loads(text)
            if isinstance(data, dict) and "tool_calls" in data:
                tool_call = data["tool_calls"][0]
                return tool_call.get("args", {})
            return data
        except (json.JSONDecodeError, TypeError, KeyError, IndexError):
            return None

    @staticmethod
    def try_parse_markdown_json(text: str) -> str | None:
        """Try to extract JSON from Markdown code blocks (```json ... ```)."""
        pattern = r"```(?:json)?\s*\n?(.*?)\n?```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            if content.startswith("{") or content.startswith("["):
                return content
        return None

    @staticmethod
    def try_parse_qwen_xml(text: str) -> str | None:
        """Try to extract JSON from Qwen's XML/Markdown format:
        
        [function=Plan]
        { ... JSON content ... }
        [/function]
        """
        pattern = r"\[function=[^\]]+\](.*?)\[/function\]"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            if "{" in content:
                return content
        return None

    @staticmethod
    def try_extract_json_from_text(text: str) -> str | None:
        """Try to find a JSON object anywhere in the text.
        
        Handles the case where Qwen outputs plain JSON mixed with other text.
        """
        # Find first { and last } in text
        first_brace = text.find("{")
        last_brace = text.rfind("}")
        if first_brace != -1 and last_brace > first_brace:
            candidate = text[first_brace:last_brace + 1]
            try:
                json.loads(candidate)
                return candidate
            except (json.JSONDecodeError, TypeError):
                pass
        return None

    def parse(self, text: str):
        """Parse output text into the pydantic model.
        
        Tries multiple strategies in order:
        1. Pure JSON (OpenAI tool_calls or direct)
        2. JSON inside Markdown code blocks
        3. JSON inside Qwen XML tags
        4. Any JSON object found in text
        """
        log.debug("QwenOutputParser received text (first 300 chars): %s", text[:300])

        # Strategy 1: Pure JSON
        parsed = self.try_parse_json(text)
        if parsed is not None:
            log.debug("Successfully parsed as pure JSON")
            parsed = _normalize_keys(parsed)
            return self.pydantic_model(**parsed)

        # Strategy 2: Markdown JSON
        md_json = self.try_parse_markdown_json(text)
        if md_json:
            try:
                data = json.loads(md_json)
                log.debug("Successfully parsed from Markdown JSON")
                data = _normalize_keys(data)
                return self.pydantic_model(**data)
            except (json.JSONDecodeError, TypeError):
                pass

        # Strategy 3: Qwen XML format
        xml_json = self.try_parse_qwen_xml(text)
        if xml_json:
            try:
                data = json.loads(xml_json)
                log.debug("Successfully parsed from Qwen XML")
                data = _normalize_keys(data)
                return self.pydantic_model(**data)
            except (json.JSONDecodeError, TypeError):
                pass

        # Strategy 4: Extract JSON from anywhere in text
        extracted = self.try_extract_json_from_text(text)
        if extracted:
            try:
                data = json.loads(extracted)
                log.debug("Successfully extracted JSON from text")
                data = _normalize_keys(data)
                return self.pydantic_model(**data)
            except (json.JSONDecodeError, TypeError):
                pass

        # All strategies failed
        log.error("Failed to parse Qwen output. Text: %s", text[:500])
        raise ValueError(
            f"Could not parse model output as structured data. "
            f"Model returned: {text[:200]}..."
        )

    async def aparse(self, text: str):
        """Async version of parse."""
        return self.parse(text)

    def parse_result(self, result: list[ChatResult], *, partial: bool = False):
        """Parse the result from the LLM."""
        if not result:
            raise ValueError("Empty result")
        content = result[0].text
        return self.parse(content)

    async def aparse_result(self, result: list[ChatResult], *, partial: bool = False):
        """Async version of parse_result."""
        return self.parse_result(result, partial=partial)

    @property
    def _type(self) -> str:
        return "qwen_output_parser"
