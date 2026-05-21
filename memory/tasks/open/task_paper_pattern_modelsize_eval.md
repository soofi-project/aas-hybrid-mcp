---
name: Task – Paper-Eval „Modellgröße × Validator" — ReAct-only, N=10
description: ReAct-only Eval über Qwen3.5 0.8B→397B + Qwen3.6-27B/35B; N=10 pro Suite; Bench B (Retrieval) + Bench C (Write-Path); Reflexion aus Eval ausgeschlossen (same-model self-eval, §12 begründet).
type: task
status: open
priority: high
---

## Summary

Der ursprüngliche Bench-B-Variant-Vergleich (ReAct/Plan/CRAG/Reflexion auf
Qwen3.6-27B) hat sich in der Diskussion als methodisch unsauber erwiesen:
die vier Patterns sind backend-spezifisch verschieden (CRAG nimmt Document-
RAG an, kollidiert mit unserem Cypher-Pfad), die nebeneinander zu stellen
vergleicht Äpfel mit Birnen. Stattdessen pivotiert das Paper auf eine
methodisch saubere Achse:

> **Forschungsfrage:** Bei welcher Modellgröße bricht welches Pattern wegen
> Instruction-Following-Defiziten zusammen — wie weit kann man für
> Edge-fähige Industrial-AI-Agenten runtergehen?

Diese Achse ist:
- **Eindimensional** (Modellgröße innerhalb derselben Familie)
- **Open in der Literatur** (Agentic-RAG-Lit evaluiert meist gegen GPT-4)
- **Direkt SOOFI-anschlussfähig** (Edge-Deployment, lokale Sovereign-Cloud,
  400B-Folgeprojekt als oberer Anker)

Die existierende Layered-Determinism-These ([[task-paper-layered-determinism-thesis]])
bleibt unverändert — sie basiert auf den drei Validation-Gap-Anekdoten
(Write/Read/Pragmatics) und ist orthogonal zum Variant-Vergleich.

## Modell-Matrix

Zwei Achsen: **Qwen3.5** (Skalierung, primäre Forschungsfrage) + **Qwen3.6** (Generations-Vergleich bei 27B und 35B).

### Qwen3.5 — Skalierungs-Achse

| Modell | Active | Slug | Deployment | Rolle |
|---|---|---|---|---|
| Qwen3.5-0.6B-FP8 | 0.6B dense | `qwen35-08b` | lokal H200 | Capability-Floor (erwartet: alle Patterns brechen) |
| Qwen3.5-2B-FP8 | 2B dense | `qwen35-2b` | lokal H200 | Untere Grenze |
| Qwen3.5-4B-FP8 | 4B dense | `qwen35-4b` | lokal H200 | Zwischen 2B und 9B |
| Qwen3.5-9B-FP8 | 9B dense | `qwen35-9b` | lokal H200 | Edge-Kandidat |
| Qwen3.5-27B-FP8 | 27B dense | `qwen35-27b` | lokal H200 | Skalierungs-Midpoint |
| Qwen3.5-122B-A10B-FP8 | 10B active (MoE) | `qwen35-122b` | lokal H200 | Großes lokales On-prem |
| Qwen3.5-397B-A17B-FP8 | 17B active (MoE) | `qwen35-397b` | Cortecs (€0.6/M in, €3.6/M out) | Obere Schranke / Open-Source-Frontier |

### Qwen3.6 — Aktuelle Generation (2 Zusatzpunkte, kein eigener Vergleichs-Anspruch)

| Modell | Active | Deployment | Rolle |
|---|---|---|---|
| Qwen3.6-27B-FP8 | 27B dense | lokal H200 | Aktuelle Generation bei 27B — ergänzender Datenpunkt |
| Qwen3.6-35B-A3B-FP8 | 3B active (MoE) | lokal H200 | Speed-Story: MoE mit Inferenzkosten eines ~3B Dense-Modells |

**Framing im Paper:** Kein "Generationsvergleich" als eigene Forschungsfrage. Qwen3.6 wird als "wir haben auch die aktuellste Modellreihe gecheckt" gerahmt. Der 35B-A3B-Datenpunkt ist für die Deployment-/Edge-Argumentation interessant: 3B active params → Inferenzgeschwindigkeit eines 3B Dense-Modells, aber mit dem Parameterreservoir eines 35B-Modells. Im Paper ein Satz als Ergänzung zur Skalierungs-Diskussion.

**Bestehende Bench-B-Daten (Qwen3.6-27B, N=3, 5 Containment-Cases):** Diese sind *nicht* direkt wiederverwendbar als Qwen3.6-27B-Datenpunkt im neuen Eval-Grid — die 5 Containment-Cases sind ein Subset der B1-B6-Queries, aber das Protokoll muss vor der Wiederverwendung explizit geprüft werden (offene Frage unter § Offene Fragen).

