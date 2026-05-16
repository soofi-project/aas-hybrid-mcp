---
name: Task – Cortecs Frontier-Model Eval für Layered-Determinism-Robustness
description: Cascade-Eval gegen GPT 5.4 (Phase 1) + biggest-sovereign open-weight + Qwen3.5-Baseline. Claude Opus 4.6 nur als Eskalation falls GPT alles sauber löst. Empirischer Beleg (oder Widerleg) der These "model scaling löst Anti-Pattern-Compliance nicht" — buy-down-risk-first Design.
type: task
status: open
priority: high
---

## Summary

Die Layered-Determinism-These ([[task-paper-layered-determinism-thesis]])
behauptet: Anti-Pattern-Compliance ist *kein* Modell-Größen-Problem,
sondern systemisch. Diese Aussage ist heute nur theoretisch belegt
(BFCL-Verweise + IEC 61508 + EU AI Act). Mit Cortecs.ai können wir sie
*empirisch* prüfen — und das Ergebnis ist binär entscheidend für den
Paper-Stand:

- **Wenn Top-Modelle (GPT 5.4, Claude Opus 4.6) auch in dieselben Anti-
  Patterns tappen** → Hammer-Befund. „Even SOTA frontier models fail
  manual compliance for AAS-specific patterns." Layered-Determinism
  wird damit *empirisch* statt nur regulatorisch begründet.
- **Wenn sie alle 100% sauber sind** → die starke Form der These ist nicht
  haltbar; wir müssen zurückfallen auf „kleine Modelle brauchen den Mantel"
  + EU-AI-Act-Regulatorik. Schwächer aber nicht widerlegt.

Beide Outcomes sind Paper-relevant — der Test selbst ist also der
eigentliche Beitrag, unabhängig vom Resultat.

## Cascade-Strategie (buy-down risk first)

Statt einer breiten 5-Modell-Wolke fahren wir **adaptiv**: die billigste
Falsifikation zuerst, Eskalation nur falls nötig. Begründung: wenn
GPT 5.4 — vermutlich das schwächere SOTA bei Agent/Tool-Tasks (BFCL- und
τ-bench-Trends haben Claude meist vorne) — schon tappt, ist die Aussage
„SOTA tappt rein" empirisch gemacht. Claude-Test ist dann überflüssig.

### Phase 1 (Default-Lauf, ~42 Runs)

3-Punkte-Linie für die paper-relevante Vergleichs-Erzählung:

| Punkt | Modell | Sovereign? | Rolle |
|---|---|---|---|
| **A. Proprietary frontier (weaker-SOTA-hypothesis)** | GPT 5.4 | Nein (Cortecs EU-residency only) | Buy-down: tappt SOTA überhaupt? |
| **B. Largest sovereign open-weight** | Llama-4 Maverick / DeepSeek-V3.5 / Mistral Large Sovereign (Cortecs-Catalog-abhängig) | Ja | Realistische Deployment-Option |
| **C. Self-hosted baseline** | `Qwen/Qwen3.6-27B-FP8` (27B dense, FP8, eigene H200) | Ja (volle Kontrolle) | Aktueller Paper-Stand, Referenz-Anker |

Damit haben wir „aus beiden Welten was": SOTA-proprietary-non-sovereign
(A) vs. sovereign-open-weight (B) — beide via Cortecs EU-routable —
plus Self-Hosted (C) als Bottom-Anker.

### Phase 2 (Eskalation, nur bedingt, +14 Runs)

**Nur ausführen wenn Phase 1 zeigt: A (GPT 5.4) löst alles sauber.**

Dann erst Claude Opus 4.6 hinzunehmen, weil dann unklar ist ob „SOTA"
generell sauber arbeitet oder ob GPT 5.4 nur ein günstiger Einzelfall
ist. Wenn Phase 1 dagegen zeigt dass GPT tappt — Phase 2 sparen, die
These ist gemacht.

### Variant- und Repetitions-Reduktion

Über alle Modelle hinweg:

- **Nur ReAct** als Agent-Variant (nicht Plan / CRAG / Reflexion).
  Begründung: Plan/CRAG/Reflexion bringen eigene Komplexität (Planner-
  Reasoning, Reranker-Logik, Reflexion-Loop) die das Modell-Quality-Signal
  verwässern. ReAct ist die minimale, modell-direkteste Variante — was
  hier tappt, ist *Modell-* und nicht *Variant-*verhalten.
