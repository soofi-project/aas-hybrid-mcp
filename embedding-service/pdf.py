"""PDF download, conversion to markdown, chunking, and embedding."""

import logging
import os
import tempfile
from typing import Sequence

import requests
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DOWNLOAD_TIMEOUT,
    EMBEDDING_BATCH_SIZE,
    get_embedding_model,
)

log = logging.getLogger(__name__)

_embedding_model = None


def _get_embedding_model():
    """Lazy-init the embedding model on first use."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = get_embedding_model()
    return _embedding_model


def download_pdf(url: str) -> bytes:
    """Download a PDF from *url* and return its content bytes."""
    log.info("Downloading PDF from %s", url)
    resp = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
    resp.raise_for_status()
    return resp.content


def _clean_text(text: str) -> str:
    """Remove non-printable characters (except whitespace)."""
    if not text:
        return ""
    return "".join(ch for ch in text if ch.isprintable() or ch in "\n\r\t")


def convert_pdf_to_markdown(pdf_bytes: bytes) -> str:
    """Convert PDF bytes to markdown using docling."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_table_structure = True
        pipeline_options.do_ocr = False
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        result = converter.convert(tmp_path)
        return result.document.export_to_markdown()
    finally:
        os.unlink(tmp_path)


def chunk_text(markdown_text: str) -> list[str]:
    """Split markdown text into cleaned chunks."""
    cleaned = markdown_text.encode("utf-8", "ignore").decode("utf-8")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    parts = splitter.split_documents([Document(page_content=cleaned)])
    return [_clean_text(p.page_content) for p in parts]


def compute_embeddings(texts: Sequence[str]) -> list[list[float]]:
    """Compute embeddings for a list of texts in batches."""
    model = _get_embedding_model()
    embeddings: list[list[float]] = []
    for i in range(0, len(texts), EMBEDDING_BATCH_SIZE):
        batch = texts[i : i + EMBEDDING_BATCH_SIZE]
        embeddings.extend(model.embed_documents(batch))
    return embeddings
