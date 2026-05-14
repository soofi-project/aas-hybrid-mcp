# Multi-Granular Relevance Evaluation (MG-CRAG)

**Created:** 2026-05-13
**Status:** **decision pending** — see Decision Gate below
**Priority:** low (after re-scoping 2026-05-13)
**Depends on:** PDF arrival (author email pending)

## Decision Gate (added 2026-05-13)

We already have a working CRAG variant (Yan §4.3 three-way action trigger) that is
implemented, Bench-B-tested, and paper-cited (`yan2024crag,masoumi2026mgcrag`
together in `06-architecture.tex:57`). MG-CRAG is now positioned in
`13-future-work.tex` as a natural extension, not a must-do for ETFA 2026.

**Before any implementation work:**

1. **Wait for the MG-CRAG PDF** — author email pending. Without the paper, no
   faithful port is possible.
2. **Decide whether to do it at all.** The honest question is whether
   within-chunk noise actually dominates Bench-B failure modes in our AAS
   domain. If Bench-B shows current CRAG mostly fails on retrieval-miss
   (no relevant chunk found) rather than mixed-quality chunks (relevant
   sentence buried in noise), MG-CRAG's value is marginal here.
3. **Trigger conditions for "yes, implement":** Bench-B shows a measurable
   class of failures attributable to chunk-level noise; PDF available; budget
   for ~2-3 days work outside ETFA submission window.
4. **Default if undecided:** stays in Future Work, no code changes, paper
   text already covers it.

## Motivation

Our current CRAG relevance evaluator (`crag_nodes.py:199-426`) scores each retrieved chunk at a single granularity: the whole evidence item gets a 0.0–1.0 score. MG-CRAG (Masoumi, Davar, Eftekhari — *Knowledge and Information Systems*, 2026) demonstrates a two-level approach:

- **Passage-Level Retrieval Evaluator (PLRE):** scores full chunk/paragraph blocks for overall relevance
- **Sentence-Level Retrieval Evaluator (SLRE):** scores individual sentences within each passage

This catches mixed-quality chunks where one sentence is highly relevant but three are noise — the current single-granularity evaluator either keeps the whole chunk (ambiguous) or discards it entirely (incorrect).

## Current Architecture

Single-granularity relevance scoring in `crag_nodes.py`:

```
executor → relevance (per-evidence-item, 0.0–1.0) → [correct | incorrect | ambiguous]
                                                    └→ refine/discard → executor (retry)
```

Key files:
- `aas-agent/src/aas_agent/crag_nodes.py` (lines 199–426) — relevance scoring + deterministic action enforcement
- `aas-agent/src/aas_agent/crag_state.py` — `RelevanceScore` schema (single score)
- `aas-agent/src/aas_agent/crag_graph.py` — state graph wiring

## Proposed Architecture

```
executor → relevance
            ├─ PLRE: score each chunk (passage-level, 0.0–1.0)
            │        → filter: discard chunks below low threshold
            ├─ SLRE: for surviving chunks, score each sentence (0.0–1.0)
            │        → keep only high-confidence sentences, drop noise
            └→ aggregate: passage score × sentence-level precision
                      → [correct | incorrect | ambiguous]
                      → refine/discard → executor (retry)
```

## Subtasks

### T1: Study MG-CRAG paper

- Read `paper/papers_downloaded/masoumi2026mgcrag/` (PDF + markdown)
- Extract the PLRE/SLRE prompt design and scoring pipeline
- Document: How does MG-CRAG aggregate sentence scores into passage scores?
- Note: their approach uses T5 evaluators (small models). We'd use our LLM with structured JSON output. Can we adapt the prompt pattern?

### T2: Schema changes

- `crag_state.py`: extend `RelevanceScore` to support multi-granularity:
  ```python
  class SentenceScore(BaseModel):
      sentence_idx: int
      text: str
      score: float

  class PassageScore(BaseModel):
      chunk_idx: int
      passage_score: float
      sentence_scores: List[SentenceScore]
      kept_sentences: List[int]  # indices of sentences above threshold
  ```
- Backward compatible: single-granularity path stays as-is (configurable via env var)

### T3: New relevance node implementation

- New module: `aas-agent/src/aas_agent/crag_multigranular.py`
- Two prompt templates: PLRE prompt + SLRE prompt
- PLRE: score each chunk (reuses existing relevance prompt, minimal change)
- SLRE: split chunk into sentences, score each, output `{sentence_idx, score}` per sentence
- Aggregation: deterministic logic — sentence scores above threshold contribute to final chunk score
- Config: `CRAG_EVALUATOR_MODE` (`single` | `multi`) — default `single`

### T4: Integration into existing CRAG graph

- `crag_graph.py`: conditional node — if `CRAG_EVALUATOR_MODE=multi`, use new multi-granular relevance node
- `crag_nodes.py`: the existing relevance node stays as `single` mode
- No changes to executor, refine, discard, uncorrect, synthesize nodes

### T5: Paper update (optional)

If implementation is complete before ETFA submission, note the multi-granular enhancement in `08-retrieval-pipeline.tex` under "Retrieval Enhancements". Otherwise, this is an implementation detail not claimed in the paper (citation to MG-CRAG covers the conceptual approach).

## Config

| Variable | Default | Purpose |
|---|---|---|
| `CRAG_EVALUATOR_MODE` | `single` | `single` = current per-chunk, `multi` = PLRE + SLRE |
| `CRAG_SENTENCE_THRESHOLD` | `0.5` | Sentence score below this → drop from chunk |
| `CRAG_PASSAGE_THRESHOLD` | `0.7` | Same as current `CRAG_RELEVANCE_THRESHOLD` |
| `CRAG_PASSAGE_THRESHOLD_LOW` | `0.3` | Same as current `CRAG_RELEVANCE_THRESHOLD_LOW` |

## Acceptance Criteria

- `CRAG_EVALUATOR_MODE=single` → behaviour identical to current implementation (no regression)
- `CRAG_EVALUATOR_MODE=multi` → two-stage scoring: passage filter → sentence refinement → aggregate
- Multi-granular path produces valid JSON, no schema errors
- Aggregated score still maps to 3-way routing: `correct` / `incorrect` / `ambiguous`
- Mixed-quality chunks are handled better: relevant sentences kept, noisy sentences dropped
- Overhead: SLRE adds one extra LLM call per surviving chunk (measure latency impact)

## Open Questions

1. **Sentence splitting:** Should we use regex-based sentence splitting (fast, no dependency) or spaCy/nltk (slower, better boundary detection)?
2. **One LLM call vs. two:** Can we combine PLRE + SLRE into a single prompt? MG-CRAG uses two separate models. A single prompt would be simpler but larger context.
3. **Granularity depth:** Should we also consider "paragraph-level" between sentence and passage? Probably overkill for our chunk sizes.

## References

- Masoumi, N., Davar, O., Eftekhari, M. (2026). "MG-CRAG: Fusion of Multi-Granular Retrieval Evaluators in Corrective RAG with Weakly Supervised Fine-Tuning". *Knowledge and Information Systems* 68(1):149. Springer. DOI: 10.1007/s10115-026-02778-2
- Current implementation: `aas-agent/src/aas_agent/crag_nodes.py` (lines 199–426)
- Memory doc: `memory/crag_paper.md`