- **N=2 Repetitions** (nicht N=3). Reicht um Sampling-Noise von
  systematischem Tappen zu unterscheiden — wenn beide Reps tappen ist
  es kein Zufall.
- **7 Cases** (Containment-Familie 5 + Anti-Pattern 2). Naming-Stress
  noch nicht (Fixture fehlt, [[task-read-validation-gap]] T2).

### Run-Bilanz

- Phase 1: 3 Modelle × 1 Variant × 7 Cases × N=2 = **42 Runs**.
- Phase 2 (bedingt): +1 Modell × 1 × 7 × 2 = **+14 Runs**, total max 56.
- Cost-Schätzung beim Compat-Probe-Schritt (T1) konkret beziffern.

## Voraussetzungen (Hard-Block)

1. **Baseline-Run** mit `Qwen/Qwen3.6-27B-FP8` fertig (siehe Task #8 —
   in_progress, läuft gerade). Liefert Vergleichs-Anker für Tier C.
2. **Anti-Pattern-Detection** im Framework live (✅ commits dieser Session
   2026-05-15).
3. **Cortecs OpenAI-Compat-Compatibility-Probe** (T1 unten) — bestätigt
   dass Modell-Pinning und Tool-Calling funktionieren bevor wir auf
   einen großen Run committen.

## Subtasks

### T1 — Cortecs Compatibility-Probe (1 Stunde)

Bevor wir den Bench planen, müssen drei Dinge bestätigt sein:

- **OpenAI-Compat-API** mit `LLM_BASE_URL` + `LLM_MODEL` Pattern.
  Test: einfacher `curl` gegen Cortecs-Endpoint mit `model=gpt-5.4` und
  einfacher Chat-Completion-Request.
- **Modell-Pinning** statt automatisches Routing. Wir wollen *spezifische*
  Modelle messen, nicht „Cortecs wählt das beste für die Frage". Falls
  Pinning nicht funktioniert ist der Bench wertlos.
- **Tool-Calling-Kompatibilität:** der LangGraph-Agent baut Tool-Specs
  im OpenAI-Function-Calling-Format. Manche Provider rewrite das intern.
  Test: kompletten Agent-Lauf gegen Cortecs-Endpoint (1 Frage, 1 Modell)
  und prüfen ob Tool-Calls korrekt durchgehen.

Output: kurze Notiz in `memory/llm_deployment.md` (auto-memory) mit
Cortecs-Endpoint, API-Key-Stelle, bestätigten Modell-IDs.

### T2 — Modell-Auswahl finalisieren

Phase-1-Trio aus dem Cortecs-Katalog festnageln:

**A. Proprietary frontier (weaker-SOTA-hypothesis):**
- GPT 5.4 — vermutlich schwächer als Claude bei Agent/Tools (siehe
  BFCL/τ-bench), damit der billigste Falsifikationspfad.

**B. Largest sovereign open-weight:**
- Aus Cortecs-Katalog das größte als sovereign markierte Modell mit
  Tool-Calling-Support. Top-Kandidaten: Llama-4 Maverick, DeepSeek-V3.5,
  Mistral Large Sovereign. *Welches konkret: nach T1 entscheiden je
  nachdem was Cortecs als sovereign markiert.*

**C. Self-hosted baseline:**
- `Qwen/Qwen3.6-27B-FP8` — 27B dense, FP8-quantisiert, via LiteLLM proxy
  auf eigener H200 (alias `qwen36-27b`), Baseline aus Task #8. **Wichtig
  fürs Paper-Argument:** das ist ein *kleines + quantisiertes* Modell
  (27B dense in FP8, deutlich unter typischem Cloud-Frontier-Footprint).
  Damit wird die Deployment-Story schärfer: kleines, quantisiertes,
  lokales Modell + MCP-Validator schlägt großes unquantisiertes
  Cloud-Modell ohne Validator.

Phase 2 (bedingte Eskalation):
- Claude Opus 4.6 — nur falls Phase 1 zeigt dass GPT 5.4 alle Anti-Patterns
  sauber vermeidet, sonst überflüssig.

