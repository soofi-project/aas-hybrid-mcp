---
name: Task – Paper Eval Table Exporter
description: Script das Eval-Result-JSONs nach Tag-Gruppen aggregiert und eine paper-fertige Bypass-Tabelle ausgibt; läuft nach den SRN-Bypass-Eval-Runs.
type: task
status: open
priority: medium
---

## Background

`reporter.py` gibt per-Run- und per-Variant-Tabellen auf der Konsole aus — für das
Paper brauchen wir eine aggregierte Ansicht **nach Query-Gruppe** (via `tags` in den
Case-Dateien) mit Bypass-Typ-Verteilung. Diese Auswertung macht erst Sinn wenn die
Eval-Runs gelaufen sind.

Das neue `write_path`-Feld im Evaluator (`bypass_type`: correct / surfaced / cascade
/ direct) liefert die Rohdaten. Das Script liest die Result-JSONs und produziert eine
Tabelle die direkt in §10-Evaluation übertragen werden kann.

**Warum Query-Gruppen statt Einzelfragen im Paper:**
Einzelne Case-Namen (`srn_bypass_spatial_hall4`) sind zu spezifisch. Im Paper steht
eher eine Gruppenzeile wie „SRN Creation (N=6)" mit aggregierten Bypass-Quoten.
Die Gruppe ergibt sich aus dem `paper_anecdote`-Tag oder einem dedizierten
`paper_group`-Feld in den Cases.

## Subtasks

### T1 — `paper_group`-Feld in Case-Schema ergänzen

`framework/cases.py`: optionales Feld `paper_group: str | None = None`.

Cases in `srn_bypass.yaml` und `srn_ablation_variant_a.yaml`:
```yaml
paper_group: "SRN Write-Path"
```

Cases in `bench_b.yaml` die ins Paper kommen:
```yaml
paper_group: "Read / Spatial Disambiguation"
```

Ohne `paper_group` → Case wird in Aggregation übersprungen (kein Rauschen durch
Hilfs-Cases die nicht ins Paper gehören).

**Status:** ⬜ Open

### T2 — `aggregate_paper_table.py` schreiben

Neues Script: `tests/agent-tests/aggregate_paper_table.py`

```
python aggregate_paper_table.py results/srn_bypass_react_N3.json [results/...] \
    [--format markdown|latex] [--out paper_table.md]
```

Aggregationslogik:
1. Alle RunRecords aus den JSON-Dateien laden
2. Nach `paper_group` gruppieren (Cases ohne `paper_group` überspringen)
3. Pro Gruppe: N Runs, Pass-Rate, Bypass-Typ-Counts

Output-Spalten:

| Query Group | N | Pass% | correct | surfaced | cascade | direct |
|---|---|---|---|---|---|---|
| SRN Write-Path | 6 | 33% | 2 | 0 | 3 | 1 |

Bei `--format latex`: LaTeX-Tabelle mit `booktabs`-Style direkt in
`paper/etfa2026/content/` schreiben oder als Snippet ausgeben.

**Status:** ⬜ Open

### T3 — `paper_group` in bestehende Cases eintragen

Nach T1: alle Cases in `srn_bypass.yaml`, `srn_ablation_variant_a.yaml`,
`containment_hall4.yaml` (Bench-B-Subset) mit `paper_group` versehen.

Mapping (vorläufig):
- `srn_bypass.yaml` → `"SRN Write-Path"`
- `srn_ablation_variant_a.yaml` → `"SRN Write-Path (Prompt-Hint)"`
- containment + read-validation Cases → `"Read / Graph Query"`

**Status:** ⬜ Open

### T4 — Eval-Run fahren + Tabelle generieren

Erst wenn T2+T3 fertig und SRN-Bypass-Eval-Runs (N=3) gelaufen sind:
```
python aggregate_paper_table.py results/srn_bypass_react_N3.json --format latex
```
Output in Paper-Task `task_paper_write_validation_defense.md` T4 einfließen lassen.

**Status:** ⬜ Open (blockiert durch Eval-Runs)

## Acceptance Criteria

- [ ] `paper_group`-Feld in `cases.py` vorhanden, optional
- [ ] `srn_bypass.yaml` und `srn_ablation_variant_a.yaml` haben `paper_group` gesetzt
- [ ] `aggregate_paper_table.py` läuft gegen Result-JSONs und produziert korrekte Tabelle
- [ ] Bypass-Typ-Counts stimmen mit manuell nachgezählten `write_path.bypass_type`-Werten überein
- [ ] LaTeX-Output direkt in Paper-Sektion verwendbar (booktabs, keine manuellen Korrekturen nötig)

## References

- Evaluator: `tests/agent-tests/framework/evaluator.py` (`WritePathAnalysis`)
- Reporter: `tests/agent-tests/framework/reporter.py`
- Case-Schema: `tests/agent-tests/framework/cases.py`
- Test-Cases: `tests/agent-tests/cases/srn_bypass.yaml`, `srn_ablation_variant_a.yaml`
- Paper-Section: `paper/etfa2026/content/10-evaluation.tex`
- Verwandte Tasks: [[task-write-tool-validation-gap]], [[task-paper-write-validation-defense]], [[task-srn-slotfilling-tool-and-eval]]
