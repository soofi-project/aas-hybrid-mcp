"""Smoke test for structured LLM calls (plain ``ainvoke`` + JSON parse).

Run inside the aas-agent container (or any environment with the same
``LLM_BASE_URL`` / ``LLM_MODEL`` / ``OPENAI_API_KEY``)::

    docker compose exec aas-agent python -m aas_agent._smoke_structured

Verifies that the planner-, reflector-, and finalizer-style structured
calls return a valid Pydantic instance. If this fails the plan/reflect
agent variant will not work — the real graph relies on the same code path.
"""

import asyncio
import json
import os
import sys
from typing import Type

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import BaseOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from aas_agent.agent_plan_state import FinalAnswer, Plan, Reflection

log = __import__("logging").getLogger(__name__)


def _parse_response(llm: ChatOpenAI, schema: Type[BaseModel], messages: list) -> BaseModel:
    """Call the LLM and parse the JSON output into a Pydantic model.

    Mirrors the approach used in ``_qwen_structured_invoke`` so the
    smoke test validates the exact same code path.
    """
    response = asyncio.get_event_loop().run_until_complete(llm.ainvoke(messages))

    content = response.content
    if isinstance(content, list):
        content = content[0].text if content else ""
    if not content or not isinstance(content, str):
        raise ValueError(f"Expected string content from LLM, got {type(content)}")

    class SimpleParser(BaseOutputParser):
        def __init__(self, schema):
            self._schema = schema
        def parse(self, text):
            from aas_agent.qwen_parser import QwenOutputParser
            return QwenOutputParser(pydantic_model=self._schema).parse(text)
        def parse_result(self, result, *, partial=False):
            return self.parse(result[0].text)

    parser = SimpleParser(schema)
    try:
        return parser.parse(content)
    except ValueError:
        # Retry with reasoning tags stripped
        stripped = __import__("re").sub(r"<think[^>]*>.*?</think>", "", content, flags=__import__("re").DOTALL).strip()
        # Try raw JSON
        try:
            data = json.loads(stripped)
            return schema(**data)
        except (json.JSONDecodeError, TypeError):
            pass
        # Try extract
        first, last = stripped.find("{"), stripped.rfind("}")
        if first != -1 and last > first:
            data = json.loads(stripped[first:last + 1])
            return schema(**data)
        raise


async def _run_one(llm: ChatOpenAI, schema, label: str, user_prompt: str) -> bool:
    try:
        result = _parse_response(llm, schema, [
            SystemMessage(content=f"You are smoke-testing the {label} schema."),
            HumanMessage(content=user_prompt),
        ])
        print(f"[OK] {label}: {type(result).__name__}")
        print(f"     {result.model_dump_json()[:300]}")
        return True
    except Exception as exc:
        print(f"[FAIL] {label}: {exc!r}")
        return False


async def main() -> int:
    base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("LLM_MODEL", "gpt-4o")
    print(f"LLM: {base_url}  model={model}")

    model_kwargs: dict = {}
    if "openai.com" not in base_url:
        model_kwargs["extra_body"] = {"chat_template_kwargs": {"enable_thinking": False}}
    llm = ChatOpenAI(base_url=base_url, model=model, model_kwargs=model_kwargs)

    cases = [
        (
            Plan,
            "Plan",
            "Plan how to find the AAS-ID of 'the UR3e in hall 4' using a graph "
            "query. Produce 1-2 steps. Output ONLY a JSON object.",
        ),
        (
            Reflection,
            "Reflection",
            "Step intent was 'find AAS-ID of UR3e in hall 4'. Tool query_aas_graph "
            "returned []. Decide whether to retry, replan, or give up. Output ONLY a JSON object.",
        ),
        (
            FinalAnswer,
            "FinalAnswer",
            "User asked 'where is the UR3e?'. Evidence: graph returned UR3e_001 in "
            "hall 4. Confidence high. Synthesize the FinalAnswer. Output ONLY a JSON object.",
        ),
    ]
    ok = True
    for schema, label, prompt in cases:
        ok &= await _run_one(llm, schema, label, prompt)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
