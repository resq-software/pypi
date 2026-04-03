# ResQ MCP Server — Agent Guide

## Mission
FastMCP server exposing ResQ platform capabilities (drone fleet, PDIE, DTSOP) to AI clients. Published to PyPI as `resq-mcp`.

## Stack
- Runtime: Python 3.11+
- Build: Hatchling
- Package Manager: uv
- Testing: pytest (+ hypothesis for property-based tests)
- Linting: ruff + mypy (strict)
- Release: python-semantic-release

## Repo Map
- `src/resq_mcp/` — Server source (core/, models/, tools, server)
- `tests/` — Unit, integration, and property-based tests
- `scripts/` — Development scripts
- `Dockerfile` — Container image
- `CHANGELOG.md` — Auto-managed by semantic-release

## Commands
```bash
uv sync && uv run pytest
uv run ruff check src/ tests/
uv run mypy src/
```

## Rules
- Python 3.11+ minimum
- ruff for linting, mypy for type checking (strict mode)
- All source files must include Apache-2.0 license header
- `AGENTS.md` is the source of truth for `CLAUDE.md` — never edit `CLAUDE.md` directly

## Safety
- Safe mode (`RESQ_SAFE_MODE=true`) is default — mutations raise errors
- Don't publish without running full test suite and linting

## Workflow
1. `uv sync` to install dependencies
2. `uv run pytest` to test
3. `uv run ruff check src/ tests/` to lint
4. Summarize: files changed, behavior change, tests run

## References
- [README](README.md) — Full server documentation
- [CHANGELOG](CHANGELOG.md) — Release history
- [SECURITY](SECURITY.md) — Security policy
