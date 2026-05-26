FROM python:3.11-slim AS builder

WORKDIR /build
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir --prefix=/install .

FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home appuser
USER appuser
WORKDIR /app

COPY --from=builder /install /usr/local

EXPOSE 8120

CMD ["uvicorn", "aas_agent.api:app", "--host", "0.0.0.0", "--port", "8120"]
