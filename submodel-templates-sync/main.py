"""Submodel Templates Sync — clone IDTA templates, extract metadata, ingest PDFs.

Init container that runs once on stack start:
1. Git clone submodel-templates repo
2. Discover latest version per template
3. Extract JSON metadata (index + per-template element structure)
4. Convert spec PDFs to markdown, chunk, embed, insert into Weaviate
"""

import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import pymupdf4llm
import weaviate
import weaviate.classes.config as wvc
import weaviate.classes.data as wcd
import weaviate.classes.query as wvq
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_URL = "https://github.com/admin-shell-io/submodel-templates.git"
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "weaviate")
WEAVIATE_HTTP_PORT = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
TEMPLATES_OUTPUT_DIR = Path(os.getenv("TEMPLATES_OUTPUT_DIR", "/data/templates"))
IDTA_COLLECTION = "IdtaTemplateSpec"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
EMBEDDING_BATCH_SIZE = 100

WEAVIATE_RETRY_INTERVAL = 5
WEAVIATE_TIMEOUT = 120


# ---------------------------------------------------------------------------
# Embedding model (mirrors embedding-service/config.py)
# ---------------------------------------------------------------------------

_embedding_model = None


def _get_embedding_model():
    global _embedding_model
    if _embedding_model is not None:
        return _embedding_model

    embedding_config = os.getenv("EMBEDDING_MODEL")
    if not embedding_config:
        raise ValueError("EMBEDDING_MODEL not set (expected format: provider:model)")

    if ":" not in embedding_config:
        raise ValueError(
            f"EMBEDDING_MODEL must be in provider:model format, got: {embedding_config}"
        )

    provider, model = embedding_config.split(":", 1)

    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings

        ollama_host = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
        log.info("Using embedding model ollama:%s at %s", model, ollama_host)
        _embedding_model = OllamaEmbeddings(model=model, base_url=ollama_host)
        return _embedding_model

    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_openai import OpenAIEmbeddings
    from langchain_voyageai import VoyageAIEmbeddings

    providers = {
        "openai": ("OPENAI_API_KEY", lambda key: OpenAIEmbeddings(model=model, api_key=key)),
        "google_genai": ("GOOGLE_API_KEY", lambda key: GoogleGenerativeAIEmbeddings(model=model, google_api_key=key)),
        "voyageai": ("VOYAGE_API_KEY", lambda key: VoyageAIEmbeddings(model=model, api_key=key)),
    }

    if provider not in providers:
        supported = ", ".join(["ollama", *providers.keys()])
        raise ValueError(f"Unknown embedding provider: {provider} (supported: {supported})")

    env_var, factory = providers[provider]
    api_key = os.getenv(env_var)
    if not api_key:
        raise ValueError(f"API key {env_var} not set for provider {provider}")

    log.info("Using embedding model %s:%s", provider, model)
    _embedding_model = factory(api_key)
    return _embedding_model


# ---------------------------------------------------------------------------
# Git clone
# ---------------------------------------------------------------------------


def clone_repo(target: Path) -> Path:
    """Shallow-clone the submodel-templates repo into target."""
    log.info("Cloning %s", REPO_URL)
    subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, str(target)],
        check=True,
        capture_output=True,
        text=True,
    )
    log.info("Cloned into %s", target)
    return target


def get_repo_hash(repo_dir: Path) -> str:
    """Return the HEAD commit SHA of the cloned repo."""
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# Template discovery
# ---------------------------------------------------------------------------

def _collect_version_leaves(template_dir: Path) -> list[tuple[tuple[int, ...], Path]]:
    """Walk numeric directory tree (Major/Minor/[Patch/]) and return (version_tuple, path) for each leaf.

    Repo structure: published/<Name>/<Major>/<Minor>/[<Patch>/]
    Files (JSON, PDF) live at the deepest numeric level.
    """
    results = []
    for major_dir in sorted(template_dir.iterdir()):
        if not major_dir.is_dir() or not major_dir.name.isdigit():
            continue
        major = int(major_dir.name)
        for minor_dir in sorted(major_dir.iterdir()):
            if not minor_dir.is_dir() or not minor_dir.name.isdigit():
                continue
            minor = int(minor_dir.name)
            # Check for patch-level subdirs
            patch_dirs = [
                d for d in minor_dir.iterdir()
                if d.is_dir() and d.name.isdigit()
            ]
            if patch_dirs:
                for patch_dir in sorted(patch_dirs):
                    patch = int(patch_dir.name)
                    results.append(((major, minor, patch), patch_dir))
            else:
                # No patch level — files are at minor level
                results.append(((major, minor, 0), minor_dir))
    return results


