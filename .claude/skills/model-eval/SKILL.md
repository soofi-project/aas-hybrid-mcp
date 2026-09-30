---
name: model-eval
description: Use when evaluating a new LLM model against the aas-hybrid-mcp agent test harness (`./eval-model.sh <slug>`), or when producing a deep-dive failure analysis for a completed eval run — covers the stack-switch/health-check/smoke-test/run/judge/stats pipeline and analyzing stream errors, recursion-limit hits, tool-call refusal, and Cypher query quality.
---

# Model Eval Workflow

## Overview

Running a new model through this repo's eval harness is a fixed pipeline:
switch stack → verify healthy → smoke-test → confirm with the user → run all
test suites (background + monitor) → judge → compute stats → (if asked) go
deeper on failure modes. This skill is the checklist plus one script that
replaces the ad-hoc Python one-liners that analysis otherwise needs.

## When to use

- User asks to evaluate a model slug (`./eval-model.sh <slug>` exists as a target) against the agent test suites.
- User asks "how did model X perform", "what were typical errors", "did it refuse tool calls", "was the Cypher valid" for an eval run that already has `results/<slug>/<temp>/*_judged.json`.

## Pipeline

Run from the repo root unless noted.

0. **Before switching anything: confirm the model name and the thinking mode — both explicitly, never assumed.**
   - Model name: verify it's actually registered on the **same base URL the eval will actually call** — i.e. the `LLM_BASE_URL` set in that model's `.env.model.<slug>` — not just "some SOOFI proxy". `./list-models.sh` defaults to `https://soofi-lite.l3s.de`; if `.env.model.<slug>` points somewhere else (e.g. a different LiteLLM instance/proxy), either point `list-models.sh` at that same `LLM_BASE_URL` (`LITELLM_BASE_URL=<that url> ./list-models.sh`) or verify with a direct `GET <that url>/v1/models` call instead. A model that's registered on soofi-lite but not on the URL actually wired into `.env.model.<slug>` will pass a naive check and then 401 (`token_not_found_in_db`) at request time — this happened with `nemotron3-nano-30b`'s stale `mrk40` proxy entry (2026-08-23; fixed by pointing it straight at `soofi-lite.l3s.de`, same as the other Soofi checkpoints). Qwen/vLLM (H200) and Cortecs (`qwen35-397b`) models go through different endpoints/keys entirely — verify those against the H200 LiteLLM alias list / Cortecs docs instead.
   - Thinking on/off: **ask the user explicitly** if it isn't already stated — don't silently inherit whatever `AGENT_DEFAULT_THINKING` happens to default to (`false`). This materially changes both the results and the recursion-limit budget a run needs (thinking-heavy tool loops burn steps faster). Set it via `./up.sh <overlay-flag> --thinking` (exports `AGENT_DEFAULT_THINKING=true` for that start) or a per-run `--reasoning-effort` on `run_tests.py`/`run_all.sh`; verify after start with `docker exec aas-agent printenv | grep AGENT_DEFAULT_THINKING`.
   - Also check `AGENT_RECURSION_LIMIT` for the overlay you're using — only `.env.vllm` sets a higher one (100) than the base `.env` default (30); other overlays (e.g. `.env.litellm`) may need it added explicitly, especially with thinking on.
1. **Switch the stack:** `./eval-model.sh <slug>`. Verify: `docker exec aas-agent printenv | grep -E "LLM_MODEL|LLM_BASE_URL"` shows the expected model/endpoint.
2. **Full health check, always — don't trust a health check from earlier in the session.** `docker ps -a` (filter out `k8s_*`/`buildx`/`registry` noise). If anything shows `Restarting` or unexpectedly `Exited` (e.g. after a host reboot or long idle gap — kafka is the usual victim, and `kafka-connect-*` crash-loops when kafka is down), just re-run `./eval-model.sh <slug>` again. It re-sources the full env chain (`.env`, `.env.vllm`, `.env.model`, `~/.env.secrets`) correctly — don't hand-roll a `docker compose -f ... up` call, it's easy to miss a var (e.g. `SECRETS_PATH`) that the script sources for you.
   - **Reranker reachability (needs the mrk40 VPN)**: `docker exec aas-hybrid-mcp python3 -c "import httpx; print(httpx.get('http://10.2.10.33:8003/health', timeout=5).status_code)"` (that container has no `curl`, use `httpx` directly). This is easy to forget after a host reboot/VPN reconnect and fails **silently for the eval**: `search_aas_documents` doesn't fall back gracefully on connection failure — every call returns `{"error":"Connection error."}`, so any `document_retrieval`-tagged case (check case tags, e.g. in `bench_b.yaml`) run without it produces confidently-wrong "answers" (the agent falls back to hammering the graph instead) that read as a model failure but are actually an infra gap. If reranker checks fail, either fix the VPN and don't proceed, or proceed only with `document_retrieval`-tagged cases excluded (`--exclude-tags document_retrieval`) and re-run those specific cases separately once it's back.
