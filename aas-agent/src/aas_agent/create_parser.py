#!/usr/bin/env python3
"""Script to create the QwenOutputParser file."""

parser_code = '''"""Custom output parser for Qwen models that output XML/Markdown format.

Qwen via vLLM + LitellM sometimes outputs structured data in an XML/Markdown
hybrid format instead of pure JSON. This parser handles both:

OpenAI format (expected):
    {"tool_calls": [{"name": "Plan", "args": {"goal": "...", "steps": [...]}}]}

Qwen format (fallback):
    [function=Plan]
    ...
    [/function]
"""

import json
import re
from typing import Generic, TypeVar

from langchain_core.output_parsers import BaseOutputParser
from pydantic import BaseModel

log = __import__("logging").getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class QwenOutputParser(BaseOutputParser, Generic[T]):
    """Output parser that handles both OpenAI and Qwen XML/Markdown formats."""

    pydantic_model: type[T]

    @classmethod
    def is_qwen_format(cls, text: str) -> bool:
        """Check if the output looks like Qwen's XML/Markdown format."""
        return "[function=" in text or "<function=" in text

    @classmethod
    def extract_json_from_qwen(cls, text: str) -> str | None:
        """Extract the JSON content from Qwen's XML/Markdown format."""
        # Try to find content between [function=...] and [/function]
        pattern = r"\\[function=([^\\]]+)\\](.*?)\\[/function\\]"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(2)
        return None

    def parse(self, text: str) -> T:
        """Parse output text into the pydantic model."""
        # First, try to parse as pure JSON (OpenAI format)
        try:
            data = json.loads(text)
            # Check if it's the tool_calls format
            if isinstance(data, dict) and "tool_calls" in data:
                tool_call = data["tool_calls"][0]
                args = tool_call.get("args", {})
                return self.pydantic_model(**args)
            # Or if it's already the model data directly
            return self.pydantic_model(**data)
        except (json.JSONDecodeError, TypeError):
            pass

        # Fallback: try to extract from Qwen format
        extracted = self.extract_json_from_qwen(text)
        if extracted:
            try:
                # Convert the pseudo-XML to valid JSON
                # Replace 