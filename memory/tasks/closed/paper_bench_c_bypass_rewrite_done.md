---
name: Paper §10/§11 Bench C Bypass Rewrite Done
description: Corrected parser-bug-corrupted bypass narrative; fixed 8→9 models / 400→450 runs; added qwen36-27b row; rewrote D2/D3 to vocabulary-gap story.
type: task
status: done
---

## What was implemented

**Root cause confirmed:** `framework/runner.py:_parse_tool_calls` regex misaligns name↔result
blocks when tool results contain embedded code fences, corrupting the bypass-type assignment.
Re-classification via `reclassify_write_path.py` (assignment-independent write-signal detection)
showed true Wrote % = 77 % (345/450), not the 22 % the parser reported.

**10-evaluation.tex — four edits:**
- L66: "eight models" → "nine models"; exclusion clause for qwen36-27b removed (it WAS evaluated).
- L72: "400 write-path runs and eight models" → "450 write-path runs and nine models".
- L76: Replaced per-tier bypass-diagnostic paragraph with vocabulary-gap narrative
  (77 % write success, model-independent ceiling, zero write-tool rejections).
- `tab:bench_c`: Added `Qwen3.6-27B-FP8` row (SRN 14 %), replaced all Primary-limitation
  cell values with `\todo{define}` (final column decision deferred). Caption note about
  "dominant failure mode" removed. `\newcommand{\todo}` added to `config/01-packages.tex`.

**11-discussion.tex — D2/D3 paragraph:**
- D2: Removed "faced with a rejection" trigger (zero rejections confirmed); specification-gaming
  claim retained but reframed as agent-discovers-unguarded-path observation.
- D3: "36 % direct bypass at 35B/397B" (parser artefact) replaced with vocabulary-gap story:
  77 % write success, 96 % write for qwen36-27b but only 14 % SRN = same as 9B.

**analysis.md:**
- Section 1: srn_autonomous row for qwen36-27b: `—` → `14 %`; overall recalculated to 74 %;
  "no SRN suite" footnote replaced with recalculation note.
- Section 3: Bypass table and five-stage narrative replaced by Wrote%/SRN% table (9 models)
  with note explaining parser-bug root cause and referencing `reclassify_write_path.py`.
- Section 4: "450 SRN-suite runs" and nine models noted.

**claim_audit.md:**
- E8: ❌ → ✅; claim updated to "nine models".
- E9: 🔍 → ✅; claim updated to "450 write-path runs / nine models".
- D2/D3: claims updated to reflect reframed text.
- Resolution Log B5: re-reverted entry noting prior fix was wrong; Bench C = nine/450 confirmed.
- Resolution Log 2026-05-27: full Bench-C-bypass rewrite note with per-row resolution.

**Paper builds without errors** (verified via `build_paper.py`).
