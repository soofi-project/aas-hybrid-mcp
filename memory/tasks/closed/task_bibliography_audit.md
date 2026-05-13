---
name: Task - Bibliography Audit
description: Systematische Online-Verifikation aller 33 BibTeX-Einträge in paper/etfa2026/main.bib
type: task
status: done
priority: high
depends_on: []
---

## Summary

Alle 33 citation keys in `paper/etfa2026/main.bib` einzeln gegen die
autoritative Online-Quelle (DOI-Resolver, arXiv, Verlags-Website,
Repository-URL) prüfen. Ziel: keine falschen Autoren, keine vertauschten
Co-Author-Reihenfolgen, keine Tippfehler im Titel, keine erfundenen oder
defekten DOIs, korrekte Venue-/Jahres-Angaben.

**Warum jetzt:** Citation-Accuracy ist eines der Standard-Reviewer-Flags
bei IEEE-Konferenzen. Vor der Einreichung billig zu fixen, nach Acceptance
peinlich (mandatory revision) oder schädlich (rejection mit „careless
work"-Begründung).

## Ausführungs-Modus (entschieden 2026-05-13)

**Automatischer WebFetch-First-Pass für die DOI-tragenden Einträge.**

- Phase A: WebFetch über `https://doi.org/<doi>` für die 15 peer-reviewed/
  conference-Einträge der oberen zwei Gruppen. Pro Eintrag wird ein
  Vergleichsbericht erzeugt (was in main.bib steht vs. was die
  Verlags-Seite ausliefert), Diffs werden hervorgehoben.
- Phase B: User reviewt die Diffs, akzeptiert/verwirft Korrekturen, ich
  übernehme die akzeptierten Änderungen in `main.bib`.
- Phase C: Industrie-/Software-URLs (14 Einträge, untere Gruppe) — reine
  Erreichbarkeits- und Inhalts-Checks via WebFetch, kein BibTeX-Field-
  Vergleich nötig, nur „Link tot/lebendig + Inhalt match".
- Phase D: arXiv-Preprints (4 Einträge) — gesondert, weil bei jedem zu
  prüfen ist ob inzwischen eine Konferenz-Version existiert, die zitiert
  werden sollte. WebFetch auf `arxiv.org/abs/<id>` plus Quersuche nach
  „<title> conference proceedings".

Vorteile gegenüber manuellem Durchklicken: kein Browser-Hopping über 33
Verlags-Seiten, deterministischer Vergleich, jede Änderung dokumentiert.

## Bekannte Verdachtsfälle (vor Phase A schon im Task vermerken, damit sie nicht durchrutschen)

- **`wu2023autogen`** ist als `@misc` markiert. AutoGen ist inzwischen
  auf **COLM 2024** publiziert. Zitations-Typ wahrscheinlich auf
  `@inproceedings` umstellen, Venue + Jahr anpassen.
- **`yan2024crag`** ist als `@article` markiert. Corrective RAG ist
  meines Wissens nach arXiv-only. `@misc` mit `eprint`-Feld wäre die
  ehrlichere Form.
- **`gao2022hyde`** als `@misc` — HyDE wurde auf **ACL 2023**
  publiziert. Auf `@inproceedings` umstellen.
- **`xu2024rewoo`** als `@misc` — Konferenz-Version verifizieren (arXiv
  only? NeurIPS?). Falls nur arXiv, `@misc` bleibt korrekt.
- **`qwen35`** als `@misc` — Alibaba-Tech-Report; prüfen ob es eine
  „offiziellere" Zitations-Form gibt (Hugging-Face-Card vs.
  arXiv-Tech-Report vs. Alibaba-Whitepaper).

## Vorgehen pro Eintrag

1. **DOI/URL in Resolver werfen.**
   - Mit DOI: `https://doi.org/<doi>` → Verlags-Seite öffnen
   - Ohne DOI, mit arXiv-ID: `https://arxiv.org/abs/<id>`
   - Ohne beides: Venue-spezifische Suche (ACM Digital Library, IEEE Xplore, Springer Link, MDPI)
