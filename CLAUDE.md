# ResQ MCP — Agent Guide

## Mission
FastMCP server exposing ResQ platform capabilities to AI clients (Claude, Cursor, etc.). Provides tools for drone dispatch, airspace queries, incident management, and mission planning over the Model Context Protocol.

## Workspace Layout
- `src/resq_mcp/` — Main package: tools, resources, prompts, and server entrypoint.
- `tests/` — pytest test suite.
- `pyproject.toml` — Project metadata, dependencies, and tool config.

## Commands
```bash
uv run resq-mcp           # Start MCP server (stdio transport)
uv run pytest             # Run test suite
uv run pytest --cov=src   # Run with coverage
uv run ruff check src/    # Lint
uv run ruff format src/   # Format
./agent-sync.sh --check   # Verify AGENTS.md and CLAUDE.md are in sync
```

## Architecture
- **Framework**: FastMCP 2.x — tools are plain async Python functions decorated with `@mcp.tool()`.
- **Transport**: stdio by default; SSE available for remote clients.
- **Auth**: Bearer token passed via MCP client config; validated in middleware.
- **Tools** are grouped by domain (drone, airspace, incident, mission) and live under `src/resq_mcp/tools/`.
- **Resources** expose read-only platform data (maps, status pages) via `@mcp.resource()`.
- **Prompts** provide reusable prompt templates via `@mcp.prompt()`.

## Standards
- Python 3.11+; use `from __future__ import annotations` in all files.
- Type-annotate all tool parameters and return types — FastMCP uses these for schema generation.
- Async functions throughout; no blocking I/O in tool handlers.
- Tests use pytest + `pytest-asyncio`; mock external HTTP with `aioresponses`.
- All source files carry the Apache-2.0 license header.
- Keep `AGENTS.md` and `CLAUDE.md` in sync using `./agent-sync.sh`.

## Repository Rules
- Do not commit `.venv/` or `__pycache__/`.
- Tool names must be snake_case and match the MCP spec identifier format.
- Every tool needs a docstring — FastMCP exposes it as the tool description to AI clients.

## References
- [Root README](README.md)
- [pyproject.toml](pyproject.toml)
- [FastMCP Docs](https://gofastmcp.com)
