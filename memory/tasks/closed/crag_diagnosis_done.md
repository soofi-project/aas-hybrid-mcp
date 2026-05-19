---
name: CRAG Diagnose Done — Out of Paper Scope nach Pivot 2026-05-16
description: Stream-Error-Bucket + Re-Klassifikation der CRAG-Fails nicht weiterverfolgt; CRAG ist out of paper scope, Diagnose-Aufwand nicht mehr paper-tragend.
type: task
status: done
---

## Outcome

CRAG-Variante wurde durch den Paper-Pivot 2026-05-16 (Pattern × Modellgröße
statt Variant-Ranking) aus der Eval rausgenommen. Damit ist die
Re-Klassifikation der 40%-Pass-Rate-Failures nicht mehr paper-relevant.

## Was nicht passiert ist

- Kein Stream-Error-Detection im Runner (T1)
- Kein 3-Bucket-Reporter (T2)
- Keine Re-Klassifikation der 9 CRAG-Fails (T3)
- Keine Paper-Implikations-Tabelle (T4)

## Was bleibt im Repo

- CRAG-Code (`aas-agent/src/aas_agent/crag*.py`) bleibt unverändert
  als potenzielle Basis für Future-Work-Reaktivierung (Node-Decomposed CRAG,
  siehe Paper-Future-Work-Eintrag in `task_paper_crag_removal_and_reframe.md`).
- Rohdaten der 2026-05-15-Eval (`tests/agent-tests/results/containment_hall4_baseline_N3.json`)
  bleiben als 27B-Datenpunkt der neuen Pattern × Modellgröße-Studie.

## References

- Pivot-Kontext: `task_paper_crag_removal_and_reframe.md`, `paper_etfa2026.md` Pivot-Sektion
