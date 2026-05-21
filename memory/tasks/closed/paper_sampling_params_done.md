---
name: Sampling-Parameter dokumentieren Done
description: temperature=0.7/top_p=0.8/top_k=20 in runner.py gesetzt; Paper-Eval-Setup + Bib-Eintrag + Multi-Agenten-Absatz ergänzt
type: task
status: done
---

## Was umgesetzt

**T1 — runner.py** (2026-05-21): `"temperature": 0.7` explizit im Request-Payload von `run_query()` gesetzt. Beseitigt Asymmetrie zum Judge (der `0.0` bereits explizit setzte).

**T3 — main.bib**: Eintrag `ouyang2024nondeterminism` (Ouyang et al., ACM TOSEM 2024, DOI 10.1145/3697010) im Abschnitt `% === LLM / Agent Evaluation ===` eingefügt.

**T2 — 10-evaluation.tex**: Sampling-Satz ans Ende des Bench-B-Setup-Absatzes angehängt: T=0.7, top_p=0.8, top_k=20 als Qwen3.5 non-thinking defaults, Cite `qwen35` + `ouyang2024nondeterminism`.

**T4 — 11-discussion.tex**: Neuer Absatz am Ende von `\subsection{The Necessity of Enforcement}`: Layered-Determinism-Prinzip vertikal auf Agenten-Schichten übertragen — Orchestrator T=0.7, Executor T=0, Validator-Gate. Verbindet die Bench-B-read-vs-write-Unterscheidung mit Multi-Agenten-Architektur.

**Build:** `=== BUILD SUCCESS ===` nach allen Edits, keine undefined citations.

## References

- `tests/agent-tests/framework/runner.py`
- `paper/etfa2026/content/10-evaluation.tex`
- `paper/etfa2026/content/11-discussion.tex`
- `paper/etfa2026/main.bib`