Cost-Schätzung pro Run: ~2k input + 1k output Tokens × 5–15 Tool-Calls.
Bei aktuellen Frontier-Preisen grob ~10–20 € für die GPT-Phase
(42 Runs × ~0,30 € avg), Open-Weight via Cortecs deutlich günstiger.
**Konkrete Zahlen nach T1 + Cortecs-Pricing-Check.**

### T3 — Bench-Infrastruktur

Zwei Optionen:

**(a) Agent-Restart pro Modell (einfach, sequenziell):**
- `.env.cortecs-gpt54`, `.env.cortecs-sovereign`, etc. als Overlays.
- `down.sh && up.sh --cortecs-<name>` zwischen den Modellen.
- Run-Framework bleibt unverändert.
- Cost: ~5 min Restart × 3 Modelle (Phase 1) + ggf. 1 (Phase 2) =
  15–20 min Overhead, akzeptabel.

**(b) Multi-Endpoint-Agent (komplex, parallel):**
- Agent-API um Modell-Parameter erweitern, der intern an einen
  konfigurierten LLM-Pool routet.
- Größere Code-Änderung, bricht möglicherweise bestehende Open-WebUI-
  Integration.
- Nur lohnenswert wenn wir den Multi-Modell-Pattern eh in Production wollen.

**Empfohlen: (a) für Paper-Bench, (b) optional als Future Work** falls
Cortecs als Routing-Backend produktiv genutzt wird.

### T4 — Bench-Run + Auswertung

**Phase 1 (Default):**

- 3 Modelle (GPT 5.4 / sovereign-open-weight / `Qwen/Qwen3.6-27B-FP8`)
  × ReAct × 7 Cases × N=2 = 42 Runs.
- Identisches Cases-Set wie Baseline-Run: Containment-Familie (5) +
  Anti-Pattern (2). Naming-Stress noch nicht (Fixture fehlt,
  siehe [[task-read-validation-gap]] T2).
- Resultate in `tests/agent-tests/results/cortecs_frontier/phase1/`
  archivieren, JSON + Markdown-Summary.
- **Entscheidungsregel** nach Phase 1:
  - Wenn GPT 5.4 in ≥1 Case Anti-Pattern-Violations oder Pass-Rate < 1.0
    zeigt → **These empirisch bestätigt**, Phase 2 entfällt.
  - Wenn GPT 5.4 in allen 7 Cases sauber pass → **Phase 2 starten**
    um zwischen „GPT-5.4-Einzelfall" und „SOTA generell" zu unter-
    scheiden.

**Phase 2 (bedingte Eskalation, nur falls Regel ausgelöst):**

- Claude Opus 4.6 × ReAct × 7 Cases × N=2 = 14 Runs.
- Resultate in `tests/agent-tests/results/cortecs_frontier/phase2/`.

**Auswertung (über alle gefahrenen Phasen):**

- **Pro Modell × Case:** Pass-Rate aus N=2.
- **Anti-Pattern-Hit-Rate:** Wie oft macht das Modell den idShort-
  CONTAINS-Lookup trotz Manual? Wichtigste Zahl, weil sie unabhängig
  vom Antwort-Inhalt detektiert wird (Cypher-Args-Inspection).
- **3-Punkte-Vergleich:** GPT 5.4 vs. largest-sovereign vs. Qwen3.5 —
  unterscheiden sie sich *signifikant*? Bei nur N=2 keine echte
  Statistik möglich, aber 0/2 vs. 2/2 ist auch ohne Statistik klar
  interpretierbar.
- **Tabelle für Paper** (3 oder 4 Zeilen je nach Phase):
  `Modell × Pass-Rate × Anti-Pattern-Hit-Rate × Tool-Calls-Avg`.

### T5 — Paper-Einbindung

**Wenn GPT 5.4 tappt (Phase 1 reicht):**

- Section *„Failure modes persist across model scale"* mit der 3-Zeilen-
  Tabelle (GPT 5.4 / sovereign-open-weight / Qwen3.5) als Headline.
- Klammer-Absatz von [[task-paper-layered-determinism-thesis]] kriegt
  die empirischen Zahlen direkt eingebaut.
