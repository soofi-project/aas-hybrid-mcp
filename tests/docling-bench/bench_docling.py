"""Docling PDF→Markdown→Chunks→Embeddings→Weaviate benchmark.

Measures the full embedding pipeline for 5 fixture manuals with N runs each.
Supports CPU (default) and CUDA via --device.

Usage:
  python bench_docling.py                         # CPU, N=10
  python bench_docling.py --runs 3                # CPU, N=3
  python bench_docling.py --no-weaviate           # skip Weaviate writes
  python bench_docling.py --device cuda           # GPU/CUDA
  python bench_docling.py --device cuda --runs 3 --no-weaviate
"""

from __future__ import annotations

import argparse
import fitz
import hashlib
import json
import logging
import os
import statistics
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

EMBEDDING_SERVICE_DIR = Path(__file__).resolve().parent.parent.parent / "embedding-service"
DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "docs"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

sys.path.insert(0, str(EMBEDDING_SERVICE_DIR))

os.environ.setdefault("WEAVIATE_HOST", "localhost")
os.environ.setdefault("WEAVIATE_PORT", "8070")
os.environ.setdefault("WEAVIATE_GRPC_PORT", "50051")
os.environ.setdefault("BASYX_SUBMODEL_REPO", "http://localhost:8081")
os.environ.setdefault("BASYX_PUBLIC_URL", "http://localhost:8081")
os.environ.setdefault("CHUNK_SIZE", "1500")
os.environ.setdefault("CHUNK_OVERLAP", "200")
os.environ.setdefault("EMBEDDING_BATCH_SIZE", "100")
os.environ.setdefault("DOWNLOAD_TIMEOUT", "60")
os.environ.setdefault("ON_PROCESSING_ERROR", "abort")
os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

if "EMBEDDING_MODEL" not in os.environ:
    os.environ["EMBEDDING_MODEL"] = "openai:qwen3-embedding-8b"
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "dummy"
if "OPENAI_BASE_URL" not in os.environ:
    os.environ["OPENAI_BASE_URL"] = "http://10.2.10.33:4000/v1"

os.environ.setdefault("WEAVIATE_COLLECTION", "bench_docling_cpu")

from pdf import ChunkData, chunk_text, compute_embeddings, convert_pdf_to_markdown, reset_converter, _items_to_markdown_with_page_markers

PDF_FILES = [
    "MiR100.pdf",
    "MiR250.pdf",
    "UR3e.pdf",
    "UR20.pdf",
    "CRX10iA.pdf",
]

log = logging.getLogger("bench_docling")

_gpu_converter = None


def _reset_converters() -> None:
    import gc
    global _gpu_converter
    reset_converter()
    _gpu_converter = None
    gc.collect()


def _get_gpu_converter():
    global _gpu_converter
    if _gpu_converter is None:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import AcceleratorOptions, PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption

        pipeline_options = PdfPipelineOptions(
            artifacts_path=os.environ.get("DOCLING_ARTIFACTS_PATH"),
            accelerator_options=AcceleratorOptions(device="cuda"),
        )
        pipeline_options.do_table_structure = os.environ.get("PDF_TABLE_STRUCTURE", "false").lower() == "true"
        pipeline_options.do_ocr = False
        pipeline_options.queue_max_size = int(os.environ.get("DOCLING_QUEUE_MAX_SIZE", "8"))
        _gpu_converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
        )
    return _gpu_converter


def _convert_pdf(pdf_bytes: bytes, device: str) -> str:
    if device == "cuda":
        from docling.datamodel.base_models import ConversionStatus

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
        try:
            result = _get_gpu_converter().convert(tmp_path)
            if result.status == ConversionStatus.SUCCESS:
                return _items_to_markdown_with_page_markers(result.document)
            return result.document.export_to_markdown()
        finally:
            os.unlink(tmp_path)
    return convert_pdf_to_markdown(pdf_bytes)


