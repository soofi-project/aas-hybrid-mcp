"""Submodel Templates Sync — clone IDTA templates, extract metadata, ingest PDFs.

Init container that runs once on stack start:
1. Git clone submodel-templates repo
2. Discover latest version per template
3. Extract JSON metadata (index + per-template element structure)
4. Convert spec PDFs to markdown, chunk, embed, insert into Weaviate
"""

import base64
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import httpx
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
WEAVIATE_HOST = os.environ["WEAVIATE_HOST"]
WEAVIATE_HTTP_PORT = int(os.environ["WEAVIATE_PORT"])
WEAVIATE_GRPC_PORT = int(os.environ["WEAVIATE_GRPC_PORT"])
TEMPLATES_OUTPUT_DIR = Path(os.environ["TEMPLATES_OUTPUT_DIR"])
IDTA_COLLECTION = "IdtaTemplateSpec"

CHUNK_SIZE = int(os.environ["CHUNK_SIZE"])
CHUNK_OVERLAP = int(os.environ["CHUNK_OVERLAP"])
EMBEDDING_BATCH_SIZE = int(os.environ["EMBEDDING_BATCH_SIZE"])

CD_REPO_URL = os.environ.get("CD_REPO_URL", "http://aas-environment:8081")
BASYX_TIMEOUT = 30.0

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
    """Return the HEAD commit SHA of the cloned repo.

    Falls back to "local" when the directory is not a git repository
    (e.g. a plain bind-mount via TEMPLATES_LOCAL_PATH without git metadata).
    In that case the Weaviate idempotency check always runs the full sync on
    first use, then skips it on subsequent restarts once "local" is stored.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        log.info("Directory %s is not a git repo; using hash 'local'", repo_dir)
        return "local"


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
    """Find latest version per template from the IDTA git repo.

    Discovers the newest version directory for each published template.
    Returns a list of {name, version, path} dicts — same format expected
    by process_json_templates, generate_classes, ingest_pdfs, etc.
    """
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

    log.info("Discovered %d IDTA templates", len(results))
    return results


def discover_custom_templates(custom_dir: Path) -> list[dict]:
    """Discover user-defined templates in a flat directory.

    Scans custom_dir (e.g. /data/user-templates) for JSON files that contain
    submodels with ``kind == "Template"``.  Each qualifying submodel becomes
    an entry in the returned list — the same {name, version, path, json_path}
    shape expected by process_json_templates, generate_classes, ingest_pdfs,
    and push_concept_descriptions.

    If a single ``.json`` file carries multiple template submodels all will
    be returned.  Returns an empty list (no-op) when custom_dir is absent or
    contains no template submodels.
    """
    if not custom_dir.is_dir():
        log.info("Custom templates directory not found: %s — skipping", custom_dir)
        return []

    results: list[dict] = []
    for json_path in sorted(custom_dir.glob("*.json")):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            log.warning("Skipping unparseable file %s", json_path.name)
            continue
        sm = data.get("submodels", [])
        for submodel in sm:
            if submodel.get("kind") != "Template":
                continue
            # Build entry — reuse the same shape as discover_templates.
            # ``path`` points to the JSON file's parent (so _find_pdfs can
            # look for sibling PDFs), and ``json_path`` shortcuts the
            # _find_json call inside process_json_templates.
            ad = submodel.get("administration", {})
            version = ad.get("version", "1")
            revision = ad.get("revision", "0")
            results.append({
                "name": submodel.get("idShort", json_path.stem),
                "version": f"{version}.{revision}",
                "path": json_path.parent,
                "json_path": json_path,
            })

    log.info("Discovered %d custom templates in %s", len(results), custom_dir)
    return results


# ---------------------------------------------------------------------------
# JSON extraction
# ---------------------------------------------------------------------------


def _find_json(template_dir: Path) -> Path | None:
    """Find the best AAS JSON in a template version directory.

    Prefers V3.1 metamodel JSON for metadata extraction (richer content).
    """
    jsons = list(template_dir.glob("*.json"))
    if not jsons:
        jsons = list(template_dir.rglob("*.json"))
    if not jsons:
        return None

    for j in jsons:
        if "forAASMetamodelV3.1" in j.name or "MetamodelV3.1" in j.name:
            return j
    for j in jsons:
        if "forAASMetamodelV3.0" in j.name or "MetamodelV3.0" in j.name:
            return j
    for j in jsons:
        if "MetamodelV" in j.name or "Metamodel_V" in j.name:
            return j
    return jsons[0]


def _find_json_v3_0(template_dir: Path) -> Path | None:
    """Find a V3.0 metamodel JSON suitable for the basyx-python-sdk code generator.

    The SDK and aas-submodel-to-py only support AAS V3.0 namespace.
    V3.1 files use a different XML namespace and cannot be parsed.
    """
    jsons = list(template_dir.glob("*.json"))
    if not jsons:
        jsons = list(template_dir.rglob("*.json"))
    if not jsons:
        return None

    # Prefer explicit V3.0 label — guaranteed to parse with basyx-python-sdk 2.x.
    for j in jsons:
        if "forAASMetamodelV3.0" in j.name or "MetamodelV3.0" in j.name:
            return j
    # Accept any non-V3.1 AAS metamodel JSON as a fallback.
    for j in jsons:
        if ("MetamodelV" in j.name or "Metamodel_V" in j.name) and "3.1" not in j.name:
            return j
    # Last resort: any JSON that is not explicitly tagged V3.1.
    for j in jsons:
        if "3.1" not in j.name:
            return j
    return None


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
    """Recursively extract element structure from a submodel.

    Preserves original AAS JSON child keys (`value`, `statements`) so an agent
    can build correct Submodel JSON for ``put_submodel`` without guessing.
    The top-level ``submodelElements`` key is stripped (implied by the template
    context) to keep the output compact.
    """

    CHILD_KEYS = ["submodelElements", "value", "statements"]

    def _walk(elements: list, depth: int) -> list[dict]:
        if depth > max_depth:
            return []
        result = []
        for el in elements:
            model_type = el.get("modelType", "")
            entry: dict = {
                "modelType": model_type,
                "idShort": el.get("idShort", ""),
            }
            # valueType on Property, Range — the agent needs this for put_submodel
            if "valueType" in el:
                entry["valueType"] = el["valueType"]

            # Extract valueTypeListElement on SubmodelElementList
            if "valueTypeListElement" in el:
                entry["valueTypeListElement"] = el["valueTypeListElement"]

            # Extract typeValueListElement and orderRelevant on SubmodelElementList
            if model_type == "SubmodelElementList":
                for k in ("typeValueListElement", "orderRelevant"):
                    if k in el:
                        entry[k] = el[k]

            # Extract semanticId
            sid = el.get("semanticId", {})
            keys = sid.get("keys", [])
            if keys:
                entry["semanticId"] = keys[0].get("value", "")

            # Recurse into children, preserving the original AAS JSON child key
            for key in CHILD_KEYS:
                children = el.get(key)
                if isinstance(children, list) and children:
                    if key == "submodelElements":
                        # Always present for Submodel — implied, omit from output
                        entry.setdefault("submodelElements", _walk(children, depth + 1))
                    else:
                        # "value" for SMC/SLE, "statements" for Entity —
                        # preserve verbatim so the agent can use it directly
                        entry[key] = _walk(children, depth + 1)
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

        # Custom templates provide json_path directly; IDTA templates need look-up.
        if "json_path" in tpl:
            json_path = Path(tpl["json_path"])
        else:
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


def _process_json_templates_no_index(templates: list[dict]) -> list[dict]:
    """Like process_json_templates but does NOT write index.json.

    Used for custom templates so the existing IDTA index.json isn't
    overwritten before the merge step writes the combined result.
    """
    TEMPLATES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    index_entries = []
    for tpl in templates:
        name = tpl["name"]
        version = tpl["version"]
        template_dir = tpl["path"]

        if "json_path" in tpl:
            json_path = Path(tpl["json_path"])
        else:
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

        entry = {
            "name": name,
            "version": version,
            **metadata,
        }
        index_entries.append(entry)

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

        safe_name = re.sub(r'[<>:"/\\|?*]', "_", name)
        out_path = TEMPLATES_OUTPUT_DIR / f"{safe_name}.json"
        out_path.write_text(json.dumps(template_data, indent=2, ensure_ascii=False), encoding="utf-8")
        log.info("Wrote %s", out_path)

    log.info("Processed %d custom templates (index.json not written)", len(index_entries))
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


def generate_classes(templates: list[dict]) -> int:
    """Generate typed Python classes from IDTA submodel templates.

    Uses aas-submodel-to-py to produce one .py file per template from its
    V3.0 AAS JSON.  Files land in TEMPLATES_OUTPUT_DIR/generated/ and are
    loaded at runtime by the MCP server's template_validator module.

    Some published IDTA templates set id_short on SubmodelElementList items,
    violating AASd-120.  The generator uses failsafe=True internally, so it
    skips non-parseable elements and produces a partial class.  We suppress
    the SDK's per-element ERROR logs during generation (they are expected noise
    for non-conformant templates) and emit a single WARNING per affected file.

    Returns the number of successfully generated files.
    """
    import logging as _logging
    from aas_submodel_to_py.generator import SubmodelCodegen

    generated_dir = TEMPLATES_OUTPUT_DIR / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    # Write an __init__.py so the directory is importable as a package.
    (generated_dir / "__init__.py").write_text("", encoding="utf-8")

    codegen = SubmodelCodegen()
    count = 0

    # Silence the basyx deserialization logger during generation: its ERROR
    # lines for AASd-120 / AASd-131 violations in template JSON are expected
    # and handled gracefully by the generator's failsafe mode.  We restore the
    # level afterwards so normal operation is unaffected.
    basyx_deser_log = _logging.getLogger("basyx.aas.adapter.json.json_deserialization")
    _saved_level = basyx_deser_log.level
    basyx_deser_log.setLevel(_logging.CRITICAL)

    try:
        for tpl in templates:
            name = tpl["name"]
            template_dir = tpl["path"]

            json_path = _find_json_v3_0(template_dir)
            if json_path is None:
                log.debug("No V3.0 JSON found for %s — skipping class generation", name)
                continue

            safe_name = re.sub(r'[<>:"/\\|?*]', "_", name)
            out_path = generated_dir / f"{safe_name}.py"

            try:
                codegen.generate_from(json_path, out_path)

                # A generated file with only the import block and no class body
                # means the parser found no usable Submodel (all elements
                # failed AASd-120).  Treat as a partial/empty result.
                content = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
                if "class " not in content:
                    log.warning(
                        "No class generated for %s — template JSON may have "
                        "AASd-120 violations throughout; falling back to "
                        "metamodel-only validation for this template.",
                        name,
                    )
                    out_path.unlink(missing_ok=True)
                    continue

                count += 1
                log.info("Generated class for %s → %s", name, out_path.name)

            except Exception as exc:
                # Non-fatal: templates without a parseable V3.0 JSON simply
                # have no generated class; metamodel-only validation applies.
                log.warning("Class generation failed for %s: %s", name, exc)
                out_path.unlink(missing_ok=True)
    finally:
        basyx_deser_log.setLevel(_saved_level)

    log.info("Class generation complete: %d / %d templates", count, len(templates))
    return count


def is_up_to_date(client: weaviate.WeaviateClient, repo_hash: str) -> bool:
    """Check if both the Weaviate collection and generated classes are current.

    Returns False if the generated/ directory is absent or empty, so a fresh
    stack start always produces classes even when the repo hash is unchanged.
    """
    if not client.collections.exists(SYNC_HASH_COLLECTION):
        return False
    if not client.collections.exists(IDTA_COLLECTION):
        return False

    # Regenerate classes if the output directory is missing or empty.
    generated_dir = TEMPLATES_OUTPUT_DIR / "generated"
    if not generated_dir.exists() or not any(generated_dir.glob("*.py")):
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
# ConceptDescription push to BaSyx CD-Repository
# ---------------------------------------------------------------------------


def _b64url(s: str) -> str:
    """Base64-URL encode an AAS identifier (no padding, per IDTA Part 2 REST spec)."""
    return base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")


def push_concept_descriptions(templates: list[dict]) -> None:
    """PUT every ConceptDescription from each template's AAS package JSON
    into the BaSyx ConceptDescription Repository.

    Idempotent: PUT-by-id replaces existing entries silently. Per-CD failures
    are logged and do not abort the loop. Templates without CDs are skipped
    quietly.
    """
    pushed_total = 0
    failed_total = 0
    skipped_total = 0
    templates_with_cds = 0

    with httpx.Client(base_url=CD_REPO_URL, timeout=BASYX_TIMEOUT) as client:
        for tpl in templates:
            name = tpl["name"]
            template_dir = tpl["path"]

            json_path_for_cd = tpl.get("json_path")
            if json_path_for_cd is not None:
                json_path_for_cd = Path(json_path_for_cd)
            else:
                json_path_for_cd = _find_json(template_dir)
            if json_path_for_cd is None:
                continue
            try:
                data = json.loads(json_path_for_cd.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue

            cds = data.get("conceptDescriptions") or []
            if not cds:
                continue

            templates_with_cds += 1
            pushed = 0
            failed = 0

            for cd in cds:
                cd_id = cd.get("id")
                if not cd_id:
                    skipped_total += 1
                    continue

                try:
                    r = client.put(
                        f"/concept-descriptions/{_b64url(cd_id)}",
                        json=cd,
                    )
                    if r.status_code == 404:
                        # CD not yet present — fall back to POST
                        r = client.post("/concept-descriptions", json=cd)
                    if r.status_code in (200, 201, 204, 409):
                        pushed += 1
                    else:
                        failed += 1
                        log.warning(
                            "PUT CD %s failed: %d %s",
                            cd_id, r.status_code, r.text[:200],
                        )
                except httpx.HTTPError as e:
                    failed += 1
                    log.warning("PUT CD %s exception: %s", cd_id, e)

            pushed_total += pushed
            failed_total += failed
            log.info(
                "Pushed %d/%d CDs for template %s",
                pushed, len(cds), name,
            )

    log.info(
        "CD push complete: %d templates carried CDs, %d pushed, %d failed, %d skipped (no id)",
        templates_with_cds, pushed_total, failed_total, skipped_total,
    )


# ---------------------------------------------------------------------------
# Custom templates (user-defined, outside the IDTA git repo)
# ---------------------------------------------------------------------------


def sync_custom_templates(
    client: weaviate.WeaviateClient,
    custom_dir: Path,
    idta_index_entries: list[dict],
) -> None:
    """Process user-defined templates through the same pipeline as IDTA.

    Discovers templates with ``kind == "Template"``, writes index + per-template
    JSON, generates typed classes, ingests PDFs (if any), pushes CDs, and
    rewrites the final merged index.json.
    """
    custom_templates = discover_custom_templates(custom_dir)
    if not custom_templates:
        return

    # 1. Extract metadata + element structures (custom processing to avoid
    #    overwriting index.json — the merged index is written at the end).
    custom_index_entries = _process_json_templates_no_index(custom_templates)

    # 2. Generate typed Python classes
    generate_custom_classes(custom_templates)

    # 3. Ingest PDFs if Weaviate collection exists (may not if IDTA was skipped
    #     and this is a fresh run with only custom templates).
    if client.collections.exists(IDTA_COLLECTION):
        ingest_pdfs(client, custom_templates, custom_index_entries)
    else:
        log.info(
            "Collection %s does not exist — skipping custom PDF ingestion",
            IDTA_COLLECTION,
        )

    # 4. Push ConceptDescriptions
    push_concept_descriptions(custom_templates)

    # 5. Write merged index (IDTA + custom)
    # Merge by semanticId so custom entries overwrite stale duplicates from
    # previous runs — no index growth on repeated starts.
    seen: dict[str, dict] = {}
    for e in idta_index_entries:
        key = e.get("semanticId") or f"__nosid__{e.get('idShort', '')}"
        seen[key] = e
    for e in custom_index_entries:
        key = e.get("semanticId") or f"__nosid__{e.get('idShort', '')}"
        seen[key] = e  # custom overwrites stale entry from prior runs
    merged = list(seen.values())
    index_path = TEMPLATES_OUTPUT_DIR / "index.json"
    index_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("Wrote merged index.json with %d templates (%d IDTA, %d custom, %d deduped)",
             len(merged), len(idta_index_entries), len(custom_index_entries),
             len(idta_index_entries) + len(custom_index_entries) - len(merged))


def generate_custom_classes(templates: list[dict]) -> int:
    """Generate typed Python classes from custom template JSON files.

    Mirrors generate_classes() but operates on the ``json_path`` key provided
    by discover_custom_templates instead of directory-based look-up.
    """
    import logging as _logging
    from aas_submodel_to_py.generator import SubmodelCodegen

    generated_dir = TEMPLATES_OUTPUT_DIR / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    (generated_dir / "__init__.py").write_text("", encoding="utf-8")

    codegen = SubmodelCodegen()
    count = 0

    basyx_deser_log = _logging.getLogger("basyx.aas.adapter.json.json_deserialization")
    _saved_level = basyx_deser_log.level
    basyx_deser_log.setLevel(_logging.CRITICAL)

    try:
        for tpl in templates:
            name = tpl["name"]
            json_path: Path | None = tpl.get("json_path")
            if json_path is None:
                continue

            safe_name = re.sub(r'["<>:|\\*?/]', "_", name)
            out_path = generated_dir / f"{safe_name}.py"

            try:
                codegen.generate_from(json_path, out_path)
                content = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
                if "class " not in content:
                    log.warning(
                        "No class generated for %s — template JSON may have "
                        "AASd-120 violations; falling back to metamodel-only "
                        "validation for this template.",
                        name,
                    )
                    out_path.unlink(missing_ok=True)
                    continue

                count += 1
                log.info("Generated custom class for %s → %s", name, out_path.name)

            except Exception as exc:
                log.warning("Class generation failed for %s: %s", name, exc)
                out_path.unlink(missing_ok=True)
    finally:
        basyx_deser_log.setLevel(_saved_level)

    log.info("Custom class generation complete: %d / %d templates", count, len(templates))
    return count


def main():
    log.info("Starting submodel-templates-sync")

    # 1. Clone repo (or use a pre-loaded local copy if TEMPLATES_LOCAL_PATH is set).
    # Set TEMPLATES_LOCAL_PATH to a bind-mounted git clone of admin-shell-io/submodel-templates
    # when the container host has no internet access to GitHub.
    local_path = os.environ.get("TEMPLATES_LOCAL_PATH", "").strip()
    if local_path:
        clone_dir = Path(local_path)
        do_cleanup = False
        log.info("Using pre-loaded templates from %s (skipping git clone)", clone_dir)
    else:
        clone_dir = Path(tempfile.mkdtemp(prefix="submodel-templates-"))
        do_cleanup = True

    try:
        if do_cleanup:
            clone_repo(clone_dir)
        repo_hash = get_repo_hash(clone_dir)
        log.info("Repo HEAD: %s", repo_hash)

        # Custom templates directory (always scanned, independent of IDTA hash).
        custom_dir = Path("/data/user-templates")

        # 2. Idempotency check — skip IDTA sync if already current from same commit
        client = wait_for_weaviate()
        try:
            idta_templates = []
            idta_index_entries = []

            if is_up_to_date(client, repo_hash):
                log.info(
                    "Collection %s already up-to-date (hash %s), skipping IDTA sync",
                    IDTA_COLLECTION, repo_hash,
                )
                # Read existing index so custom templates can merge correctly.
                existing_index = TEMPLATES_OUTPUT_DIR / "index.json"
                if existing_index.exists():
                    idta_index_entries = json.loads(existing_index.read_text(encoding="utf-8"))
            else:
                # The published templates are in published/
                published_dir = clone_dir / "published"
                if not published_dir.is_dir():
                    # Try alternative locations
                    for candidate in ["Published", "submodel-templates", "."]:
                        alt = clone_dir / candidate
                        if alt.is_dir() and any(alt.iterdir()):
                            published_dir = alt
                            break

                # 3. Discover IDTA templates
                idta_templates = discover_templates(published_dir)
                if not idta_templates:
                    log.error("No templates discovered in %s", published_dir)
                else:
                    # 4. Extract IDTA JSON metadata and element structures
                    idta_index_entries = process_json_templates(idta_templates)

                    # 5. Generate typed Python classes from V3.0 IDTA JSONs
                    generate_classes(idta_templates)

                    # 6. Ingest IDTA PDFs into Weaviate
                    setup_collection(client)
                    ingest_pdfs(client, idta_templates, idta_index_entries)

                    # 7. Push template-defined ConceptDescriptions to BaSyx
                    push_concept_descriptions(idta_templates)

                    # 8. Store sync hash on success
                    store_sync_hash(client, repo_hash)

            # 9. Custom templates — ALWAYS run (independent of IDTA hash)
            sync_custom_templates(client, custom_dir, idta_index_entries)

        finally:
            client.close()

    finally:
        if do_cleanup:
            shutil.rmtree(clone_dir, ignore_errors=True)

    log.info("submodel-templates-sync complete")


if __name__ == "__main__":
    main()