- 1 zusätzlicher Absatz „EU-sovereign deployment options" mit Cortecs
  als konkretes Beispiel — verstärkt die Sovereignty-Story und macht
  die 3-Punkte-Linie (proprietary-frontier-EU-residency / sovereign-
  open-weight / self-hosted) zum Deployment-Spektrum-Schaubild.

**Wenn GPT 5.4 alles sauber löst (Phase 2 ausgelöst):**

- Mit Claude-Phase-2-Daten: falls Claude *auch* sauber → schwächere
  Form der These im Paper. „Current SOTA frontier models comply with
  manuals on these patterns; smaller models do not. MCP-validation
  remains the safe deployment choice because (a) failure rate is never
  measured zero in larger samples (BFCL), (b) EU AI Act requires
  deterministic controls regardless." Fokus auf Deployment + Regulatorik.
- Falls Claude tappt aber GPT nicht → interessant: zwischen-vendor-
  Inkonsistenz, das ist auch ein Argument („Compliance ist nicht
  reproduzierbar über Modell-Wechsel hinweg → deterministischer Mantel
  unerlässlich für stabile Deployments").

Beide Ausgänge sind belastbar — der wissenschaftliche Wert ist die
empirische Messung, nicht ein vorausgesetztes Ergebnis.

## Acceptance Criteria

- Cortecs-Compatibility-Probe dokumentiert in `llm_deployment.md`.
- Phase-1-Modell-Liste (3 Modelle) konkret festgenagelt: GPT 5.4,
  ein largest-sovereign-open-weight, `Qwen/Qwen3.6-27B-FP8`-Baseline.
- Phase-1-Bench-Run gefahren (42 Runs), Rohdaten in
  `tests/agent-tests/results/cortecs_frontier/phase1/`.
- Entscheidungsregel nach Phase 1 dokumentiert ausgewertet (tappt GPT
  oder nicht?) und Phase 2 entweder begründet ausgelassen oder
  begründet gefahren.
- 3-Punkte-Tabelle (oder 4 mit Phase 2) erzeugt mit Pass-Rates und
  Anti-Pattern-Hit-Rates pro Modell.
- Auswertung dokumentiert welche Form der Layered-Determinism-These
  empirisch belegt ist (starke / mittlere / schwache Form).
- Cost-Bilanz dokumentiert (tatsächliche Cortecs-Kosten vs. Schätzung).
- Paper-Einbindung entschieden — entweder als eigene Subsection oder als
  Tabelle in der Layered-Determinism-Klammer.

## Open Questions

- **Cortecs-Pricing pro Modell:** nicht spekulieren, beim ersten Probe-
  Call abklären. Beeinflusst N (Repetitions) — wenn ein Run zu teuer ist,
  reduzieren wir auf N=1 für Tier 1.
- **Modell-Pinning vs. Auto-Routing:** falls Cortecs nur Auto-Routing
  bietet ist der Bench unbrauchbar — wir messen dann „was Cortecs für
  optimal hält", nicht spezifische Modelle. Kritisches Compat-Probe-Element.
- **Tool-Call-Konfiguration:** falls Cortecs intern OpenAI-Function-Calling
  in ein anderes Format rewrites, kann das Bias einführen. Mit dem
  Compat-Probe-Run prüfen.
- **Trotzdem Future Work:** Naming-Stress-Run gegen Tier 1 + 2. Braucht
  die Fixtures aus [[task-read-validation-gap]] T2; falls die zeitlich
  passen, gleichzeitig mit T4 dieses Tasks fahren.

## References

- Cortecs.ai (Anker): https://cortecs.ai/ — EU-sovereign LLM routing,
  Principles: EU-native clouds, data residency, GDPR-compliant, no training.
- Hauptthese: [[task-paper-layered-determinism-thesis]].
- Anekdoten-Tasks: [[task-paper-modeling-vs-pragmatics-anecdote]],
  [[task-paper-read-validation-anecdote]], [[task-write-tool-validation-gap]].
- Test-Framework: `tests/agent-tests/`, mit `forbidden_cypher_patterns`
  als zentralem Mess-Mechanismus.
- Engineering-Position: [[feedback-agent-constraint-philosophy]] (auto-memory).
- Deployment-Memory: `llm_deployment.md` (auto-memory) — `Qwen/Qwen3.6-27B-FP8`
  Baseline; wird durch T1 erweitert.
