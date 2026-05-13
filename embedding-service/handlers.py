"""AAS event handlers — process Kafka events for PDF ingestion into Weaviate."""

import base64
import hashlib
import logging
from collections import deque
from urllib.parse import quote

import requests

from config import BASYX_PUBLIC_URL, BASYX_SUBMODEL_REPO
from pdf import ChunkData, _strip_page_markers, chunk_text, compute_embeddings, convert_pdf_to_markdown, download_pdf
from vectorstore import delete_documents, has_chunks, insert_chunks

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
        """Return the full idShortPath for the current element stack.

        SubmodelElementCollection children are addressed by idShort (dots).
        SubmodelElementList children are addressed by 0-based index ([n]).
        All other containers (Submodel root, Entity) use idShort.
        """
        stack = list(self._stack)
        if not stack:
            return self._base or ""

        parts: list[str] = []
        for i, el in enumerate(stack):
            if not isinstance(el, dict):
                continue
            parent = stack[i - 1] if i > 0 else None
            if parent and parent.get("modelType") == "SubmodelElementList":
                # Parent is a list — children have no idShort, use index instead.
                siblings = parent.get("value", [])
                try:
                    idx = siblings.index(el)
                    parts.append(f"[{idx}]")
                except ValueError:
                    parts.append("[?]")
            else:
                id_short = el.get("idShort", "")
                if parts and not parts[-1].startswith("["):
                    parts.append(".")
                parts.append(id_short)

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


def _download_url(url: str | None, submodel_id: str, sm_element_path: str) -> str:
    """Resolve the internal download URL — for fetching the PDF bytes."""
    if url and url.startswith("http"):
        return url
    sm_id_b64 = base64.urlsafe_b64encode(submodel_id.encode()).decode().rstrip("=")
    return f"{BASYX_SUBMODEL_REPO}/submodels/{sm_id_b64}/submodel-elements/{quote(sm_element_path, safe='')}/attachment"


def _public_url(url: str | None, submodel_id: str, sm_element_path: str) -> tuple[str, str]:
    """Return (user_visible_url, filename) for Weaviate metadata.

    For external PDFs: URL is used as-is, filename is the last path segment.
    For BaSyx attachments: URL is built from BASYX_PUBLIC_URL, filename is "attachment".
    Path segments are URL-encoded so that BaSyx idShortPath syntax (e.g.
    ``Documents[0]DigitalFiles[0]``) survives copy/paste into a browser —
    bare ``[``/``]`` are reserved in RFC 3986 and break unencoded links.
    """
    if url and url.startswith("http"):
        filename = url.split("/")[-1].split("?")[0] or "document.pdf"
        return url, filename
    sm_id_b64 = base64.urlsafe_b64encode(submodel_id.encode()).decode().rstrip("=")
    pu = f"{BASYX_PUBLIC_URL}/submodels/{sm_id_b64}/submodel-elements/{quote(sm_element_path, safe='')}/attachment"
    return pu, "attachment"


def _ingest_pdf(
    url: str,
    id_short: str,
    submodel_id: str,
    sm_element_path: str,
) -> None:
    """Download a PDF, convert, chunk, embed, and store in Weaviate.

    `id_short` is the leaf idShort of the element and is stored as Weaviate
    metadata; `sm_element_path` is the full dotted/bracketed BaSyx idShortPath
    and is what's used to build the attachment URLs.

    Idempotent: if chunks with the same content hash already exist for
    (submodel_id, sm_element_path), the ingest is skipped after the
    download + hash step, avoiding the expensive PDF conversion and
    embedding work. Stale chunks from a previous version of the element
    are removed before the fresh ingest.

    Raises:
        PermanentProcessingError: PDF cannot be processed (corrupt, 404, no text).
            Will not succeed on retry.
        Exception: Transient errors (network timeout, service down) bubble up
            unchanged — caller decides whether to retry.
    """
    resolved_dl_url = _download_url(url, submodel_id, sm_element_path)
    public_url, source_filename = _public_url(url, submodel_id, sm_element_path)

    log.info(
        "Ingesting PDF idShort=%s submodel=%s from %s",
        id_short, submodel_id, resolved_dl_url,
    )

    try:
        pdf_bytes = download_pdf(resolved_dl_url)
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code in (404, 410):
            raise PermanentProcessingError(
                f"PDF not found at {resolved_dl_url} (HTTP {exc.response.status_code})"
            ) from exc
        raise  # other HTTP errors (5xx, 429) are transient

    content_hash = hashlib.sha256(pdf_bytes).hexdigest()

    if has_chunks(submodel_id, sm_element_path, content_hash):
        log.info(
            "Skipping ingest for idShort=%s submodel=%s — content unchanged (hash=%s)",
            id_short, submodel_id, content_hash[:12],
        )
        return

    # Content is new or changed — remove any stale chunks from the previous
    # version of this element before writing the fresh ones.
    delete_documents(submodel_id, sm_element_path)

    try:
        markdown = convert_pdf_to_markdown(pdf_bytes)
    except Exception as exc:
        raise PermanentProcessingError(
            f"Failed to convert PDF {source_filename}: {exc}"
        ) from exc

    chunk_data_list = chunk_text(markdown)

    if not chunk_data_list or all(not cd.text.strip() for cd in chunk_data_list):
        raise PermanentProcessingError(
            f"No text extracted from PDF {source_filename}"
        )

    # Strip page markers from text before embedding (they're metadata, not content)
    chunks_for_embed = [
        {"text": _strip_page_markers(cd.text), "heading": cd.heading, "page": cd.page}
        for cd in chunk_data_list
    ]
    vectors = compute_embeddings([cd["text"] for cd in chunks_for_embed])

    insert_chunks(
        chunks=chunks_for_embed,
        vectors=vectors,
        source="document",
        source_url=public_url,
        source_filename=source_filename,
        submodel_id=submodel_id,
        sm_element_path=sm_element_path,
        id_short=id_short,
        content_hash=content_hash,
    )


# ---------------------------------------------------------------------------
# Recursive element processing
# ---------------------------------------------------------------------------


def _process_element(path: AasPathBuilder, element: dict, submodel_id: str) -> None:
    """Recursively walk SubmodelElements and ingest any PDF files found.

    Children of SubmodelElementCollection and SubmodelElementList live under
    the "value" key (a list), not "submodelElements" — both are checked.
    Entity statements use "statements".
    """
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
        # Walk all child slots: submodel root, SMC/SML contents, Entity statements.
        for key in ("submodelElements", "value", "statements"):
            children = element.get(key)
            if isinstance(children, list):
                for child in children:
                    if isinstance(child, dict) and "modelType" in child:
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
    """Handle UPDATED events.

    Per-element updates delegate to ``_ingest_pdf``, which is itself
    idempotent on the content hash and replaces stale chunks only when
    the bytes actually differ. Whole-submodel updates still bulk-delete
    first, because a removed PDF element would otherwise leave orphaned
    chunks that no subsequent ``_ingest_pdf`` call would touch.
    """
    submodel_id = event.get("id", "")

    if "smElement" in event:
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
    elif "submodel" in event:
        delete_documents(submodel_id)
        handle_create(event)


def handle_delete(event: dict) -> None:
    """Handle DELETED events — remove chunks from Weaviate."""
    submodel_id = event.get("id", "")
    sm_element_path = event.get("smElementPath")
    delete_documents(submodel_id, sm_element_path)
