# CRAG (Yan et al. 2023) — Paper & Implementation Notes

## Paper

**"Corrective Retrieval Augmented Generation"** (ACL 2023, arXiv:2305.14283)

### Core concept

Solves the problem: **what happens when retrieval goes wrong?** Standard RAG blindly feeds all retrieved docs to the generator, even irrelevant ones. CRAG adds a corrective layer between retriever and generator:

1. **Retrieval Evaluator** (lightweight T5-based model, 0.77B) scores each retrieved doc individually for relevance
2. **3 Action Triggers** based on thresholds:
   - **Correct** (score >= upper threshold): refine knowledge strips from relevant docs
   - **Incorrect** (all scores < lower threshold): discard all retrieved docs, use web search
   - **Ambiguous** (between thresholds): combine both — refine + web search

### Key results

| Method | PopQA | Biography | PubHealth | Arc-Challenge |
|---|---|---|---|---|
| RAG (LLaMA2-hf-7b) | 50.5 | 44.9 | 48.9 | 43.4 |
| **CRAG** | **54.9** | **47.7** | **59.5** | **53.7** |
| Self-RAG (SelfRAG-LLaMA2-7b) | 54.9 | 81.2 | 72.4 | 67.3 |
| **Self-CRAG** | **61.8** | **86.2** | **74.8** | **67.2** |

CRAG improves RAG on all 4 datasets. Self-CRAG (CRAG + Self-RAG) outperforms Self-RAG alone on PopQA (+6.9%) and Biography (+5%).

### Key ablation findings

**Impact of each action (PopQA):**
| Variant | CRAG | w/o Correct | w/o Incorrect | w/o Ambiguous |
|---|---|---|---|---|
| LLaMA2-hf-7b | 54.9 | 53.2 | 54.4 | 54.0 |

All 3 actions are needed — removing any one degrades performance. **Ambiguous is the stabilizer**: without it, hard threshold switching makes the system volatile.

**Impact of each knowledge operation:**
| Variant | w/o refine | w/o rewrite | w/o selection |
|---|---|---|---|
| CRAG (hf-7b) | 49.8 | 51.7 | 50.9 |

All 3 operations (document refinement, query rewriting, external knowledge selection) contribute.

**Robustness to retrieval quality:** As retrieval accuracy drops, CRAG degrades more gently than standard RAG. The corrective mechanism acts as a safety net.

**Retrieval Evaluator vs ChatGPT:** The T5-based evaluator (84.3% accuracy) significantly outperforms ChatGPT direct (58.0%), ChatGPT-CoT (62.4%), and ChatGPT-few-shot (64.7%) on relevance judgment. Paper argues fine-tuned lightweight models beat prompted LLMs for this task.

### Knowledge Refinement (decompose-then-recompose)

1. Split each retrieved document into "strips" (segments of a few sentences)
2. Score each strip for relevance using the same evaluator
3. Filter out low-relevance strips, concatenate remaining strips
4. Result: dense, relevant "internal knowledge" without noise

### Web Search for correction

When retrieval is Incorrect:
1. **Rewrite** the query into search keywords (using ChatGPT)
2. **Search** via Google Search API
3. **Select** relevant content from web pages
3. Same knowledge refinement method applied to web results

### Computational overhead

FLOPs per token: RAG 26.5, CRAG 27.2 (only +0.7 overhead). Execution time: RAG 0.363s, CRAG 0.512s (+0.15s). Lightweight and plug-and-play.

### Why this fits our AAS domain

- **Retrieval evaluation is critical in our setup** — Neo4j/Weaviate queries can easily return wrong results for ambiguous queries
- **Multi-source evidence** (graph + vector) benefits from per-source relevance scoring
- **Iterative refinement** is needed for complex queries like B5/B6 (multi-hop)
- **Ambiguous action** is especially valuable — partial evidence is common in our domain

## Our Implementation

### Architecture: `executor → relevance → (synthesize | refine → executor | discard → uncorrect → executor)`

Six nodes in a loop with conditional routing:

| Node | Purpose | LLM |
|---|---|---|
| executor | Bounded ReAct sub-loop for retrieval | `create_react_agent` with MCP tools |
| relevance | Scores evidence 0.0-1.0, triggers 3-way action | structure LLM (no tools) |
| refine | Generates supplementary query for Ambiguous | structure LLM |
| discard | Clears evidence after Incorrect | (deterministic) |
| uncorrect | Generates fresh query after Incorrect | structure LLM |
| synthesize | Combines evidence into FinalAnswer | structure LLM |

Conditional routing after relevance:
- **correct** → synthesize
- **incorrect** → discard → uncorrect → executor (retry from scratch)
- **ambiguous** → refine → executor (supplement)
- **max_refinements reached** → synthesize (force-stop)

