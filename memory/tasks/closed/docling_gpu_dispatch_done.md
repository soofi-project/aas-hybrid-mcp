---
name: Docling GPU Dispatch Done
description: CPU vs. CUDA benchmark durchgeführt (3.8× speedup). Ergebnisse in §10 Bench A2 und in tests/docling-bench/.
type: task
status: done
---

## Was umgesetzt

**Benchmark:** CPU vs. CUDA auf H200, 5 PDFs (MiR100, MiR250, UR3e, UR20, CRX10iA), N=3 pro PDF.

**Ergebnisse (Convert-Latenz):**

| PDF | Pages | CPU (s) | CUDA (s) | Speedup |
|---|---|---|---|---|
| MiR100 | 30 | 21.0 | 6.2 | 3.3× |
| MiR250 | 213 | 145.1 | 41.2 | 3.5× |
| UR3e | 238 | 192.7 | 46.2 | 4.2× |
| UR20 | 217 | 155.4 | 43.5 | 3.6× |
| CRX10iA | 122 | 87.9 | 20.7 | 4.3× |
| **Total** | **820** | **602.1** | **157.8** | **3.8×** |

**Paper-Integration:** Tabelle in §10 Benchmark A2 (`10-evaluation.tex`, Table `tab:bench_a2`). Werte direkt aus den Bench-Ergebnissen übernommen.

**Nicht umgesetzt (bewusst):**
- Kein dauerhafter `docling-gpu-service` als eigener Docker-Service. Stattdessen Benchmark-Only: `tests/docling-bench/bench_docling.py` mit lokalem `.venv` und CUDA-Support.
- Kein `DOCLING_GPU_URL`-Dispatcher im embedding-service. Der Bench beweist den Speedup; produktive Integration ist Future Work.

## Referenzen

- Bench-Script: `tests/docling-bench/bench_docling.py`
- CPU-Results: `tests/docling-bench/results/bench_cpu_20260527T190919Z.json`
- CUDA-Results: `tests/docling-bench/results/bench_cuda_20260527T200725Z.json`
- Paper: `paper/etfa2026/content/10-evaluation.tex` Table `tab:bench_a2`
