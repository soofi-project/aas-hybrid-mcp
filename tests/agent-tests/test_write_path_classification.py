"""Regression for fence-robust write-path classification.

Standalone script (the repo has no pytest/CI; see AGENTS.md). Run from
tests/agent-tests/ so the ``framework`` package import resolves, exactly like
run_tests.py / reclassify_write_path.py:

    cd tests/agent-tests && python test_write_path_classification.py

Guards the bug fixed by the success-signal evaluator. Tool results are
reconstructed by a regex over the agent's rendered stream
(runner._parse_tool_calls). When results embed code fences (```), as
get_graph_schema / get_manual_page / get_template emit, that regex mis-binds
result blocks: a foreign Cypher/validator error can land on a put_submodel call
whose write actually succeeded. The OLD error-substring heuristic then marked the
run as a failed write ("surfaced"). The NEW evaluator detects the BaSyx success
token across the joined result blob, independent of the (unreliable) per-call
binding, so it stays correct.

The test reproduces the post-parse misbound state directly (independent of how
the regex got there) and asserts the OLD heuristic misfires while the NEW one is
correct on identical input. Exits non-zero on any assertion failure.
"""

from __future__ import annotations

import sys

from framework.evaluator import _analyse_write_path
from framework.runner import ToolCall, TResult, _parse_tool_calls

sys.stdout.reconfigure(encoding="utf-8")

BT = "```"  # avoid embedding a literal fence run in this module's own docstring


def _old_classify(result: TResult) -> tuple[str | None, bool]:
    """Replica of the pre-fix error-substring heuristic, for discrimination.

    Mirrors the old framework/evaluator._analyse_write_path logic so the test can
    prove old-vs-new behaviour diverges on identical input. The old code had no
    ``wrote`` field, so we derive an equivalent "write succeeded" boolean as
    "put_submodel attempted and not flagged as error" (its implicit success).
    """
    write_tools = {"put_submodel", "put_submodel_element"}
    relevant = [(i, tc) for i, tc in enumerate(result.tool_calls) if tc.name in write_tools]
    if not relevant:
        return None, False
    ps_attempted = False
    ps_error = False
    for _, tc in relevant:
        if tc.name != "put_submodel":
            continue
        ps_attempted = True
        rt = (tc.result or "").lower()
        if "error" in rt or "failed" in rt or "validation" in rt:
            ps_error = True
    pse = any(tc.name == "put_submodel_element" for _, tc in relevant)
    if not ps_attempted and pse:
        return "direct", True
    if ps_attempted and ps_error and pse:
        return "cascade", False
    if ps_attempted and not pse:
        return ("surfaced", False) if ps_error else ("correct", True)
    return None, ps_attempted and not ps_error


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def test_misbound_success_is_not_surfaced() -> None:
    """Fence breakage mis-binds results: success token on one call, a foreign
    error string on the put_submodel call. The write really succeeded.

    OLD heuristic: put_submodel.result holds 'error'/'validation' → surfaced.
    NEW heuristic: BaSyx success token in the joined blob → wrote=True, correct.
    """
    tcs = [
        # Success signal mis-landed on a read tool's result block.
        ToolCall(
            name="get_graph_schema",
            args={},
            result='{"status":"ok","id":"https://example.com/sm/Created"}',
        ),
        # Foreign validator error mis-landed on the (actually successful) write.
        ToolCall(
            name="put_submodel",
            args={"submodel": {"idShort": "X"}},
            result="forbidden_pattern: validation failed on a prior query",
        ),
    ]
    result = TResult(query="q", variant="react", model_id="m")
    result.tool_calls = tcs

    old_bt, old_wrote = _old_classify(result)
    if old_bt != "surfaced" or old_wrote:
        _fail(f"expected OLD heuristic to misfire as surfaced, got {old_bt!r} wrote={old_wrote}")

    wp = _analyse_write_path(result)
    if wp is None:
        _fail("write-path analysis returned None despite put_submodel call")
    if not wp.wrote:
        _fail(f"expected NEW wrote=True (blob success signal), got {wp.wrote}")
    if wp.bypass_type == "surfaced":
        _fail("NEW evaluator still misclassifies as surfaced")
    if wp.bypass_type not in (None, "correct"):
        _fail(f"expected bypass_type in {{None, 'correct'}}, got {wp.bypass_type!r}")
    print(f"OK  misbound success: OLD={old_bt!r} -> NEW wrote={wp.wrote} bypass={wp.bypass_type!r}")


def test_genuine_failure_is_surfaced() -> None:
    """put_submodel really failed (no success token, no element fallback)."""
    result = TResult(query="q", variant="react", model_id="m")
    result.tool_calls = [
        ToolCall(
            name="put_submodel",
            args={"submodel": {"idShort": "X"}},
            result='{"error": "validation failed: missing semanticId"}',
        )
    ]
    wp = _analyse_write_path(result)
    if wp is None:
        _fail("write-path analysis returned None despite put_submodel call")
    if wp.wrote:
        _fail("expected wrote=False for genuine failure")
    if wp.bypass_type != "surfaced":
        _fail(f"expected bypass_type 'surfaced', got {wp.bypass_type!r}")
    print(f"OK  genuine failure: wrote={wp.wrote} bypass={wp.bypass_type!r}")


def test_parser_preserves_names_and_order() -> None:
    """Sanity: _parse_tool_calls keeps tool names + order even with an embedded
    fence in a result block (the property the success-signal logic relies on)."""
    schema_result = (
        "Cypher example:\n"
        f"{BT}cypher\nMATCH (n:AssetAdministrationShell) RETURN n LIMIT 1\n{BT}\n"
        "end of schema"
    )
    stream = (
        f"<think>**Tool** `get_graph_schema`\n\n{BT}json\n{{}}\n{BT}\n\n"
        f"**Result**\n\n{BT}\n{schema_result}\n{BT}\n</think>\n"
        f"<think>**Tool** `put_submodel`\n\n{BT}json\n{{\"submodel\": {{}}}}\n{BT}\n\n"
        f"**Result**\n\n{BT}\n{{\"status\":\"ok\",\"id\":\"x\"}}\n{BT}\n</think>\n"
    )
    names = [tc.name for tc in _parse_tool_calls(stream)]
    if names != ["get_graph_schema", "put_submodel"]:
        _fail(f"tool names/order not preserved: {names}")
    print(f"OK  parser names/order: {names}")


def main() -> None:
    test_misbound_success_is_not_surfaced()
    test_genuine_failure_is_surfaced()
    test_parser_preserves_names_and_order()
    print("\nAll write-path classification regression checks passed.")


if __name__ == "__main__":
    main()
