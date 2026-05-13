---
name: Task - PDF Inline Viewer via Nginx Sidecar
description: Nginx-Container zwischen Browser und BaSyx, der Content-Disposition von attachment auf inline umschreibt, damit source_jump_url PDFs im Browser-Viewer öffnet statt herunterzuladen
type: task
status: done
priority: medium
depends_on: [task_rag_metadata_overhaul]
---

## Status (2026-05-13)

**Done.** Implementation: `nginx-proxy/nginx.conf`, neuer
`basyx-viewer-proxy` Service in `docker-compose.yml` (Port **8091:80** —
8082 war kollidiert mit `submodel-registry`), `.env`
`BASYX_PUBLIC_URL=http://localhost:8091`. Vom User verifiziert: PDFs
öffnen jetzt inline im Browser-Viewer mit korrektem Page-Jump.

## Summary

Die `source_url`/`source_jump_url`-Felder in Weaviate (siehe
`task_rag_metadata_overhaul`) zeigen heute direkt auf den BaSyx
`/attachment`-Endpoint. BaSyx sendet dort hardcoded
`Content-Disposition: attachment; filename="..."` — der Browser lädt das
PDF herunter, statt es im eingebauten PDF-Viewer zu rendern. Page-Jump
über `#page=N` funktioniert dadurch nicht, weil der Browser den Viewer
gar nicht erst startet.

**Ziel:** Klick auf `source_jump_url` öffnet das PDF im Browser-eigenen
Viewer, springt zur richtigen Seite. Keine Änderung an BaSyx (Upstream-
Komponente, wollen wir nicht forken).

## Architektur-Entscheidung — warum Nginx, nicht PDF.js

Kurz die abgelehnten Alternativen, damit das nicht wieder aufkommt:

- **BaSyx forken / patchen:** verworfen. Aufwand für regelmäßiges Rebasing
  steht in keinem Verhältnis zum HTTP-Header-Tweak.
- **Python-Proxy in mcp-server:** ginge auch, aber mcp-server soll auf
  MCP-Protokoll fokussiert bleiben. Ein Single-Purpose-Container
  trennt Verantwortlichkeiten sauberer.
- **PDF.js Web-Viewer self-hosten:** **verworfen**, weil der Browser-
  eingebaute PDF-Viewer von Chrome und Firefox **schon PDF.js ist**. Self-
  Hosting bringt funktional null Gewinn — nur Zusatz-Container (statische
  Assets), CORS-Konfiguration, hässlichere URLs
  (`viewer.html?file=ENCODED_URL#page=97`), zusätzlichen Round-Trip
  (Browser holt Viewer, Viewer holt PDF). PDF.js lohnt sich nur, wenn man
  den Viewer **in eine eigene UI** einbetten will (eigene Toolbar,
  Annotationen, Side-by-Side mit Chat). Das ist hier nicht der Fall.
- **Browser-Plugins / Extensions:** nicht reproduzierbar, jeder User
  müsste das selbst installieren — taugt nicht für Demo / Paper-Story.

**Gewählter Ansatz:** Nginx-Sidecar-Container, ~20 Zeilen Konfig über
drei Dateien. Pure Header-Rewrite via `proxy_hide_header
Content-Disposition` + `add_header Content-Disposition 'inline'`. Browser
sieht `inline` → nutzt seinen nativen PDF-Viewer → `#page=N`-Fragment
funktioniert nativ.

## Konkrete Implementierung

### Datei 1: `nginx-proxy/nginx.conf` (neu)

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://aas-environment:8081;
        proxy_http_version 1.1;
        proxy_set_header Host $host;

        # Streaming statt Buffering — sonst lädt nginx die ganze PDF in
        # RAM bevor's an den Client geht (PDFs sind gerne 5–50 MB).
        proxy_buffering off;

        # BaSyx' attachment-Header neutralisieren, durch inline ersetzen.
        proxy_hide_header Content-Disposition;
        add_header Content-Disposition 'inline; filename="document.pdf"' always;
    }
}
```

### Datei 2: `docker-compose.yml` (neuer Service-Block)

```yaml
basyx-viewer-proxy:
  image: nginx:alpine
  container_name: basyx-viewer-proxy
  restart: unless-stopped
  ports:
    - "8091:80"
  volumes:
    - ./nginx-proxy/nginx.conf:/etc/nginx/conf.d/default.conf:ro
  depends_on:
    - aas-environment
  networks:
    - aas-network
