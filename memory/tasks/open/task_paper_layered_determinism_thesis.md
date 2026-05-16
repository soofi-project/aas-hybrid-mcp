---
name: Task – Paper-These „Layered Determinism" + Citation-Anker
description: Engineering-Position aus drei AAS-Hybrid-MCP-Befunden als gemeinsame Paper-These ausarbeiten; Sekundärliteratur sauber recherchieren (Anthropic-Essay, EU AI Act, NIST AI RMF, Agent-Failure-Mode-Benches) statt aus dem Gedächtnis zitieren; Klammer-Absatz für die drei Anekdoten formulieren.
type: task
status: open
priority: medium
---

## Summary

Die drei AAS-spezifischen Validation-Gap-Befunde (write / read / pragmatics)
sind isoliert wirkende Bug-Anekdoten — gemeinsam betrachtet motivieren sie
aber eine schärfere These als „wir haben drei Bugs gefunden":

> **Layered Determinism.** Industrial-AI-Agenten in domänenmodellierten
> Kontexten (AAS, OPC UA, etc.) brauchen einen geschichteten Aufbau:
> der Agent liefert Sprachverständnis und Strategiewahl, die MCP/Tool-
> Boundary erzwingt domänenspezifische Invarianten *deterministisch*.
> Prompts und Manuals sind Hinweise, keine Garantien. Wo Compliance mit
> Domänen-Konventionen sicherheits- oder konsistenz-relevant ist, gehört
> sie in deterministischen Code, nicht in System-Prompts.

Diese Position vertritt der User bereits zu seinen Kollegen — sie ist in der
Engineering-Praxis verbreitet, aber **kein Peer-Reviewed-Paper im Industrial-
AI-Kontext** argumentiert sie sauber durch. Das ist der Forschungs-Spot für
ETFA 2026.

Dieser Task sorgt dafür dass die These im Paper nicht aus dem Bauch heraus
behauptet wird, sondern mit echten Citation-Ankern und einer expliziten
Position gegen das Spektrum existierender Literatur.

## Hintergrund (siehe auch auto-memory)

- [[feedback-agent-constraint-philosophy]] — die Position des Users selbst.
- [[task-write-tool-validation-gap]] — Befund 1.
- [[task-paper-modeling-vs-pragmatics-anecdote]] — Befund 2.
- [[task-paper-read-validation-anecdote]] — Befund 3.

Die drei Anekdoten-Tasks erwähnen die Klammer bereits, aber keiner liefert
die Citation-Anker oder den eigentlichen Klammer-Absatz.

## Subtasks

### T1 — Citation-Anker recherchieren (keine Halluzination)

Per WebSearch / WebFetch konkret nachschauen + Bibtex-Einträge bauen für:

**Primäranker (direkte Stützung):**
- Anthropic, „Building Effective Agents" (Schluntz & Zaharia, Dez 2024) —
  Workflows vs. Agents, Empfehlung zugunsten Workflows.
  → URL + exaktes Wording prüfen, Quotation-fähigen Absatz extrahieren.

**Sekundäranker (Failure-Mode-Empirie):**
- ReAct (Yao et al., ICLR 2023) — strukturiertes Reasoning > frei.
- Reflexion (Shinn et al., NeurIPS 2023) — Selbst-Verifikation als
  deterministische Constraint.
- Berkeley Function Calling Leaderboard / „Gorilla" (Patil et al.) —
  Tool-Argument-Halluzination, Schema-Validation als Antwort.
- τ-Bench / AgentBench / SWE-Bench — Agent-Failure-Quoten.

**Industrieller / regulatorischer Anker:**
- EU AI Act (Verordnung 2024/1689) — Artikel zu High-Risk-Systems,
  deterministische Controls + Human Oversight.
- NIST AI RMF 1.0 — „measurable trustworthiness".
- (Optional) IEC 61508 funktionale Sicherheit — stochastische Komponenten
  in safety-functions brauchen deterministische Wrapper.

