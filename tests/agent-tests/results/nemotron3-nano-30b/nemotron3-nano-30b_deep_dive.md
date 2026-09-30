# Nemotron-3-Nano-30B — Deep-Dive Evaluation (superseded, N=10 run)

> **Superseded 2026-08-23.** This deep-dive covers the original N=10 run against the
> old `mrk40` LiteLLM proxy (recursion limit 100, 120s connection timeout). That run's
> raw/judged JSON, `stats.json`, and `analysis_*.md` were discarded and replaced by a
> fresh N=4 run through the direct `soofi-lite.l3s.de` proxy with the current settings
> (recursion limit 200, 300s timeout) — see `t07/analysis_nemotron3-nano-30b_t07.md`
> and `t07/stats.json` for current numbers. The core finding below (self-correction
> failure: the model repeats an identical/near-identical tool call instead of revising
> its approach on a null/empty result) reproduced identically in the new run, just at
> roughly double the tool-call count before hitting the (also doubled) recursion cap —
> confirming it's a genuine non-convergence behavior, not a budget artifact. Kept here
> for the pre-fix headline-vs-Soofi-S-M7/Qwen3.6-35B comparison table and the
> LiteLLM-hop analysis, both still accurate.

Generated: 2026-08-21 · Evaluated against the AAS Hybrid MCP agent test harness (5 suites, N=10, T=0.7, 200 runs total)

## Setup

- **Model:** `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16`, served via an external LiteLLM proxy (`litellm-lxc.mrk40.dfki.lan:4000`).
- **Serving path has two LiteLLM hops, not one.** Response headers on a direct smoke-test call show the request traveling through `litellm-lxc.mrk40.dfki.lan` and then a second LiteLLM instance (`x-litellm-model-api-base: https://soofi-lite.l3s.de`) before reaching the actual Telekom-Cloud-hosted backend. The Qwen3.5/3.6 scaling-axis models run on our own H200 behind a **single** LiteLLM hop. This asymmetry matters for interpreting the stream-error rate below — see "Failure mode 1".
- **Agent pattern: ReAct.** All 200 runs used the `aas-agent:react` variant — a plain observe → think → act loop, no planning/reflection/corrective-retrieval scaffolding.
- **Thinking: OFF** (`AGENT_DEFAULT_THINKING=false`), **recursion limit 100** (`AGENT_RECURSION_LIMIT=100`, i.e. 50 tool-call turns for a ReAct loop). The model does emit its own `reasoning_content` inline (confirmed via a direct proxy call outside the agent), so visible step-by-step narration in transcripts is the model's own text, not a suppressed budget.
- **Architecture/training provenance:** not publicly documented; treated here as a black box, same status as the other externally-served candidate, Soofi-S-M7 — not part of the Qwen3.5/3.6 family used for the main scaling axis.

## Headline result

| | Nemotron-3-Nano-30B | Soofi-S-M7 (also 2-hop external) | Qwen3.6-35B (H200, 1-hop) |
|---|--:|--:|--:|
| **Correct (overall)** | **2% (4/200)** | 38% (77/200) | 74% (148/200) |
| Stream errors (`[stream error — see server logs]`) | 74% (148/200) | 53% (106/200) | 0% |
| Hit the tool-call recursion cap (50 calls) | 70% (139/200) | 26% (52/200) | 0% |
| Runs that triggered ≥1 Cypher-validator rejection | 58% (116/200) | 74% (149/200) | 42% (83/200) |
| Minimum `tool_call_count` across all runs | **0** | 3 | — |

Nemotron-3-Nano-30B performs at essentially floor level on this benchmark — 4 correct answers out of 200 runs, and none at all on `bench_b` or `srn_autonomous` (the write-path suite). This is categorically worse than Soofi-S-M7, the other externally-served, 2-hop-proxy candidate, which itself already trailed the H200-hosted Qwen models substantially.

### Per-suite correct rate

| Suite | N | Correct |
|---|--:|--:|
| anti_pattern | 20 | 5% |
| asset_specs | 20 | 5% |
| bench_b | 60 | **0%** |
| containment_hall4 | 50 | 4% |
| srn_autonomous (write-path) | 50 | **0%** |
| **Total** | **200** | **2%** |

## Did the model refuse to call tools?

**Mostly no, but with a distinct new failure pattern not seen in the Soofi-S-M7 run.**

- No occurrence of classic refusal-style language ("I cannot help", "as an AI", "not authorized", etc.) in any final answer.
- However, **9 of 200 runs (4.5%) made zero tool calls** and instead produced a final answer that describes the plan and then *asks the user for permission to proceed*, e.g.:

  > "First I'll retrieve the graph schema and the published IDTA templates so I can construct the correct Cypher query. Could you please confirm that I may proceed with these preliminary calls?"

  This happened even though the system prompt and tool descriptions give the agent standing authorization to call `query_aas_graph`, `get_graph_schema`, etc. without asking — it is not a policy refusal (the model clearly intends to help and states a correct plan) but a **failure to act autonomously in an agentic context**: it treats read-only lookup tools as if they required interactive confirmation, and since the harness has no human in the loop, this stalls the conversation with no further turns. Only 2 of the 9 use explicit confirmation language ("could you confirm", "may I") — the rest ask an under-specified clarifying question first (e.g. "which robot are you referring to?") on cases where the ground truth requires the agent to enumerate candidates itself.

## Failure mode 1: Recursion-cap exhaustion, mislabeled as "stream error" (70% of all runs)