**FP8 wo verfügbar:** Modelle mit offiziellem FP8-Checkpoint (Qwen3.5 ab 27B, Qwen3.6 27B + 35B-A3B) laufen in W8A8-FP8 via vLLM. Kleinere Modelle ohne FP8-Checkpoint (Qwen3.5 0.8B–9B) laufen in BF16. Methodische Begründung: W8A8-FP8 ist im Wesentlichen verlustfrei gegenüber BF16 \cite{kurtic2025bf16} — beide Varianten gelten als methodisch äquivalent. Task [[task-paper-fp8-quantization-cite]] setzt das Cite in die Eval-Sektion (done).

**MoE-Caveat:** 122B, 397B und 3.6-35B sind MoE, der Rest dense. Im Paper:
„Total parameters reported; active-parameter counts at inference marked separately for MoE models."

**Pattern:** Nur **ReAct**. Plan-and-Reflect und Reflexion aus Eval ausgeschlossen:
- Reflexion: same-model self-eval konfundiert Ergebnisse (§12 Limitations begründet das)
- Plan-and-Reflect: Citation (`wang2023plan_solve`) zu weit gedehnt, kein sauberer Beitrag ohne eigene Eval
- CRAG: out-of-scope per [[task-paper-crag-removal-and-reframe]]

**Eval-Budget:** 1 Pattern × 9 Modelle × N=10 = **~810 Runs** (Bench B + Bench C kombiniert).
Cortecs-Kosten (nur 397B, N=10, Bench B+C): ~15–25 €. Judge-Kosten (gpt-5.4-mini): ~1–2 $.
H200-Runs: sequenziell, je ~15–30 Min Reload-Zeit pro Modellwechsel.
Begründung N=10: Existence-Framing — 6 Cases × 10 = 60 Obs. pro Suite reicht für Capability-Floor-Aussagen; kein Anspruch auf präzise Frequenzschätzung.
Script: `tests/agent-tests/run_all.sh` — ReAct-only, N=10 für alle Paper-Eval-Suiten.

## Subtasks

### T1 — Eval-Infrastruktur ✅ Done (2026-05-18)

`eval-model.sh` + `docker-compose.eval-model.yml` + 7 `.env.model.*`-Dateien im Repo-Root.
Workflow: `./eval-model.sh qwen35-27b` → kopiert `.env.model.qwen35-27b` → Stack neu mit Overlay.
Verify: `docker exec aas-agent printenv | grep LLM_MODEL`

### T2 — H200-Vorbereitung (vor erstem Eval-Lauf)

**a) LiteLLM-Aliases auf H200 anlegen** — 5 neue Aliases (bestehender `qwen36-27b` bleibt):

| Alias | HuggingFace-Modell |
|---|---|
| `qwen35-2b` | `Qwen/Qwen3.5-2B-Instruct-FP8` |
| `qwen35-9b` | `Qwen/Qwen3.5-9B-Instruct-FP8` |
| `qwen35-27b` | `Qwen/Qwen3.5-27B-Instruct-FP8` |
| `qwen35-122b` | `Qwen/Qwen3.5-122B-A10B-Instruct-FP8` |
| `qwen36-35b` | `Qwen/Qwen3.6-35B-A22B-Instruct-FP8` |

**b) Cortecs-Setup** (nur für 397B):
- Cortecs API-Key in `~/.env.secrets` als `OPENAI_API_KEY` eintragen
- Exakte Cortecs-URL + Modell-ID in `.env.model.qwen35-397b` prüfen (Cortecs-Dashboard)

**c) Sanity-Check** nach erstem Alias-Setup:
```bash
./eval-model.sh qwen35-27b
docker exec aas-agent printenv | grep LLM_MODEL   # → qwen35-27b
```
Dann eine einzelne B1-Query manuell schicken und auf valide Antwort prüfen.

### T3 — Eval-Läufe (Reihenfolge: Größe aufsteigend)

**Reihenfolge** (H200-Lade-Overhead minimieren, kleine Modelle zuerst):
```
qwen35-08b → qwen35-2b → qwen35-4b → qwen35-9b → qwen35-27b → qwen35-122b
→ qwen36-27b → qwen36-35b → qwen35-397b (Cortecs, letzter Run)
```

**Pro Modell — Phase 1 (Agent-Runs, kein Judge, inkrementell gespeichert):**
```bash
# Aus tests/agent-tests/ ausführen
./eval-model.sh <slug>          # Stack auf neues Modell umschalten
./run_all.sh <slug>             # alle Suites, N=30, OPENAI_API_KEY aus ~/.env.secrets
```

**Phase 2 — LLM-Judge (nachträglich, lokal, kein Agent-Traffic):**
```bash
# OPENAI_API_KEY wird via run_all.sh aus ~/.env.secrets gezogen
python run_tests.py \
  --judge-only results/<slug>_bench_b_N30.json \
  --llm-judge \
  --export results/<slug>_bench_b_N30_judged.json
```

Judge-Modell: **gpt-5.4-mini** (independent judge, family-unabhängig von Qwen; OpenAIs aktuell stärkstes kompaktes Modell; gepinnt für Reproduzierbarkeit; im Paper dokumentieren).
Vollständiger Workflow: `tests/agent-tests/README.md` → Sektion „Paper eval".