3. **Smoke-test before the full run:**
   - Proxy endpoint directly: `curl .../v1/chat/completions` with the relevant API key (see the model's `.env.model.<slug>` header comment for which key/endpoint).
   - The agent itself: get its port via `docker port aas-agent`, then `curl http://localhost:<port>/v1/chat/completions -d '{"model":"aas-agent:react","messages":[{"role":"user","content":"..."}]}'` — confirm a sane, in-context reply, not just a 200.
   - **If the agent smoke-test fails or loops (500, recursion-limit crash, tool calls repeating), check the database before blaming the model.** Query Neo4j directly (`docker exec neo4j cypher-shell -u neo4j -p "$PASS" "..."`) for the relationship types (`CALL db.relationshipTypes()`), node labels (`CALL db.labels()`), and the actual properties on the node the model queried (`RETURN keys(a)`). A loop is only a model-behavior finding if the data is genuinely reachable and the model queried it wrong (bad relationship name, non-existent property, ignoring a null-filled result) — not if the fixture data is actually missing or the schema changed. Don't skip this: a smoke-test failure caused by missing fixtures would invalidate the whole run, while a failure caused by the model mishandling real, reachable data is itself a valid eval finding (loop/no-self-correction behavior) and a green light to proceed.
4. **Ask "Soll ich anfangen?" and wait for explicit go-ahead before starting `run_all.sh`.** This is a standing per-model instruction for this repo, not a one-time confirmation — ask again for every model in a multi-model session.
5. **Run the suites in the background, watch with Monitor — never sleep-poll:**
   ```
   cd tests/agent-tests
   ./run_all.sh <slug> 0.7 > <scratchpad>/run_all_<slug>.log 2>&1 &
   ```
   Attach a persistent `Monitor` over that log:
   ```
   tail -n +1 -f "$LOG" | grep -iE --line-buffered "^-> |suite|error|traceback|exception|failed|complete|done|====|all suites"
   ```
   `TaskStop` the monitor once you see `All suites done for model: <slug>`.
6. **Verify outputs:** 4 raw suite JSONs under `results/<slug>/<temp>/` (temp dir is lowercase, e.g. `t07`).
   
   **Note:** `anti_pattern` suite is no longer run separately — it's evaluated via `judge_multi.py` on the `asset_specs` results (same questions, different judging criteria).
7. **Judge — done by Claude (you) interactively via `judge_claude.py`, not an external LLM API.** Two steps, both through `judge.sh`, which wraps `judge_claude.py` and never re-implements its rubric logic (that reimplementation is exactly how the old `judge_local.py` drifted from `judge.py`'s tool lists and under-counted errors — it's been deleted):
   1. `./judge.sh export <slug> T07` — for every suite with raw results but no `*_judged.json` yet, writes a `*_export.jsonl` (one line per non-errored record: `{idx, case, query, ground_truth, final_answer}`) plus a manifest (`results/<slug>/<temp>/_judge_manifest_*.tsv`). Skips suites already judged.
   2. **You then read each `*_export.jsonl` and grade every record**, applying `judge.py`'s `JUDGE_PROMPT` rubric verbatim (same rules the old cortecs judge used — esp. the must-not-claim step: only a violation if positively asserted, not merely mentioned to exclude/contrast). Write one verdict per idx to the matching `*_verdicts.jsonl`: `{"idx": 0, "answer_correct": true|false, "reasoning": "...", "missing_facts": [...], "wrong_claims": [...]}`.
   3. `./judge.sh merge <slug> T07` — merges verdicts with the programmatic process block (`analyse_process`, imported from `judge.py` — manual-tools-first check, tool-error classification) into schema-identical `*_judged.json` files, then runs `analyze_results.py`. Re-running `merge` after grading more suites picks up newly-present verdicts files; suites still missing a verdicts file are skipped with a warning.
   - `judge_model` in the output is stamped `"claude-sonnet-5 (claude-code interactive)"` — no token cost, stays inside the Claude Code plan budget. This replaced a cortecs-billed `gpt-5.4` LLM judge; spot-checked agreement between the two on one suite was 45/50 (90%).
   - **asset_specs suite**: automatically exported/merged against both `asset_specs.yaml` (answer-only) and `anti_pattern_idShort_lookup.yaml` (answer + method) via `judge_claude.py`'s `--case-mapping-from`, driven by the manifest — no duplicate test runs needed.
   - Don't re-implement any of `judge_claude.py`'s logic ad hoc — if the export/merge shape needs to change, edit `judge_claude.py` itself so `judge.py`'s imports stay the single source of truth.
8. **Cross-model stats:** `python3 compute_eval_stats.py results/<slug>/<temp> --output results/<slug>/<temp>/stats.json`.
9. **Report headline numbers** (per-suite + total correct rate) to the user. Don't front-load deep-dive analysis — wait until asked.

## Going deeper: failure-mode analysis

When asked "what were the typical errors", "did it refuse tools", "was the Cypher any good", "how much of this is infra vs. the model" — don't write fresh `python3 -c` one-liners for this each time (they're error-prone: raw JSON here contains non-ASCII characters that break the default Windows `cp1252` stdout/file encoding unless you pass `encoding="utf-8"` explicitly, and it's easy to typo the tool-call arg key — it's `cypher`, not `query`, in `tool_calls[].args`).

