---
name: Task - Download Remaining Papers
description: Alle 33 citation keys aus dem ETFA paper liegen als PDF in papers_downloaded/
type: task
status: done
priority: medium
---

## Summary

Von 33 citation keys im ETFA paper sind 32 als PDF in `paper/papers_downloaded/{key}/` vorhanden,
1 fehlt noch hinter IEEE Xplore paywall. Cleanup (archived/) + BibTeX-Korrekturen + Ordner-Struktur + neue Zitationen (sakurada2025mas_aas_type3) sind abgeschlossen.

## Erledigt

- ✓ 6 Papers heruntergeladen + in citation-key-Ordner strukturiert (shi2025enhancing, xia2024zdm, xia2025cdt_rag, luxenburger2023i40, docling2024, bfcl2024)
- ✓ 19+1 citation-key-Ordner angelegt, alle zitierten Papers abgedeckt
- ✓ `metadata.txt` für alle Ordner erstellt
- ✓ Lockere PDFs + Duplikate entfernt
- ✓ `archived/`-Ordner für unreferenzierte Papers (→ `memory/tasks/closed/task_cleanup_unused_papers.md`)
- ✓ BibTeX in `main.bib` verifiziert + 8 Einträge korrigiert (bfcl2024, liu2024agentbench, shinn2023reflexion, yao2022react, maadaan2023self_refine, xu2024rewoo, wu2023autogen) + 1 neu (sakurada2025mas_aas_type3)
- ✓ `ruebel2023skill` → `ruebel2025agent_comm` ersetzt (älteres IEEE Paper durch aktuelles Springer OA-Paper der gleichen Autoren)
- ✓ `Bronto.pdf` → `archived/schmeyer2024data_broker/` archiviert
- ✓ `sakurada2025mas_aas_type3` → in `03-introduction.tex` + `04-related-work.tex` zitiert
- ✓ `nul`-File entfernt

## Erledigt (Fortsetzung)

- ✓ `garmaev2023submodel_classes.pdf` heruntergeladen + in `paper/papers_downloaded/garmaev2023submodel_classes/` (2026-05-13). BibTeX-Eintrag stand schon in `main.bib`. Damit alle 33 citation keys vollständig.

## Acceptance Criteria

- ✓ Alle citation keys haben PDF in `paper/papers_downloaded/{key}/`
