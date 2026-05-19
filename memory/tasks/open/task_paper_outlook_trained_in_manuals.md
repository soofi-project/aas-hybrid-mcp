---
name: Task – Paper-Outlook: Trained-In Manuals als 4-Layer-Verfeinerung
description: Future-Work-Idee — stabile generische Manual-Regeln ins Modell nachtrainieren statt zur Laufzeit injizieren. Spart Token-Cost und Latenz, passt zur SOOFI-Plug-Stelle. Muss als 4-Layer-Strukturierung formuliert sein (Trained-in + System-Prompt + On-Demand-Manual + MCP-Validator), nicht als "Manual weg" — sonst untergräbt die Idee die eigene Layered-Determinism-These.
type: task
status: open
priority: medium
---

## Summary

User-Idee (2026-05-15, kurz vor Feierabend): wenn wir alle generischen
Manual-Regeln ins Modell trainieren oder nachtrainieren, dann:

- Manual muss zur Inference-Zeit nicht mehr im Context sein → Token-Cost
  fällt drastisch (heute ~50k Token Manual-Injection pro Conversation).
- Agent ist schneller weil weniger Context = schnellere Generation.
- Agent folgt der Regel eher, weil sie aus dem Modell kommt statt aus
  reinem Prompt-Text (höhere implizite Compliance).
- MCP-Endpoint muss nicht mehr so detailliert beschrieben werden.
- Manual als MCP-Resource könnte sogar abgeschafft werden.

