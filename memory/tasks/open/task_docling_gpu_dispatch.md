---
name: Task - Docling GPU Dispatch + Performance Measurement
description: Verlagere CPU-bound PDF→Markdown-Konvertierung auf einen GPU-Service auf H200; quantifiziere Speedup vs. CPU-Baseline
type: task
status: open
priority: medium
depends_on: [task_rag_metadata_overhaul]
---

## Summary

`embedding-service` macht heute docling-PDF→Markdown auf CPU. Gemessene
Realzeiten aus den Logs vom 2026-05-13:

- `tmpjyf8xmov.pdf`: 163.42 s
- `tmpwwqu9kmw.pdf`: 167.25 s

Bei 5 Fixture-PDFs × ~165 s = ~14 min einmaliger Ingest, akzeptabel. Bei
Production-Scale (1000+ Assets × mehrere Manuals) ist das blockierend.

**Ziel:** docling-Modelle (`layout-heron`, `tableformer`) auf H200 GPU
laufen lassen, embedding-service dispatcht via HTTP. Per `DOCLING_GPU_URL`
zur Laufzeit umschaltbar → A/B-Vergleich gegen CPU-Baseline ohne Code-Änderung.

## Architektur

**Scope-Abgrenzung.** Nur die docling-Konvertierung wandert auf H200 — *nicht*
der gesamte embedding-service. Heute hat embedding-service fünf
Verantwortlichkeiten:

1. Kafka-Events konsumieren
2. PDF von BaSyx runterladen
3. **docling-Konvertierung** ← einziger GPU-relevanter Teil, wird ausgelagert
4. Embedding berechnen (läuft via vLLM ohnehin schon auf H200, externer Call)
5. Chunks in Weaviate schreiben

Ihn komplett zu verschieben würde Kafka, BaSyx und Weaviate von H200 aus
erreichen müssen — Netzwerk-/Firewall-Aufwand, der für ein
A/B-Speedup-Experiment unverhältnismäßig ist und die Messung verfälscht.

**Klarstellung — vLLM ≠ docling-Runtime.** vLLM serviert Decoder-LLMs
(Qwen3.5-120B) per OpenAI-kompatibler API. docling nutzt eigene
Vision-Transformer (`docling-layout-heron`, `tableformer-v2`) direkt über
PyTorch. Beide laufen auf derselben H200-GPU, teilen aber keine
Serving-Infrastruktur und kein Modell-Format. docling-Modelle gehören
**nicht** in einen vLLM-Ordner; sie leben unter
`~/.cache/docling/models/` bzw. dem in `DOCLING_ARTIFACTS_PATH`
spezifizierten Pfad — exakt wie im embedding-service-Image gehandhabt.

**Komponenten:**
- Neuer Service `docling-gpu-service/` (parallel zu `embedding-service/`)
- FastAPI + uvicorn, hält Modelle persistent im VRAM (kein Re-Init pro Request — Singleton-Converter beim Service-Start instanziieren)
- Läuft auf H200 mit GPU-Reservation (compose `deploy.resources.reservations.devices`)
- embedding-service `pdf.py` dispatcht:
  - `DOCLING_GPU_URL` gesetzt → `httpx.post(f"{url}/convert", content=pdf_bytes)`
  - `DOCLING_GPU_URL` unset → bestehender lokaler `DocumentConverter`-Pfad
- Selbe Modelle wie Image-Bake (`docling-tools models download` + `DOCLING_ARTIFACTS_PATH`), aber `AcceleratorOptions(device="cuda")` statt cpu-default
- PyTorch **CUDA-Wheels** im docling-gpu-Image (nicht CPU-only wie im embedding-service)

## Subtasks

### T1: Baseline-Instrumentierung (heutiger CPU-Pfad)

**`embedding-service/pdf.py`:**
- `convert_pdf_to_markdown()` mit Zeitstempeln pro Phase: download, convert, chunk
- Pro PDF loggen: bytes, page_count, ms_to_markdown, ms_to_chunks, chunk_count
- Log-Format strukturiert (JSON-like), damit man später per `jq` / awk auswerten kann

**`embedding-service/handlers.py`:**
- Gesamtdauer pro Submodel-Element-Ingest (download bis Weaviate-Insert)

### T2: `docling-gpu-service` Skeleton

**Neues Verzeichnis `docling-gpu-service/`:**
- `pyproject.toml`: deps = fastapi, uvicorn, docling, torch (mit CUDA)
- `app.py`: FastAPI mit `POST /convert` (bytes → markdown), `GET /healthz` (CUDA verfügbar? Modelle geladen?)
- `Dockerfile`:
  - Builder mit PyTorch **CUDA**-Wheels (nicht CPU-only wie embedding-service)
  - `docling-tools models download` ins Image gebakt
  - `ENV HF_HUB_OFFLINE=1`
  - Runtime mit `nvidia-container-runtime`-kompatibler Konfig
