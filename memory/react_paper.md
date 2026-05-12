# REACT Prompting — Paper Notes

## Source

Yao et al. (2023), "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023, arXiv:2210.03629)

## Core Idea

ReAct ist ein **interleaved Pattern**: der LLM generiert Reasoning Traces (Thoughts) und task-specific Actions abwechselnd. Thought → Action → Observation → Thought → Action ...

Die Synergie:
- **Reasoning to Act:** Thoughts induzieren Action Plans, tracken Fortschritt, handlen Exceptions
- **Act to Reason:** Actions sammeln Daten aus externen Quellen — grounded, nicht aus internen Repräsentationen

## Thought-Typen (Section 2)

Das Paper identifiziert konkrete Thought-Typen, die im interleaved Loop vorkommen:

| Thought-Typ | Zweck |
|---|---|
| Goal decomposition | Frage in Sub-Tasks zerlegen |
| Progress tracking | "Was habe ich, was fehlt noch?" |
| Exception handling | Route nicht fruchtbar → neu orientieren |
| Commonsense | Domain knowledge anwenden, wo Locations likely sind |
| Final synthesis | Evidence zu Antwort zusammenführen |

**Wichtig:** Bei knowledge-intensive tasks (QA, fact verification) sind Thoughts **dense** — jeder Action-Step beginnt mit einem Thought. Bei decision-making tasks (ALFWorld, WebShop) sind Thoughts **sparse** — nur an kritischen Entscheidungspunkten.

## Key Results

| Methode | HotpotQA EM | Fever Acc |
|---|---|---|
| Act-only | 25.7% | 58.9% |
| CoT | 29.4% | 56.3% |
| **ReAct** | 27.4% | **60.9%** |
| ReAct + CoT-SC | **35.1%** | — |

**Halluzination:** CoT hat 14% false positive, ReAct nur 6%. ReAct ist grounded, CoT halluziniert aus internem Knowledge. CoT-SC (self-consistency, 21 samples majority vote) + ReAct ist best overall.

## Relevanz für unsere Implementierung

Unser ReAct-Agent (`agent.py`) nutzt `create_react_agent` aus LangGraph — ein built-in ReAct loop mit Thought/Action/Observation interleaving. Der system-prompt (§Self-validating approach) implementiert den Validation-Loop.

### Passt direkt

- Thought/Action interleaving ✓ (`create_react_agent` intern)
- Validation nach jeder Action ✓ ("Describe → Query → Validate → Refine")
- "Act, don't ask permission" ✓ (Paper: actions allow interfacing with external sources)
- Source citation ✓ ("Act to reason" — externes Evidence, nicht internes Knowledge)

### CoT-Fallback: NICHT relevant für uns

Das Paper kombiniert ReAct + CoT-SC als Fallback. CoT = reines Reasoning aus **internen Modellrepräsentationen** — also aus dem Modell, nicht aus externen Quellen. Das ist genau das Halluzinationsrisiko.

**Unser Agent ist strikt evidence-based:** Graph + PDF, kein internes Modell-Knowledge als Antwortquelle. Der richtige Fallback bei erschöpften Tools ist: ehrlich sagen "nichts gefunden". Das ist bereits so implementiert. CoT-Fallback haben wir bewusst nicht — und das ist richtig.

### Few-shot vs Zero-shot

Das Paper nutzt 3-6 hand-crafted Trajectories als in-context examples. Zero-Shot + finetuning skaliert besser (PaLM-8B finetuned ReAct > PaLM-540B prompting). Wir sind rein Zero-Shot mit strukturierten Instructions. Hand-crafted Trajectories sind in unserem Kontext nicht praktikabel — Tool Calls sind zu domain-spezifisch und zu lang für den Prompt-Kontext.

### Bench-B Eval-Asymmetrie (2026-05-12)

ReAct hat strukturell **keinen separaten Finalizer/Synthesizer-Node** — der `create_react_agent`-Loop produziert die finale Antwort direkt als freien Text. Im Gegensatz dazu liefern plan/crag/reflexion/rewoo strukturierte `FinalAnswer`-Objekte mit `confidence` (high/medium/low) und `unresolved[]`-Listen.

**Konsequenz für Bench B:** ReAct kann das `confidence`-Feld nicht ausfüllen — paper-inhärente Asymmetrie, kein Bug. Für die manuelle Grading-Auswertung muss man bei ReAct anhand der Antwort-Substanz selbst klassifizieren (high/medium/low), während die anderen Varianten ihre Self-Assessment liefern.

**Anti-Hallucination-Rules** (no fabricate IDs, cite sources, no "Shall I…?") sind in `system-prompt.md` (von ReAct als base_system genutzt) bereits abgedeckt: "Never assume a pattern or semanticId from memory", "Cite the source", "Act, don't ask permission". Der shared `synthesizer_rules.md` block wird ReAct **nicht** zugeschaltet, da es keinen synthesis-Node gibt, dem man ihn anhängen könnte ohne den Pattern-Mechanismus zu verändern.
