---
name: Task – Paper-Methodologie: Iterative Optimization Loop + Held-Out Eval
description: Methodologisches Framework für Prompt/MCP/Daten-Optimierung mit getrennten Dev- und Held-Out-Sets. Strukturiert die drei Validation-Gap-Befunde als kontrolliertes Experiment zwischen agent-side (Prompt) und MCP-side (Validator) Interventionen.
type: task
status: open
priority: high
---

## Summary

User-Vorschlag (2026-05-15): statt ad-hoc Bugs zu fixen, einen *strukturierten
Optimierungs-Loop* fahren:

1. **Dev-Set bauen** mit Test-Cases deren erwartete Antworten der Mensch
   vorher festlegt (deterministisch, nachprüfbar).
2. **Failure-Modes identifizieren** durch Agent-Lauf auf Dev-Set.
3. **Intervention wählen**: Prompt-Anpassung / MCP-Description-Update /
   synthetische Trainings-Daten / deterministischer MCP-Validator.
4. **Re-testen** auf Dev-Set bis Failure-Modes weg sind.
5. **Held-Out-Evaluation:** Final-Lauf auf separatem Dataset das während
   der Optimierung **nie gesehen** wurde — verhindert Overfitting auf
   Dev-Cases.

Das ist Standard-ML-Praxis (Train/Dev/Test-Split) für LLM-/Agent-Systeme,
aber im Industrial-AI-AAS-Kontext nicht etabliert. Mit DSPy / APE /
Promptbreeder als Referenz-Literatur belegt.

## Warum das für unser Paper kritisch ist

Das Paper macht aktuell drei isolierte Validation-Gap-Befunde
([[task-paper-modeling-vs-pragmatics-anecdote]], [[task-paper-read-validation-anecdote]],
[[task-write-tool-validation-gap]]) plus die [[task-paper-layered-determinism-thesis]].

Eine methodologische Klammer in Form eines „controlled experiment" macht
daraus eine *publikations-würdige Studie*:

- **Branch A (agent-side):** Iterative Prompt-/Manual-Optimierung mit
  Dev-Set bis Failure-Mode verschwunden.
- **Branch B (MCP-side):** Deterministischer Validator am Tool-Endpoint
  einbauen, kein Prompt-Update.
- **Held-Out-Eval:** Beide Branches gegen unbekanntes Dataset
  (Naming-Stress, neue Container-Patterns, andere Worker-Phrasen).
- **Erwartung der These:** Branch A überfittet auf Dev-Cases, Branch B
  generalisiert. Falls Branch A genauso gut generalisiert → These
  schwächer.

Das ist ein deutlich schärferes Argument als „wir haben 3 Bugs gefunden".

## Subtasks

### T1 — Dev/Held-Out-Split entwerfen

**Dev-Set (für Optimierung, optimierungs-sichtbar):**

- Aktuelle Containment-Familie: `cases/containment_hall4.yaml`
- Anti-Pattern-Smoke-Cases: `cases/anti_pattern_idShort_lookup.yaml`
- Bench-B-Eval-Cases (existierende)

**Held-Out-Set (nur für Final-Eval, optimierungs-unsichtbar):**

- Naming-Stress-Fixtures (siehe [[task-read-validation-gap]] T2) mit
  künstlich umbenannten Assets.
- Neue Container-Patterns: LKW (statt Halle), Schrank, Anlage —
  testet ob die Pragmatik-Regel auf andere Container-Typen
  generalisiert.
- Worker-Phrasen-Set aus `cases_rewrite_ablation.yaml` (existiert
  schon, war nicht im aktuellen Bench).
- Eine *neue* Hall-Variante mit anderen Roboter-IDs (z.B. Hall5 mit
  KUKA-Robotern) — testet ob die Container-Lesart-Regel asset-unabhängig
  greift.

**Hard Rule:** Held-Out wird *vor* der Optimierung definiert und während
der Optimierung **nicht** angeschaut. Sonst ist's Daten-Leakage und der
Held-Out verliert seinen Sinn.

### T2 — Optimierungs-Loop-Tooling

- Skript / Notebook das einen Optimierungs-Lauf orchestriert:
  1. Run auf Dev-Set, archivieren.
  2. Failure-Cases identifizieren (manuell oder via LLM-Judge-Reasoning).
  3. User wählt Intervention (Prompt/Manual/Validator).
  4. Re-Run, Diff-Bericht.
- Versionierung der Interventionen — z.B. Git-Tags `optim-v1`,
  `optim-v2`, ...
- Held-Out-Eval läuft *manuell* (nicht durch Loop-Skript) damit niemand
  versehentlich darauf optimiert.

### T3 — Methodologie-Sektion im Paper

`paper/etfa2026/content/08-evaluation.tex` (oder neue Subsection)
schreibt die Methodologie:

- Train/Dev/Test-Split-Erklärung
- Branch-A vs Branch-B-Vergleich als kontrolliertes Experiment
- DSPy / APE / Promptbreeder als verwandte Arbeit referenzieren
- Statistische-Signifikanz-Diskussion (siehe T4)

### T4 — Statistische-Signifikanz-Disclaimer