139 of 200 runs (70%) hit the 50-tool-call cap without producing an answer. Because the agent's exception handler (`aas_agent/agent.py`, generic `except Exception` around the LangGraph invocation) catches `GraphRecursionError` the same way it catches a genuine connection failure, **both surface as the identical `[stream error — see server logs]` string** — the harness cannot distinguish "ran out of budget" from "backend dropped the connection" from the final-answer text alone.

Splitting the 148 stream-error runs by `tool_call_count` shows this is overwhelmingly the recursion-cap case, not a network issue:

| `tool_call_count` at failure | Runs |
|---|--:|
| 50 (cap) | 139 |
| 49 | 3 |
| 10–42 (scattered) | 6 |

94% of stream errors are at or one below the cap. Only 6 runs failed at a low call count where a genuine mid-stream backend problem (dropped connection, proxy timeout somewhere in the two-hop chain) is a plausible explanation — but a slow/near-timeout request that simply ran out of wall-clock time under load is an equally plausible explanation, and the data here can't tell those apart. Unlike the Soofi-S-M7 run, where roughly half of stream errors occurred at low call counts (a real backend-instability signature), this run's failures are dominated by one specific, reproducible model behavior rather than proxy noise.

**Root cause, confirmed by direct inspection (not just inference from counts):** a manual smoke test before the full run reproduced this from a single turn. Asked "how many robot instances are there in Hall 4" and "list all robots located in Hall 4", the model queried the graph for `Asset` node properties (`idShort`, `id`, `category`) that **do not exist** on `Asset` nodes in this schema — `Asset` carries `globalAssetId`, `assetKind`, `assetType` instead (confirmed directly against Neo4j: `MANAGES_ASSET` correctly returns 14 assets, but with the properties the model asked for, every row comes back `null`). Rather than reading the null-filled result as a signal to inspect the schema (`keys(a)`, or re-reading `get_graph_schema()`), the model re-issued the same failing query, alternating between two near-identical wrong variants, until the recursion cap was hit.

This generalizes across the full run: **118 of 200 runs (59%) contain a single identical Cypher query repeated 5 or more times**, with one run repeating the same query **47 times**. This is a self-correction failure, not a data-availability problem — the underlying facts were reachable in every case checked.

## Failure mode 2: Genuine wrong answers (48 runs, excluding stream-error and cap-hit)

Excluding the 148 stream-error and near-cap runs, 48 runs produced a real final answer the judge scored incorrect (4 more were scored correct — see Headline table). Representative patterns:

1. **False negatives / premature "no data" claims** — e.g. *"the search returned no indexed documents for the query 'maximum speed'... there is no PDF-document evidence available"* for `mir100_max_speed`, when the value is present in the graph's technical-data submodel.
2. **Right submodel, wrong property name** — same root cause as failure mode 1, just resolved into a (wrong) final answer instead of a loop: *"No submodel element with the idShort `MaximumSpeed`... was found"* — the model looked for a property name it invented rather than the one actually present.
3. **Correct-shaped but unconverted answer** — some runs build an elaborate multi-row table of candidate values across both `MiR100_Type` and `MiR100_001` without picking the one the question actually asks for, leaving the judge unable to credit a specific claim.
4. **Wrong shell resolved** — e.g. matching `UR3e_Type` when the question's ground truth requires the concrete instance shell, or vice versa.

## Cypher query quality — did it write wrong/invalid Cypher?

Checked across every `query_aas_graph` call in all 200 runs (5,958 Cypher calls total):

| Outcome | Count | Share |
|---|--:|--:|
| Validator rejection (forbidden anti-pattern, e.g. substring/regex `idShort` lookup) | 388 | 7% |
| **Genuine Cypher syntax error** (Neo4j exception, would fail for any model) | 447 | 8% |
| **Syntactically valid, zero rows returned** | 3,080 | 52% |
| Syntactically valid, returned data | 2,043 | 34% |

**Interpretation, compared to Soofi-S-M7's profile (6% / 5% / 40% / 48%):**

- The validator-rejection and syntax-error shares are comparable to Soofi-S-M7 and not the dominant problem here either.
- The **zero-rows share is noticeably higher (52% vs. 40%)** — consistent with the loop pattern in failure mode 1: a large fraction of all Cypher calls across the run are the *same* wrong query being repeated, so the zero-rows count is inflated by a comparatively small number of runs generating a disproportionate number of empty-result queries. This is a distinct signature from Soofi-S-M7, where the empty-result queries were spread across many different queries (broad, unstructured trial-and-error) rather than concentrated in exact repeats of one wrong hypothesis.

## Bottom line

Nemotron-3-Nano-30B under ReAct/thinking-off is not usable for this benchmark as currently deployed — 2% correct overall, 0% on both multi-step suites (`bench_b`, `srn_autonomous`). The dominant failure is not invalid Cypher or refusal to engage with tools; it is a **self-correction failure**: when a query returns a null-filled or empty result, the model does not treat that as a signal to re-examine its schema assumptions, and instead repeats the identical query (up to 47 times observed) until the recursion budget is exhausted, which the agent's generic exception handler then reports as a generic `[stream error]` rather than a distinguishable "gave up" signal. A secondary, smaller failure mode (4.5% of runs) is the model asking the user for confirmation before making read-only lookup calls it is already authorized to make, stalling the conversation with no further turns possible in a non-interactive harness. Both failure modes were confirmed by direct inspection (a manual smoke-test reproduction for the loop, and reading the zero-tool-call transcripts for the confirmation-seeking pattern), not inferred from aggregate counts alone. Whether the ~4.5% of stream errors that occurred at low tool-call counts reflect an actual backend/connection failure on the two-LiteLLM-hop serving path or simply a slow request timing out under load could not be determined from the available data.
