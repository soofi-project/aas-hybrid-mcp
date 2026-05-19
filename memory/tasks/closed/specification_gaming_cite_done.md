---
name: Specification Gaming Cite Done
description: Park 2024 + Chan 2023 in main.bib eingetragen; Beobachtungsfall in §Agentic Reads vs. Workflow Writes eingebaut; DOIs verifiziert.
type: task
status: done
---

## Was umgesetzt

**DOIs verifiziert (2026-05-17):** Beide Paper via OpenAlex bestätigt — keine Halluzination.
- Park et al. 2024 "AI Deception" — Patterns (Cell Press), 161 Cites, OA ✅
- Chan et al. 2023 "Harms from Agentic Systems" — ACM FAccT 2023, 97 Cites, OA ✅

**`main.bib`:** Neuer Abschnitt `% === Agent Safety / Alignment ===` mit Einträgen
`park2024aideception` und `chan2023harms` eingefügt.

**`11-discussion.tex`:** Beobachtungsfall als 3-Satz-Paragraph in
`§Agentic Reads vs. Workflow Writes` eingebaut — nach dem `\end{itemize}`.
Framing: Specification Gaming als konkreter Beleg für per-tool vs. holistic
enforcement; `create_service_request_notification` als genannte Mitigation.

**`§The Necessity of Enforcement`:** Bestehenden Claim minimal qualifiziert
("via the validated `put_submodel` path") um Widerspruch mit der
Specification-Gaming-Beobachtung zu vermeiden.

**Advisor-Empfehlung umgesetzt:** Beobachtung in `§Agentic Reads vs. Workflow Writes`
platziert statt als widersprüchlicher Append in `§The Necessity of Enforcement`.

## Nicht umgesetzt (T4 — optional)
PDFs nicht heruntergeladen — kein Blocker, Links in main.bib über DOI erreichbar.

## Verwandte Tasks
- Slot-Filling-Implementierung + Eval: [[task-srn-slotfilling-tool-and-eval]]
- Write Tool Validation Gap (T0 noch offen): [[task-write-tool-validation-gap]]
