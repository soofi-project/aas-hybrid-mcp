ARG VARIANT=fast

# ---------------------------------------------------------------------------
# Precise variant: docling + PyTorch CPU for ML-based layout/table recognition
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder-precise

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
RUN pip install --no-cache-dir --prefix=/install ".[precise]"

# ---------------------------------------------------------------------------
# Fast variant: pymupdf4llm only, rule-based, no ML dependencies
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder-fast

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install ".[fast]"

# ---------------------------------------------------------------------------
# Variant selector: resolve build arg to a concrete stage
# ---------------------------------------------------------------------------
ARG VARIANT=fast
FROM builder-${VARIANT} AS selected-builder

# ---------------------------------------------------------------------------
# Final image
# ---------------------------------------------------------------------------
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser
USER appuser
WORKDIR /app

COPY --from=selected-builder /install /usr/local
COPY app.py config.py handlers.py pdf.py vectorstore.py ./

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "300", "app:app"]