def discover_templates(published_dir: Path) -> list[dict]:
    """Find latest version per template. Returns list of template info dicts."""
    if not published_dir.is_dir():
        log.warning("Published directory not found: %s", published_dir)
        return []

    results = []
    for entry in sorted(published_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue

        name = entry.name
        versions = _collect_version_leaves(entry)
        if not versions:
            log.debug("No version directories found in %s", entry)
            continue

        versions.sort(key=lambda x: x[0], reverse=True)
        latest_version, latest_dir = versions[0]
        version_str = ".".join(str(v) for v in latest_version)
        results.append({
            "name": name,
            "version": version_str,
            "path": latest_dir,
        })

    log.info("Discovered %d templates", len(results))
    return results


# ---------------------------------------------------------------------------
# JSON extraction
# ---------------------------------------------------------------------------


def _find_json(template_dir: Path) -> Path | None:
    """Find the best AAS JSON in a template version directory.

    Prefers V3.1 metamodel JSON if available.
    """
    jsons = list(template_dir.glob("*.json"))
    if not jsons:
        # Check subdirectories
        jsons = list(template_dir.rglob("*.json"))
    if not jsons:
        return None

    # Prefer V3.1 metamodel
    for j in jsons:
        if "forAASMetamodelV3.1" in j.name or "MetamodelV3.1" in j.name:
            return j
    # Then V3.0
    for j in jsons:
        if "forAASMetamodelV3.0" in j.name or "MetamodelV3.0" in j.name:
            return j
    # Then any AAS metamodel JSON
    for j in jsons:
        if "MetamodelV" in j.name or "Metamodel_V" in j.name:
            return j
    # Fallback to first JSON
    return jsons[0]


def extract_metadata(json_path: Path) -> dict | None:
    """Extract template metadata from an AAS package JSON."""
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        log.warning("Failed to parse %s: %s", json_path, e)
        return None

    # AAS package structure: look for submodels array
    submodels = data.get("submodels", [])
    if not submodels:
        # Try AASX package structure
        submodels = data.get("assetAdministrationShells", [])
        if not submodels:
            log.warning("No submodels found in %s", json_path)
            return None

    sm = submodels[0]
    semantic_id = ""
    sid = sm.get("semanticId", {})
    keys = sid.get("keys", [])
    if keys:
        semantic_id = keys[0].get("value", "")

    description = ""
    desc_list = sm.get("description", [])
    if isinstance(desc_list, list):
        for d in desc_list:
            if isinstance(d, dict) and d.get("language", "").startswith("en"):
                description = d.get("text", "")
                break
        if not description and desc_list:
            first = desc_list[0]
            if isinstance(first, dict):
                description = first.get("text", "")

    return {
        "idShort": sm.get("idShort", ""),
        "semanticId": semantic_id,
        "description": description,
    }


def extract_element_structure(submodel: dict, max_depth: int = 10) -> list[dict]:
    """Recursively extract element structure from a submodel."""

    def _walk(elements: list, depth: int) -> list[dict]:
        if depth > max_depth:
            return []
        result = []
        for el in elements:
            entry = {
                "modelType": el.get("modelType", ""),
                "idShort": el.get("idShort", ""),
            }
            # Extract semanticId
            sid = el.get("semanticId", {})
            keys = sid.get("keys", [])
            if keys:
                entry["semanticId"] = keys[0].get("value", "")

            # Recurse into children
            children_keys = ["submodelElements", "value", "statements"]
            for key in children_keys:
                children = el.get(key)
                if isinstance(children, list) and children:
                    entry["children"] = _walk(children, depth + 1)
                    break

            result.append(entry)
        return result

    elements = submodel.get("submodelElements", [])
    return _walk(elements, 0)


def process_json_templates(templates: list[dict]) -> list[dict]:
    """Extract metadata and element structure, write JSON files."""
    TEMPLATES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    index_entries = []
    for tpl in templates:
        name = tpl["name"]
        version = tpl["version"]
        template_dir = tpl["path"]

        json_path = _find_json(template_dir)
        if json_path is None:
            log.warning("No JSON found for template %s", name)
            index_entries.append({
                "name": name,
                "version": version,
                "idShort": "",
                "semanticId": "",
                "description": "",
            })
            continue

        metadata = extract_metadata(json_path)
        if metadata is None:
            log.warning("Failed to extract metadata for %s", name)
            index_entries.append({
                "name": name,
                "version": version,
                "idShort": "",
                "semanticId": "",
                "description": "",
            })
            continue

        # Build index entry
        entry = {
            "name": name,
            "version": version,
            **metadata,
        }
        index_entries.append(entry)

        # Extract element structure from the full JSON
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        submodels = data.get("submodels", [])
        if submodels:
            structure = extract_element_structure(submodels[0])
            template_data = {**entry, "elements": structure}
        else:
            template_data = {**entry, "elements": []}

        # Write per-template JSON
        safe_name = re.sub(r'[<>:"/\\|?*]', "_", name)
        out_path = TEMPLATES_OUTPUT_DIR / f"{safe_name}.json"
        out_path.write_text(json.dumps(template_data, indent=2, ensure_ascii=False), encoding="utf-8")
        log.info("Wrote %s", out_path)

    # Write index
    index_path = TEMPLATES_OUTPUT_DIR / "index.json"
    index_path.write_text(json.dumps(index_entries, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("Wrote index.json with %d templates", len(index_entries))

    return index_entries


# ---------------------------------------------------------------------------
# PDF processing and Weaviate ingestion
# ---------------------------------------------------------------------------


def _find_pdfs(template_dir: Path) -> list[Path]:
    """Find PDF files in a template version directory.

    If the directory (e.g. patch-level 1/0/1/) has no PDFs, fall back to
    the parent directory (minor-level 1/0/) where spec PDFs often live.
    """
    pdfs = list(template_dir.rglob("*.pdf")) + list(template_dir.rglob("*.PDF"))
    if not pdfs and template_dir.parent.is_dir():
        pdfs = [
            p for p in template_dir.parent.glob("*.pdf")
        ] + [
            p for p in template_dir.parent.glob("*.PDF")
        ]
    return pdfs


def _convert_pdf(pdf_path: Path) -> str:
    """Convert a PDF to markdown using pymupdf4llm."""
    return pymupdf4llm.to_markdown(str(pdf_path))


def _clean_text(text: str) -> str:
    """Remove non-printable characters (except whitespace)."""
    if not text:
        return ""
    return "".join(ch for ch in text if ch.isprintable() or ch in "\n\r\t")


def _chunk_text(markdown: str) -> list[str]:
    """Split markdown into cleaned chunks."""
    cleaned = markdown.encode("utf-8", "ignore").decode("utf-8")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    parts = splitter.split_documents([Document(page_content=cleaned)])
    return [_clean_text(p.page_content) for p in parts if _clean_text(p.page_content).strip()]


def _compute_embeddings(texts: list[str]) -> list[list[float]]:
    """Compute embeddings in batches."""
    model = _get_embedding_model()
    embeddings: list[list[float]] = []
    for i in range(0, len(texts), EMBEDDING_BATCH_SIZE):
        batch = texts[i : i + EMBEDDING_BATCH_SIZE]
        embeddings.extend(model.embed_documents(batch))
    return embeddings


def wait_for_weaviate() -> weaviate.WeaviateClient:
    """Wait for Weaviate to become ready, then return a connected client."""
    deadline = time.time() + WEAVIATE_TIMEOUT
    while True:
        try:
            client = weaviate.connect_to_custom(
                http_host=WEAVIATE_HOST,
                http_port=WEAVIATE_HTTP_PORT,
                http_secure=False,
                grpc_host=WEAVIATE_HOST,
                grpc_port=WEAVIATE_GRPC_PORT,
                grpc_secure=False,
                skip_init_checks=True,
            )
            if client.is_ready():
                log.info("Weaviate is ready")
                return client
            client.close()
        except Exception as e:
            if time.time() > deadline:
                raise TimeoutError(
                    f"Weaviate not ready after {WEAVIATE_TIMEOUT}s"
                ) from e
            log.info("Waiting for Weaviate (%s)...", e)
        time.sleep(WEAVIATE_RETRY_INTERVAL)


SYNC_HASH_COLLECTION = "SyncMetadata"


def is_up_to_date(client: weaviate.WeaviateClient, repo_hash: str) -> bool:
    """Check if the IdtaTemplateSpec collection was already built from this repo hash."""
    if not client.collections.exists(SYNC_HASH_COLLECTION):
        return False
    if not client.collections.exists(IDTA_COLLECTION):
        return False

    collection = client.collections.get(SYNC_HASH_COLLECTION)
    result = collection.query.fetch_objects(
        filters=wvq.Filter.by_property("key").equal("idta_templates"),
        limit=1,
    )
    if not result.objects:
        return False

    stored_hash = result.objects[0].properties.get("hash", "")
    return stored_hash == repo_hash


def store_sync_hash(client: weaviate.WeaviateClient, repo_hash: str) -> None:
    """Store the repo hash after successful sync."""
    if not client.collections.exists(SYNC_HASH_COLLECTION):
        client.collections.create(
            name=SYNC_HASH_COLLECTION,
            properties=[
                wvc.Property(name="key", data_type=wvc.DataType.TEXT),
                wvc.Property(name="hash", data_type=wvc.DataType.TEXT),
            ],
        )

    collection = client.collections.get(SYNC_HASH_COLLECTION)

    # Delete old entry if exists
    old = collection.query.fetch_objects(
        filters=wvq.Filter.by_property("key").equal("idta_templates"),
        limit=1,
    )
    for obj in old.objects:
        collection.data.delete_by_id(obj.uuid)

    collection.data.insert({"key": "idta_templates", "hash": repo_hash})
    log.info("Stored sync hash %s", repo_hash)


def setup_collection(client: weaviate.WeaviateClient) -> None:
    """Drop and recreate the IdtaTemplateSpec collection."""
    if client.collections.exists(IDTA_COLLECTION):
        log.info("Deleting existing collection %s", IDTA_COLLECTION)
        client.collections.delete(IDTA_COLLECTION)

    log.info("Creating collection %s", IDTA_COLLECTION)
    client.collections.create(
        name=IDTA_COLLECTION,
        vector_config=wvc.Configure.Vectors.self_provided(),
        properties=[
            wvc.Property(name="text", data_type=wvc.DataType.TEXT),
            wvc.Property(name="templateName", data_type=wvc.DataType.TEXT),
            wvc.Property(name="pdfSource", data_type=wvc.DataType.TEXT),
            wvc.Property(name="version", data_type=wvc.DataType.TEXT),
            wvc.Property(name="semanticId", data_type=wvc.DataType.TEXT),
        ],
    )


def ingest_pdfs(
    client: weaviate.WeaviateClient,
    templates: list[dict],
    index_entries: list[dict],
) -> None:
    """Convert template PDFs to chunks and insert into Weaviate."""
    collection = client.collections.get(IDTA_COLLECTION)

    # Build lookup for semantic IDs
    semantic_ids = {e["name"]: e.get("semanticId", "") for e in index_entries}

    total_chunks = 0
    total_pdfs = 0

    for tpl in templates:
        name = tpl["name"]
        version = tpl["version"]
        template_dir = tpl["path"]
        semantic_id = semantic_ids.get(name, "")

        pdfs = _find_pdfs(template_dir)
        if not pdfs:
            log.info("No PDFs found for %s", name)
            continue

        for pdf_path in pdfs:
            try:
                markdown = _convert_pdf(pdf_path)
            except Exception as e:
                log.warning("Failed to convert %s: %s", pdf_path, e)
                continue

            chunks = _chunk_text(markdown)
            if not chunks:
                log.warning("No text extracted from %s", pdf_path)
                continue

            try:
                vectors = _compute_embeddings(chunks)
            except Exception as e:
                log.error("Failed to embed chunks from %s: %s", pdf_path, e)
                continue

            data_objects = [
                wcd.DataObject(
                    properties={
                        "text": text,
                        "templateName": name,
                        "pdfSource": pdf_path.name,
                        "version": version,
                        "semanticId": semantic_id,
                    },
                    vector=vec,
                )
                for text, vec in zip(chunks, vectors)
            ]
            collection.data.insert_many(data_objects)

            total_chunks += len(chunks)
            total_pdfs += 1
            log.info(
                "Ingested %d chunks from %s (%s)",
                len(chunks), pdf_path.name, name,
            )

    log.info("PDF ingestion complete: %d PDFs, %d total chunks", total_pdfs, total_chunks)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    log.info("Starting submodel-templates-sync")

    # 1. Clone repo
    clone_dir = Path(tempfile.mkdtemp(prefix="submodel-templates-"))
    try:
        clone_repo(clone_dir)
        repo_hash = get_repo_hash(clone_dir)
        log.info("Repo HEAD: %s", repo_hash)

        # 2. Idempotency check — skip if already synced from same commit
        client = wait_for_weaviate()
        try:
            if is_up_to_date(client, repo_hash):
                log.info(
                    "Collection %s already up-to-date (hash %s), skipping",
                    IDTA_COLLECTION, repo_hash,
                )
                return

            # The published templates are in published/
            published_dir = clone_dir / "published"
            if not published_dir.is_dir():
                # Try alternative locations
                for candidate in ["Published", "submodel-templates", "."]:
                    alt = clone_dir / candidate
                    if alt.is_dir() and any(alt.iterdir()):
                        published_dir = alt
                        break

            # 3. Discover templates
            templates = discover_templates(published_dir)
            if not templates:
                log.error("No templates discovered in %s", published_dir)
                return

            # 4. Extract JSON metadata and element structures
            index_entries = process_json_templates(templates)

            # 5. Ingest PDFs into Weaviate
            setup_collection(client)
            ingest_pdfs(client, templates, index_entries)

            # 6. Store sync hash on success
            store_sync_hash(client, repo_hash)

        finally:
            client.close()

    finally:
        shutil.rmtree(clone_dir, ignore_errors=True)

    log.info("submodel-templates-sync complete")


if __name__ == "__main__":
    main()