Use the bundled script instead:

```
cd tests/agent-tests
python3 ../../.claude/skills/model-eval/analyze_eval_run.py <slug> --temp t07
```

It reports, from the raw + judged result files already on disk:
- per-suite and total correct rate, stream-error rate, and recursion-limit-cap-hit rate (cap is auto-detected as the observed max `tool_call_count`)
- correct rate recomputed with stream-error runs excluded — with an explicit survivorship-bias caveat printed inline, since dropping crashed runs is not a random subsample (crashes correlate with longer/harder runs)
- a tool-call-refusal check (minimum tool_call_count across all runs, plus any final answers matching refusal-style phrases) — **read the flagged excerpts yourself**, the keyword match surfaces candidates for a human read, it does not assert refusal (e.g. "I don't have access to X field" is usually a data-limitation claim, not a policy refusal, even though it matches the same phrase)
- a Cypher query-quality breakdown across every `query_aas_graph` call: validator rejection / genuine Neo4j syntax error / syntactically-valid-but-zero-rows / returned data — this is the key metric for "did it write bad Cypher" vs. "did it write plausible-but-wrong Cypher"

Run `--help` for the full flag list.

## Writing up a deep-dive doc

If the user wants a standalone report (e.g. for external distribution), write it as its own file under `results/<slug>/` (not merged into the cross-model `analysis.md`, which stays reserved for the tabular Qwen-family comparison). Always state explicitly, near the top:
- which agent pattern was used (check `AGENT_VARIANT` / the `model_id` field in the raw results — this harness supports `react`/`plan`/`crag`/`reflexion`/`rewoo`)
- whether thinking was enabled — either the deployment default (`AGENT_DEFAULT_THINKING` in the container env) or a per-run override via `run_all.sh <slug> <temp> <reasoning_effort>` (encoded in export filenames as `_TH<effort>`)

These two settings materially change what the numbers mean and are easy to omit if you don't check for them explicitly.

## Common mistakes

- Assuming stack health from earlier in the conversation still holds after any gap (reboot, VPN reconnect, long idle) — always re-check `docker ps -a`.
- Hand-rolling `docker compose up` instead of re-running `./eval-model.sh <slug>` — misses env vars the script sources.
- Polling with `sleep` loops for run/judge progress instead of a backgrounded process + `Monitor`.
- Treating `tool_calls[].args.query` as the Cypher field — it's `.args.cypher`.
- Reading JSON with the platform default encoding on Windows — always pass `encoding="utf-8"` (raw results contain non-ASCII text that trips `cp1252`).
- Reporting a "clean" (stream-error-excluded) correct rate without the survivorship-bias caveat — the surviving subsample skews toward easier/shorter runs.