```

### Datei 3: `.env`

```diff
- BASYX_PUBLIC_URL=http://localhost:8081
+ BASYX_PUBLIC_URL=http://localhost:8091
```

Wichtig: **8081 bleibt unverändert** für direkte BaSyx-Calls (Postman,
Dev-Tools, internal MCP-Aufrufe gegen `BASYX_SUBMODEL_REPO`). Der
neue 8091-Port ist **nur** für User-facing Viewer-Links.

## Subtasks

### T1: Nginx-Verzeichnis + Config anlegen

- `nginx-proxy/` Verzeichnis im Repo-Root erstellen
- `nginx-proxy/nginx.conf` mit obigem Inhalt
- README-Header-Kommentar in der Config: was sie tut, warum sie existiert,
  warum nicht in mcp-server

### T2: Docker-Compose erweitern

- Neuer Service-Block `basyx-viewer-proxy` an thematisch passender Stelle
  in `docker-compose.yml` (Empfehlung: direkt nach dem `aas-environment`-
  Block, weil's logisch zu BaSyx gehört)
- `depends_on: [aas-environment]` — Reihenfolge beim `up`
- Port 8091 reservieren — **Korrektur gegenüber der ersten Task-Skizze, die
  8082 vorgesehen hatte**: 8082 ist schon durch `submodel-registry` belegt.
  8091 sitzt thematisch neben `open-webui` (8090) und ist frei.

### T3: BASYX_PUBLIC_URL umstellen

- `.env` Anpassung: `BASYX_PUBLIC_URL=http://localhost:8091`
- `BASYX_SUBMODEL_REPO` (internal Docker URL) bleibt **unverändert** auf
  `http://aas-environment:8081` — der embedding-service holt PDFs
  weiterhin direkt von BaSyx auf dem internen Docker-Netz, nicht über den
  Proxy (Streaming bleibt einfach + 0 ms Overhead)
- Nur `_public_url` in `handlers.py` profitiert (Output zeigt auf 8091)

### T4: Weaviate Re-Ingest

- Weil bestehende Chunks ihre `source_url` schon mit `localhost:8081`
  gespeichert haben, müssen sie neu ingestiert werden:
  - Weaviate-Collection droppen (`curl -X DELETE
    http://localhost:8080/v1/schema/Aas_documents...`)
  - Connector-Offset reset oder Submodel-Events replayen → embedding-
    service ingestet neu mit `localhost:8091`-URLs

### T5: Verifikation

- Manual-Click-Test: aus dem MCP-Search-Result eine `source_jump_url` in
  den Browser kopieren → PDF öffnet sich im Browser-Tab im PDF-Viewer
  (NICHT als Download-Dialog), springt zur in `source_page` angegebenen
  Seite
- Browser-DevTools Network-Tab: Response-Header zeigt
  `Content-Disposition: inline; filename="document.pdf"` (statt
  `attachment`)
- Test mit Chrome und Firefox (beide native PDF-Viewer haben ihre eigenen
  Quirks)
- Test mit URL-encoded Pfaden (`%5B0%5D` etc.) — die nginx-Konfig sollte
  das ohne Special-Treatment durchreichen, aber doppelt geprüft schadet
  nicht

## Acceptance Criteria

- `source_jump_url` aus MCP-Search-Response öffnet im Browser-PDF-Viewer
  (kein Download-Dialog) und springt zur korrekten Seite
- Response-Header beim `localhost:8091/...`-GET enthält
  `Content-Disposition: inline`
- Port 8081 weiterhin direkt für BaSyx-Calls nutzbar (keine Regression)
- Funktioniert in Chrome **und** Firefox

## Open Questions

- **Soll nginx alle BaSyx-Pfade durchreichen oder nur `/.../attachment`?**
  Empfehlung: alle durchreichen (sparsamer Config-Code,
  Single-Location-Block). Andere BaSyx-Endpoints kriegen dann auch das
  inline-Header gesetzt — schadet nicht, weil sie meist JSON sind und der
  Browser Content-Disposition nur für Binär-MIME-Types interpretiert.
- **Soll der Sidecar HTTPS sprechen?** Für lokale Entwicklung nein. Für
  ein produktives Deployment ja — aber dann gehört das Cert-Management
  ohnehin auf eine vorgelagerte Reverse-Proxy-Ebene (Traefik / Caddy in
  Kubernetes / ingress-nginx), nicht in diesen Single-Purpose-Sidecar.

## Notes

- Der Sidecar ist deliberate **Single-Purpose**: Header-Rewrite, sonst
  nichts. Keine Caching-Layer (BaSyx ist schon lokal, ETag-Cache bringt
  nichts), kein Rate-Limiting (interne Komponente), kein
  Auth-Forwarding (BaSyx ist im Docker-Netz isoliert). Wenn diese Sachen
  später relevant werden, gehören sie auf eine eigene Reverse-Proxy-
  Ebene, nicht in diesen Container.
- Für Production wäre die nächste sinnvolle Evolution: Reverse-Proxy
  (Traefik) vor dem ganzen Stack, der Routing + TLS + Header-Rewrites
  zentral handhabt. Dann verschwindet dieser Sidecar wieder in der
  generischen Proxy-Konfig. Aber das ist Phase X (Kubernetes-Deployment-
  Task), nicht hier.
