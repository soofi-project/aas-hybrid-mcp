---
name: Task – Gemma-3 Neo4j Text-to-Cypher Eval
description: Neo4j-fine-tuned Gemma-3 (4B/9B/27B) in Eval-Suite aufnehmen und Failure-Mode vs. Qwen3.5-08b vergleichen
type: task
status: open
priority: medium
---

## Background

Die kleinen Qwen3.5-Modelle (≤9B) versagen nicht am Tool-Calling selbst, sondern
an der Query-Qualität: SQL statt Cypher, erfundene Template-Namen, Validator-Rejections,
und Halluzinations-Fallback wenn Queries scheitern (belegt in bench_b judged-Daten,
`results/qwen35-08b/t07/qwen35-08b_bench_b_N10_T07_judged.json`).

Neo4j hat Gemma-3-Instruct (4B/9B/27B) auf `text2cypher-2024v1` nachtrainiert
(HuggingFace: `neo4j/text-to-cypher-Gemma-3-4B-Instruct-2025.04.0` u.a.).
Da Basis Gemma-3-Instruct ist, erben diese Modelle Tool-Calling.

Forschungsfrage: Löst das Cypher-Finetuning die SQL-vs-Cypher-Fehler,
oder versagen die Modelle an Template-Namen-Halluzination und Validator-Rejections
genauso wie Qwen-08b?

## Subtasks

### T1 — LiteLLM-Aliase auf H200 konfigurieren
Modelle von HuggingFace pullen und LiteLLM-Aliases anlegen:
- `gemma3-neo4j-4b` → `neo4j/text-to-cypher-Gemma-3-4B-Instruct-2025.04.0`
- `gemma3-neo4j-9b` → HuggingFace-ID vorab verifizieren
- `gemma3-neo4j-27b` → HuggingFace-ID vorab verifizieren

Größen: 4B ≈ 8 GB, 9B ≈ 18 GB, 27B ≈ 54 GB BF16 — passen einzeln auf H200.

### T2 — `.env.model.*` Dateien anlegen
Drei Dateien analog zu `.env.model.qwen35-4b`:
- `C:\repo\soofi\aas-hybrid-mcp\.env.model.gemma3-neo4j-4b`
- `C:\repo\soofi\aas-hybrid-mcp\.env.model.gemma3-neo4j-9b`
- `C:\repo\soofi\aas-hybrid-mcp\.env.model.gemma3-neo4j-27b`

### T3 — `eval-model.sh` SLUGS-Liste erweitern
`gemma3-neo4j-4b`, `gemma3-neo4j-9b`, `gemma3-neo4j-27b` in die SLUGS-Variable
eintragen. Cortecs-Bedingung bleibt unverändert (alle drei laufen lokal).

### T4 — Pilot-Lauf (bench_b, N=3, T=0.7)
```bash
./eval-model.sh gemma3-neo4j-4b
cd tests/agent-tests
python run_tests.py --cases cases/bench_b.yaml --repetitions 3 \
  --temperature 0.7 \
  --export results/gemma3-neo4j-4b_bench_b_N3_T07_pilot.json
```
Failure-Mode klassifizieren anhand `tool_call_count` und `process.tool_errors`:
- SQL-Fehler → kein Vorteil ggü. Qwen-08b
- Korrekte Cypher, falsche Templates → Finetuning hilft partiell
- tc=0 → Tool-Calling durch Finetuning beschädigt (dann T=0.0 testen)

### T5 — Volle Suite (wenn Pilot sinnvoll)
```bash
./run_all.sh gemma3-neo4j-4b 0.7
./run_all.sh gemma3-neo4j-9b 0.7
./run_all.sh gemma3-neo4j-27b 0.7
```

### T6 — Ergebnis in Paper einarbeiten
- §Eval: Gemma-Zeile in Eval-Tabelle, Failure-Mode-Vergleich mit Qwen-08b
- §Future Work: "Combining Cypher fine-tuning [neo4j/text2cypher-2024v1] with
  template-name grounding (RAG or in-context examples)" als konkreten Pfad

## Acceptance Criteria

- Pilot-JSON vorhanden, Failure-Mode eindeutig klassifiziert
- Bei sinnvollem Verhalten: volle Suite für 4B/9B/27B gelaufen
- Paper §Future Work nennt `neo4j/text2cypher-2024v1` als Datensatz-Cite
- Confounder (Modellfamilie Gemma vs. Qwen) im Paper transparent gemacht

## References

- Pilot-Daten Qwen-08b: `tests/agent-tests/results/qwen35-08b/t07/qwen35-08b_bench_b_N10_T07_judged.json`
- Eval-Setup: `eval-model.sh`, `tests/agent-tests/run_all.sh`
- Verwandte Tasks: `[[task-paper-pattern-modelsize-eval]]`
