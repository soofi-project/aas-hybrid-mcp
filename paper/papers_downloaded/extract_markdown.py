"""PDF → Markdown extractor for papers_downloaded/

Usage:
    python extract_markdown.py                              # all PDFs without markdown
    python extract_markdown.py path/to/paper.pdf           # single PDF
    python extract_markdown.py --short-name foo paper.pdf  # custom output name

Output format: single .md file per PDF with ### Page N sections, matching the
existing convention in this directory.

Dependencies: pip install pymupdf4llm
"""

import argparse
import os
import re
import sys

import fitz
from pymupdf4llm import to_markdown


def find_page_markers(lines, page_count):
    """Find page marker lines (standalone numbers) and return [(line_no, page_num), ...].

    Handles three cases:
    1. Natural ordering: consecutive standalone numbers starting from 1
    2. Conference footers: consecutive numbers not starting from 1 (e.g. 5303–5315)
    3. No markers: return None → caller should use fallback
    """
    raw = []
    for i, line in enumerate(lines):
        s = line.strip()
        if re.match(r"^\d+$", s):
            val = int(s)
            raw.append((i, val))

    if not raw:
        return None

    # Check for consecutive run matching page_count
    for start in range(len(raw)):
        run = []
        for j in range(start, len(raw)):
            if j > start and raw[j][1] != raw[j - 1][1] + 1:
                break
            run.append(raw[j])
            if len(run) >= page_count:
                return run[:page_count]

    return None


def extract_title(lines):
    """Extract paper title from pymupdf4llm output."""
    for line in lines:
        s = line.strip()
        if s.startswith("#"):
            title = re.sub(r"^#+\s*", "", s).strip()
            # Strip trailing bold markers
            title = title.strip("*")
            if title:
                return title
        if s:
            title = s.strip("*")
            if title:
                return title
    return "Paper"


def split_by_markers(lines, markers):
    """Split lines into per-page content strings using page marker positions."""
    pages = []
    for idx, (line_no, _num) in enumerate(markers):
        start = line_no + 1
        end = markers[idx + 1][0] if idx + 1 < len(markers) else len(lines)

        content_lines = lines[start:end]
        while content_lines and not content_lines[0].strip():
            content_lines.pop(0)

        pages.append("\n".join(content_lines).strip())
    return pages


def fitz_per_page(pdf_path):
    """Fallback: per-page text extraction using PyMuPDF directly."""
    doc = fitz.open(pdf_path)
    pages = []
    for i in range(doc.page_count):
        page = doc[i]
        text_dict = page.get_text("dict")
        page_lines = []

        for block in text_dict.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                spans = [s.get("text", "") for s in line.get("spans", [])]
                text = " ".join(spans).strip()
                if text:
                    page_lines.append(text)

        pages.append("\n".join(page_lines).strip())
    doc.close()
    return pages


def short_name_from_pdf(pdf_path):
    """Derive short name from PDF filename (remove .pdf)."""
    return os.path.splitext(os.path.basename(pdf_path))[0]


def extract(pdf_path, short_name=None):
    """Extract a single PDF to markdown. Returns (md_content, page_count)."""
    if short_name is None:
        short_name = short_name_from_pdf(pdf_path)

    # Full pymupdf4llm extraction
    md = to_markdown(pdf_path)
    lines = md.split("\n")

    # Real page count
    doc = fitz.open(pdf_path)
    page_count = doc.page_count
    doc.close()

    title = extract_title(lines)

    # Try page markers
    markers = find_page_markers(lines, page_count)

    if markers:
        pages = split_by_markers(lines, markers)
    else:
        print(f"  [warn] No page markers found, using PyMuPDF per-page fallback", file=sys.stderr)
        pages = fitz_per_page(pdf_path)

    # Build output
    parts = [
        f"# {title}",
        "",
        f"Source: {os.path.basename(pdf_path)}",
        "",
        "",
        "---",
    ]

    for i, content in enumerate(pages, 1):
        parts.append("")
        parts.append(f"### Page {i}")
        parts.append("")
        parts.append(content)

    return "\n".join(parts), len(pages)


def main():
    parser = argparse.ArgumentParser(description="PDF → Markdown extractor for papers_downloaded/")
    parser.add_argument("pdf", nargs="?", default=None, help="Path to a single PDF (omit to process all)")
    parser.add_argument("-o", "--short-name", default=None, help="Custom short name for output .md file")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    if args.pdf:
        # Single PDF mode
        pdf_path = os.path.abspath(args.pdf)
        if not os.path.isfile(pdf_path):
            print(f"Error: {pdf_path} not found", file=sys.stderr)
            sys.exit(1)

        target_dir = os.path.dirname(pdf_path)
        short = args.short_name or short_name_from_pdf(pdf_path)
        out_path = os.path.join(target_dir, f"{short}.md")

        print(f"Extracting: {pdf_path} → {short}.md", file=sys.stderr)
        content, pages = extract(pdf_path, short_name=short)

        # Check for existing
        if os.path.exists(out_path):
            existing_size = os.path.getsize(out_path)
            print(f"  {out_path} exists ({existing_size} bytes). Overwriting...", file=sys.stderr)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  Done: {len(content)} chars, {pages} pages", file=sys.stderr)

    else:
        # Bulk mode: process all subdirectories with .pdf but no .md
        for entry in sorted(os.listdir(base_dir)):
            dir_path = os.path.join(base_dir, entry)
            if not os.path.isdir(dir_path):
                continue
            if entry == "archived":
                continue

            # Find PDFs in this directory
            pdf_files = [f for f in os.listdir(dir_path) if f.lower().endswith(".pdf")]
            if not pdf_files:
                continue

            # Check if markdown already exists (any .md file, single or per-page)
            md_files = [f for f in os.listdir(dir_path) if f.endswith(".md")]
            if md_files:
                print(f"SKIP {entry}/ - already has {len(md_files)} .md file(s)", file=sys.stderr)
                continue

            for pdf_file in pdf_files:
                pdf_path = os.path.join(dir_path, pdf_file)
                short = short_name_from_pdf(pdf_path)
                out_path = os.path.join(dir_path, f"{short}.md")

                print(f"Extracting: {entry}/{pdf_file} → {short}.md", file=sys.stderr)
                content, pages = extract(pdf_path, short_name=short)

                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"  Done: {len(content)} chars, {pages} pages", file=sys.stderr)


if __name__ == "__main__":
    main()