### T4 — Cypher-vs-JSON-Hypothese empirisch prüfen

Wenn 2B/9B bei Cypher-affinen Queries (B1, B2) deutlich schlechter
abschneiden als bei Vector-affinen Queries → Evidenz für die Hypothese
aus [[task-paper-future-work-template-cypher]]. Konkret:

- Per-Query-Type-Aufschlüsselung in der Eval-Auswertung
- Wenn signifikanter Gap: Quick Probe mit angereicherten Templates
  (Richtung A aus dem Future-Work-Task) auf dem schwächsten Modell, das
  noch funktioniert
- Ergebnis fließt zurück in den Cypher-Template-Task als T4-Datenpunkt

### T5 — Paper-Sektion „Pattern × Modellgröße" schreiben

- Neue Subsection oder umbenannte Variant-Sektion in `paper/etfa2026/content/`
- Tabelle mit Erfolgsquoten pro Modell × Pattern — zwei Blöcke: Qwen3.5 (Skalierung) + Qwen3.6 (Generation)
- Generations-Interpretationslinie: „Größe ist nicht alles — neuere Modelle schlagen ältere bei gleicher Parameterzahl"
- Existence-Framing (nicht Frequency-Estimation)
- Caveats: MoE-vs-dense, N=30, eine einzige Modellfamilie, Qwen3.6 nur 2 Punkte
- Hook auf SOOFI-400B-Folgeprojekt als praktischer Anwendungsfall
- Limitation: nur Qwen-Familie — Verallgemeinerung auf Llama/DeepSeek offen
- FP8-Methodology-Satz mit \cite{kurtic2025bf16} (delegiert an [[task-paper-fp8-quantization-cite]])

## Acceptance Criteria

- 7 Modell-Konfigurationen aufrufbar (5 Qwen3.5 + 2 Qwen3.6, lokal + Cortecs)
- Stack läuft mit Qwen3.5-27B-FP8, sanity-check mind. 1 Replicate gegen B1-B6
- Eval-Ergebnisse als CSV/JSON in `tests/agent-tests/results/` getrennt nach Modell × Pattern
- Paper-Sektion ersetzt den alten Variant-Vergleich; Bench-B-Daten als ein Datenpunkt eingebettet
- MoE-Caveat und FP8-Methodology-Satz (\cite{kurtic2025bf16}) in Paper
- Cypher-vs-JSON-Aufschlüsselung beantwortet (oder explizit „kein signifikanter Gap")
- Qwen3.6-27B-Bench-B-Daten: Entscheidung dokumentiert, ob wiederverwendbar oder neuer Run

## Non-Goals

- Kein N>10 — Existence-Framing; Suite-Aggregation (6 Cases × N=10 = 60 Obs.) gibt ausreichend Abdeckung
- Kein Vergleich gegen ChatGPT/Claude — würde Data-Sovereignty-Story
  verwässern und zwei Achsen confounden
- Kein Cross-Family-Vergleich (Llama/DeepSeek) — Limitation, nicht Aufgabe
- Keine CRAG-Variante in der neuen Eval — sauber out-of-scope per
  [[task-paper-crag-removal-and-reframe]]

## Offene Fragen

- **Bench-B-Daten-Wiederverwendung:** Sind die 5 Containment-Cases aus `containment_hall4_baseline_N3.json` ein vollständiges Subset von B1-B6? Falls ja und Protokoll stimmt (gleiche Nudge-Regel, gleiche Multi-Turn-Grenze), können die Qwen3.6-27B-Läufe als Datenpunkt eingebettet werden — sonst neuer Run nötig.
- Reichen B1-B6 für die Skalierungs-Aussage, oder braucht es Queries mit gestaffelter Schwierigkeit?
- 4B und 0.6B (08b) wurden aufgenommen — Skalierungs-Achse ist jetzt vollständig.
- Thinking-Mode konstant `false` halten (`AGENT_DEFAULT_THINKING`), nicht als Variable mitvariieren — Confound vermeiden.

## References

- Stack-Compose: `docker-compose.yml`, `docker-compose.vllm.yml`
- Bench-B-Protokoll: `memory/bench_b_evaluation.md`
- Bestehende Eval-Daten: `tests/agent-tests/results/containment_hall4_baseline_N3.json`
- Verwandte Tasks:
  - [[task-paper-crag-removal-and-reframe]] — Paper-Text-Anpassung
  - [[task-paper-future-work-template-cypher]] — T4 dieser Task liefert
    den ersten empirischen Datenpunkt für deren Trigger-Bedingungen
  - [[task-paper-layered-determinism-thesis]] — bleibt unverändert,
    orthogonal zur neuen Achse
- Memory-Notiz Qwen3.5-Familie + Cortecs-Verfügbarkeit: siehe Diskussion
  vom 2026-05-16
- Externe Lit für neue Bib-Anker (in Paper-Task abzuarbeiten):
  Huang et al. 2023 „LLMs Cannot Self-Correct Reasoning Yet", BFCL
