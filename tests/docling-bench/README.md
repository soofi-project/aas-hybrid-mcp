# Docling PDF Pipeline Benchmark

Measures the full PDF → Markdown → Chunks → Embeddings → Weaviate pipeline
for 5 fixture manuals (820 pages total) with N runs per PDF.

The benchmark is independent of the stack configuration (`./up.sh` vs
`./up.sh --vllm`). It only needs Weaviate for the write phase, and the
embedding model for the embed phase. All other env vars have defaults
hardcoded in the script.

## Test PDFs

| PDF | Pages | Size |
|-----|-------|------|
| MiR100.pdf | 30 | 2.7 MB |
| MiR250.pdf | 213 | 13.5 MB |
| UR3e.pdf | 238 | 19.5 MB |
| UR20.pdf | 217 | 19.4 MB |
| CRX10iA.pdf | 122 | 2.7 MB |

## Prerequisites

### Minimal (Docling timing only, no Weaviate, no embeddings)

```bash
cd tests/docling-bench

python -m venv .venv
source .venv/Scripts/activate   # Linux: .venv/bin/activate

pip install docling pymupdf weaviate-client langchain-text-splitters langchain-core langchain-openai

# Run — skips Weaviate writes, measures Docling + Chunk + Embed:
python bench_docling.py --no-weaviate
```

### Full pipeline (with Weaviate)

```bash
# Start Weaviate only:
docker compose up weaviate

# Then run the benchmark:
python bench_docling.py
```

The embedding model defaults to `openai:qwen3-embedding-8b` against
`http://10.2.10.33:4000/v1`. Override with env vars if needed:

```bash
OPENAI_BASE_URL=https://api.openai.com/v1 OPENAI_API_KEY=sk-... EMBEDDING_MODEL=openai:text-embedding-3-small python bench_docling.py
```

### GPU variant (on H200 or any CUDA GPU)

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu121
python bench_docling.py --device cuda --no-weaviate
```

## Usage

```bash
# CPU benchmark, N=3 (default):
python bench_docling.py

# CPU benchmark, N=10:
python bench_docling.py --runs 10

# CPU benchmark without Weaviate (Docling + Chunk + Embed only):
python bench_docling.py --no-weaviate

# GPU benchmark, N=3 (default):
python bench_docling.py --device cuda

# GPU benchmark, N=10:
python bench_docling.py --device cuda --runs 10
```

## Output

Stdout table:

```
PDF              Pages  Runs  convert    chunk    embed    write    total  chunks
--------------------------------------------------------------------------------
MiR100.pdf         30    10   12.345±0.42   0.012   1.234   0.056  13.647    45.0
MiR250.pdf        213    10   98.765±3.21   0.089   8.901   0.234 107.989   320.0
...
```

JSON results in `results/`:
- `bench_cpu_20260527T120000Z.json`
- `bench_cuda_20260527T140000Z.json`

## What is measured per run

| Phase | Description |
|-------|-------------|
| `convert_s` | Docling PDF → Markdown (layout model + table structure) |
| `chunk_s` | Markdown → Chunks (header split + recursive split) |
| `embed_s` | Chunks → Embeddings (LangChain batch) |
| `write_s` | Embeddings → Weaviate (insert_many) |
| `total_s` | Sum of all phases |

The warmup run (MiR100.pdf) loads Docling's models into memory and is not counted.

## Cleanup

The script creates a dedicated Weaviate collection (`BenchDoclingCpu` or
`BenchDoclingGpu`) and **drops it on exit**. If the script crashes, the
collection may remain — drop manually:

```bash
curl -X DELETE http://localhost:8080/v1/schema/BenchDoclingCpu
curl -X DELETE http://localhost:8080/v1/schema/BenchDoclingGpu
```

## For the paper

Use the results to fill §06 (Architecture, Document Ingestion section):

> "On a benchmark set of five fixture manuals (30–238 pages, 820 pages total),
> CPU-based conversion takes X s per document on average. On an NVIDIA H200,
> the same workload completes in Y s (Z× speedup), at identical chunk count
> (±5%)."
