---
name: paper-search
description: Akademische Paper-Suche via OpenAlex (250M Werke, frei, kein API-Key). Findet Cites für Claims, prüft Duplikate vor `main.bib`-Einträgen, liefert BibTeX-Rohdaten. Aufrufen bei Related-Work-Recherche, Claim-Audit-Lücken, oder bevor ein neuer Bib-Eintrag manuell zusammengestoppelt wird.
---

# Paper-Search (OpenAlex)

OpenAlex (https://openalex.org/) indiziert 250M+ wissenschaftliche Werke — arXiv, IEEE, ACM, Springer, Elsevier, Workshops. Frei, kein API-Key, kein Rate-Limit-Stress mit `mailto`-Identifier. Vorzugswert gegenüber Google-Scholar-Scraping oder Semantic-Scholar (das hat eigene API-Limits).

## Script-Lokation

`.claude/skills/paper-search/search_openalex.py` (bundled mit dem Skill — Layered Determinism).

## Workflow

Vor jedem neuen Bib-Eintrag in `paper/etfa2026/main.bib`:

### 1. Duplikat-Check (deterministisch zuerst)

```bash
# Wir suchen einen Cite für "agent tool calling reliability"
grep -i "tool.calling\|function.calling" paper/etfa2026/main.bib
grep -lr "tool.calling\|function.calling" paper/papers_downloaded/*/
```

Wenn schon ein Eintrag oder ein heruntergeladenes Paper existiert: dort starten, nicht neu suchen.

### 2. OpenAlex-Suche

```bash
python .claude/skills/paper-search/search_openalex.py "agent tool calling reliability"
python .claude/skills/paper-search/search_openalex.py "BFCL Berkeley Function Calling Leaderboard"
python .claude/skills/paper-search/search_openalex.py "asset administration shell agent" --year-from 2023
```

Default: Top-10 nach Relevanz, mit Titel/Autoren/Jahr/Cites/Venue/DOI/Abstract-Snippet/PDF-URL falls Open Access. `--limit 20` für breitere Suche. `--year-from 2023` zum Eingrenzen.

### 3. DOI-Lookup für gezielten Eintrag

Wenn jemand schon einen DOI/URL genannt hat:

```bash
python .claude/skills/paper-search/search_openalex.py --doi 10.1109/ETFA54631.2023.10275464
```

Liefert ein einzelnes Werk mit allen Metadaten — Grundlage für den BibTeX-Eintrag.

### 4. Cite-Entscheidung

Aus den Results auswählen nach folgenden Kriterien (in dieser Reihenfolge):

1. **Peer-reviewed?** Venue muss IEEE / ACM / Springer / Elsevier-Konferenz/Journal sein (`venue_type` ≠ `repository` für preprint-only).
2. **Citation count + Jahr** — bei jungen Papers (≤ 2 Jahre) Cites weniger relevant; bei älteren Papers hohe Cites = Quality-Signal.
3. **Open Access?** `[OA]`-Marker + PDF-URL — direkt mit `/paper-download` weiter.
4. **Autoren-Kontext** — bekannte Reviewer-Kreise (Miny, Garmaev, Ristin, ImplAAS-Organisatoren) bevorzugen für politisch sensitive Cites; siehe `/paper`-Skill Sektion „Cite-Positioning".

### 5. PDF + BibTeX

Wenn das Paper relevant ist:

a) **PDF** — wenn `[OA]`-Marker da: PDF-URL aus dem Result manuell oder über `/paper-download`-Workflow nach `paper/papers_downloaded/<bibkey>/` ablegen, dann `extract_markdown.py` aufrufen.

b) **BibTeX-Stub** — aus den Metadaten (title, authors, year, venue, doi) einen Eintrag bauen. Bib-Key-Format `<firstauthor><year><slug>` (siehe `/paper`-Skill Sektion „Citation-Disziplin"). Beispiel:

```bibtex
@inproceedings{garmaev2023submodel,
  author={Garmaev, Igor and Miny, Torben and Kleinert, Tobias},
  title={Automatic Generation of Submodel-Specific Classes ...},
  booktitle={IEEE ETFA},
  year={2023},
  doi={10.1109/ETFA54631.2023.10275464}
}
```

Workshop-Papers: `note={Workshop paper at <Venue>}` setzen. arXiv-only: `note={arXiv preprint}` setzen und **nicht** für quantitative Block-Claims verwenden (siehe Claim-Audit-Regel in `/paper`).

## Use-Cases

| Aufgabe | Aufruf |
|---|---|
| Cite für einen unbelegten Claim aus `claim_audit.md` finden | `search_openalex.py "<claim keywords>"` |
| Prüfen ob ein angeblicher Cite real existiert (Hallu-Schutz) | `search_openalex.py --doi <doi>` oder `search_openalex.py "<exakter Titel>"` |
| Related-Work-Cluster auffüllen (z. B. „Agent Failure Modes") | `search_openalex.py "agent failure mode benchmark"` |
| ImplAAS-2025 Workshop-Papers nachziehen | `search_openalex.py "asset administration shell" --year-from 2025` |
| Vor neuem `main.bib`-Eintrag verifizieren dass er nicht halluziniert ist | `search_openalex.py --doi <doi>` |

## Output-Beispiel

```
[1] Building Effective Agents
    Erik Schluntz, Barret Zoph — 2024 — cited 142x [OA]
    Venue: Anthropic Engineering (blog)
    DOI: ...
    PDF:  https://www.anthropic.com/...
    Agents that perform best on tool-calling benchmarks rely on workflows...

[2] ...
```

`[OA]`-Marker = Open Access, direkt downloadbar.
Kein `[OA]` = Paywall, User muss PDF anderweitig beschaffen.

## Anti-Patterns

- ❌ OpenAlex-Suche **vor** dem Duplikat-Check in `main.bib` / `papers_downloaded/` machen — verschwendet Calls und kann Duplikat-Keys erzeugen.
- ❌ BibTeX-Stub aus dem Gedächtnis schreiben statt aus den OpenAlex-Metadaten — Hallu-Risiko (siehe Claim-Audit).
- ❌ Suchen ohne `--year-from`-Filter bei jungen Topics — alte Surveys verdrängen aktuelle Arbeiten.
- ❌ Preprint-only-Results (`venue_type: repository`) für quantitative Paper-Claims verwenden — Workshop-/Konferenz-Variante muss her, sonst `note={arXiv preprint}` und Cite weichen.
- ❌ DOI ohne Prüfung ins Paper schreiben — bei `[OA]`-Lookup zeigt OpenAlex selbst, ob der DOI auflöst.

## Quellen-Erweiterung (Future)

OpenAlex deckt das meiste ab, aber:
- **IDTA-Specs / White Papers** sind nicht in OpenAlex → manuelle Pflege in `main.bib`
- **DFKI-interne Reports** sind nicht in OpenAlex → über interne Quellen
- **GitHub-Software-Releases** als Cite (`@software{...}`) gibt's nicht über OpenAlex → manuell

Diese Lücken sind dokumentiert in `task_paper_implaas2025_citations.md` (Workshop-Papers) und `task_paper_write_validation_defense.md` T5 (Software-Tools wie `aas-test-engines`).
