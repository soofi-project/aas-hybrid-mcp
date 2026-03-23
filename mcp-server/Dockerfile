FROM python:3.11-slim AS builder

WORKDIR /build
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir --prefix=/install .

FROM python:3.11-slim

RUN useradd --create-home appuser
USER appuser
WORKDIR /app

COPY --from=builder /install /usr/local

EXPOSE 8110

CMD ["aas-hybrid-mcp"]
