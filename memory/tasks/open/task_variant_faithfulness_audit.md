---
name: Task – Variant-Implementierungen gegen Paper-Originale validieren
description: Bevor Bench-Zahlen für CRAG/Plan/Reflexion ans Paper gehängt werden, prüfen ob unsere Implementierungen die Original-Paper-Patterns sauber umsetzen. CRAG akut wegen 40% Pass-Rate. Mapping-Tabelle Paper-Komponente vs. Code, Gaps fixen oder als Deviation transparent dokumentieren.
type: task
status: open
priority: high
---

## Summary

Wenn wir im Paper sagen „CRAG erreicht 40% Pass-Rate auf Containment-
Family", dann müssen wir auch sagen können: *„und das ist CRAG nach
Yan et al. 2024, nicht eine vereinfachte Variante."* Sonst zerlegt
ein aufmerksamer Reviewer den Befund mit „eure CRAG-Implementierung ist
unvollständig, das ist kein CRAG-Effekt sondern ein Code-Bug".

Das Problem ist nicht hypothetisch: unsere CRAG-Variante hat im 2026-05-15
Containment-Bench *deutlich* schlechter performt als ReAct (40% vs 100%).
Bevor das als „more complexity = more failure surface" ins Paper geht,
muss verifiziert werden dass die Komplexität auch tatsächlich die ist die
das Paper beschreibt.

Das gleiche Problem gilt für **alle vier Varianten**:

- **ReAct** (Yao et al., ICLR 2023) — am ehesten OK weil simpel und gut
  etabliert in LangGraph (`create_react_agent` Prebuild).
- **Plan-and-Solve / Plan-Reflect** (Wang et al., 2023) — eigene Implementierung
  in `agent_plan*.py`, höheres Deviation-Risiko.
- **CRAG** (Yan et al., 2024) — eigene Implementierung in `crag*.py`,
  höchstes akutes Risiko (40%-Pass-Rate begründet werden muss).
- **Reflexion** (Shinn et al., NeurIPS 2023) — eigene Implementierung in
  `reflexion*.py`, mittleres Risiko.

## Voraussetzung

