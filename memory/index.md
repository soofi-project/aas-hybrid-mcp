# Memory Index

| Datei | Thema |
|---|---|
| `architecture.md` | Gesamtarchitektur + Datenfluss, Service-Inventory, MCP tools |
| `agent_variants.md` | 8 Agent-Varianten, lazy init, model name routing, budget params |
| `aas_template_compliance.md` | IDTA Template Konformität status |
| `aas_type_instance_separation.md` | Type- vs Instance-AAS separation |
| `weaviate_collection_model_naming.md` | Model-aware collection naming (`{base}_{model_slug}`) |
| `aas_mcp_endpoint_generic.md` | MCP endpoint is generic, data-agnostic |
| `future_phases.md` | Zukünftige Phasen, open tasks |
| `planned_features.md` | Features als future work im paper, noch nicht implementiert |
| `paper_build.md` | LaTeX Paper Build mit docker compose |
| `react_paper.md` | REACT Prompting (Yao et al. 2023, ICLR) — Paper-Zusammenfassung, CoT-Fallback nicht relevant (Halluzinationsrisiko), few-shot vs zero-shot |
| `plan_and_solve_paper.md` | Plan-and-Solve Prompting (Wang et al. 2023) — Paper-Zusammenfassung, Abweichungen unserer Implementierung, Empfehlung für generischen Planner |
| `rewoo_paper.md` | ReWOO (Xu et al. 2024, NeurIPS) — Paper-Zusammenfassung, Planner/Worker/Solver Architektur, zero-shot > few-shot, Paper-abgeleitete Änderungen an unserer Implementierung (base_system relocation, exemplar, failed-evidence sections) |
| `reflexion_paper.md` | Reflexion (Shinn et al. 2023) — Paper-Zusammenfassung, implementation notes, fixed bugs, architectural differences vs. paper |
| `multiagent_debate_paper.md` | Multi-Agent Debate (Du et al. 2023) — Paper-Zusammenfassung, iterative debate-Mechanismus, Supervisor-Audit: MAD nicht implementiert (keine cross-agent critique-loops) |
| `autogen_paper.md` | AutoGen (Wu et al. 2023) — Referenced only in Future Work (§Specialized Worker vs. Generalist Agent) |
| `self_refine_paper.md` | Self-Refine (Madaan et al. 2023) — Related-work nur, keine Agent-Variante, Single-LLM text refinement, nicht tool-gestützt |
| `bench_b_evaluation.md` | Bench B — 6-question read-only eval, 4 agent variants, ETFA 2026 §Bench B |

## Regel

Bei neuen Erkenntnissen, Entscheidungen oder mit dem Nutzer ausgearbeiteten Konzepten: **Nachfrage**, ob es in den `memory/` Ordner gehört — entweder in bestehende Datei oder als neue. Keine memory-Files ohne Abstimmung anlegen.
