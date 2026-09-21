#!/usr/bin/env bash
# Starts the Dremio MCP server in streamable-HTTP mode (for Dify and other HTTP MCP clients).
# Prereq: ~/.config/dremioai/config.yaml exists (created via: dremio-mcp-server config create dremioai)
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"
HOST_IP=$(hostname -I | awk '{print $1}')
PORT="${1:-8001}"

echo "Dremio MCP server starting on http://0.0.0.0:${PORT}/mcp"
echo "From Dify (in Docker), use: http://${HOST_IP}:${PORT}/mcp"
echo "Press Ctrl+C to stop."

cd "$(dirname "$0")/dremio-mcp"
exec uv run dremio-mcp-server run \
  --enable-streaming-http \
  --host 0.0.0.0 \
  --port "${PORT}" \
  --disable-dns-rebinding-protection
