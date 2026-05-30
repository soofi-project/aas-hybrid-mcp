---
name: Ablation Sections Done
description: Write-Path Benchmark C completed with PSE bypass data, validator gap evidence, and primary limitation classifications.
type: task
status: done
---

## Umgesetzt

### §10 Evaluation — Benchmark C

1. **Finding (2) erweitert** (`10-evaluation.tex:95`): Konkrete PSE-Bypass-Zahlen eingefügt:
   - 6/9 Modelle rufen PSE in ≥24% der Runs (Range: 4-92%)
   - 4B/9B: 6-7 PSE-Calls pro Run im Durchschnitt
   - qwen36-27b: 92% PSE-Rate trotz bester Manual-Lektüre
   - Trotz expliziter Tool-Description "Do NOT use PSE to construct new submodels"

2. **Table bench_c `\todo{define}` gefüllt** (`10-evaluation.tex:109-117`):
   - ≤9B: "Turn budget" (2B), "PSE bypass" (4B, 9B)
   - ≥27B: "Vocabulary" (27B, 35b, 122b, 397b, qwen36-35b)
   - qwen36-27b: "PSE bypass" (92% PSE-Rate, kollabiert auf Write-Path)

3. **0 Validator-Rejections** über alle 450 Runs bestätigt.

### §11 Discussion — Domain Pragmatics

4. **§11.2 erweitert** (`11-discussion.tex:16`): Querverweis auf §10.3 PSE-Daten:
   - Tool-Description "Do NOT use PSE" wird systematisch ignoriert
   - 6/9 Modelle in ≥24% der Runs
   - Prompt-side guidance allein garantiert kein compliant Tool Use

## Daten-Quellen

- PSE-Statistiken: `tests/agent-tests/results/<model>/t07/<model>_srn_autonomous_N10_T07.json`
- Validator-Gap-Test: `tests/validator-tests/test_template_validator_gap.py`
- Tool-Description: `mcp-server/src/aas_hybrid_mcp/tool_descriptions/put_submodel_element.md:5`
