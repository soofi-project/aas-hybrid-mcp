---
name: Task - Bibliography Audit
description: Systematische Online-Verifikation aller 33 BibTeX-Einträge in paper/etfa2026/main.bib
type: task
status: open
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

- [ ] `shi2025enhancing` (article) — DOI prüfen, Autoren, Venue (Journal-Name + Vol/Issue)
- [ ] `xia2024zdm` (article)
- [ ] `xia2025cdt_rag` (article)
- [ ] `xia2024aasbyllm` (article)
- [ ] `sonnenberg2025aas_kg` (INPROCEEDINGS) — **self-citation**, sollte 100% korrekt sein, trotzdem cross-checken (ETFA 2024 oder 2025?)
- [ ] `sakurada2025mas_aas_type3` (article, Future Internet, OA) — License-Note bereits `CC BY 4.0`, prüfen
- [ ] `luxenburger2023i40` (INPROCEEDINGS)
- [ ] `ruebel2025agent_comm` (inbook, Springer OA) — Ersatz für ruebel2023skill; Autoren-Konsistenz prüfen
- [ ] `garmaev2023submodel_classes` (INPROCEEDINGS, ETFA 2023) — PDF gerade dazugekommen, gegen das eingegangene BibTeX vom User abgleichen
- [ ] `yan2024crag` (article) — Corrective RAG, ist eigentlich arXiv-only; prüfen ob `@article` oder `@misc` der richtige Typ ist

### Konferenzen mit DOI

- [ ] `bfcl2024` (inproceedings) — Berkeley Function Calling Leaderboard
- [ ] `liu2024agentbench` (inproceedings)
- [ ] `yao2022react` (inproceedings, ICLR 2023)
- [ ] `wang2023plan_solve` (inproceedings, ACL 2023)
- [ ] `madaan2023self_refine` (inproceedings, NeurIPS 2023)
- [ ] `shinn2023reflexion` (inproceedings, NeurIPS 2023)

### arXiv / Preprints (Konferenz-Version prüfen!)

- [ ] `qwen35` (misc) — Tech Report; gibt's eine offizielle Version?
- [ ] `gao2022hyde` (misc) — HyDE; ACL 2023? prüfen
- [ ] `xu2024rewoo` (misc) — ReWOO; arXiv only oder NeurIPS-published?
- [ ] `wu2023autogen` (misc) — AutoGen; COLM 2024 published — sollte als `@inproceedings` rein?

### Industrie/Software-URLs (Link-Check)

- [ ] `smartfactorykl_aasmcp` (misc) — URL erreichbar, Inhalt match?
- [ ] `beyerlein2025aas_mcp` (misc)
- [ ] `anthropic2024workflows` (misc)
- [ ] `kit2025aas_mcp` (misc)
- [ ] `basyx_pdf2aas` (misc)
- [ ] `idta_templates_repo` (misc) — github.com/IndustrialDigitalTwin/submodel-templates ?
- [ ] `idta_srn` (misc) — IDTA Submodel Template 02022 SRN
- [ ] `idta_mi` (misc) — IDTA Submodel Template 02002 Maintenance Instructions
- [ ] `basyx_python_sdk` (misc)
- [ ] `rwthiat_template2py` (misc)
- [ ] `docling2024` (techreport) — IBM tech report, prüfen ob arXiv-Version verfügbar/zitiert werden sollte
- [ ] `pymupdf4llm_doc` (software)
- [ ] `soofi_reranker` (misc) — Eigene SOOFI-Repo; URL + Beschreibung match?

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