def _make_bench_collection(weaviate_available: bool, bench_collection: str) -> object | None:
    if not weaviate_available:
        return None
    import weaviate
    import weaviate.collections.classes.config as wvc

    client = weaviate.connect_to_custom(
        http_host=os.environ["WEAVIATE_HOST"],
        http_port=int(os.environ["WEAVIATE_PORT"]),
        http_secure=False,
        grpc_host=os.environ["WEAVIATE_HOST"],
        grpc_port=int(os.environ["WEAVIATE_GRPC_PORT"]),
        grpc_secure=False,
        skip_init_checks=True,
    )

    if client.collections.exists(bench_collection):
        log.info("Dropping existing bench collection %s", bench_collection)
        client.collections.delete(bench_collection)

    client.collections.create(
        name=bench_collection,
        vector_config=wvc.Configure.Vectors.self_provided(),
        properties=[
            wvc.Property(name="text", data_type=wvc.DataType.TEXT),
            wvc.Property(name="source", data_type=wvc.DataType.TEXT),
            wvc.Property(name="source_heading", data_type=wvc.DataType.TEXT),
            wvc.Property(name="source_page", data_type=wvc.DataType.INT),
            wvc.Property(name="source_url", data_type=wvc.DataType.TEXT),
            wvc.Property(name="source_filename", data_type=wvc.DataType.TEXT),
            wvc.Property(name="submodel_id", data_type=wvc.DataType.TEXT),
            wvc.Property(name="sm_element_path", data_type=wvc.DataType.TEXT),
            wvc.Property(name="id_short", data_type=wvc.DataType.TEXT),
            wvc.Property(name="content_hash", data_type=wvc.DataType.TEXT),
        ],
    )
    log.info("Created bench collection %s", bench_collection)
    return client


def _cleanup_bench_collection(client: object | None, bench_collection: str) -> None:
    if client is None:
        return
    if client.collections.exists(bench_collection):
        client.collections.delete(bench_collection)
        log.info("Dropped bench collection %s", bench_collection)
    client.close()


def _run_single(
    pdf_bytes: bytes,
    pdf_name: str,
    pages: int,
    run_idx: int,
    client: object | None,
    device: str,
    bench_collection: str,
) -> dict:
    submodel_id = f"bench_{pdf_name}_{run_idx}"
    content_hash = hashlib.sha256(pdf_bytes).hexdigest()

    t0 = time.perf_counter()
    markdown = _convert_pdf(pdf_bytes, device)
    t_convert = time.perf_counter() - t0

    t1 = time.perf_counter()
    chunks: list[ChunkData] = chunk_text(markdown)
    t_chunk = time.perf_counter() - t1

    texts = [c.text for c in chunks]
    t_embed = 0.0
    vectors = []
    if texts:
        t2 = time.perf_counter()
        vectors = compute_embeddings(texts)
        t_embed = time.perf_counter() - t2

    t_write = 0.0
    if client is not None:
        import weaviate.collections.classes.data as wcd

        t3 = time.perf_counter()
        collection = client.collections.get(bench_collection)
        data_objects = [
            wcd.DataObject(
                properties={
                    "text": ch.text,
                    "source": "benchmark",
                    "source_heading": ch.heading,
                    "source_page": ch.page,
                    "source_url": "",
                    "source_filename": pdf_name,
                    "submodel_id": submodel_id,
                    "sm_element_path": "",
                    "id_short": "bench",
                    "content_hash": content_hash,
                },
                vector=v,
            )
            for ch, v in zip(chunks, vectors)
        ]
        if data_objects:
            collection.data.insert_many(data_objects)
        t_write = time.perf_counter() - t3

    t_total = time.perf_counter() - t0

    return {
        "pdf": pdf_name,
        "run": run_idx,
        "pages": pages,
        "chunks": len(chunks),
        "convert_s": round(t_convert, 3),
        "chunk_s": round(t_chunk, 3),
        "embed_s": round(t_embed, 3),
        "write_s": round(t_write, 3),
        "total_s": round(t_total, 3),
    }


def _warmup(pdf_path: Path, device: str) -> None:
    log.info("Warmup (%s): converting %s ...", device, pdf_path.name)
    pdf_bytes = pdf_path.read_bytes()
    markdown = _convert_pdf(pdf_bytes, device)
    chunk_text(markdown)
    log.info("Warmup done (%d chars markdown)", len(markdown))


