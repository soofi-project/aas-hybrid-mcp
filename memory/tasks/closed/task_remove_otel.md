---
name: Task – OTel aus aas-agent entfernen
description: OpenTelemetry-Packages, Dockerfile-Wrapper und docker-compose-ENV entfernen — Langfuse-Service fehlt, OTel ist toter Code mit CVE-Exposition
type: task
status: open
priority: medium
---

## Background

Sonatype-Check (2026-05-20) hat 5 OTel-Packages in `aas-agent/pyproject.toml` aufgedeckt.
Analyse zeigt: OTel ist **konfiguriert aber funktionslos** —

- Kein manueller OTel-Code in Python-Dateien (kein TracerProvider, kein Span-Setup)
- Auto-Instrumentation läuft via `opentelemetry-instrument`-Wrapper im Dockerfile-CMD
- `docker-compose.yml` schickt Traces an `http://langfuse:4318` — aber der `langfuse`-Service ist **nicht definiert** → Verbindungsfehler beim Start, Traces gehen nirgendwo hin
- `opentelemetry-exporter-otlp` zieht gRPC rein → persistente transitive CVEs (CVE-2026-44431 CVSS 5.3, CVE-2026-44432 CVSS 7.5) die auch in neuesten Versionen erhalten bleiben

Langfuse ist erst für Benchmark C vorgesehen. OTel soll wieder eingebaut werden, wenn Langfuse tatsächlich deployed wird.

## Subtasks

### T1 — `aas-agent/pyproject.toml` bereinigen
Entfernen:
```toml
"opentelemetry-api>=1.30,<2",
"opentelemetry-sdk>=1.30,<2",
"opentelemetry-exporter-otlp>=1.30,<2",
"opentelemetry-instrumentation-fastapi>=0.51b0,<1",
"opentelemetry-instrumentation-httpx>=0.51b0,<1",
```

### T2 — `aas-agent/Dockerfile` CMD vereinfachen
```dockerfile
# vorher:
CMD ["opentelemetry-instrument", "uvicorn", "aas_agent.api:app", "--host", "0.0.0.0", "--port", "8120"]
# nachher:
CMD ["uvicorn", "aas_agent.api:app", "--host", "0.0.0.0", "--port", "8120"]
```

### T3 — `docker-compose.yml` ENV-Block entfernen
OTel-Vars aus dem `aas-agent`-Service-Environment entfernen:
```yaml
OTEL_SERVICE_NAME: aas-agent
OTEL_EXPORTER_OTLP_ENDPOINT: http://langfuse:4318
OTEL_EXPORTER_OTLP_PROTOCOL: http/protobuf
```

## Acceptance Criteria
- `docker build` des aas-agent-Images schlägt nicht wegen fehlendem `opentelemetry-instrument` fehl
- `./up.sh --vllm` startet ohne OTel-/OTLP-Verbindungsfehler in den Logs
- `docker logs aas-agent` zeigt keine `OTLP exporter failed`-Meldungen
- Eine Agent-Anfrage liefert eine normale Antwort zurück

## References
- Files: `aas-agent/pyproject.toml`, `aas-agent/Dockerfile`, `docker-compose.yml`
- `trace.py` (lokaler Conversation-Logger) bleibt unberührt — kein OTel
- Verwandter Kontext: [[task-paper-pattern-modelsize-eval]] (Bench C / Langfuse kommt später)
