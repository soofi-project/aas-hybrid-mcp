---
name: Task – CRAG-Parser-Bug `int('E0')` bei nicht-Qwen-LLM-Output
description: crag_nodes.py:335 crasht beim Parsen von item_idx wenn LLM-Output nicht im Qwen-Format ist. Blockt Cortecs-Frontier-Eval (GPT 5.4, Claude Opus 4.6) für CRAG-Variant. Aus Out-of-Scope-Notiz von task_container_location_traversal_prompt_fix.md.
type: task
status: open
priority: high
---

## Background

Live-Test 2026-05-14 (ohne vLLM, GPT-5.4-mini Backend) zeigte:

```
CRAG: 500 — Parse-Bug int('E0') in crag_nodes.py:335
```

Der Parser erwartet `item_idx` als reine Ziffernfolge (Qwen-Output-Form),
bekommt aber String-Konstrukte wie `E0` (vermutlich aus GPT-Output mit
Enumeration-Format) und crasht beim `int()`-Cast.

Wurde damals als Out-of-Scope notiert weil Bench B mit Qwen lief und der
Bug dort nicht auftrat. **Mit [[task-paper-cortecs-frontier-eval]] wird
das aber kritisch:** der ganze Phase-1-Bench für CRAG würde an diesem
Bug platzen, weil GPT 5.4 und das größte sovereign-Open-Weight nicht
Qwen-Format liefern.

## Goal

`crag_nodes.py:335` (oder wo immer der Parser-Crash sitzt — kann sich
durch spätere Edits verschoben haben) robuster machen, sodass alle
gängigen LLM-Output-Formate sauber geparst werden.

## Subtasks

### T1 — Bug lokalisieren

- Genauen Code-Spot in `aas-agent/src/aas_agent/crag_nodes.py` finden
  (Zeilennummer kann gewandert sein seit 2026-05-14).
- Kontext: was wird geparst? Vermutlich Index aus einem Listings-Output
  („Item 1: ..., Item 2: ..., E0: ...") oder ähnlich.

### T2 — Robust-Parsing implementieren

Optionen:

- **(a) Defensive `int()`** mit try/except + Skip-Strategie:
  ```python
  try:
      idx = int(raw_idx)
  except ValueError:
      log.warning("Skipping unparseable item_idx %r", raw_idx)
      continue
  ```
  Schnell, aber kann zu silent-skip führen wenn alle Items ein anderes Format haben.

- **(b) Structured-Output via `response_format={"type":"json_object"}`**
  oder Pydantic-Schema enforcen — LLM liefert garantiert geparste
  Struktur. Sauberer, aber model-dependent (nicht alle Modelle support'en
  structured output gleich gut).

- **(c) Regex-basierter Extractor** der `item_idx` aus jeder gängigen
  Output-Form pullt: `\bItem\s+(\d+)\b`, `\b(\d+)\.\s`, `^\s*-\s*(\d+)`,
  etc. Pragmatisch, deckt die Vielfalt ab, kommt mit Edge-Cases klar.

**Empfehlung:** (b) wenn alle Ziel-Modelle structured-output sauber
können (Cortecs-Compat-Probe in #14 T1 klärt das); sonst (c) als Fallback.

### T3 — Unit-Tests

`aas-agent/src/tests/test_crag_parser.py` (neu, falls nicht vorhanden):

- Test-Inputs aus den Output-Formaten von Qwen, GPT 5.4, Claude Opus 4.6
  (jeweils 1–2 Echt-Beispiele aus interaction-protocol-Traces).
- Pro Input: Parser darf nicht crashen, soll plausible Item-Indices
  liefern oder sauber leere Liste.

### T4 — Cortecs-Bench-Sanity vor Phase 1

Bevor [[task-paper-cortecs-frontier-eval]] Phase 1 startet: einen
einzelnen CRAG-Run gegen GPT 5.4 + Claude Opus 4.6 als Smoke fahren.
Wenn das durch ist, ist Phase 1 für CRAG safe.

## Acceptance Criteria

- Bug-Location aktuell verifiziert (Zeilennummer + Funktion).
- Robust-Parsing implementiert, unter mindestens 3 verschiedenen
  LLM-Output-Formaten getestet.
- Unit-Tests im Repo, laufen grün.
- Smoke-Run mit GPT 5.4 + Claude Opus 4.6 CRAG-Variant erfolgreich.
- Notiz in [[task-paper-cortecs-frontier-eval]] T1: „Voraussetzung
  CRAG-Parser-Fix erfüllt" oder „CRAG aus Phase 1 ausgenommen wegen
  ungelöstem Bug".

## Open Questions

- **Sind das die einzigen output-format-abhängigen Parser-Stellen?** Plan
  und Reflexion haben auch Custom-Parser (`crag_nodes.py`, `agent_plan_nodes.py`,
  `reflexion_graph_nodes.py`). Im Audit ([[task-variant-faithfulness-audit]])
  T2/T3 mit-prüfen ob die gleiche Robustheits-Lücke da auch existiert.
- **Structured-Output-Kompatibilität:** Cortecs-Compat-Probe muss zeigen
  ob alle Ziel-Modelle structured output supporten. Falls nicht, fällt
  Option (b) und wir machen (c) als universellen Fallback.

## References

- Ursprungs-Notiz: `task_container_location_traversal_prompt_fix.md` „Out of Scope".
- Verwandt: [[task-paper-cortecs-frontier-eval]] — blockt durch diesen Bug.
- Verwandt: [[task-variant-faithfulness-audit]] — gleiche Robustheits-Lücke
  in Plan/Reflexion-Parsern mit-prüfen.
- Verwandt: [[task-crag-failure-deep-dive]] — vielleicht trägt der Bug
  zur 40%-Pass-Rate bei wenn er gelegentlich auch mit Qwen triggert.
- Live-Test-Befund: 2026-05-14 Curl-Tests (GPT) und
  `interaction-protocol/2026-05-14T17-50-30Z__1962b4110f55/`.