**Counter-Anker (Position gegen):**
- Pure-Agent-Frameworks (AutoGPT, BabyAGI, Voyager) und ihre dokumentierten
  Failure-Modes. Damit zeigen warum die Klammer nicht trivial ist.

Output: aktualisierter Eintrag in `paper/etfa2026/main.bib` mit allen
bestätigten Quellen, plus 1-Satz-Zusammenfassung je Quelle als
Memory-Notiz (worauf der spezifische Cite-Kontext geht).

### T2 — Klammer-Absatz formulieren

Ein paper-fertiger Absatz (6–9 Sätze) in englischer Paper-Sprache,
platziert vor den drei Anekdoten im Evaluation-/Discussion-Bereich.
Struktur:

1. Beobachtung: drei voneinander unabhängige Failure-Modes in dieser
   Studie — alle haben dasselbe Muster (Manual sagt nein, Agent macht's
   trotzdem).
2. Position: Manual-Disziplin reicht nicht; deterministische Validierung
   am Tool-Endpoint schon.
3. **Anti-Counter-Argument (kritisch — siehe Sektion „Positionierung"
   unten):** das gilt unabhängig von Modellgröße. Failure-Rate ist nie
   exakt 0; Industrial-Safety-Engineering und EU-AI-Act verlangen den
   deterministischen Wrapper auch für hypothetisch perfekte Modelle.
   Konkret: kleines Modell + Validator schlägt großes Modell ohne
   Validator hinsichtlich Konsistenz und Sicherheit — das ist der
   eigentliche Punkt, nicht „bis bessere Modelle da sind".
4. Einbettung: konsistent mit (a) Anthropic-Workflow-vs-Agent-Empfehlung,
   (b) Function-Call-Reliability-Literatur (auch SOTA unter 100%),
   (c) EU-AI-Act-Forderung nach deterministischen Controls in High-Risk-
   Systems.
5. Abgrenzung: gilt für Compliance-/Konsistenz-relevante Operationen;
   für rein UX-/Sprach-Aufgaben bleibt Agent-Freiheit erhalten.
6. Forschungs-Beitrag: erste systematische Belegung für AAS-/Industrial-
   IoT-Kontext, mit drei messbaren Fällen — *und* erstes Industrial-AI-
   Paper das die Position explizit gegen die „scaling löst es"-Annahme
   stellt.

Speichern in `paper/etfa2026/content/11-discussion.tex` oder
`12-limitations.tex` — Entscheidung mit den drei Anekdoten-Tasks
abstimmen.

### T3 — Konsistenz mit den drei Anekdoten-Tasks

- Jeder Anekdoten-Absatz darf sich auf die Klammer beziehen, nicht das
  ganze Argument wiederholen.
- Anekdoten-Reihenfolge im Paper: Write → Read → Pragmatics (oder
  umgekehrt — Diskussion mit Co-Autoren-Sicht).
