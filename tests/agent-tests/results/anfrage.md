Analysiere die Eval-Results in c:\repo\soofi\aas-hybrid-mcp\tests\agent-tests\results\qwen35-2b\t07 und schreibe eine analysis.md (auf Englisch) in denselben Ordner.

## Schritt 1: Statistiken berechnenf

Führe das Helper-Script aus:
```
python tests/agent-tests/compute_eval_stats.py tests/agent-tests/results/qwen35-2b/t07 -o tests/agent-tests/results/qwen35-2b/t07/stats.json
```

Lies dann die `stats.json` — sie enthält alle harten Zahlen. Du musst die 50KB-Roh-JSONs **nicht** mehr selbst parsen.

## Schritt 2: analysis.md schreiben

Brauche 8 Sections:

1. **Paper-Evaluation-Tabelle pro Suite** — N, Correct, Manuals first, idShort violation, Bypass (pse), Median correct/wrong. Alle Zahlen aus stats.json → suites.*.paper_row + totals.paper_totals
2. **idShort violation self-correction rate** — aus stats.json → suites.*.idshort_detail + totals.violation_rules_merged. Self-correction rate aus paper_row.idshort_self_corrected_rate
3. **Write-Path Bypass** — aus stats.json → totals.bypass_stats (bypass_type_distribution, bypass_per_case, put_submodel_element_called). Nur bei SRN-Suites vorhanden
4. **Template Validation** — aus stats.json → suites.*.template_validation. Ob put_submodel/put_submodel_element rejections aufgetreten sind
5. **Judge failure modes pro SRN-Case** — aus stats.json → totals.judge_failure_modes (missing_facts + wrong_claims Frequencies pro Case)
6. **Duration: Median pro Suite** — aus stats.json → suites.*.paper_row.median_duration_correct/wrong + suites.*.duration_per_case (SRN per-case)
7. **Manuals-first Korrelation** — aus stats.json → totals.manuals_first_contingency (2x2 Tabelle)
8. **Key Takeaways / Action Items** — interpretive Section, nicht im stats.json. Was müssen wir am System fixen? Welche Muster fallen auf?

## Wichtige Hinweise

- Die stats.json enthält **nur** die harten Zahlen. Die erzählerischen Verknüpfungen, Root-Cause-Erklärungen und Action Items musst du selbst formulieren.
- Verarbeite die 5 Suites **parallel mit je einem Sub-Agenten**, der die jeweilige Suite-Section aus der stats.json liest und eine Text-Zusammenfassung liefert.
- Falls ein Vergleich mit einem anderen Modell gewünscht ist, lies dessen analysis.md und vergleiche. Sonst weglassen.
- Quelldateien (falls du doch in die Rohdaten musst): *_judged.json für Judge/Process-Daten, *.json (ohne judged) für raw eval/write_path-Daten. Cases in cases/srn_autonomous.yaml.