def _summarize(runs: list[dict]) -> dict:
    fields = ["convert_s", "chunk_s", "embed_s", "write_s", "total_s"]
    summary = {"pdf": runs[0]["pdf"], "pages": runs[0]["pages"], "runs": len(runs)}
    for f in fields:
        vals = [r[f] for r in runs]
        summary[f"{f}_mean"] = round(statistics.mean(vals), 3)
        summary[f"{f}_std"] = round(statistics.stdev(vals), 3) if len(vals) > 1 else 0.0
        summary[f"{f}_min"] = round(min(vals), 3)
        summary[f"{f}_max"] = round(max(vals), 3)
    summary["chunks_mean"] = round(statistics.mean([r["chunks"] for r in runs]), 1)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Docling PDF pipeline benchmark")
    parser.add_argument("--runs", type=int, default=3, help="Number of runs per PDF (default: 3)")
    parser.add_argument("--no-weaviate", action="store_true", help="Skip Weaviate writes")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu", help="Compute device (default: cpu)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-5s %(message)s",
        datefmt="%H:%M:%S",
    )

    device = args.device
    n = args.runs
    weaviate_available = not args.no_weaviate
    bench_collection = "BenchDoclingCpu" if device == "cpu" else "BenchDoclingGpu"

    log.info("Device: %s", device)
    log.info("Runs per PDF: %d", n)
    log.info("Weaviate: %s", "enabled" if weaviate_available else "disabled")
    log.info("Embedding model: %s", os.environ.get("EMBEDDING_MODEL"))
    log.info("Embedding service: %s", EMBEDDING_SERVICE_DIR)

    page_counts: dict[str, int] = {}
    for pdf_name in PDF_FILES:
        pdf_path = DOCS_DIR / pdf_name
        if pdf_path.exists():
            doc = fitz.open(str(pdf_path))
            try:
                page_counts[pdf_name] = len(doc)
            finally:
                doc.close()

    client = _make_bench_collection(weaviate_available, bench_collection)

    try:
        _warmup(DOCS_DIR / PDF_FILES[0], device)

        all_runs: list[dict] = []
        all_summaries: list[dict] = []

        header = f"{'PDF':14s} {'Pages':>5s} {'Runs':>4s} {'convert':>9s} {'chunk':>8s} {'embed':>8s} {'write':>8s} {'total':>8s} {'chunks':>7s}"
        print(f"\n{header}")
        print("-" * len(header))

        for pdf_name in PDF_FILES:
            pdf_path = DOCS_DIR / pdf_name
            if not pdf_path.exists():
                log.warning("Skipping %s — not found", pdf_name)
                continue

            pdf_bytes = pdf_path.read_bytes()
            runs = []

            try:
                for i in range(n):
                    log.info("Run %2d/%d: %s", i + 1, n, pdf_name)
                    result = _run_single(pdf_bytes, pdf_name, page_counts[pdf_name], i, client, device, bench_collection)
                    runs.append(result)
                    all_runs.append(result)
            finally:
                _reset_converters()

            summary = _summarize(runs)
            all_summaries.append(summary)

            print(
                f"{pdf_name:14s} {summary['pages']:>5d} {summary['runs']:>4d}"
                f" {summary['convert_s_mean']:>8.3f}±{summary['convert_s_std']:.2f}"
                f" {summary['chunk_s_mean']:>7.3f}"
                f" {summary['embed_s_mean']:>7.3f}"
                f" {summary['write_s_mean']:>7.3f}"
                f" {summary['total_s_mean']:>7.3f}"
                f" {summary['chunks_mean']:>7.1f}"
            )

        total_pages = sum(s["pages"] for s in all_summaries)
        total_mean = sum(s["total_s_mean"] for s in all_summaries)
        print("-" * len(header))
        print(
            f"{'TOTAL':14s} {total_pages:>5d} {n * len(all_summaries):>4d}"
            f" {'':>9s} {'':>8s} {'':>8s} {'':>8s}"
            f" {total_mean:>7.3f}"
            f" {sum(s['chunks_mean'] for s in all_summaries):>7.1f}"
        )

        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        result_path = RESULTS_DIR / f"bench_{device}_{ts}.json"
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        result_path.write_text(
            json.dumps(
                {
                    "device": device,
                    "runs_per_pdf": n,
                    "weaviate": weaviate_available,
                    "embedding_model": os.environ.get("EMBEDDING_MODEL"),
                    "timestamp": ts,
                    "summaries": all_summaries,
                    "raw_runs": all_runs,
                },
                indent=2,
            )
        )
        log.info("Results written to %s", result_path)

    finally:
        _cleanup_bench_collection(client, bench_collection)


if __name__ == "__main__":
    main()