2. **Felder vergleichen mit der autoritativen Quelle:**
   - **Autoren:** Reihenfolge, vollständige Vornamen vs. Initialen, Umlaute, akzentuierte Buchstaben (Leitão statt Leitao)
   - **Titel:** exakt, inklusive Kapitalisierung — IEEE/Springer/ACM haben unterschiedliche Title-Case-Conventions. Untertitel nicht vergessen.
   - **Venue:** `booktitle` für conferences, `journal` für journals; offizieller Conference-Name (z.B. „2023 IEEE 28th International Conference on …"), nicht nur das Akronym
   - **Jahr, Monat:** für Springer/MDPI relevant (year-of-issue vs. year-of-publication)
   - **Seiten:** `1-7` vs. `1-12` — bei IEEE-Conference-Papers oft 6–8 Seiten Standard
   - **Volume/Issue/Article-Nummer:** für Journals
3. **Cite-Key-Konsistenz** — passt das Format `<firstauthor><year><shortname>` zur Realität?
4. **Open-Access-Note ergänzen** wo zutreffend (`note = {CC BY 4.0 (Open Access)}` oder ähnlich) — hilft fürs Paper, weil Reviewer manchmal explizit OA für Methoden-Reproduzierbarkeit erwarten und es signalisiert verantwortungsvolle Quellenwahl
5. **Diskrepanzen → main.bib editieren** + commit pro Block (z.B. „bib: fix author order for ruebel2025agent_comm + add CC BY note")
6. **Eintrag in der Checkliste unten markieren** (✓ wenn ok, ✗ mit Note wenn korrigiert)

## Eintrags-Checkliste

Reihenfolge wie in main.bib. Empfohlene Bearbeitungsreihenfolge: **die
peer-reviewed-Einträge zuerst** (die mit echtem DOI), weil dort der
Schaden am größten wäre. Industrie-/Software-URLs danach (einfacher zu
verifizieren — Link funktioniert oder nicht).

### Peer-Reviewed mit DOI (zuerst — höchstes Reviewer-Risiko)

- [✓] `shi2025enhancing` (article) — Autoren/DOI/Venue OK (CrossRef: Computers in Industry, vol 171, 2025)
- [✓] `xia2024zdm` (article) — OK (Journal of Manufacturing Systems, vol 77, 678–696, 2024)
- [✓] `xia2025cdt_rag` (article) — OK (Robotics and CIM, vol 97, 2026. Year 2026 is correct per CrossRef.)
- [✓] `xia2024aasbyllm` (article) — OK (IEEE Access, vol 12, 2024)
- [✓] `sonnenberg2025aas_kg` (INPROCEEDINGS) — Self-citation 100% korrekt (ETFA 2025, 1–8)
- [✓] `sakurada2025mas_aas_type3` (article, OA) — OK (Future Internet 17(7), 270, CC BY 4.0)
- [✓] `luxenburger2023i40` (INPROCEEDINGS) — OK (ETFA 2023, 1–8)
- [✓] `ruebel2025agent_comm` (inbook, Springer OA) — OK, `@inbook` korrekt für Book Chapter
- [✓] `garmaev2023submodel_classes` (INPROCEEDINGS, ETFA 2023) — OK (1–7)
- [✗] `yan2024crag` → **Korrigiert:** `@article` → `@misc` (arXiv-only, keine Peer-Review-Publikation gefunden). DOI 10.48550/arXiv.2401.15884 hinzugefügt, Note ergänzt.

### Konferenzen mit DOI

- [✓] `bfcl2024` (inproceedings) — OK (ICML 2025, OpenReview, CC BY 4.0, Autoren bestätigt)
- [✓] `liu2024agentbench` (inproceedings) — OK (ICLR 2024)
- [✓] `yao2022react` (inproceedings, ICLR 2023) — OK
- [✓] `wang2023plan_solve` (inproceedings, ACL 2023) — OK
- [✓] `madaan2023self_refine` (inproceedings, NeurIPS 2024) — OK
- [✓] `shinn2023reflexion` (inproceedings, NeurIPS 2023) — OK

### arXiv / Preprints (Konferenz-Version prüfen!)

- [✓] `qwen35` (misc) — OK, qwen.ai/blog ist offizielle Quelle; kein arXiv paper
- [✗] `gao2022hyde` → **Korrigiert:** `@misc` → `@inproceedings` (ACL 2023 publiziert, DOI 10.18653/v1/2023.acl-long.99, pages 1762–1777, CC BY 4.0)
- [✓] `xu2024rewoo` (misc) — OK, arXiv-only, keine Konferenz-Publikation gefunden
- [✓] `wu2023autogen` (misc) — OK, COLM 2024 workshop paper only, kein Haupttrack; `@misc` korrekt

### Industrie/Software-URLs (Link-Check)

- [✓] `smartfactorykl_aasmcp` — GitHub live, 3 commits, MIT, Python — OK
- [✓] `beyerlein2025aas_mcp` — innoq.com live, 15. Jul 2025, Philipp Beyerlein — OK
- [✓] `anthropic2024workflows` — anthropic.com live, Dec 19, 2024 — OK
- [✓] `kit2025aas_mcp` — keine öffentliche URL; Note "Could not verify any public web presence" ist korrekt
- [✓] `basyx_pdf2aas` — GitHub live, 468 commits, v1.0.0 — OK
- [✓] `idta_templates_repo` — GitHub live, 78 stars, 795 commits — OK
- [✓] `idta_srn` — admin-shell.io live, Template in der published/ Liste — OK
- [✓] `idta_mi` — admin-shell.io live, Template in der published/ Liste — OK
- [✓] `basyx_python_sdk` — GitHub live, latest 2.0.1 (Apr 20, 2026) — OK
- [✓] `rwthiat_template2py` — GitHub live, v0.1.1, GPL-3.0 — OK
- [✗] `docling2024` → **Korrigiert:** Autoren von "A. U. Deep Search Team" auf 19 echte Autoren korrigiert (Auer, Lysak, Nassar, ... Staar). DOI 10.48550/arXiv.2408.09869 + month/day hinzugefügt. Note: "arXiv preprint (v5, 2024-12-09). No peer-reviewed venue publication."
- [✓] `pymupdf4llm_doc` — readthedocs.live, MIT-licensed — OK
- [✗] `soofi_reranker` → **Entfernt:** Niemals im Paper zitiert (`\cite{soofi_reranker}` nicht gefunden), aus main.bib gelöscht

## Acceptance Criteria

- Alle 33 Einträge in der Checkliste oben mit ✓ markiert
- Jede Korrektur in `main.bib` committed; Commit-Message dokumentiert was geändert wurde (z.B. „bib: fix author order for X, add OA note for Y")
- Keine erfundenen DOIs (alle resolvieren auf das richtige Paper)
- Open-Access-Status dort vermerkt wo zutreffend
- Cite-Key-Convention konsistent (`<firstauthor><year><shortname>`)

## Notes / Gotchas

- **IDTA-Templates** haben keine DOIs — autoritative Quelle ist
  `industrialdigitaltwin.org` (Direktlink zum jeweiligen Template-PDF)
  oder das `submodel-templates`-GitHub-Repo
- **arXiv-Papers, die später auf einer Konferenz erschienen sind** —
  letztere ist die zu bevorzugende Zitation (Reviewer mögen das, Camera-
  Ready-Version ist autoritativ). Beispiele unter „arXiv / Preprints"
  oben markiert.
- **Manche Konferenzen ändern Titel zwischen accepted-version und
  camera-ready** (z.B. Untertitel fallen weg, Kürzel-Expansion) —
  Camera-Ready ist autoritativ
- **Umlaute / Akzente in Autorennamen:** Leitão, Müller, Rübel usw. —
  in BibTeX als `Leit\~ao` oder Unicode-Direkt; je nachdem was die
  IEEEtran-Klasse rendert. Mit dem aktuellen Compile-Setup testen.
- **„self-citation"** (sonnenberg2025aas_kg): doppelt sorgfältig
  prüfen, das ist eigenes Material — peinlich wenn dort Fehler stehen
- **soofi_reranker:** SOOFI-Repo ist intern, prüfen ob die URL für ein
  Reviewer-Publikum sinnvoll ist (z.B. ob der Repo public ist oder ob
  ein Tech-Report-Style-Zitat besser wäre)

## Bonus / nice-to-have

- Nach der Verifikation: `bibtex-tidy --modify main.bib` oder ähnliches
  Tool laufen lassen, um Formatierung konsistent zu machen
  (Indentation, Feld-Reihenfolge)
- Doppel-Verwendungen prüfen: wird jeder cite key auch tatsächlich im
  Paper `\cite{...}`d? Falls nicht, raus damit — schlanker bib ist
  besser
  - **`soofi_reranker`** — gefunden! Nicht im Paper zitiert → aus main.bib gelöscht ✓
