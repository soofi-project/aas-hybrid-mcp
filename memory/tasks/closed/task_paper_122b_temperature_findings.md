---
name: Task – 122B MoE Temperature-Befund ins Paper einbauen
description: §11 Discussion + §10 Evaluation um empirische Evidenz für T=0 am Executor ergänzen, sobald T=0.0-Runs vorliegen
type: task
status: open
priority: medium
---

## Background

Die aktuelle §11-Discussion (Absatz „The Necessity of Enforcement", Zeilen 24–31) argumentiert
bereits theoretisch für per-role temperature assignment: T=0 am Executor-Agenten, T=0.7 am
Orchestrator. Dieser Claim war bisher rein architektonisch begründet.

Die qwen35-122b-Eval-Daten (T=0.7) liefern die erste empirische Evidenz für diese These:
- 229/230 Runs: `tool_call_count=0` — das Modell tritt nicht in die Tool-Use-Schleife ein
- Ursache: T=0.7 bricht Function-Calling beim 122B-A10B-MoE-Checkpoint
- T≈0 (aus anderem Projekt bekannt) rehabilitiert das Modell vermutlich

Blockierend: T=0.0-Testläufe für alle Modelle der Qwen3.5-Familie müssen erst abgeschlossen sein.
Erst dann ist der Claim belastbar genug fürs Paper.

## Update 2026-05-22 — T=0-Hypothese widerlegt

Getestet auf Cortecs AI (externer Endpunkt, kein vLLM-Konfig-Artefakt):
- 122b führt auch bei T=0.7 nur selten Tool Calls aus — das Problem ist modell-seitig, nicht konfigurationsbedingt
- T=0.0 ist sogar schlechter: Greedy Decoding → deterministischer Loop, Modell wiederholt dieselbe
  Abfrage endlos weil kein Sampling-Rauschen zur Exploration zwingt

**Konsequenz für Paper-Eval:** T=0.0 wird aus dem gesamten Eval-Protokoll gestrichen.
Alle Paper-Eval-Läufe (alle Modelle, alle Suiten) laufen ausschließlich mit **T=0.7**.
Begründung für Paper: agent tasks require exploratory sampling — greedy decoding causes
deterministic failure loops in multi-step tool use; T=0.7 follows standard practice
from BFCL and AgentBench.

**Konsequenz für diese Task:** Die Subtasks T1–T3 (T=0.0-Runs, §11-Satz, Eval-Tabellen-Caveat)
sind obsolet in ihrer ursprünglichen Form. 122b bleibt aus dem quantitativen Vergleich
ausgeschlossen (→ [[task-paper-122b-tool-call-footnote]]). §11-Satz muss neu formuliert werden:
nicht „T=0 rehabilitiert das Modell", sondern „T=0 verstärkt das Problem durch Greedy-Loop".

## Subtasks

### T1 — T=0.0-Runs auswerten

Nach Abschluss aller Modellläufe bei T=0.0:
- `tests/agent-tests/results/qwen35-122b_*_judged.json` prüfen
- Vergleich: war T=0.7 → ~0% Tool-Calls, T=0.0 → deutlich höhere Tool-Call-Rate?
- Falls ja: Befund als Existenz-Claim formulierbar ("at T=0.7 the 122B MoE failed to engage
  the tool-use API in 229/230 runs; re-running at T=0.0 restored function-calling behaviour")

### T2 — §11 Discussion: einen Satz empirische Evidenz einfügen

Im Absatz „The Necessity of Enforcement", nach dem T=0/T=0.7-Satz:

Ziel: einen Satz ergänzen der den 122B-Befund als Beleg zitiert.
Entwurf: *"This effect was observed empirically: at $T=0.7$, the 122\,B MoE model
(\texttt{Qwen3.5-122B-A10B}) produced zero tool calls in $229/230$ runs, generating
free-text reasoning instead of structured function invocations; lowering to $T=0$
restored function-calling behaviour, confirming that temperature assignment is a
deployment prerequisite, not merely an optimisation."*

Datei: `paper/etfa2026/content/11-discussion.tex`

### T3 — §10 Evaluation: 122B-Zeile mit T-Caveat versehen

In der Eval-Tabelle (§10) die 122B-Zeile mit Fußnote oder Klammer-Hinweis versehen:
„results at T=0.7; re-run at T=0.0 in progress" oder nach T=0.0-Confirmation:
„T=0.7 results shown; T=0.0 restores function-calling (see §11)"

Datei: `paper/etfa2026/content/10-evaluation.tex`

## Acceptance Criteria

- [ ] T=0.0-Runs für qwen35-122b abgeschlossen und ausgewertet (bestätigt oder widerlegt)
- [ ] Falls bestätigt: §11 Discussion enthält empirischen Satz mit konkreten Zahlen
- [ ] §10 Eval-Tabelle referenziert T-Caveat für 122B-Zeile
- [ ] Build erfolgreich (`python .claude/skills/paper/build_paper.py`)
- [ ] Kein neuer Bib-Key nötig (eigene Messdaten, kein Fremdcite)

## References

- Paper §11: `paper/etfa2026/content/11-discussion.tex` (Zeilen 24–31 — bestehender T=0/T=0.7-Absatz)
- Paper §10: `paper/etfa2026/content/10-evaluation.tex`
- Rohdaten 122b T=0.7: `tests/agent-tests/results/qwen35-122b_*_judged.json`
- Cross-model Analysis: `tests/agent-tests/results/analysis.md` (Abschnitt §6 + MoE-Warnung)
- Verwandte Tasks: [[task-paper-pattern-modelsize-eval]]