- Env: `MODEL_DEVICE=cuda` (default), `MODEL_DTYPE=float16` (optional für VRAM-Sparsamkeit)
- Modelle einmal beim Service-Start laden + im Memory halten (Singleton-Converter)

### T3: Dispatcher in `pdf.py`

**`embedding-service/pdf.py`:**
- Env-Var `DOCLING_GPU_URL` lesen (config.py)
- Wenn gesetzt: HTTP-Call statt lokaler Conversion
  ```python
  resp = httpx.post(f"{url}/convert", content=pdf_bytes, timeout=600)
  resp.raise_for_status()
  markdown = resp.text
  ```
- Wenn unset: bestehender lokaler `DocumentConverter`-Pfad bleibt
- Single Code Path: dieselbe Timing-Instrumentierung aus T1 deckt beide Modi ab
- Fehlersemantik: bei Network-Error gegen GPU-Service **lautes Fehlschlagen**, kein stiller CPU-Fallback (clean A/B)

### T4: Deployment auf H200

- Entscheidung: standalone `docker run --gpus all -p 8201:8000 ...` vs. compose-Overlay falls H200 schon vLLM-Stack hostet
- Netzwerk: embedding-service-Container muss H200-Port erreichen — Firewall, DNS / IP, ggf. Tailscale/internes Netz
- Verifikation: während eines Test-Converts `nvidia-smi` auf H200 → Auslastung > 0% sichtbar
- Container Health-Check via `GET /healthz` in compose

### T5: A/B-Benchmark

- **Run 1 (CPU-Baseline):** `DOCLING_GPU_URL` unset; Weaviate-Collection gedroppt; volles Fixture-Set ingest (Hall3/4 + 7 Roboter-Instanzen + 5 Type-Shells); Zahlen aus T1-Logs aggregieren
- **Run 2 (GPU):** `DOCLING_GPU_URL=http://h200:8201`; Weaviate gedroppt; selbes Fixture-Set; aus T1-Logs aggregieren
- **Metriken:** total wall-clock, per-PDF mean + p95, per-page time
- **Äquivalenz-Check:** Chunk-Count pro PDF und Heading-Verteilung zwischen CPU/GPU innerhalb ±5 %; bei größerer Drift Output-Diff untersuchen (GPU-Inference kann numerisch leicht abweichen → andere Layout-Entscheidungen?)
- Resultate als Tabelle in diese Task-Datei eintragen

### T6: Dokumentation + Paper-Bezug

- T5-Resultate als Tabelle am Ende dieser Datei eintragen
- **`paper/etfa2026/content/06-architecture.tex` §6.2 Document Ingestion** — Platzhalter `[X]` und `[Y]` mit echten Messzahlen aus T5 ersetzen
- **`memory/future_phases.md` Phase 9** — mit konkreten Messzahlen ergänzen: CPU baseline X s/PDF, GPU Y s/PDF, Speedup Z×
- **Ausblick fürs Paper** (siehe eigener Abschnitt unten)

## Acceptance Criteria

- `DOCLING_GPU_URL`-Toggle funktioniert ohne Code-Änderung (nur env-Var setzen oder löschen)
- GPU-Run ≥5× schneller als CPU-Baseline auf per-PDF-Mittelwert
- Markdown-Output strukturell äquivalent (Chunk-Count ±5 %, sonst Drift-Investigation)
- `nvidia-smi` bestätigt GPU-Utilization > 0 % während Convert-Phase
- Health-Check über `GET /healthz` reportet CUDA verfügbar + Modelle geladen

## Architektur-Entscheidungen

**Entschieden (2026-05-13, nach Klärung der H200-Infrastruktur):**

1. **Service-Shape: FastAPI + uvicorn.** Triton verworfen — Setup-Overhead für einen Research-Bench nicht gerechtfertigt; eine spätere Migration zu Triton bleibt offen, falls produktive Model-Lifecycle-Verwaltung (mehrere Modellversionen parallel, A/B-Routing) dazukommt. FastAPI passt zum Rest des Stacks (embedding-service, mcp-server beide Flask/FastAPI-style).
2. **Batching: single-PDF-per-Request in v1.** Bench-B-Workload ist sequentiell. Horizontale Skalierung adressiert Phase 9.5 (parallele Connect-Consumer, die alle denselben GPU-Service hämmern), nicht der GPU-Service selbst — die Modelle im VRAM sind stateless und thread-safe.
3. **Fallback bei `DOCLING_GPU_URL`-Ausfall: lautes Fehlschlagen.** Stiller CPU-Fallback würde die A/B-Messung verfälschen und produktive Service-Ausfälle maskieren. Wenn der GPU-Service wegfällt, soll der embedding-service den Kafka-Event mit `TransientProcessingError` zurückstellen, damit Retry/Replay die normale Wiederherstellung übernimmt.