Loop runs up to `CRAG_MAX_REFINEMENTS` (default 3).

### Changes applied (paper-aligned)

| # | Change | File | Rationale |
|---|---|---|---|
| 1 | Per-evidence-item scoring replacing holistic block scoring | `crag_nodes.py:181-387` | Paper scores each document individually (§4.2). We now score each `[Ei]` individually in one LLM call with fallback to holistic scoring on parse failure. |
| 2 | Deterministic 3-way action from per-item scores | `crag_nodes.py:` `_finalize_relevance()` | Paper §4.3: `correct` if ONE item >= upper, `incorrect` if ALL items <= lower. Implemented in code, not trusted from LLM output. |
| 3 | Shared `synthesizer_rules.md` appended to `_SYNTHESIZER_PROMPT` (2026-05-12) | `crag_nodes.py` | **Deliberate addition beyond paper.** Confidence calibration (high/medium/low), empty-result hard rule, forced-termination rule (e.g. `CRAG_MAX_REFINEMENTS` hit without high-relevance evidence), anti-hallucination don'ts. Shared across rewoo/crag/reflexion finalizers so Bench-B compares retrieval mechanisms, not synthesizer-prompt quality. Paper has no confidence dimension — our eval-fair extension. |

### Architectural differences from paper (by design)

| Aspect | Paper | Ours | Rationale |
|---|---|---|---|
| Retrieval Evaluator | Fine-tuned T5 (0.77B), per-doc scoring | LLM-based, per-item scoring | No fine-tuning infrastructure; LLM can reason about AAS domain context. Per-item scoring is paper-aligned. |
| Individual doc scoring | Each doc scored separately by T5 | Each evidence item scored individually in one LLM call | One call is more efficient; fallback to holistic scoring on parse failure preserves robustness. |
| Web search fallback | Google Search API | No web search — retry with different MCP tool strategy | **Deliberate omission:** no external web access by design (data-sovereignty / self-hosted stack, see `CLAUDE.md` §Data sovereignty). The "Incorrect" path retries within the local tool set instead. |
| Knowledge Refinement | Decompose strips + filter + recompose | LLM-based relevance evaluation (no strip decomposition) | Our evidence is already tool-structured; strip-level refinement not applicable |
| Correct → refine | Refine documents into knowledge strips | Go directly to synthesize | High-relevance evidence is already filtered; refinement would add cost without benefit |
| Correct action trigger | Score of at least ONE doc above threshold | Score of at least ONE item >= upper threshold | Paper-aligned (§4.3), enforced deterministically in `_finalize_relevance` |
| Generator | Standard RAG or Self-RAG | LLM synthesizer with evidence + confidence | Same concept, different framing |

### Architectural deviations / known limitations

1. **No fine-tuned evaluator.** The paper shows the T5 evaluator (84.3%) beats ChatGPT (58-65%) for relevance judgment. Our LLM-based evaluator is inherently less accurate and more expensive. We can't replicate the paper's evaluation accuracy without fine-tuning.
2. **No web search (by design).** The "Incorrect → web search" path is CRAG's primary novelty for handling retrieval failure. We deliberately omit it because external web access violates the stack's data-sovereignty property. The trade-off is explicit: when the local sources (graph + vector + manual + templates) cannot answer, "Incorrect → uncorrect → executor" retries within the same tool set, and the synthesizer must report the gap honestly via `unresolved`. This is a documented architectural deviation from the paper, not a missing feature.
3. **No strip-level knowledge refinement.** The paper's decompose-then-recompose is effective at removing noise from individual documents. Our evidence is already tool-structured (graph results, PDF chunks), so this level of refinement doesn't apply directly.

### What could be improved

1. **Broader local-source fallback for the "Incorrect" path:** Instead of relying solely on retrying with the same MCP tools, the uncorrect node could explicitly switch retrieval modality (e.g. graph→vector, vector→manual, or BaSyx direct lookup with different parameters). Stays within the data-sovereignty boundary; serves the same role as web search in the paper.
2. **Strip-level refinement for large results:** When graph queries return large result sets, a decompose-filter-recompose step could help the synthesizer focus on relevant entries.

### Env config

| Var | Default | Purpose |
|---|---|---|
| `CRAG_MAX_REFINEMENTS` | `3` | Maximum executor→relevance loop iterations |
| `CRAG_RELEVANCE_THRESHOLD` | `0.7` | Score >= this → Correct → synthesize |
| `CRAG_RELEVANCE_THRESHOLD_LOW` | `0.3` | Score <= this → Incorrect → discard + retry |
