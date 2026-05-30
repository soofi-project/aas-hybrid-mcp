"""Count pages of PDF documents stored as File SMEs in Neo4j.

Queries Neo4j for distinct PDF URLs, downloads them in parallel, and
reports page-count statistics. Useful for estimating docling processing load.

Usage:
  python count_pdf_pages.py                # random sample of 200
  python count_pdf_pages.py --sample 500   # larger sample
  python count_pdf_pages.py --all          # all 9k+ unique PDFs (slow)
  python count_pdf_pages.py --workers 10   # parallel download workers
"""

from __future__ import annotations

import argparse
import logging
import random
import statistics
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

log = logging.getLogger("count_pdf_pages")

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = ""

CYPHER_PDF_URLS = """
MATCH (n:File)
WHERE n.value ENDS WITH '.pdf'
RETURN DISTINCT n.value AS url, n.idShortPath AS path
"""

CYPHER_PDF_URLS_HTTP = """
MATCH (n:File)
WHERE n.value ENDS WITH '.pdf' AND n.value STARTS WITH 'http'
RETURN DISTINCT n.value AS url, n.idShortPath AS path
"""

HEADERS = {"User-Agent": "Mozilla/5.0 (research/page-count-analysis)"}
FETCH_TIMEOUT_S = 20


@dataclass
class PageResult:
    url: str
    pages: int | None
    size_kb: int | None
    error: str | None = None


def query_pdf_urls(http_only: bool = False) -> list[dict]:
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD) if NEO4J_USER else None)
    query = CYPHER_PDF_URLS_HTTP if http_only else CYPHER_PDF_URLS
    try:
        with driver.session() as session:
            rows = session.run(query).data()
    finally:
        driver.close()
    # Deduplicate by normalized URL (Cypher DISTINCT misses whitespace/case variants)
    seen: set[str] = set()
    unique: list[dict] = []
    for row in rows:
        key = row["url"].strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(row)
    log.info("Found %d distinct PDF URLs in Neo4j%s (%d raw)",
             len(unique), " (http only)" if http_only else "", len(rows))
    return unique


def fetch_page_count(url: str) -> PageResult:
    try:
        import fitz
    except ImportError:
        return PageResult(url=url, pages=None, size_kb=None,
                          error="PyMuPDF not installed: pip install pymupdf")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        data = urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_S).read()
        doc = fitz.open(stream=data, filetype="pdf")
        pages = len(doc)
        doc.close()
        return PageResult(url=url, pages=pages, size_kb=len(data) // 1024)
    except Exception as e:
        return PageResult(url=url, pages=None, size_kb=None, error=str(e))


def run(urls: list[str], workers: int, until_success: int | None = None) -> list[PageResult]:
    results: list[PageResult] = []
    done = 0
    errors = 0
    successes = 0

    if until_success and workers == 1:
        # Sequential mode: stop as soon as we hit the success target
        for url in urls:
            r = fetch_page_count(url)
            results.append(r)
            done += 1
            if r.error:
                errors += 1
                log.debug("ERROR %s: %s", r.url.split("/")[-1], r.error)
            else:
                successes += 1
                log.info("  [%d/%d] %3d pages  %5d KB  %s",
                         successes, until_success, r.pages, r.size_kb, r.url.split("/")[-1])
                if successes >= until_success:
                    log.info("Reached %d successful downloads (tried %d, errors=%d)",
                             successes, done, errors)
                    break
        return results

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fetch_page_count, u): u for u in urls}
        for future in as_completed(futures):
            r = future.result()
            results.append(r)
            done += 1
            if r.error:
                errors += 1
                log.debug("ERROR %s: %s", r.url.split("/")[-1], r.error)
            else:
                successes += 1
                log.debug("  %3d pages  %5d KB  %s", r.pages, r.size_kb, r.url.split("/")[-1])
            if done % 20 == 0 or done == len(urls):
                log.info("Progress: %d/%d  success=%d  errors=%d", done, len(urls), successes, errors)

    return results


def print_stats(results: list[PageResult], total_unique: int) -> None:
    good = [r for r in results if r.pages is not None]
    bad = [r for r in results if r.pages is None]
    pages = [r.pages for r in good]
    sizes = [r.size_kb for r in good if r.size_kb is not None]

    print(f"\n{'=' * 56}")
    print(f" PDF Page Count Statistics")
    print(f"{'=' * 56}")
    print(f"  Sampled:        {len(results)} of {total_unique} unique PDFs")
    print(f"  Successful:     {len(good)}")
    print(f"  Errors:         {len(bad)}")

    if pages:
        pages_sorted = sorted(pages)
        mean = statistics.mean(pages)
        median = statistics.median(pages)
        p95 = pages_sorted[int(len(pages_sorted) * 0.95)]
        p99 = pages_sorted[int(len(pages_sorted) * 0.99)]

        print(f"\n  Pages per PDF:")
        print(f"    min     = {min(pages)}")
        print(f"    mean    = {mean:.1f}")
        print(f"    median  = {median:.0f}")
        print(f"    p95     = {p95}")
        print(f"    p99     = {p99}")
        print(f"    max     = {max(pages)}")

        projected_pages = int(mean * total_unique)
        print(f"\n  Projected total pages ({total_unique} unique PDFs):")
        print(f"    ~{projected_pages:,} pages  (mean × unique count)")

    if sizes:
        print(f"\n  Size per PDF:")
        print(f"    mean    = {statistics.mean(sizes):.0f} KB")
        print(f"    median  = {statistics.median(sizes):.0f} KB")
        print(f"    total sample = {sum(sizes) // 1024:.0f} MB")
        projected_mb = int(statistics.mean(sizes) * total_unique / 1024)
        print(f"    projected total = ~{projected_mb:,} MB ({total_unique} unique PDFs)")

    print(f"{'=' * 56}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Count PDF pages from Neo4j File SMEs")
    parser.add_argument("--sample", type=int, default=200,
                        help="Random sample size (default: 200)")
    parser.add_argument("--all", action="store_true",
                        help="Process all unique PDFs (slow)")
    parser.add_argument("--workers", type=int, default=1,
                        help="Parallel download workers (default: 1 sequential)")
    parser.add_argument("--until", type=int, default=None,
                        help="Stop after N successful downloads (sequential only)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducible sampling")
    parser.add_argument("--http-only", action="store_true",
                        help="Only include URLs starting with http (skip BaSyx-internal paths)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-5s %(message)s",
        datefmt="%H:%M:%S",
    )

    rows = query_pdf_urls(http_only=args.http_only)
    total_unique = len(rows)
    urls = [r["url"] for r in rows]

    if not args.all:
        n = min(args.sample, len(urls))
        random.seed(args.seed)
        urls = random.sample(urls, n)
        log.info("Using random sample of %d URLs (seed=%d)", n, args.seed)
    else:
        log.info("Processing all %d unique PDF URLs", len(urls))

    log.info("Starting downloads with %d workers...", args.workers)
    t0 = time.monotonic()
    results = run(urls, args.workers, until_success=args.until)
    elapsed = time.monotonic() - t0
    log.info("Done in %.1fs", elapsed)

    print_stats(results, total_unique)


if __name__ == "__main__":
    main()
