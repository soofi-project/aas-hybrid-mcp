#!/bin/bash
# ===========================================
# AAS Hybrid MCP - Stop Stack
# ===========================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  AAS Hybrid MCP - Stopping Stack"
echo "========================================"
echo ""

# Stop containers
#   default          — wipe ephemeral data stores (mongo/kafka/neo4j),
#                      keep named volumes (weaviate, templates, open-webui).
#                      BaSyx redeploys AASX on next ./up.sh; Weaviate embeddings stay.
#   --clean          — full reset, removes all volumes including weaviate.
#   --keep-all       — stop only, keep everything (matches old default behavior).
case "${1:-}" in
    --clean)
        echo "[INFO] Full reset — stopping containers and removing ALL volumes (including weaviate)..."
        docker compose down -v
        ;;
    --keep-all)
        echo "[INFO] Stopping containers, keeping all volumes..."
        docker compose down
        ;;
    "")
        echo "[INFO] Stopping containers, wiping ephemeral data (mongo/kafka/neo4j), keeping weaviate..."
        # rm -fsv: stop (-s), force (-f), remove anonymous volumes attached to these services (-v).
        # Named volumes (weaviate_content, template_data, open_webui_data) are unaffected.
        docker compose rm -fsv mongo kafka neo4j
        docker compose down
        ;;
    *)
        echo "[ERROR] Unknown flag: $1" >&2
        echo "Usage: $0 [--clean | --keep-all]" >&2
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "  Stack is down"
echo "========================================"
echo ""
echo "To start again, run: ./up.sh"
echo ""
