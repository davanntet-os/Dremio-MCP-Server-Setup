# Dremio MCP Server (local, for Dify)

## What's here
- `dremio-mcp/` — cloned repo (github.com/dremio/dremio-mcp), deps installed via `uv sync`
- `print_token.py` — generates a Dremio PAT by logging into `http://localhost:9047`
- `pat.txt` — the generated PAT (keep private)
- `start-mcp-server.sh` — runs the MCP server in streamable-HTTP mode on port 8000
- `~/.config/dremioai/config.yaml` — server config (uri + PAT + mode)

## Stack
1. Dremio OSS in Docker: container `dremio`, UI/API at http://localhost:9047
   - Admin user bootstrapped via `PUT /apiv2/bootstrap/firstuser` (user: `dremioadmin`)
   - Restart with: `docker start dremio`
2. MCP server: `./start-mcp-server.sh` → listens on `http://0.0.0.0:8000/mcp`
   - Default mode `FOR_DATA_PATTERNS` (data exploration, NL→SQL, view creation)
   - Auth: any non-empty `Authorization: Bearer <token>` is accepted when `jwks_uri`
     is not configured — use the PAT as the bearer token.

## Dify setup (MCP over streamable HTTP)
1. In Dify: Plugins → install the official **MCP** plugin (marketplace).
2. In your app → Tools → Add tool → **MCP Server (HTTP)** → *Add MCP Server*:
   - Name: `Dremio`
   - Server URL: `http://192.168.0.25:8000/mcp`
     (use the host LAN IP, not `localhost`, if Dify runs inside Docker)
   - Headers: `Authorization: Bearer <contents of pat.txt>`
3. Save — tools appear: `RunSqlQuery`, `GetUsefulSystemTableNames`,
   `GetSchemaOfTable`, `GetDescriptionOfTableOrSchema`, `GetTableOrViewLineage`.
4. Add them to your agent/chatflow and ask e.g.
   *"what tables or views are available in Dremio?"*

## Useful commands
```bash
# verify server responds (should return MCP initialize result)
curl -s -X POST http://localhost:8000/mcp \
  -H "Authorization: Bearer $(cat pat.txt)" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}'

# test a tool without Dify
cd dremio-mcp
uv run dremio-mcp-server tools invoke -t RunSqlQuery query='SELECT 1'

# regenerate PAT if it expires/is revoked
uv run --with dremio-simple-query print_token.py > pat.txt

# change mode (e.g. system introspection)
cd dremio-mcp
uv run dremio-mcp-server config create dremioai --uri http://localhost:9047 \
  --pat @/home/super-computer/Desktop/Dremio-MCP/pat.txt --mode FOR_SELF
```

MCP jobs show up in the Dremio console under Jobs → QUERY TYPE = External Tools,
with SQL prefixed `dremioai:`.