Das ist ein guter Future-Work-Punkt — *vorausgesetzt* er wird im Paper
sauber positioniert. Naiv formuliert („wir stellen Manuals gar nicht
mehr bereit") **untergräbt es unsere Layered-Determinism-These**, weil
die These ja gerade sagt: Prompts/Manuals sind Hinweise, Validator ist
die Garantie. Trained-in-Regeln sind „high-quality prompts im Gewicht"
— immer noch Hinweise, immer noch stochastisch, immer noch keine
Garantie.

Die Lösung: **4-Layer-Strukturierung statt Substitution.**

## 4-Layer-Outlook-Modell (paper-tauglich)

| Layer | Inhalt | Update-Mechanismus | Compliance-Charakter |
|---|---|---|---|
| **1. Trained-in** | Stabile, projekt-übergreifende Regeln (semanticId-Disziplin, Container-Pragmatik, AAS-Metamodel-Grundlagen) | Fine-Tune-Lauf | Stochastisch, hohe Rate |
| **2. System-Prompt** | Deployment-spezifische Anpassungen (Sprache, Rolle, Branding) | env-Variable | Stochastisch, mittlere Rate |
| **3. On-Demand-Manual** | Detail-Regeln, Edge-Cases, neue Patterns | MCP-Resource (nicht auto-injected) | Stochastisch, Fallback-Path |
| **4. MCP-Validator** | Deterministische Compliance-Garantie | Code-Update | Deterministisch, 100% |

**Die Pointe:** Layer 1 ersetzt Layer 3 als *Standard-Pfad*, aber Layer 3
bleibt als *Fallback* verfügbar. Layer 4 bleibt unverändert wichtig —
egal wie gut das Modell trainiert ist, der Validator bleibt die einzige
*Garantie*.

So formuliert ist der Outlook **stärkend** statt schwächend für die
Layered-Determinism-These:

> „We move the prompt layer into the weights for efficiency, but the
> validator layer remains because no amount of training reduces failure
> rate to zero."

## Warum „Manual weg" allein die These bricht

Wenn wir naiv sagen „Manual ist im Modell, wir brauchen das Manual nicht
mehr": ein aufmerksamer Reviewer fragt: „Aber ihr habt doch gerade
argumentiert dass selbst SOTA-Modelle in dieselben Anti-Patterns tappen —
warum sollte trained-in besser sein als prompt-injected?" Die ehrliche
Antwort ist: *ist es nicht*. Trained-in ist effizienter, nicht
zuverlässiger. Wer das nicht klar macht, verliert die These.

## Outlook-Absatz für das Paper (Entwurfsskizze)

Für `paper/etfa2026/content/14-future-work.tex` oder ähnlich, ~5–7 Sätze:

> A natural evolution of the architecture presented here is to migrate
> stable, project-wide compliance rules from the runtime manual into
> the model weights through targeted fine-tuning. For the AAS schema —
> which evolves slowly and is largely standardized — this is particularly
> attractive: token cost at inference time drops to zero for the
> internalized rules, response latency improves, and the deployment
> footprint of the MCP server shrinks. The SOOFI 120B model, scheduled
> for ~September 2026, is the natural target for this experiment: an
> open-source EU-sovereign model that can be retrained on AAS-specific
> compliance corpora. **However, this does not eliminate the need for
> deterministic validation at the MCP boundary.** Trained-in rules
> remain stochastic — they shift the compliance rate upward but cannot
> reduce the failure rate to zero. The architecture we propose therefore
> generalizes to a four-layer pattern: trained-in weights (stable
> rules), system prompt (deployment customization), on-demand manual
> (edge cases, available but not auto-injected), and deterministic MCP
> validator (the safety net). The combination, not any one layer,
> provides industrial-grade reliability.

(Englisch, weil das gesamte Paper auf Englisch ist. Auf Deutsch
übersetzbar falls Sektion mehrsprachig.)

## Subtasks

### T1 — Outlook-Absatz finalisieren und platzieren

- Entwurf oben in `paper/etfa2026/content/<future-work>.tex` einbauen.
- Datei-Name verifizieren (`14-future-work.tex`, `outlook.tex`, je
  nachdem wie das LaTeX-Setup aktuell strukturiert ist).
- 4-Layer-Tabelle als TikZ-Diagramm oder einfache Tabelle, falls
  Platz reicht.

### T2 — SOOFI-Verlinkung in Related Work / Future Work

- SOOFI-Erwähnung im Paper konsistent machen: aktuell als „Plug-in-
  Replacement via LLM_BASE_URL" beschrieben, jetzt zusätzlich als
  „Fine-Tune-Target für Layer-1-Internalisierung".
- Konsistenz-Check mit auto-memory `SOOFI Project Context` Sektion.

### T3 — Cortecs-Bench als Motivator zitieren

- Falls [[task-paper-cortecs-frontier-eval]] zeigt dass SOTA-Modelle
  ohne Fine-Tune tappen: explizit machen dass Layer 1 (trained-in)
  genau dort hilft wo Layer 2 (prompt-only) versagt.
- Die Eskalations-Logik im Paper: prompt-only → trained-in → validator
  als drei Stufen mit unterschiedlichen Compliance-Charakteristiken.

### T4 — Fine-Tune-Korpus skizzieren (optional, Detail-Outlook)

Falls Platz reicht im Future-Work-Absatz, einen Satz zur Korpus-
Generierung:

- Manual-Texte selbst als Trainings-Material (instruction-following).
- Synthetic Q&A-Paare aus Manual-Regeln (z.B. „Frage: was darf nicht
  bei Containment? Antwort: MANAGES_ASSET-Selbstreferenz.").
- Anti-Pattern-Traces als Negativ-Beispiele (RLHF / DPO-Stil).
- Größenordnung: hundert bis paar tausend Beispiele — Fine-Tune-Level,
  nicht Pre-Training.

**Wichtiges Argument (2026-05-19):** Trainingsbeispiele für Layer 1
müssen **nicht automatisiert** entstehen. 50–200 menschlich geschriebene
Q&A-Paare reichen für Domain-Adaptation. Das ist kein Aufwandsproblem —
es ist ein **Designvorteil**: ein Domänenexperte schreibt die Beispiele,
behält volle Kontrolle, und der Trainingssatz hat verifizierbare Provenienz
(kein Hallu-Risiko durch LLM-generierte Trainingsdata). Teilautomatisierung
(z.B. Validator-Rejections als Kandidaten, menschlich bestätigt) ist
möglich, aber nicht notwendig. Passt direkt zur SOOFI-Datensouveränitäts-
Story: transparente, menschlich kuratierte Trainingsdaten für
domänenspezifische Feinabstimmung.

Das ist Detail-Outlook und kann auch ins Follow-up-Paper. Im ETFA-Paper
nur erwähnen falls Platz.

## Acceptance Criteria

- Outlook-Absatz im Paper steht und macht die 4-Layer-Pointe klar.
- Trained-in wird nicht als Ersatz, sondern als Verfeinerung positioniert.
- MCP-Validator-Notwendigkeit bleibt explizit unangetastet.
- SOOFI-Verlinkung konsistent mit dem Rest des Papers.
- Falls Cortecs-Bench-Daten vorliegen: Layer-1-Argument darauf abgestützt.
- Reviewer-Bingo „warum nicht einfach besseres Modell?" ist im Absatz
  vorab adressiert (Layer-1 ist *genau* das, aber löst nicht alles).

## Open Questions

- **Wann Fine-Tune-Korpus bauen?** Vermutlich erst nach Cortecs-Bench
  (sobald wir wissen ob SOTA-Modelle ohne Fine-Tune tappen, lohnt sich
  der Fine-Tune-Aufwand).
- **Verhältnis zu Slot-Filling/MCP-side-Tools?** Layer 4 (Validator)
  könnte auch durch Slot-Filling-Tools realisiert werden statt durch
  Regex-Cypher-Pre-Checks. Beide sind deterministische Layer.
- **Multi-Modell-Komplikation:** wenn der Kunde Cortecs nutzt mit
  wechselnden Modellen, ist Layer 1 (trained-in) nicht garantiert —
  das Modell könnte das AAS-Fine-Tune fehlen. Antwort: Layer 3 + 4
  fangen das ab. Genau dafür ist die 4-Layer-Architektur da.

## References

- Hauptthese-Task: [[task-paper-layered-determinism-thesis]] — Outlook
  ergänzt die These um eine Effizienz-Dimension.
- SOOFI-Kontext: auto-memory `MEMORY.md`, Sektion „SOOFI Project Context".
- Cortecs-Bench: [[task-paper-cortecs-frontier-eval]] — liefert
  Motivation für Layer-1-Investition.
- Iterative-Loop-Methodologie: [[task-paper-iterative-optimization-loop]]
  — Branch C (Trained-in) als dritte Intervention-Option neben Branch A
  (Prompt) und Branch B (Validator).
- Engineering-Position: [[feedback-agent-constraint-philosophy]] (auto-memory).
