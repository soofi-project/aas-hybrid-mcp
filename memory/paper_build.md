# Paper Build

## Build command

```bash
cd paper/etfa2026
docker compose up
```

`latexmk` macht automatisch alle pdflatex + bibtex Passes. Verwende **nicht** `build-paper.bat` — windows paths in Docker volumes scheitern.

## Validate

| Check | OK |
|---|---|
| `=== BUILD SUCCESS ===` im output | Ja |
| `conference_etfa_2026.pdf` existiert | Ja |
| Keine "No file" warnings für Bilder | Ja (nur underfull/overfull hbox, normal für IEEEtran) |
| refs (fig:..., sec:...) sind definiert | Ja |

## Bilder

Jedes `.png` im ordner wird direkt von `\includegraphics` gelesen. Keine konvertierung nötig.

`architecture.png` → `fig:arch` (line ~95 `.tex`)
