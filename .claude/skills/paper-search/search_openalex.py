#!/usr/bin/env python
"""OpenAlex search wrapper for academic paper discovery.

OpenAlex (https://openalex.org/) indexes 250M+ scholarly works — arXiv, IEEE,
ACM, Springer, Elsevier — and is free, no API key required. Polite usage adds
a mailto identifier so OpenAlex can route requests to a faster pool.

Usage:
    python search_openalex.py "query terms"                    # search
    python search_openalex.py --doi 10.1109/ETFA54631.2023.10275464  # DOI lookup
    python search_openalex.py "query" --limit 20 --json       # 20 results, JSON output
    python search_openalex.py "query" --year-from 2023        # year filter

Output: human-readable table by default; --json for downstream piping.

This script lives bundled with the /paper-search skill (Layered Determinism:
the skill carries its tool, not just prompt instructions to call an API).
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

OPENALEX_BASE = "https://api.openalex.org"
USER_AGENT = "aas-hybrid-mcp/paper-search (gerhard.sonnenberg@googlemail.com)"
MAILTO = "gerhard.sonnenberg@googlemail.com"


def _request(path: str, params: dict | None = None) -> dict:
    if params is None:
        params = {}
    params["mailto"] = MAILTO
    qs = urllib.parse.urlencode(params)
    url = f"{OPENALEX_BASE}/{path}?{qs}" if params else f"{OPENALEX_BASE}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _reconstruct_abstract(inv_index: dict | None) -> str:
    """OpenAlex stores abstracts as inverted index {word: [positions]}. Reconstruct."""
    if not inv_index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, pos_list in inv_index.items():
        for p in pos_list:
            positions.append((p, word))
    positions.sort()
    return " ".join(w for _, w in positions)


def _extract_work(work: dict) -> dict:
    """Pull the fields we care about out of an OpenAlex work record."""
    authors = [
        a.get("author", {}).get("display_name", "?")
        for a in work.get("authorships", [])
    ]
    primary_loc = work.get("primary_location") or {}
    source = primary_loc.get("source") or {}
    oa = work.get("open_access") or {}

    return {
        "title": work.get("title") or "?",
        "authors": authors,
        "year": work.get("publication_year"),
        "cited_by_count": work.get("cited_by_count", 0),
        "doi": (work.get("doi") or "").replace("https://doi.org/", "") or None,
        "venue": source.get("display_name"),
        "venue_type": source.get("type"),
        "is_oa": oa.get("is_oa", False),
        "pdf_url": oa.get("oa_url"),
        "openalex_id": work.get("id"),
        "abstract": _reconstruct_abstract(work.get("abstract_inverted_index")),
    }


def search(query: str, limit: int, year_from: int | None) -> list[dict]:
    params = {
        "search": query,
        "per-page": str(limit),
        "sort": "relevance_score:desc",
    }
    if year_from:
        params["filter"] = f"publication_year:>{year_from - 1}"
    data = _request("works", params)
    return [_extract_work(w) for w in data.get("results", [])]


def lookup_doi(doi: str) -> dict | None:
    doi = doi.strip().replace("https://doi.org/", "")
    try:
        data = _request(f"works/doi:{doi}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    return _extract_work(data)


def _format_table(works: list[dict]) -> str:
    if not works:
        return "(no results)"
    lines = []
    for i, w in enumerate(works, 1):
        authors_str = ", ".join(w["authors"][:3])
        if len(w["authors"]) > 3:
            authors_str += f" et al. ({len(w['authors'])} total)"
        oa_marker = " [OA]" if w["is_oa"] else ""
        lines.append(f"[{i}] {w['title']}")
        lines.append(f"    {authors_str} — {w['year']} — cited {w['cited_by_count']}x{oa_marker}")
        if w["venue"]:
            lines.append(f"    Venue: {w['venue']} ({w['venue_type'] or '?'})")
        if w["doi"]:
            lines.append(f"    DOI: {w['doi']}")
        if w["pdf_url"]:
            lines.append(f"    PDF:  {w['pdf_url']}")
        if w["abstract"]:
            abstract = w["abstract"][:300] + ("…" if len(w["abstract"]) > 300 else "")
            lines.append(f"    {abstract}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OpenAlex academic paper search")
    parser.add_argument("query", nargs="?", default=None, help="Free-text search query")
    parser.add_argument("--doi", default=None, help="Look up a single work by DOI")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--year-from", type=int, default=None, help="Only results from this year or later")
    parser.add_argument("--json", action="store_true", help="Raw JSON output instead of table")
    args = parser.parse_args()

    if args.doi:
        work = lookup_doi(args.doi)
        if not work:
            print(f"No work found for DOI {args.doi}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(work, indent=2))
        else:
            print(_format_table([work]))
        return

    if not args.query:
        parser.error("Provide a query or --doi")

    works = search(args.query, args.limit, args.year_from)
    if args.json:
        print(json.dumps(works, indent=2))
    else:
        print(_format_table(works))


if __name__ == "__main__":
    main()
