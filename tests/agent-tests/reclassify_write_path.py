"""Offline re-classification of SRN write-path bypass types.

ARCHIVE / VERIFICATION TOOL. As of the fence-robust evaluator change, the LIVE
path (framework/evaluator.py:_analyse_write_path) already classifies via the
BaSyx success signal — no offline re-processing is needed for new runs. This
script is kept to (a) re-verify the already-collected SRN JSONs that were graded
under the old error-substring heuristic, and (b) cross-check the live evaluator's
`wrote` aggregate against this script's NEW_wrote column. No logic change.

The original bypass classification (framework/evaluator.py:_analyse_write_path)
reads per-call tool results. Those results are reconstructed by a regex over the
agent's rendered text stream (framework/runner.py:_parse_tool_calls), and the
regex mis-assigns result blocks whenever a tool result contains embedded code
fences (```), which get_manual_page / get_template / get_graph_schema all emit.
A foreign Cypher error then lands on a put_submodel call and the error-string
heuristic (evaluator.py:213) marks the run as a failed write ("surfaced").

Tool NAMES and their order are parsed correctly (block headers do not break),
and the BaSyx success signal is short enough to survive the 200-char preview
truncation. So we re-derive the write outcome assignment-independently:

  put_submodel  success  -> {"status":"ok","id":...}        (basyx_client.put_submodel)
  put_submodel_element    -> {"status":"ok","idShortPath":...} (put_submodel_element)

This is a heuristic: the exact call<->result binding is lost, so a run that
calls both put_aas and put_submodel where only put_aas succeeded would be
mis-counted. For the SRN suite (agents add a submodel to an existing shell) that
is rare. We cross-validate against the judge verdict: every judge-correct run
MUST have a successful write; violations are reported.
"""

from __future__ import annotations

import glob
import json
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

PS_OK = re.compile(r'"status"\s*:\s*"ok"\s*,\s*"id"')
PSE_OK = re.compile(r'"status"\s*:\s*"ok"\s*,\s*"idShortPath"')


def reclassify(tool_calls: list[dict]) -> tuple[str, bool]:
    names = [tc.get("name") for tc in tool_calls]
    blob = " ".join((tc.get("result_preview") or "") for tc in tool_calls)

    ps_attempted = "put_submodel" in names
    pse_called = "put_submodel_element" in names
    ps_ok = ps_attempted and bool(PS_OK.search(blob))
    pse_ok = pse_called and bool(PSE_OK.search(blob))
    wrote = ps_ok or pse_ok

    if not ps_attempted and not pse_called:
        bt = "no_write_tool"
    elif ps_ok:
        bt = "wrote_submodel"          # atomic put_submodel succeeded
    elif pse_ok and not ps_attempted:
        bt = "direct"                  # element write, no submodel attempt
    elif pse_ok and ps_attempted:
        bt = "element_fallback"        # tried submodel, fell back to element
    elif ps_attempted and not pse_called:
        bt = "submodel_no_success"     # attempted, no success signal, no fallback
    else:
        bt = "other"
    return bt, wrote


def load_judge(path: str) -> dict[tuple[str, int], bool]:
    """Map (case, repetition) -> judge says correct."""
    d = json.load(open(path, encoding="utf-8"))
    recs = d["records"] if isinstance(d, dict) else d
    out = {}
    for r in recs:
        key = (r["case"], r["repetition"])
        j = r.get("judge") or {}
        out[key] = bool(j.get("answer_correct"))
    return out


def main() -> None:
    files = sorted(glob.glob("tests/agent-tests/results/*/t07/*_srn_autonomous_N10_T07.json"))
    files = [f for f in files if "_judged" not in f]

    print(f"{'model':12} {'runs':>4} {'old_correct':>11} {'NEW_wrote':>9} {'judge_ok':>8} "
          f"{'old_surfaced':>12} {'sanity_viol':>11}")
    print("-" * 78)

    grand_old = Counter()
    grand_new = Counter()
    for f in files:
        model = f.split("/")[-1].replace("\\", "/").split("/")[-1].split("_srn")[0]
        d = json.load(open(f, encoding="utf-8"))
        recs = d["records"]
        judge = load_judge(f.replace(".json", "_judged.json"))

        old = Counter()
        new = Counter()
        wrote_n = 0
        judge_ok = 0
        sanity_viol = 0
        for r in recs:
            wp = r["evaluation"].get("write_path") or {}
            old_bt = wp.get("bypass_type")
            old[old_bt] += 1
            grand_old[old_bt] += 1

            bt, wrote = reclassify(r["result"]["tool_calls"])
            new[bt] += 1
            grand_new[bt] += 1
            if wrote:
                wrote_n += 1

            jk = judge.get((r["case"], r["repetition"]))
            if jk:
                judge_ok += 1
                if not wrote:
                    sanity_viol += 1

        print(f"{model:12} {len(recs):>4} {old.get('correct',0):>11} {wrote_n:>9} "
              f"{judge_ok:>8} {old.get('surfaced',0):>12} {sanity_viol:>11}")

    print("-" * 78)
    print("\nOLD bypass_type totals:", dict(grand_old))
    print("NEW bypass_type totals:", dict(grand_new))
    print("\nLegend NEW: wrote_submodel=atomic put_submodel ok | direct=element only | "
          "element_fallback=submodel tried+element | submodel_no_success=tried, no ok | "
          "no_write_tool=never wrote")
    print("sanity_viol = judge-correct runs that the new heuristic marks as no-write "
          "(should be 0)")


if __name__ == "__main__":
    main()