**Noch offen vor T4:**

4. **Deployment-Topologie auf H200.** Auf H200 liegt bereits eine
   `docker-compose.yml` (vermutlich vLLM-Stack). Empfehlung: `docling-gpu-service`
   **in den bestehenden compose-Stack einhängen** — neuer Service-Block neben
   vLLM, gemeinsame NVIDIA-Runtime-Konfig, gemeinsame `up`/`down`-Orchestrierung,
   kein Konflikt um GPU-Reservation weil vLLM auf seinen Modellen sitzt und docling
   nur Layout/TableFormer braucht (zusammen ~1–2 GB VRAM, peanuts neben Qwen).
   Standalone bleibt Plan B falls Compose-Datei-Ownership oder Port-Konflikte
   auftreten.
5. **CUDA-Version-Match.** Die vLLM-Container auf H200 nutzen eine bestimmte
   CUDA-Version; die PyTorch-Wheels im docling-gpu-Image müssen damit
   kompatibel sein. Vor T2 die Version verifizieren (am einfachsten:
   `nvidia-smi` auf der Box, dann das passende `--index-url
   https://download.pytorch.org/whl/cuXXX` wählen — typisch cu121 oder cu124
   für H200-Driver-Stand 2026).
6. **Modell-Versionierung über Image-Tags.** Wie im embedding-service-Image:
   `docling-tools models download` baked die Modelle ins Image. Beim Image-
   Rebuild bekommt man neue Modell-Versionen automatisch. Bei einem Volume-
   Mount muss man die Stale-Cache-Falle (alte Modelle maskieren neue) wieder
   bedenken — Empfehlung: **kein Volume-Mount für docling-gpu-service**, weil
   der Service stateless ist und ein Image-Rebuild billig sein soll.

## Ausblick / Paper-Anschluss

Dieser Task ist nicht nur Engineering-Optimierung — die **Messzahlen sind ein
direkter Datenpunkt für die Paper-Story**:

- **Phase 9 im `future_phases.md`** ist heute hypothesengetrieben („GPU-Dispatch
  würde helfen"). Nach T5 ist es **gemessen**: konkrete Speedup-Ratio mit
  reproduzierbarem Setup.
- **Für das ETFA-2026-Paper** (oder das Folge-Paper, falls Phase 9 dort
  ausführlicher behandelt wird) ein einzelner Satz mit den Messzahlen ist
  stärker als jede qualitative „könnte schneller sein"-Aussage. Beispiel-
  Formulierung: *„On commodity CPU, docling-based conversion of Fanuc-class
  manuals takes ~165 s/document; routing the same workload to a GPU-resident
  docling service on H200 reduces this to ~X s, a Y× speedup at no quality
  cost (chunk count ±5 %)."*
- **Story-Anschluss zur Data-Sovereignty-Argumentation:** zeigt, dass die
  ganze Pipeline auch unter Production-Scale-Latenz on-premise funktioniert
  — die GPU bleibt im Haus, kein Cloud-Dispatch-Tradeoff.
- **Anschluss zu Phase 9.5 (parallel docling-java consumers):** GPU-Dispatch
  und Connect-side-Parallelisierung sind komplementär — mehrere Consumer
  saturieren dieselbe H200-GPU ohne Konflikte (Modelle im VRAM stateless,
  thread-safe). Im Paper als „two orthogonal scaling axes" framen.
- **Verbindung zu Phase 13/14 (LoRA + CDC):** GPU-Service-Architektur ist
  derselbe Pattern wie ein potentieller LoRA-Inference-Service — beide
  laufen als HTTP-Microservice auf H200, beide werden vom embedding-service
  / agent dispatcht. Konsistente Architektur fürs Paper.

## Notes

- Erstmal nur die docling-Modelle auf GPU — Embedding-Generation
  (Qwen3-Embedding-8B) ist davon unabhängig und läuft schon via vLLM auf H200.
- Kein Modellwechsel: layout-heron und tableformer sind GPU-fähig out-of-the-box,
  docling unterstützt `AcceleratorOptions(device="cuda")` nativ.
- VRAM-Bedarf: layout-heron + tableformer zusammen ~1-2 GB, lächerlich neben
  Qwen3.5-120B. Co-Existenz auf H200 unproblematisch.
- Falls Triton später doch interessant wird (für ConceptDescription-Embedding,
  Multimodal-Search etc.), kann der FastAPI-Service als „v0" stehenbleiben
  und Triton parallel dazu aufgebaut werden.