- Kein Anekdoten-Absatz darf die These widersprechen — z.B. der
  Pragmatik-Fix ist eine Prompt-Regel; dort den Grenzfall sauber
  diskutieren („für Pragmatik-Disambiguierung ist Prompt akzeptabel
  weil deterministische Detektion legitime Cases brechen würde").

### T4 — Related-Work-Sektion ergänzen

Eintrag in `paper/etfa2026/content/02-related-work.tex` oder vergleichbar:

- 1 Absatz „Agent autonomy spectrum" — verweist auf Anthropic + Voyager
  als Extreme.
- 1 Absatz „Tool-call reliability" — Function-Calling-Lit + Schema-
  Validation.
- 1 Absatz „Industrial-AI regulatory framing" — EU AI Act + NIST RMF.

Speichern als Markdown-Synopsis in auto-memory unter
`related_work.md` (Update statt Neuanlage) — der bestehende Eintrag im
Index ist `related_work.md` mit „citations grouped by theme + Our
Differentiator pitch".

## Acceptance Criteria

- `main.bib` enthält alle Primär- und Sekundäranker mit verifizierten
  Bibtex-Einträgen (kein „author=??? year=????").
- Klammer-Absatz steht in einer `.tex`-Datei und wird von allen drei
  Anekdoten-Absätzen referenziert (`\cref{sec:layered-determinism}`
  oder analog).
- Related-Work-Sektion erwähnt die drei Cluster (Autonomy-Spektrum,
  Tool-Reliability, Regulatorisches).
- Keine Citation halluziniert — jede zitierte Quelle wurde via WebFetch
  bestätigt oder als unbestätigt explizit markiert.
- Klammer + Anekdoten zusammen passen in das 8-Seiten-Budget (siehe
  `paper_etfa2026.md` Kompressionsplan).
- Position ist klar abgegrenzt: nicht „keine Agenten", sondern
  „minimaler Agent + maximaler deterministischer Mantel".

## Positionierung gegen das „bessere Modelle fixen das"-Counter-Argument

Diese Sektion muss im Paper explizit gemacht werden — sonst wird das
Reviewer-Bingo „warum nicht einfach ein größeres Modell?" zu unserer
größten Schwäche. Die These hält *unabhängig von Modellgröße*, aus drei
zusammenhängenden Gründen:

1. **Failure-Rate ist nie 0.** Selbst SOTA-Modelle (GPT-5, Claude-4) liegen
   im BFCL unter 100% Tool-Compliance — bei stochastischen Komponenten
   gilt Murphy's Law. Industrial-Safety-Engineering (IEC 61508 ff.)
   behandelt stochastische Elemente seit Jahrzehnten so: deterministischer
   Wrapper ist *Pflicht*, nicht Optimierungs-Option.

2. **Deployment-Story.** Das Paper argumentiert explizit für Self-Hosting,
   Souveränität und kleinere Modelle (SOOFI-Pluggability, EU-Compliance).
   „Wartet auf größere Modelle" untergräbt diesen ganzen Strang. Die
   These muss daher *im Gegenteil* lauten: **kleines Modell + Validator
   schlägt großes Modell ohne Validator** hinsichtlich Konsistenz und
   Sicherheit. Empirisch demonstrieren wir das mit Qwen3.5-120B; das
   Argument generalisiert nicht weil größere Modelle perfekt werden,
   sondern weil der deterministische Mantel jede Failure-Rate dominiert.

3. **Regulatorisch.** EU AI Act, High-Risk-Systems-Artikel verlangt
   deterministische Controls + Human-Oversight **unabhängig** von
   Modellqualität. Selbst ein hypothetisch perfektes Modell braucht
   den deterministischen Mantel um deploy-bar zu sein. Das macht
   „bessere Modelle" zu einem regulatorischen Dead-End.

Diese drei Punkte müssen im Klammer-Absatz oder einer expliziten
Anti-Counter-Sektion stehen. Wenn das fehlt, wird das Paper als
„temporäre Hilfslösung bis bessere Modelle da sind" gelesen — was das
Gegenteil unserer Aussage ist.

## Offene Fragen (nicht-These-relevant)

- **Co-Autoren-Sicht:** ist die These auch im Sinne des technischen
  Supervisors (Owner des Neo4j-Kafka-Plugins)? Diskussion mit dem User
  vor finaler Platzierung.
- **Sektionsplatz:** Eigene Subsection in Discussion, oder als Klammer-
  Absatz vor den drei Anekdoten ohne eigenen Header? Hängt vom Page-
  Budget ab.

## References

- Engineering-Position: [[feedback-agent-constraint-philosophy]] (auto-memory).
- Anekdoten-Tasks: [[task-write-tool-validation-gap]], [[task-paper-modeling-vs-pragmatics-anecdote]], [[task-paper-read-validation-anecdote]].
- Bestehender Related-Work-Snapshot: auto-memory `related_work.md`.
- Paper-Working-File: `paper/etfa2026/conference_etfa_2026.tex`, `main.bib`.
- Kompressionsplan: auto-memory `paper_etfa2026.md`.
