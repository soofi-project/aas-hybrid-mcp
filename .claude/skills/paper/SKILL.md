---
name: paper
description: Arbeit am ETFA-2026-Paper (ImplAAS Workshop, 8 Seiten IEEE). Kodiert Pfade, Build-Befehl, Section-Layout, inhaltliche Constraints (Layered-Determinism-These, Eval-Modell, SOOFI als Future Work) und die Eskalationsregel für Edit-Größen. Aufrufen für jede TeX/bib-Änderung im paper/etfa2026/-Verzeichnis.
---

# Paper-Arbeit (ETFA 2026, ImplAAS Workshop)

## Verzeichnislayout

```
paper/etfa2026/
├── conference_etfa_2026.tex   # Haupt-TeX (\input{content/...})
├── main.bib                   # BibTeX
├── IEEEtran.cls               # IEEE-Klasse (nicht anfassen)
├── content/
│   ├── 00-begin-document.tex
│   ├── 01-title-and-authors.tex
│   ├── 02-abstract-keywords.tex
│   ├── 03-introduction.tex
│   ├── 04-related-work.tex
│   ├── 05-scenario-requirements.tex
│   ├── 06-architecture.tex
│   ├── 07-ingestion-plugin.tex
│   ├── 08-retrieval-pipeline.tex
│   ├── 09-write-loop.tex
│   ├── 10-evaluation.tex
│   ├── 11-discussion.tex
│   ├── 12-limitations.tex
│   ├── 13-future-work.tex
│   └── 14-conclusion.tex
├── docker-compose.yml         # latexmk Single-Shot
├── build-paper.sh             # 4-Pass-Backup (selten nötig)
└── conference_etfa_2026.pdf   # Output
```

## Build

**Primary** — bundled Python-Wrapper im Skill (Layered Determinism: Skill trägt sein Build-Tool):

```bash
python .claude/skills/paper/build_paper.py
```

Der Wrapper findet repo-root automatisch (Walk-up vom Skript-Pfad), ruft die kanonische `docker compose`-Invocation, prüft den `=== BUILD SUCCESS ===`-Marker und exitet mit korrektem Code. Funktioniert von jedem CWD aus.

**Direkter Aufruf** (wenn der Wrapper nicht greift):

```bash
docker compose -f paper/etfa2026/docker-compose.yml up --build
```

Erfolg = letzte Zeile enthält `=== BUILD SUCCESS ===` **und** `*.pdf` wird gelistet.

**Fallback** (explizite 4 Passes wenn latexmk hängt): `paper/etfa2026/build-paper.sh` — schreibt Log nach `/tmp/latex-build-log.txt`.

**Image-Pinning:** `docker-compose.yml` pinnt `qmcgaw/latexdevcontainer` per Content-Digest (sha256:…), nicht per `:latest-full`. Reproduzierbarer Build, kein Drift zwischen Sessions. Update-Workflow als Kommentar in der Compose-Datei dokumentiert.

## Log-Analyse

LaTeX-Logs sind verrauscht. Bei Build-Fehler **gezielt** nach folgenden Mustern suchen:

- `! ` (Ausrufezeichen + Space am Zeilenanfang) → echter Fehler, Zeilennummer in der Folgezeile.
- `LaTeX Error:` / `Package ... Error:` → semantischer Fehler.
- `Undefined control sequence` → unbekanntes Makro (häufig Tippfehler oder fehlendes Package).
- `Citation '...' undefined` → bib-Key existiert nicht in `main.bib`.
- `Reference '...' undefined` → `\label` fehlt.

**Nicht alarmieren bei** `Overfull \hbox`, `Underfull \vbox`, `Font Warning` — kosmetisch, ignorieren solange PDF gebaut wird.

## Inhaltliche Constraints (must-respect)

- **Format:** IEEE Conference, **8 Seiten Hardlimit**. Bei Overflow zuerst Sections kompaktieren, nicht streichen — Plan in `~/.claude/projects/.../memory/paper_etfa2026.md`.
- **Kernthese:** *Layered Determinism* — Prompts sind Hints, Validatoren sind Garantien. Diese These zieht sich durch §06 Architecture, §09 Write-Loop, §10 Evaluation, §11 Discussion.
- **Eval-Modell (aktiv):** `Qwen/Qwen3.6-27B-FP8` via LiteLLM-Proxy `http://10.2.10.33:4000/v1` (Alias `qwen36-27b`). Nicht Qwen3.5-120B — ältere Memory-Einträge sind outdated; bei Zweifel `docker exec aas-agent printenv` checken.
- **SOOFI 120B = Future Work**, nicht aktuelles Eval-Modell. Plug-in über `LLM_BASE_URL`/`LLM_MODEL`.
- **N=3-Caveat:** Bench-B/Containment-Bench mit N=3 erlaubt **Existence Claims** ("Agent CAN trip on X"), **keine** präzise Frequenz-Schätzung. Höhere N als Future Work framen.
- **HyDE ist explizit verworfen** — keine `gao2022hyde`-Cite, kein HyDE-Abschnitt. §08 ist „Retrieval Enhancements" (Reranker + Query-Rewriting nach `ma2023rewrite`).
- **BaSyx-Version pinnen** — bei jedem write-/validation-Argument in §06/§12: Eclipse BaSyx Java Server vX.Y.Z + Commit explizit nennen. Begründung: „BaSyx error reporting is implementation-specific" — ohne Pin ist die Reframe-Argumentation gegen FA³ST/basyx-dotnet leer.
- **Drei Validation-Gap-Anekdoten als Klammer** — Write / Read / Pragmatics gemeinsam in §11 Discussion (oder §12 Limitations) unter „Layered Determinism". Reihenfolge nach Evidenzstärke: Write (harte Evidenz) → Read (harte Evidenz) → Pragmatics (Grenzfall — Prompt-Fix legitim, kein Validator-Fix). Niemals isoliert behandeln, sonst werden's „drei Bug-Reports" statt einer These.

