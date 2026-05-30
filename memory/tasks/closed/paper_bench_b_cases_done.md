---
name: Bench-B Cases Done
description: Bench-B Eval-Daten (9 Modelle, 5 Suites, 1750 Runs) vollständig in §10 evaluation.tex integriert — Tabellen, Text und Analyse konsistent mit analysis.md.
type: task
status: done
---

## Umgesetzt

- **Phase 1 + 2 abgeschlossen:** Alle 9 Modelle (qwen35-2b bis qwen35-397b) haben `bench_b_N10_T07.json` + `_judged.json` für alle 5 Suites (anti_pattern, asset_specs, bench_b, containment_hall4, srn_autonomous)
- **Cross-Model-Analyse** in `tests/agent-tests/results/analysis.md` (240 Zeilen, 8 Key Takeaways)
- **§10 `10-evaluation.tex` integriert:**
  - **Table `bench_b`**: 9 Modelle × 4 Read-Path-Suites + run-weighted Averages — alle Werte verifiziert gegen analysis.md
  - **Table `bench_c`**: 9 Modelle × SRN Write-Path — alle Werte verifiziert
  - **Text**: Drei Regime (Floor/Sub-viable/Viable), Manuals-first-Effekt, Anti-pattern-Compliance, Benchmark-C-Findings (Vocabulary Gap, Template Validation Gap, Validator Effectiveness)
- **Tool-Call-Analyse** via `analyze_tool_calls.py` ergänzt die Evaluation (AP-hit-Nichtmonotonie, Self-Correction 95-98%)

## Referenzen

- Daten: `tests/agent-tests/results/<model>/t07/*_bench_b_N10_T07*.json`
- Analyse: `tests/agent-tests/results/analysis.md`
- Paper: `paper/etfa2026/content/10-evaluation.tex`
- Tool-Analyse: `tests/agent-tests/results/tool_call_analysis_t07.md`