Im Paper offen sagen *was* N=3 leistet und *was nicht*:

- **N=3 reicht für Existence-Claims:** „Modell X tappt in Anti-Pattern Y
  mindestens einmal." Ein deterministischer Detect ist ausreichend.
- **N=3 reicht für grobe Variant-Vergleiche:** 100% vs 40% Pass-Rate
  ist auch ohne Statistik klar interpretierbar.
- **N=3 reicht NICHT für präzise Frequenz-Schätzung:** „Modell X tappt
  in 23% der Fälle" ist mit N=3 nicht aussagekräftig (95%-CI wäre
  riesig).
- **N=3 reicht NICHT für kleine Effekt-Größen:** Wenn Branch A 73%
  und Branch B 80% liefert, ist das mit N=3 nicht signifikant.

Wenn das Paper große Aussagen über Frequenz machen will, brauchen wir
N≥10 (besser 30) — dann werden's aber 200+ Runs pro Bench, was im
Cortecs-Bench-Budget knapp wird. Konservativ: Existence-Claims im
Paper, Frequenz-Schätzungen in Future Work.

### T5 — Dev/Held-Out konkret pro Befund

Jeden der drei Validation-Gap-Befunde durch den Loop:

- **Containment-Pragmatik** ([[task-paper-modeling-vs-pragmatics-anecdote]]):
  - Branch A: Prompt-Regel in `query_aas_graph.md` + `cypher.md`
    (Stand: Task [[task-container-location-traversal-prompt-fix]] T1+T2).
  - Branch B: deterministischer MCP-Filter der MANAGES_ASSET-
    Selbst-Edges bei HAS_ELEMENT-Queries automatisch entfernt.
  - Held-Out: Container „LKW Halle 5" oder ähnlich, mit neu modellierter
    HierarchicalStructures-Submodel.
- **Read-Validation-Gap (idShort-Lookup)** ([[task-paper-read-validation-anecdote]]):
  - Branch A: Manual-Regeln verschärfen, Beispiele ergänzen.
  - Branch B: `STRICT_READ_VALIDATION=strict` (siehe [[task-read-validation-gap]] T1).
  - Held-Out: Naming-Stress-Fixtures.
- **Write-Validation-Gap** ([[task-write-tool-validation-gap]]):
  - Branch A: Manual + System-Prompt-Anweisungen für `put_submodel`.
  - Branch B: Slot-Filling-Tool oder Entzug von `put_submodel_element`.
  - Held-Out: andere Submodel-Templates die der Agent vorher nicht
    gesehen hat.

## Acceptance Criteria

- Dev/Held-Out-Sets formal definiert, Held-Out **vor** Optimierungs-Start
  eingefroren.
- Optimierungs-Loop-Tooling existiert und ist reproducibel.
- Pro Validation-Gap-Befund: Branch A vs Branch B durchgespielt,
  Held-Out-Zahlen erhoben.
- Methodologie-Sektion im Paper geschrieben mit DSPy/APE-Bezug.
- Statistische-Signifikanz-Disclaimer im Paper transparent gemacht.
- Tabelle Branch A vs Branch B auf Dev- und Held-Out-Set.

## Verwandte Literatur (zu recherchieren via [[task-paper-layered-determinism-thesis]] T1)

- **DSPy** (Khattab et al., Stanford) — explizites Framework für
  Prompt-Optimierung mit Train/Test-Splits.
- **APE / Automatic Prompt Engineer** (Zhou et al.) — automatisierte
  Prompt-Suche.
- **Promptbreeder** (Fernando et al., DeepMind) — evolutionäre
  Prompt-Optimierung.
- **„The Effect of Prompt Optimization on Held-Out Sets"** —
  generelles Overfitting-Problem in der Prompt-Engineering-Literatur,
  Zitate suchen.

## Open Questions

- **Wer macht die Held-Out-Daten?** Brauchen wir einen Co-Autor der die
  Held-Out-Cases blind designt? Oder reicht es wenn der User sie *vor*
  Optimierung definiert und sich selbst diszipliniert?
- **Wieviele Iterationen pro Branch?** Beliebige Anzahl bis stabil, oder
  cap bei z.B. 3 Iterationen damit der Aufwand begrenzt ist?
- **Synthetic-Training-Data-Variante** — User erwähnte Modell-Nachtraining
  als dritte Intervention. Das ist deutlich teurer (LoRA/SFT + Daten-
  Generierung). Vorschlag: für ETFA 2026 weglassen, im Follow-up-Paper
  als Branch C einbauen.

## References

- Engineering-Position: [[feedback-agent-constraint-philosophy]] (auto-memory).
- Hauptthese-Task: [[task-paper-layered-determinism-thesis]].
- Anekdoten-Tasks: [[task-paper-modeling-vs-pragmatics-anecdote]],
  [[task-paper-read-validation-anecdote]], [[task-write-tool-validation-gap]].
- Bench-Run: `tests/agent-tests/results/containment_hall4_baseline_N3.json`
  (2026-05-15, 60 Runs, N=3).
- Test-Framework: `tests/agent-tests/`.
