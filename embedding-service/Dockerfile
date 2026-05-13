FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Install PyTorch CPU-only first to avoid pulling ~3 GB of CUDA libraries
RUN pip install --no-cache-dir --prefix=/install \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install .

FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser
USER appuser
WORKDIR /app

COPY --from=builder /install /usr/local
COPY app.py config.py handlers.py pdf.py vectorstore.py ./

# Pre-download docling models so the runtime container is offline-capable.
# Models land in /home/appuser/.cache/docling/models (docling default cache path).
RUN docling-tools models download

# Skip HuggingFace Hub revalidation at runtime; use the baked cache directly.
ENV HF_HUB_OFFLINE=1
ENV DOCLING_ARTIFACTS_PATH=/home/appuser/.cache/docling/models

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "1800", "app:app"]
