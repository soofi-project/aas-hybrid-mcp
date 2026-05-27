"""PDF download, conversion to markdown, chunking, and embedding."""

import logging
import os
import re
import tempfile
from dataclasses import dataclass
from typing import Sequence

import requests
from docling.datamodel.base_models import ConversionStatus, InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import DocItemLabel, DoclingDocument, ListItem, NodeItem, TableItem
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DOWNLOAD_TIMEOUT,
    EMBEDDING_BATCH_SIZE,
    get_embedding_model,
)

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Chunk data type
# ---------------------------------------------------------------------------


@dataclass
class ChunkData:
    """A single text chunk with source metadata."""
    text: str
    heading: str
    page: int


# ---------------------------------------------------------------------------
# Embedding model (lazy singleton)
# ---------------------------------------------------------------------------

_embedding_model = None
_converter = None


def _get_embedding_model():
    """Lazy-init the embedding model on first use."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = get_embedding_model()
    return _embedding_model


def reset_converter() -> None:
    """Release the DocumentConverter singleton and run a GC cycle."""
    global _converter
    import gc
    _converter = None
    gc.collect()


def _get_converter() -> "DocumentConverter":
    """Lazy-init the DocumentConverter on first use (loads layout models once)."""
    global _converter
    if _converter is None:
        pipeline_options = PdfPipelineOptions(artifacts_path=os.environ.get("DOCLING_ARTIFACTS_PATH"))
        pipeline_options.do_table_structure = os.environ.get("PDF_TABLE_STRUCTURE", "false").lower() == "true"
        pipeline_options.do_ocr = False
        pipeline_options.queue_max_size = int(os.environ.get("DOCLING_QUEUE_MAX_SIZE", "8"))
        _converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
    return _converter


# ---------------------------------------------------------------------------
# PDF download
# ---------------------------------------------------------------------------


def download_pdf(url: str) -> bytes:
    """Download a PDF from *url* and return its content bytes."""
    log.info("Downloading PDF from %s", url)
    resp = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
    resp.raise_for_status()
    return resp.content


# ---------------------------------------------------------------------------
# Custom markdown export with page markers
# ---------------------------------------------------------------------------

_PAGE_BREAK_PATTERN = re.compile(r"<!--page:(\d+)-->", re.MULTILINE)


def _render_item_markdown(item: NodeItem) -> str:
    """Render a single document item to a markdown fragment."""
    if isinstance(item, list):
        return ""

    # --- Headings ---
    if hasattr(item, "text") and hasattr(item, "label"):
        text = item.text

        if item.label == DocItemLabel.TITLE:
            return f"# {text}\n"

        elif item.label == DocItemLabel.SECTION_HEADER:
            return f"## {text}\n"

        elif item.label in (
            DocItemLabel.PARAGRAPH,
            DocItemLabel.TEXT,
            DocItemLabel.CAPTION,
            DocItemLabel.FOOTNOTE,
            DocItemLabel.REFERENCE,
            DocItemLabel.MARKER,
            DocItemLabel.HANDWRITTEN_TEXT,
        ):
            return f"{text}\n\n"

        elif hasattr(item, "text"):
            # Page headers/footers and other text-like items
            if item.label in (DocItemLabel.PAGE_HEADER, DocItemLabel.PAGE_FOOTER):
                return f"_[{text}]_\n\n"
            return f"{text}\n\n"

        elif isinstance(item, ListItem):
            bullet = item.marker if hasattr(item, "marker") and item.marker else "-"
            return f"{bullet} {text}\n"

    # --- Tables ---
    if isinstance(item, TableItem) and item.data and item.data.table_cells:
        return _table_to_markdown(item.data) + "\n"

    return ""


def _table_to_markdown(table_data) -> str:
    """Render a docling table to markdown.

    `TableData.table_cells` is a flat list of cells carrying row/column offset
    spans, not row arrays. Reconstruct the num_rows x num_cols grid by placing
    each cell's text at every (row, col) position it covers — handles row and
    column spans by duplicating text across covered cells.
    """
    cells = table_data.table_cells
    num_rows = table_data.num_rows
    num_cols = table_data.num_cols
    if not cells or num_rows == 0 or num_cols == 0:
        return ""

    grid: list[list[str]] = [["" for _ in range(num_cols)] for _ in range(num_rows)]
    header_rows: set[int] = set()
    for cell in cells:
        text = (cell.text or "").replace("|", r"\|").replace("\n", " ").strip()
        for r in range(cell.start_row_offset_idx, cell.end_row_offset_idx):
            for c in range(cell.start_col_offset_idx, cell.end_col_offset_idx):
                if 0 <= r < num_rows and 0 <= c < num_cols:
                    grid[r][c] = text
        if getattr(cell, "column_header", False):
            for r in range(cell.start_row_offset_idx, cell.end_row_offset_idx):
                header_rows.add(r)

    header_idx = min(header_rows) if header_rows else 0
    lines = [
        "| " + " | ".join(grid[header_idx]) + " |",
        "|" + "|".join(["---"] * num_cols) + "|",
    ]
    for i, row in enumerate(grid):
        if i == header_idx:
            continue
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _items_to_markdown_with_page_markers(doc: DoclingDocument) -> str:
    """Linear walk of document items, injecting page markers at page boundaries."""
    parts: list[str] = []

    for item, _level in doc.iterate_items():
        # Emit a page marker before every prov-bearing item, on its own line.
        # An own-line marker keeps heading lines clean (`## NOTICE` instead of
        # `<!--page:97-->## NOTICE`), which both `MarkdownHeaderTextSplitter`
        # and our own `_extract_heading_for_chunk` need — they detect headings
        # via `line.strip().startswith("#")`. Group items (e.g. list
        # containers) lack `prov`, so guard with getattr.
        prov = getattr(item, "prov", None)
        if prov:
            page = prov[0].page_no
            parts.append(f"<!--page:{page}-->\n")

        md = _render_item_markdown(item)
        if md:
            parts.append(md)

    return "".join(parts)


def convert_pdf_to_markdown(pdf_bytes: bytes) -> str:
    """Convert PDF bytes to markdown using docling.

    Produces markdown with embedded page markers for page tracking:
    ``<!--page:1>``, ``<!--page:2>``, etc.

    Headings are rendered from the document structure (## for section headers,
    # for title), providing hierarchical context for MarkdownHeaderTextSplitter.
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        # artifacts_path points docling at models pre-fetched by `docling-tools models download`
        # (flat layout under ~/.cache/docling/models/), bypassing huggingface_hub snapshot_download
        # which expects a different on-disk format and would hit the network under HF_HUB_OFFLINE=1.
        result = _get_converter().convert(tmp_path)

        if result.status == ConversionStatus.SUCCESS:
            md = _items_to_markdown_with_page_markers(result.document)
        else:
            # Fallback: lose page markers but at least get text
            log.warning("Conversion had issues (%s), falling back to built-in export", result.status)
            md = result.document.export_to_markdown()

        return md
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------


def _clean_text(text: str) -> str:
    """Remove non-printable characters and collapse whitespace, keeping structure."""
    if not text:
        return ""
    cleaned = "".join(ch for ch in text if ch.isprintable() or ch in "\n\r\t")
    # Collapse excessive blank lines (more than 2 consecutive newlines → 2)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _extract_page(text: str) -> int:
    """Extract the first page number from a chunk's text."""
    match = _PAGE_BREAK_PATTERN.search(text)
    if match:
        return int(match.group(1))
    return 1


def _strip_page_markers(text: str) -> str:
    """Remove page marker comments from text, collapsing excess whitespace."""
    cleaned = _PAGE_BREAK_PATTERN.sub("", text)
    # Collapse any whitespace left behind by marker removal
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _extract_heading_for_chunk(text: str) -> str:
    """Extract the most recent heading from a chunk's text.

    Returns the text after the last heading line (e.g., '## 3.2 Overview').
    If no heading is found, returns an empty string.
    """
    lines = text.split("\n")
    heading = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            # Clean up the heading — strip '#' and leading whitespace
            heading = stripped.lstrip("#").strip()
    return heading


# ---------------------------------------------------------------------------
# Chunking with heading metadata
# ---------------------------------------------------------------------------


def chunk_text(markdown_text: str) -> list[ChunkData]:
    """Split markdown into chunks with heading and page metadata.

    Two-phase splitting:
    1. MarkdownHeaderTextSplitter splits on headings — each chunk gets heading metadata.
    2. Oversized chunks are further split with RecursiveCharacterTextSplitter,
       preserving the heading metadata.

    Returns a list of ChunkData(text, heading, page) objects.
    """
    cleaned = markdown_text.encode("utf-8", "ignore").decode("utf-8")

    # Phase 1: split on headings to capture section context
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "heading1"),
            ("##", "heading2"),
            ("###", "heading3"),
            ("####", "heading4"),
            ("#####", "heading5"),
            ("######", "heading6"),
        ],
        strip_headers=False,
        return_each_line=False,
    )

    from langchain_core.documents import Document

    header_chunks = header_splitter.split_text(cleaned)

    # Phase 2: split oversized chunks
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        keep_separator=True,
    )

    results: list[ChunkData] = []

    for chunk in header_chunks:
        raw_text = chunk.page_content
        raw_metadata = chunk.metadata

        # Build heading string from metadata
        heading_parts = []
        for key in ("heading1", "heading2", "heading3", "heading4", "heading5", "heading6"):
            if raw_metadata.get(key):
                heading_parts.append(raw_metadata[key])
        heading = " > ".join(heading_parts) if heading_parts else ""

        # Check if this chunk needs further splitting
        if len(raw_text) > CHUNK_SIZE:
            sub_chunks = recursive_splitter.split_documents([chunk])
            for sub in sub_chunks:
                text = _clean_text(sub.page_content)
                if not text:
                    continue
                page = _extract_page(sub.page_content)
                # Try to find a more specific heading in the sub-chunk
                sub_heading = _extract_heading_for_chunk(sub.page_content)
                final_heading = sub_heading or heading
                results.append(ChunkData(text=text, heading=final_heading, page=page))
        else:
            text = _clean_text(raw_text)
            if not text:
                continue
            page = _extract_page(raw_text)
            results.append(ChunkData(text=text, heading=heading, page=page))

    return results


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------


def compute_embeddings(texts: Sequence[str]) -> list[list[float]]:
    """Compute embeddings for a list of texts in batches."""
    model = _get_embedding_model()
    embeddings: list[list[float]] = []
    for i in range(0, len(texts), EMBEDDING_BATCH_SIZE):
        batch = texts[i : i + EMBEDDING_BATCH_SIZE]
        embeddings.extend(model.embed_documents(batch))
    return embeddings
