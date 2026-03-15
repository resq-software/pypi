---
name: run
description: Start the MCP server in STDIO or SSE mode.
---

# /run

Start the ResQ MCP server.

## Usage

```
/run [--sse]
```

## Steps

1. Without `--sse`: Run `uv run resq-mcp` (STDIO mode — for Claude Desktop / MCP Inspector).
2. With `--sse`: Run `RESQ_HOST=0.0.0.0 RESQ_PORT=8000 uv run resq-mcp` (SSE/HTTP mode).
3. Confirm the server started and is accepting connections.
4. If startup fails, report the Pydantic validation error (missing required env vars) and show which `.env` variable to set.