## Claim-Belegbarkeit & Citation-Disziplin

Jede sachliche Aussage im Paper braucht **einen** Beleg. Sonst wird sie geweicht oder gestrichen.

**Erlaubte Belegtypen:**

| Typ | Wann | Wie zitieren |
|---|---|---|
| Own measurement | Bench A (Retrieval) / B (End-to-End) / C (Write-path) | File + Zeile/Row im Bench-Verzeichnis |
| Peer-reviewed reference | IEEE / ACM / Springer / Elsevier Konferenz oder Journal | Bib-Key in `main.bib`, ohne Note |
| Workshop paper | Workshop bei peer-reviewter Hauptkonferenz | `note={Workshop paper at <Venue>}` im Bib-Eintrag |
| arXiv-only / Preprint | Nur wenn keine peer-reviewte Quelle existiert | `note={arXiv preprint}` — und **nicht** für quantitative Block-Claims verwenden |
| Architectural decision | Eigene Designwahl | Klar als Entscheidung formulieren („we chose X because Y"), keine Auto-Behauptung wie „X is the right approach" |
| Common knowledge | Wirklich unstrittig („AAS ist I4.0-Standard") | Defensiv verwenden |

**Zitations-Hallu-Verbot:**

- **NIE** Citation aus dem Gedächtnis schreiben. Bei jedem neuen Bib-Eintrag: WebFetch (oder konkrete Quelle vom User) bestätigt Autoren, Jahr, Venue, DOI **bevor** der Eintrag committet wird.
- Vor Hinzufügen: `main.bib` greppen ob Key oder Variante existiert.
- Pflichtfelder: `author`, `title`, `year`, `venue`/`booktitle`, `pages`/`volume` (bei Journal/Konferenz), `doi` (Crossref-Check).
- BibTeX-Konvention: `<firstauthor><year><slug>` lowercase. Slug bevorzugt einwortig (`yan2024crag`), unterstrich erlaubt aber inkonsistent im Repo (`wang2023plan_solve`).
- Audit-Doku: `paper/etfa2026/claim_audit.md` ist die Wahrheitsquelle für Belegstatus. Siehe `task_paper_claim_audit.md`.

## Reviewer-Bingo: „Bessere Modelle fixen das"-Defense

Default-Reviewer-Einwand bei jedem Layered-Determinism-Argument: *„Warum nicht einfach ein größeres Modell?"* Wenn das ungeantwortet bleibt, wird das Paper als „temporäre Hilfslösung bis bessere Modelle da sind" gelesen — exakt das Gegenteil unserer Aussage.

Drei Gründe **immer mitdenken**, mindestens einer muss in jedem entsprechenden Absatz explizit stehen:

1. **Failure-Rate ist nie 0** — selbst SOTA-Modelle (GPT-5, Claude-4) liegen im BFCL unter 100 % Tool-Compliance. IEC 61508 / Industrial-Safety behandelt stochastische Komponenten seit Jahrzehnten so: deterministischer Wrapper ist Pflicht, nicht Optimierungsoption.
2. **Deployment-Story** — *kleines* Modell + Validator schlägt großes Modell ohne Validator hinsichtlich Konsistenz und Sicherheit. Self-Hosting + Souveränität + EU-Compliance untergräbt „wartet auf größere Modelle".
3. **Regulatorisch** — EU AI Act (Verordnung 2024/1689) High-Risk-Systems-Artikel + NIST AI RMF 1.0 verlangen deterministische Controls + Human Oversight **unabhängig** von Modellqualität.

**Trained-In-Outlook-Konsistenz:** Wenn das Paper an irgendeiner Stelle „Fine-Tune statt Manual" als Future Work formuliert, **muss** dort die 4-Layer-Klarstellung stehen (Trained-In + System-Prompt + On-Demand-Manual + Validator) — sonst untergräbt der Outlook die eigene These. Details: `task_paper_outlook_trained_in_manuals`.

## Outlook-/Future-Work-Konsistenz

Jede §13-Formulierung (Trained-In, Data-Quality-Layer, IR/DSL zwischen JSON+Cypher, Server-Plugin) muss die Layered-Determinism-These **stärken** oder mindestens **nicht widersprechen**. Faustregel:

- ✅ „X verschiebt die Compliance nach unten / macht den Validator effizienter / füllt eine neue Layer" — stärkt These
- ❌ „X macht den Validator überflüssig / ersetzt die Manual-Schicht ohne Ersatz" — bricht These

Outlook-Texte sind teurer zu fixen als sie zu prüfen — vor Commit kurz gegen Layered-Determinism gegenchecken.

## Cite-Positioning (für bekannte Reviewer im Workshop)

Bestimmte Citations haben eine politische Dimension — die Autoren sind potentielle Reviewer im ImplAAS-Workshop.

- **Garmaev et al. 2023** (`garmaev2023submodel`, Miny = ImplAAS-2026-Organisator): Positionierung als **Adoption + Modus-Erweiterung** („we use their generator in write-mode"), niemals „Baseline" / „surpass" / „we improve on". Wir erben ihre Limits (AllowedRange, AllowedValue, TechnicalData-extensions) explizit.
- **Stolze 2025, Büttner 2025, Miny-Paper aus ImplAAS-2025**: müssen mindestens als Related-Work-Anker auftauchen (siehe `task_paper_implaas2025_citations` für die Pflicht-/Strategie-Liste).
- **`sonnenberg2025aas_kg`** (eigenes Vorjahrs-Paper): Selbstzitat als Kontinuität, nicht als „we previously claimed X".

## Style

- Akademischer Ton, keine Marketing-Sprache, keine vagen Claims. Details: `paper/guideline.md`.
- Bei neuen Citations: erst `main.bib` greppen ob Key existiert; Key-Format `<erstautor><jahr><kurztitel>` (z. B. `ma2023rewrite`).
- Memory-Pointer für Paper-Status, Related Work, Bench-Pläne: `~/.claude/projects/C--repo-soofi-aas-hybrid-mcp/memory/` (`paper_etfa2026.md`, `related_work.md`, `benchmark_c_plan.md`).

## Eskalationsregel (User-Präferenz)

Für TeX/bib-Edits gilt **Edit-Größe → Vorgehen**:

| Größe | Beispiele | Vorgehen |
|---|---|---|
| **klein** | Tippfehler, einzelne Sätze, fehlende Cite einfügen, Tabellenwert | **Direkt edit**, kurze Statusnotiz |
| **mittel** | Neuer Absatz, Reformulierung eines Paragraphen, Tabellen-Restrukturierung | **Ankündigen** was und warum, dann edit |
| **groß** | Neue Subsection, Argumentation verschieben, These umformulieren, Section-Reihenfolge ändern, mehrere Sections gleichzeitig anfassen | **Erst fragen** mit Diff-Plan/Skizze, dann edit |

Im Zweifel eine Stufe höher einordnen — Paper ist nahe Submission, jeder Edit zählt.

## Anti-Patterns

- ❌ `\input{...}` mit relativem Pfad außerhalb `content/` einbauen.
- ❌ `main.bib` mit Duplikat-Keys versehen (BibTeX schweigt manchmal, das Paper hat dann falsche Cites).
- ❌ Auto-generierte Files (`.aux`, `.bbl`, `.blg`, `.fls`, `.log`, `.fdb_latexmk`, `.synctex.gz`) editieren oder committen — werden regeneriert.
- ❌ Cite-Keys raten — immer in `main.bib` verifizieren oder mit `[[task-paper-citations]]`-Workflow eskalieren.
- ❌ Style-Constraints von `paper/guideline.md` durch Marketing-Phrasen verletzen ("revolutionary", "unprecedented").
- ❌ Harte URN/URI-Strings im Fließtext (`urn:asset:hall4`, `urn:fabrik:device:9f2a-7c1`, IDTA-Submodel-URIs). Nur in Beispiel-Boxen / Listings.
- ❌ Vage Reviewer-Bait-Phrasen: „significantly improves", „state of the art", „efficient", „scalable", „novel", „innovative", „cutting-edge" ohne Zahlen oder Vergleich.
- ❌ „Due to space constraints / details omitted / future work" als Ausrede für fehlende Substanz — wenn der Punkt wichtig ist, gehört er rein; wenn er rausfällt, ehrlich als Limitation benennen.
- ❌ Garmaev als „Baseline" / „we surpass" / „we improve on" framen — Adoption-Positioning gilt (siehe Cite-Positioning).
- ❌ Trained-In-Outlook ohne 4-Layer-Klarstellung — bricht die eigene These.