- Paper-Summary-Digests existieren im **repo** unter `memory/` (siehe
  CLAUDE.md, „paper-summary digests"). Diese sind die schnelle Referenz
  vor dem Re-Read der Original-Paper.
- Bench-Daten 2026-05-15 als Ausgangspunkt:
  `tests/agent-tests/results/containment_hall4_baseline_N3.json`.

## Subtasks

### T1 — CRAG-Audit (priorität 1, akut)

Original-Paper-Pattern (Yan et al., 2024 — *Corrective Retrieval
Augmented Generation*):

1. **Retrieval evaluator** — bewertet pro Dokument die Relevanz auf
   einer ternären Skala (correct / ambiguous / incorrect).
2. **Knowledge refinement** — decompose-recompose: relevante Chunks in
   feinkörnigere Strips zerlegen, irrelevante Strips filtern, übrige
   recompose.
3. **Knowledge searching** — wenn Retrieval-Qualität niedrig (ambiguous
   oder incorrect), Fallback auf Web-Search für zusätzliches Wissen
   (oder equivalentes Erweitern der Wissensbasis).
4. **Generation** — final answer aus refinten + ergänzten Daten.

Mapping erstellen:

| Paper-Komponente | Wo im Code? | Vollständig? | Fidelity-Kommentar |
|---|---|---|---|
| Retrieval evaluator (ternäre Bewertung) | `crag_nodes.py::?` | ? | ? |
| Knowledge refinement (decompose-recompose) | ? | ? | ? |
| Knowledge searching (Fallback) | ? | ? | ? |
| Generation | ? | ? | ? |

Dann pro Zeile dokumentieren: vollständig / partiell / fehlt. Bei
partiell/fehlt: Entscheidung treffen:

- **(a) Fixen + Bench neu fahren** — wenn Gap signifikant ist und
  Implementierungsaufwand vertretbar (< 1 Tag).
- **(b) Als Deviation im Paper transparent machen** — wenn Gap aus
  guten Gründen besteht (z.B. Web-Search-Fallback wäre für AAS-Kontext
  unsinnig, also ersetzen wir's durch X). Im Paper §-CRAG-Beschreibung
  explizit: „Wir folgen dem Pattern von Yan et al. 2024 mit folgenden
  AAS-Kontext-spezifischen Adaptionen: ..."

Out-of-Scope-Bug-Notiz aus `task_container_location_traversal_prompt_fix.md`
(`int('E0')` Parser-Crash in `crag_nodes.py:335`) hier mit-prüfen — wenn
der zugrundeliegende Bug die Pipeline systematisch beschädigt, ist das
Teil des Audit.

### T2 — Plan-and-Solve-Audit

Original-Paper-Pattern (Wang et al., 2023 — *Plan-and-Solve Prompting*):

1. **Planner** — erstelle einen detaillierten Plan aus mehreren Schritten.
2. **Executor** — führe jeden Schritt aus, hole Zwischenergebnisse.
3. **Reflector** (in unserer Variante, evtl. Wang+Reflexion-Hybrid?) —
   prüft nach jedem Schritt ob das Ziel erreicht ist.

Mapping wie T1 erstellen. Spezifisch prüfen: ist unsere `plan_reflect`-
Variante reines Plan-and-Solve oder ein Hybrid mit Reflexion? Falls
Hybrid → das im Paper als „Plan-and-Solve with stepwise reflection
(combining Wang et al. 2023 with Shinn et al. 2023)" deklarieren statt
als reines Plan-and-Solve.

### T3 — Reflexion-Audit

Original-Paper-Pattern (Shinn et al., NeurIPS 2023):

1. **Actor** — generiert Aktion / Antwort.
2. **Evaluator** — bewertet Aktion mit Score (0-1) und Feedback-Text.
3. **Self-reflection** — Actor generiert Reflexion über vergangene
   Trials, wird Teil des Memory.
4. **Memory** — Verbal-Memory aus Reflexionen wird in next iteration
   gefüttert.

Mapping wie T1. Bench zeigte Reflexion mit 93% Pass-Rate als
zweitstärkste Variante — wenn Audit hier sauber durchgeht, ist das
ein robustes Datenpunkt für das Paper.

### T4 — ReAct-Audit (minimal)

ReAct ist über LangGraph `create_react_agent` als Prebuild eingebunden
(siehe `agent.py`). Risk niedrig, aber kurz verifizieren:

- Ist das wirklich der LangGraph-Prebuild oder eine custom-Version?
- Sind die Reasoning/Action-Trace-Patterns aus Yao et al. 2023 erkennbar
  in den Tool-Call-Sequenzen?

### T5 — Paper-Konsistenz

Pro Variante einen 2-3-Satz-Abschnitt in der Eval-Sektion zu „Wie wir
$VARIANT implementiert haben" — mit:

- Referenz zum Original-Paper.
- Genannte AAS-Kontext-spezifische Adaptionen.
- Wo deviiert wird, das offen sagen.

Das ist nicht nur defensives Schreiben — es ist gute wissenschaftliche
Praxis und schützt vor Reviewer-Bingo.

## Acceptance Criteria

- Mapping-Tabelle für jede der 4 Varianten in einem neuen Memory-File
  (z.B. `memory/variant_paper_fidelity.md`) erzeugt.
- Pro Variante dokumentiert: vollständig faithful / mit X
  Deviation / Bug.
- Bei signifikanten Gaps: Entscheidung „fixen" oder „transparent
  dokumentieren" festgehalten.
- Falls T1 zeigt dass CRAG-Implementierung systematisch unvollständig
  ist → Bench-Tabelle für CRAG bekommt im Paper eine Fußnote
  („our implementation; deviates from Yan et al. 2024 in X, Y, Z")
  oder wird neu gefahren nach Fix.
- Paper-Eval-Sektion enthält pro Variante einen kurzen Implementation-
  Description-Absatz.

## Open Questions

- **Hybrid-Variants korrekt deklarieren:** unsere Plan-Variante heißt
  intern `plan_reflect` — wenn das wirklich ein Hybrid ist, sollten wir
  es im Paper auch so beschreiben, nicht als reines Plan-and-Solve.
- **CRAG ohne Web-Search:** wenn unsere CRAG-Implementierung den
  Knowledge-Searching-Fallback weglässt (weil im AAS-Kontext sinnvoll),
  ist das eine deklarations-bedürftige Deviation oder eine vernünftige
  Adaption? Wahrscheinlich letzteres, aber im Paper *sagen* dass wir's
  weggelassen haben und warum.
- **Sollten wir die Variants in der Paper-Tabelle umbenennen?** Z.B.
  „CRAG-adapted" statt „CRAG" wenn Deviation vorhanden ist? Cleaner aber
  weniger Reviewer-erkennbar. Tendenz: Original-Name behalten,
  Deviationen im Fließtext erklären.

## References

- Bench-Daten: `tests/agent-tests/results/containment_hall4_baseline_N3.json`.
- Bekannter CRAG-Bug (Parser, `int('E0')`): `task_container_location_traversal_prompt_fix.md` „Out of Scope".
- Variant-Implementierungen im Code:
  - `aas-agent/src/aas_agent/agent.py` (ReAct via LangGraph Prebuild)
  - `aas-agent/src/aas_agent/agent_plan*.py` (Plan-Reflect)
  - `aas-agent/src/aas_agent/crag*.py` (CRAG)
  - `aas-agent/src/aas_agent/reflexion*.py` (Reflexion)
- Paper-Summary-Digests: repo `memory/` (siehe CLAUDE.md, „paper-summary digests").
- Variant-Übersicht: repo `memory/agent_variants.md`.
- Verwandt: [[task-crag-failure-deep-dive]] — beide Tasks zusammen
  klären „warum 40%": Audit klärt Implementierungs-Fidelity, Deep-Dive
  klärt Infra-vs-Content-Fail.
