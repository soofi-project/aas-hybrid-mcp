# Memory Index

| Datei | Thema |
|---|---|
| `architecture.md` | Gesamtarchitektur + Datenfluss, Service-Inventory, MCP tools |
| `agent_variants.md` | 4 Agent-Varianten, lazy init, model name routing, budget params |
| `aas_template_compliance.md` | IDTA Template Konformität status |
| `aas_type_instance_separation.md` | Type- vs Instance-AAS separation |
| `weaviate_collection_model_naming.md` | Model-aware collection naming (`{base}_{model_slug}`) |
| `aas_mcp_endpoint_generic.md` | MCP endpoint is generic, data-agnostic |
| `future_phases.md` | Zukünftige Phasen, open tasks |
| `planned_features.md` | Features als future work im paper, noch nicht implementiert |
| `paper_build.md` | LaTeX Paper Build mit docker compose |
| `react_paper.md` | REACT Prompting (Yao et al. 2023, ICLR) — Paper-Zusammenfassung, CoT-Fallback nicht relevant (Halluzinationsrisiko), few-shot vs zero-shot |
| `plan_and_solve_paper.md` | Plan-and-Solve Prompting (Wang et al. 2023) — Paper-Zusammenfassung, Abweichungen unserer Implementierung, Empfehlung für generischen Planner |
| `reflexion_paper.md` | Reflexion (Shinn et al. 2023) — Paper-Zusammenfassung, implementation notes, fixed bugs, architectural differences vs. paper |
| `multiagent_debate_paper.md` | Multi-Agent Debate (Du et al. 2023) — Paper-Zusammenfassung, iterative debate-Mechanismus, Supervisor-Audit: MAD nicht implementiert (keine cross-agent critique-loops) |
| `autogen_paper.md` | AutoGen (Wu et al. 2023) — Referenced only in Future Work (§Specialized Worker vs. Generalist Agent) |
| `self_refine_paper.md` | Self-Refine (Madaan et al. 2023) — Related-work nur, keine Agent-Variante, Single-LLM text refinement, nicht tool-gestützt |
| `bench_b_evaluation.md` | Bench B — 6-question read-only eval, 4 agent variants, ETFA 2026 §Bench B |

## Tasks

Actionable work items — prefix `task_`, enthalten Subtasks, Acceptance Criteria, References. Open tasks in `tasks/open/`, completed in `tasks/closed/`.

### Open Tasks (`memory/tasks/open/`)

**High priority**

| Datei | Thema | Status |
|---|---|---|
| `tasks/open/task_paper_pattern_modelsize_eval.md` | Paper-Pivot: Pattern × Modellgröße (Qwen 3.5 2B→397B); Setup-Swap auf 3.5-27B-FP8 | open |
| `tasks/open/task_paper_crag_removal_and_reframe.md` | CRAG aus Paper raus; Bench-B als 27B-Datenpunkt der Skalierungs-Studie umrahmen | open |
| `tasks/open/task_variant_faithfulness_audit.md` | Varianten gegen Paper-Originale prüfen — auf ReAct/Plan/Reflexion reduzieren (CRAG-Teil entfällt durch Pivot) | open |
| `tasks/open/task_n30_evaluation_run.md` | N=30 serieller Run für Paper-Tabelle + statistische KIs | open |
| `tasks/open/task_container_location_traversal_prompt_fix.md` | Pragmatik-Regel: Containment ≠ MANAGES_ASSET-Selbstreferenz | open |
| `tasks/open/task_paper_claim_audit.md` | ETFA-Claim-Audit: jede Aussage belegen | open |
| `tasks/open/task_paper_implaas2025_citations.md` | ImplAAS-2025-Zitate nachziehen & Bib-Hygiene | open |
| `tasks/open/task_paper_langgraph_orchestration.md` | LangGraph-Orchestration im Paper aufbereiten | open |
| `tasks/open/task_paper_write_validation_defense.md` | Write-Path-Validierung + Reporting verteidigen | open |

**Medium priority**

