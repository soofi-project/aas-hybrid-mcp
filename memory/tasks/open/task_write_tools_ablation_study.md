---
name: Task – Write-Tools Prompt-vs-Validator Eval
description: Misst ob eine explizite Prompt-Instruktion den put_submodel_element-Bypass verhindert; kein typed Tool, kein Variant-B — nur Befund dokumentieren.
type: task
status: open
priority: high
---

## Background

**Variant B (typed-only) ist aus dem Scope gestrichen.** Das `create_service_request_notification`-
Tool wird nicht implementiert. Stattdessen nur eine Bedingung:

**Variant A — "Prompt als Hint":**
- Alle generischen Write-Tools aktiv (`put_submodel`, `put_submodel_element` etc.)
- System-Prompt + Tool-Description sagen explizit: kein `put_submodel_element` für neue Submodelle
- Erwarteter Befund: Agent nimmt den Bypass trotzdem → starke Evidenz für Layered-Determinism-These

Das ist der Paper-Beitrag: Prompt-Instruktion war vorhanden, Validator fehlte, Bypass geschah.
Empfehlung für Produktion (typisierte Tools) wird in §Discussion erwähnt, nicht implementiert.

**Composite-Overlays:** `docker-compose.variant-a.yml` und `docker-compose.variant-b.yml`
können im Repo bleiben (bereits committed), Variant-B wird einfach nicht genutzt.

## Subtasks

### T1 — `WRITE_TOOLS_MODE` Tri-State in `write_tools.py`

Env-Var `WRITE_TOOLS_MODE=generic | typed | both` (Default: `both`).
Für Variant A reicht `WRITE_TOOLS_MODE=generic` — deaktiviert kein Tool, da
`create_service_request_notification` nicht existiert. Der Tri-State-Code bleibt
als Erweiterungspunkt erhalten.

**Status:** ✅ Done (2026-05-18)

### T2 — Variant-A-System-Prompt

Datei: `aas-agent/src/aas_agent/prompts/variant-a/system-prompt.md`
Inhalt: normales `system-prompt.md` + Append-Abschnitt:

```
## Write-Path Guidance
When writing a whole new Submodel, always use `put_submodel` as a single atomic
operation — never construct it piece-by-piece with multiple `put_submodel_element`
calls. Include all mandatory fields in one JSON payload.
```

**Status:** ✅ Done (2026-05-18)

### T3 — Compose-Overlay Variant A

`docker-compose.variant-a.yml` aktiviert Variant-A-Prompt via `AGENT_SYSTEM_PROMPT_DIR`.

**Status:** ✅ Done (2026-05-18)

### T4 — Test-Cases `srn_ablation_variant_a.yaml`

Gleiche Query wie `srn_bypass.yaml` (aus [[task-srn-slotfilling-tool-and-eval]]),
aber als eigenständige Datei für den Ablation-Kontext:
- `forbidden_tools: [put_submodel_element]` — Bypass-Check
- Kein `tool_called`-Constraint

**Status:** ✅ Done (2026-05-18)

### T5 — Eval-Run Variant A + Auswertung

Variant A gegen `aas-agent:react`, N=3 pro Case.
Ergebnis-JSON: `tests/agent-tests/results/srn_ablation_variant_a_N3.json`

Auswerten:
- Bypass trotz Prompt-Instruktion? (Tool-Violations)
- `put_submodel`-Erfolg / Fehler?

**Status:** ⬜ Open

### T6 — Paper §Write-Loop / §Evaluation

Tabelle + 2-Satz-Interpretation, Existence-Framing:

| Bedingung | Instruktion | Bypass in BaSyx | Befund |
|-----------|------------|-----------------|--------|
| Prompt-only | Tool-Desc + System-Prompt | x/N | Prompt reicht nicht |

§Discussion: Befund als Pragmatics-Validation-Gap. Empfehlung:
typisierte Tools (vgl. `garmaev2023submodel_classes`) — Future Work.

**Status:** ⬜ Open

## Acceptance Criteria

- [ ] Eval-JSON mit N=3 für Variant A vorhanden
- [ ] Bypass-Quote dokumentiert (x von N Runs)
- [ ] Paper-Tabelle + 2-Satz-Interpretation in §Evaluation
- [ ] §Discussion-Empfehlung referenziert `garmaev2023submodel_classes`

## Non-Goals

- Kein `create_service_request_notification` implementieren
- Kein Variant-B-Eval-Run
- Kein N>3 für Ablation

## References

- Write-Tools: `mcp-server/src/aas_hybrid_mcp/tools/write_tools.py`
- Compose-Overlays: `docker-compose.variant-a.yml`
- Test-Cases: `tests/agent-tests/cases/srn_ablation_variant_a.yaml`
- Bypass-Task: [[task-srn-slotfilling-tool-and-eval]]
- Paper Write-Loop: `paper/etfa2026/content/09-write-loop.tex`
- Verwandte Tasks: [[task-write-tool-validation-gap]], [[task-paper-layered-determinism-thesis]]
