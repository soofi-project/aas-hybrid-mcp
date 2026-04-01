#!/bin/bash
# ===========================================
# AAS Hybrid MCP - Start Stack
# ===========================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  AAS Hybrid MCP - Starting Stack"
echo "========================================"
echo ""

# Load environment variables
source .env 2>/dev/null || true

# Parse args
BUILD_FLAG=""
if [ "$1" == "--build" ]; then
    BUILD_FLAG="--build"
fi

# Start containers (build only if --build passed)
if [ -n "$BUILD_FLAG" ]; then
    echo "[INFO] Building and starting containers..."
else
    echo "[INFO] Starting containers..."
fi
docker compose up -d --wait $BUILD_FLAG

# Check container status
echo ""
echo "[INFO] Container Status:"
docker compose ps

# Print URLs
echo ""
echo "========================================"
echo "  Services are ready!"
echo "========================================"
echo ""
echo "  AAS GUI:         http://localhost:8099"
echo "  AAS Environment: http://localhost:8081"
echo "  AAS Registry:    http://localhost:8083"
echo "  Neo4j Browser:   http://localhost:7474"
echo "  Weaviate:        http://localhost:8070"
echo "  AKHQ (Kafka):    http://localhost:8086"
echo "  Embedding Svc:   http://localhost:8000/health"
echo "  MCP Server:      http://localhost:8110/mcp/"
echo "  MCP Inspector:   http://localhost:6274/?transport=streamable-http&serverUrl=http://aas-hybrid-mcp:8110/mcp/&MCP_PROXY_AUTH_TOKEN=${MCP_AUTH_TOKEN}"
echo "  Open WebUI:      http://localhost:8090 (${OPEN_WEBUI_EMAIL} | ${OPEN_WEBUI_PASSWORD})"
echo ""
echo "========================================"
echo ""
echo "To stop the stack, run:  ./down.sh"
echo "To stop and wipe data:  ./down.sh --clean"
echo ""
