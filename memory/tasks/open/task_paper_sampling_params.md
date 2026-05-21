---
name: Task – Sampling-Parameter dokumentieren und Paper Experimental-Setup ergänzen
description: temperature=0.7 explizit in runner.py setzen; Paper-Abschnitt um Qwen3.5-Sampling-Defaults erweitern + Cite Ouyang et al.
type: task
status: open
priority: medium
---

## Background

Die Tests liefen mit implizitem T=0.7 (Qwen3.5 non-thinking default aus
`generation_config.json`, durchgereicht von LiteLLM ohne Override). Das ist
methodisch korrekt, aber undokumentiert — Reviewer können die Ergebnisse nicht
reproduzieren ohne zu wissen welche Temperature verwendet wurde.

Außerdem: der Judge in `judge.py` setzt `temperature=0.0` explizit (korrekt),
der Agent-Runner (`runner.py`) setzt nichts. Diese Asymmetrie fällt auf.

Nachgewiesen durch:
- vLLM-Docs: "vllm will use the sampling parameters from the `generation_config.json`"
- Qwen3.5 non-thinking recommended: T=0.7, top_p=0.8, top_k=20
- LiteLLM-Config: kein temperature-Override, `drop_params: false`

## Subtasks

### T1 — temperature=0.7 in runner.py setzen

**Status:** ✅ Done (2026-05-21)

`tests/agent-tests/framework/runner.py`, Payload in `run_query()`:
```python
payload = {
    "model": verbose_model,
    "messages": messages,
    "stream": True,
    "temperature": 0.7,
}
```

### T2 — Paper Experimental-Setup um Sampling-Parameter ergänzen

`paper/etfa2026/conference_etfa_2026.tex` — Abschnitt Evaluation / Experimental Setup:

> "All agent evaluations use temperature=0.7, top\_p=0.8, top\_k=20,
> consistent with Qwen3.5 recommended non-thinking mode settings.
> Sampling parameters are set explicitly to ensure reproducibility [cite: ouyang2024nondeterminism]."

### T3 — Bib-Eintrag Ouyang et al. anlegen

```bibtex
@article{ouyang2024nondeterminism,
  author={Ouyang, Shuyin and Zhang, Jie M. and Harman, Mark and Wang, Meng},
  title={An Empirical Study of the Non-Determinism of {ChatGPT} in Code Generation},
  journal={ACM Transactions on Software Engineering and Methodology},
  year={2024},
  doi={10.1145/3697010}
}
```

## Acceptance Criteria

- `runner.py` enthält `"temperature": 0.7` im Request-Payload
- Paper Experimental-Setup nennt T=0.7, top_p=0.8, top_k=20
- `main.bib` enthält Eintrag `ouyang2024nondeterminism`
- Kein Neulauf der Tests nötig (bestehende Ergebnisse gültig)

## References

- Files: `tests/agent-tests/framework/runner.py`
- Files: `paper/etfa2026/conference_etfa_2026.tex`
- Files: `paper/etfa2026/main.bib`
- Verwandte Tasks: [[task-paper-pattern-modelsize-eval]]
