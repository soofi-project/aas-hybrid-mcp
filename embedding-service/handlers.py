"""AAS event handlers — process Kafka events for PDF ingestion into Weaviate."""

import base64
import logging
from collections import deque

import requests

from config import BASYX_SUBMODEL_REPO
from pdf import chunk_text, compute_embeddings, convert_pdf_to_markdown, download_pdf
from vectorstore import delete_documents, insert_chunks

log = logging.getLogger(__name__)


class PermanentProcessingError(Exception):
    """Raised when an event cannot be processed regardless of retries.

    Examples: corrupt PDF, 404 from BaSyx, no text extracted.
    """


# ---------------------------------------------------------------------------
# AAS idShort path builder
# ---------------------------------------------------------------------------


class AasPathBuilder:
    """Build AAS idShort paths by walking a stack of referable elements.

    Used to compute the full smElementPath for nested SubmodelElements,
    e.g. ``TechnicalData.Documents[0].OperatingManual``.
    """

    def __init__(self, base_id_short_path: str | None = None) -> None:
        self._stack: deque = deque()
        self._base = base_id_short_path

    def push(self, element: dict) -> None:
        self._stack.append(element)

    def pop(self) -> None:
        if self._stack:
            self._stack.pop()

    def get_path(self) -> str:
        """Return the current full idShort path."""
        parts: list[str] = []
        prev_is_list = False

        it = iter(self._stack)
        first = next(it, None)
        if first is None:
            return self._base or ""

        # First element in stack is the top-level SME — check if it's a list container
        prev_is_list = (
            isinstance(first.get("value"), list) if isinstance(first, dict) else False
        )

        for el in it:
            if prev_is_list:
                # Inside a SubmodelElementList — emit index
                parent_value = self._stack[len(parts)]  # approximate parent
                try:
                    idx = list(parent_value.get("value", [])).index(el)
                    parts.append(f"[{idx}]")
                except (ValueError, AttributeError):
                    pass
            else:
                id_short = el.get("idShort", "") if isinstance(el, dict) else ""
                if parts and not parts[-1].startswith("["):
                    parts.append(".")
                parts.append(id_short)

            prev_is_list = isinstance(el.get("value"), list) if isinstance(el, dict) else False

        stack_path = "".join(parts)
        if self._base:
            return f"{self._base}.{stack_path}" if stack_path else self._base
        return stack_path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_pdf(element: dict) -> bool:
    return (
        element.get("modelType") == "File"
        and "application/pdf" in str(element.get("contentType", "")).lower()
    )


def _resolve_pdf_url(url: str | None, submodel_id: str, id_short: str) -> str:
    """Resolve the download URL — fall back to BaSyx attachment endpoint."""
    if url and url.startswith("http"):
        return url
    sm_id_b64 = base64.urlsafe_b64encode(submodel_id.encode()).decode().rstrip("=")
    return f"{BASYX_SUBMODEL_REPO}/submodels/{sm_id_b64}/submodel-elements/{id_short}/attachment"


def _source_name(url: str) -> str:
    return url.split("/")[-1].split("?")[0]


def _ingest_pdf(
    url: str,
    id_short: str,
    submodel_id: str,
    sm_element_path: str | None = None,
) -> None:
    """Download a PDF, convert, chunk, embed, and store in Weaviate.

    Raises:
        PermanentProcessingError: PDF cannot be processed (corrupt, 404, no text).
            Will not succeed on retry.
        Exception: Transient errors (network timeout, service down) bubble up
            unchanged — caller decides whether to retry.
    """
    resolved_url = _resolve_pdf_url(url, submodel_id, id_short)
    source = _source_name(resolved_url)

    log.info(
        "Ingesting PDF idShort=%s submodel=%s from %s",
        id_short, submodel_id, resolved_url,
    )

    try:
        pdf_bytes = download_pdf(resolved_url)
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code in (404, 410):
            raise PermanentProcessingError(
                f"PDF not found at {resolved_url} (HTTP {exc.response.status_code})"
            ) from exc
        raise  # other HTTP errors (5xx, 429) are transient

    try:
        markdown = convert_pdf_to_markdown(pdf_bytes)
    except Exception as exc:
        raise PermanentProcessingError(
            f"Failed to convert PDF {source}: {exc}"
        ) from exc

    texts = chunk_text(markdown)

    if not texts or all(not t.strip() for t in texts):
        raise PermanentProcessingError(
            f"No text extracted from PDF {source}"
        )

    vectors = compute_embeddings(texts)

    insert_chunks(
        texts=texts,
        vectors=vectors,
        source=source,
        submodel_id=submodel_id,
        sm_element_path=sm_element_path,
        id_short=id_short,
    )


# ---------------------------------------------------------------------------
# Recursive element processing
# ---------------------------------------------------------------------------


def _process_element(path: AasPathBuilder, element: dict, submodel_id: str) -> None:
    """Recursively walk SubmodelElements and ingest any PDF files found."""
    path.push(element)
    try:
        if _is_pdf(element):
            sm_element_path = path.get_path()
            _ingest_pdf(
                url=element.get("value", ""),
                id_short=element.get("idShort", ""),
                submodel_id=submodel_id,
                sm_element_path=sm_element_path,
            )
        for child in element.get("submodelElements", []):
            _process_element(path, child, submodel_id)
    except Exception:
        log.exception(
            "Error processing element idShort=%s in submodel=%s",
            element.get("idShort"), submodel_id,
        )
    finally:
        path.pop()


# ---------------------------------------------------------------------------
# Event handlers (called from app.py)
# ---------------------------------------------------------------------------


def handle_create(event: dict) -> None:
    """Handle CREATED events — ingest PDFs from new submodels or elements."""
    submodel_id = event.get("id", "")

    if "submodel" in event:
        path = AasPathBuilder()
        for el in event["submodel"].get("submodelElements", []):
            _process_element(path, el, submodel_id)

    elif "smElement" in event:
        el = event["smElement"]
        if _is_pdf(el):
            id_short = el.get("idShort", "")
            path = AasPathBuilder(base_id_short_path=id_short)
            _ingest_pdf(
                url=el.get("value", ""),
                id_short=id_short,
                submodel_id=submodel_id,
                sm_element_path=path.get_path(),
            )


def handle_update(event: dict) -> None:
    """Handle UPDATED events — delete old chunks, then re-ingest."""
    submodel_id = event.get("id", "")

    if "smElement" in event:
        el = event["smElement"]
        if _is_pdf(el):
            id_short = el.get("idShort", "")
            sm_element_path = event.get("smElementPath")
            delete_documents(submodel_id, sm_element_path)
            path = AasPathBuilder(base_id_short_path=id_short)
            _ingest_pdf(
                url=el.get("value", ""),
                id_short=id_short,
                submodel_id=submodel_id,
                sm_element_path=path.get_path(),
            )
    elif "submodel" in event:
        delete_documents(submodel_id)
        handle_create(event)


def handle_delete(event: dict) -> None:
    """Handle DELETED events — remove chunks from Weaviate."""
    submodel_id = event.get("id", "")
    sm_element_path = event.get("smElementPath")
    delete_documents(submodel_id, sm_element_path)
