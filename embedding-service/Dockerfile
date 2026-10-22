FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# The packages live in a venv: pip resolves against the environment it runs in, and with
# `--prefix` that never includes the target, so an earlier CPU-only torch was invisible and
# docling pulled the default PyPI wheel again (CUDA: ~4 GB of nvidia/triton libraries, unused,
# this service runs on CPU). In the venv the CPU torch counts as installed.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY pyproject.toml .
RUN pip install --no-cache-dir . \
    # fail the build if a CUDA stack came back in with a dependency
    && ! pip list --format=freeze | grep -i -E '^(nvidia-|triton)'

FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# The cache dir and its parent (huggingface_hub writes next to it) must exist and belong to appuser: a named volume mounted on a path the image lacks is created root-owned.
RUN useradd --create-home appuser \
    && mkdir -p /home/appuser/.cache/docling/models \
    && chown -R appuser:appuser /home/appuser/.cache
USER appuser
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# No models are baked into the image: the full `docling-tools models download`
# catalog (~1.7 GB, incl. CodeFormula, picture classifier and RapidOCR that
# this service never uses — do_ocr is off and no enrichment is enabled) blew
# up both the image and the mode=max buildcache in the project registry, per
# platform, and pushed the CI build past its timeout under QEMU on arm64.
# pdf.py instead downloads only the pipeline's needs (layout + tableformer,
# ~600 MB) into DOCLING_ARTIFACTS_PATH on first use; the compose stack mounts
# a volume there, so the download happens once and is reused across restarts
# and image updates.
ENV DOCLING_ARTIFACTS_PATH=/home/appuser/.cache/docling/models

COPY app.py config.py events.py handlers.py pdf.py vectorstore.py ./

EXPOSE 8000

# One process, two threads: the second thread answers /health during a long ingestion; app.py serializes the handlers.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--worker-class", "gthread", "--threads", "2", "--timeout", "1800", "app:app"]
