# Plan-and-Solve Prompting — Paper Notes

## Source

Wang et al. (2023), "Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models" (arXiv:2305.04091)

## Core Idea

Plan-and-Solve (PS) ist ein **two-phase pattern**, kein Framework. Statt "Let's think step by step" (Zero-shot-CoT) erhält der LLM einen Prompt mit zwei Teilen:

1. **Devise a plan** — die Aufgabe in kleinere Subtasks zerlegen
2. **Carry out the plan** — Schritt für Schritt ausführen

Der PS+ prompt fügt detaillierte Instructions hinzu:
- "extract relevant variables and their corresponding numerals"
- "calculate intermediate variables (pay attention to correct numerical calculation and commonsense)"

## Key Findings

| Metric | CoT | PS | PS+ |
|---|---|---|---|
| GSM8K | 56.4% | 58.2% | 59.3% |
| Missing-step errors | 12% | 10% | 7% |
| Calculation errors | 7% | 7% | 5% |

**Wichtigste Erkenntnis:** Der Plan als solcher bringt moderaten Gewinn. Der *hebeleffekt* kommt von den detaillierten Instructions in Phase 2:
- "Intermediate results" anfordern reduziert Step-Missing-Errors (Korrelation -0.83)
- "Variables extrahieren" anfordern reduziert Calculation-Errors (Korrelation -0.56)

## Was das Paper NICHT ist

Es handelt sich **NICHT um ein Agent-Framework mit separaten Rollen**. Es ist ein Prompting-Pattern:

> "we simply replace 'Let's think step by step' ... with 'Let's first understand the problem and devise a plan to solve the problem. Then, let's carry out the plan and solve the problem step by step'"

Das Paper definiert keine separaten Planner/Executor/Reflector-Module, keine JSON schemas, keine state machine.

## Relevanz für unsere Implementierung

Unsere Plan-And-Reflect agent (`agent_plan.py` mit Planner Executor Reflector Finalizer) geht **weit über das Paper hinaus**. Wir haben eine Multi-Agent-Architektur mit separaten nodes — das Paper macht das komplett in einem monolithischen Prompt.

### Wo die Idee passt

Der Paper-Kern "devise a plan first, then execute" ist der richtige prinzipielle Ansatz. Die Trennung von Plan-Erstellung und Ausführung ist sinnvoll.

### Wo wir abweichen

Das Paper liefert **keine** Guidance für:
- Wie der planner prompt konkret aussieht
- Wie man mit 0-row Ergebnissen umgeht
- Wie templates als Schema-Brücke genutzt werden
- Wie replan funktioniert
- Wie der reflector entrechtet, ob ein Step erfolgreich war

Alles das sind unsere eigene design decisions.

## Prompt Design für den Planner

Das Paper sagt: "devise a plan to divide the entire task into smaller subtasks". **Keine** Domain knowledge wird injiziert — der LLM soll den Plan generisch auf der Frage aufbauen.

Für unseren Kontext bedeutet das:

- Der planner sollte **generisch** arbeiten: "Finde die relevanten Templates, dann querye den Graph"
- Domain-spezifische Hinweise (wie "Location queries → HierarchicalStructures") sind **unsere** Addition — nicht im Paper verankert
- Die Gefahr: zu spezifische Hinweise machen den planner zum Code — er routet auf einen Pfad statt flexibel zu planen

### Stand der Umsetzung

Der `planner.md` ist bereits paper-konform generisch: keine Submodel-Namen hardcoded, statt dessen template-discovery mit generischen Beispielen ("location", "hierarchy", "capacity", "payload"). Das entspricht dem Paper-Geist ("devise a plan from the question, not from rules").

**Was beibehalten werden muss:** Vorsicht, dass keine domain-spezifischen Hinweise in Replan-/Reflector-Prompts einsickern. Wenn der LLM `HierarchicalStructures` selbständig findet, ist das richtig; wenn der Prompt es nennt, ist es Code-statt-Plan.

### Finalizer-Unification mit shared block (2026-05-12)

`agent_plan_prompts/finalizer.md` enthielt eine eigene Confidence-Calibration + Empty-Result-Hard-Rule + "Things you must NOT do" Section. Diese sind jetzt in `synthesizer_rules.md` ausgelagert (shared mit crag/reflexion). `agent_plan.py:_lazy_init` hängt den shared block beim Laden an `finalizer.md` an. In `finalizer.md` bleiben nur plan-spezifische Teile: die `evidence`-Struktur (plan-eigenes FinalAnswer-Feld), Cite-Source-Style ("according to the graph data…"), und die `give_up`-Hard-Rule (referenziert Reflector-Entscheidung — kein anderer Pattern hat einen Reflector mit `give_up`-Decision). **Deliberate addition beyond paper** — Paper ist nur Prompting-Pattern, Confidence ist unsere Bench-B-Eval-Erweiterung.