| Datei | Thema | Status |
|---|---|---|
| `tasks/open/task_paper_fp8_quantization_cite.md` | FP8-Cite (kurtic2025bf16) in Eval-Sektion + Bib-Check | open |
| `tasks/open/task_read_validation_gap.md` | Read-Validierungs-Lücke: Agent liest falsche Werte | open |
| `tasks/open/task_write_tool_validation_gap.md` | Write-Tool-Validierungslücke dokumentieren | open |
| `tasks/open/task_paper_layered_determinism_thesis.md` | Layered-Determinism-These im Paper ausarbeiten | open |
| `tasks/open/task_paper_read_validation_anecdote.md` | Read-Validation-Anekdote für Paper formulieren | open |
| `tasks/open/task_paper_modeling_vs_pragmatics_anecdote.md` | Modeling-vs-Pragmatics-Anekdote für Paper ausarbeiten | open |
| `tasks/open/task_agent_test_framework.md` | Externes Agent-Testframework für `/v1/chat/completions` | open |
| `tasks/open/task_skills_create.md` | Claude-Code-Skills anlegen (paper, paper-download, task-workflow) | open |
| `tasks/open/task_docling_gpu_dispatch.md` | Docling-Pipeline auf GPU-Offload & messen | open |
| `tasks/open/task_paper_data_quality_assumption.md` | Datenqualitäts-Annahme im Paper verankern | open |
| `tasks/open/task_paper_future_work_template_cypher.md` | Future Work: AAS Query IR — JSON-Traversal vs. DSL vs. pre-compiled Cypher (Read + Write) | open |
| `tasks/open/task_paper_readme_repo.md` | Paper-fähiges README + GitHub-Mirror vorbereiten | open |
| `tasks/open/task_paper_style_review.md` | Reviewer-Stil-Review durch Agent fahren | open |
| `tasks/open/task_prompt_quality.md` | Prompt-Qualität & Grounding-Heuristiken nachschärfen | open |

**Low priority**

| Datei | Thema | Status |
|---|---|---|
| `tasks/open/task_paper_cortecs_frontier_eval.md` | Cortecs-Budget-Einsatz für Frontier-Modell-Eval | open |
| `tasks/open/task_paper_iterative_optimization_loop.md` | Iterativer Optimierungs-Loop für Paper-Eval | open |
| `tasks/open/task_paper_outlook_trained_in_manuals.md` | Outlook: trainiertes Modell in Manuals | open |

### Closed Tasks (`memory/tasks/closed/`)

| Datei | Thema |
|---|---|
| `tasks/closed/retrieval_enhancements_done.md` | Reranker + Query Rewriting + Metadata + PDF Viewer (Phase 9) |
| `tasks/closed/bibliography_done.md` | Bib-Audit, Downloads, Korrekturen, Archivierung |
| `tasks/closed/agent_cleanup_done.md` | ReWOO entfernt, Verbose Streaming, Token Tracking, Prompt Conciseness |
| `tasks/closed/crag_diagnosis_done.md` | CRAG-Diagnose nicht weiterverfolgt — out of paper scope nach Pivot 2026-05-16 |
| `tasks/closed/crag_peer_review_done.md` | MG-CRAG Peer-Review nicht weiterverfolgt — out of paper scope nach Pivot 2026-05-16 |
| `tasks/closed/crag_parser_int_e0_bug_done.md` | CRAG-Parser-Bug nicht gefixt — out of paper scope nach Pivot 2026-05-16 |
| `tasks/closed/multigranular_eval_done.md` | MG-CRAG-Implementierung nicht gemacht — out of paper scope nach Pivot 2026-05-16 |

## Konventionen

- **`task_`-prefix:** Actionable work items mit Subtasks, Acceptance Criteria, References
- **Ohne prefix:** Architektur, Paper-Zusammenfassungen, Entscheidungen, Dokumentationen
- Tasks schließen → `status: done`, `planned_features.md` + `future_phases.md` entsprechend updaten

## Regel

Bei neuen Erkenntnissen, Entscheidungen oder mit dem Nutzer ausgearbeiteten Konzepten: **Nachfrage**, ob es in den `memory/` Ordner gehört — entweder in bestehende Datei oder als neue. Keine memory-Files ohne Abstimmung anlegen.
