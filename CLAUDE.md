# ResQ MCP — Developer & Agent Guide

## Mission
ResQ MCP connects AI agents to the ResQ platform's robotics, physics simulations, and disaster telemetry. It provides a secure, typed interface for drone fleet command, predictive intelligence (PDIE), and digital twin optimization (DTSOP) over the Model Context Protocol.

## Workspace Layout
```
src/resq_mcp/
├── server.py              # FastMCP init, lifespan, background tasks
├── resources.py           # @mcp.resource() endpoints (drones, sims)
├── prompts.py             # @mcp.prompt() templates (incident response)
├── core/                  # Cross-cutting: config, errors, security, telemetry, timeout
├── drone/                 # Drone feed: scan, swarm, deployment (models + service)
├── dtsop/                 # Digital Twin: simulation, optimization (models + service + tools)
├── hce/                   # Hybrid Coordination: incidents, missions (models + service + tools)
└── pdie/                  # Predictive Intelligence: vulnerability, alerts (models + service)
tests/
├── unit/                  # Domain-specific logic and tool unit tests
├── integration/           # Multi-module workflow validation
└── property/              # Hypothesis-driven probabilistic testing
```

## Essential Commands
```bash
uv run resq-mcp           # Start server in STDIO mode
uv run pytest             # Run full test suite
uv run ruff check .       # Lint and check style
./agent-sync.sh           # Synchronize AGENTS.md and CLAUDE.md
```

## Technical Architecture
- **Protocol**: FastMCP 2.x — strictly typed async tool handlers.
- **Transport**: Native support for STDIO (local) and SSE (networked).
- **Domain Structure**: Modules (`drone/`, `dtsop/`, etc.) encapsulate logic in `service.py` and models in `models.py`. Tool registrations reside in domain-specific `tools.py`.
- **Background Tasks**: The server maintains a lifespan-managed `simulation_processor` for async job status updates and SSE notifications.

## Safety & Operations
- **Safe Mode**: Enabled by default (`RESQ_SAFE_MODE=true`). Mutations (deployments, sim starts) raise `FastMCPError`. Agents should use this mode for mission planning and validation.
- **Fail-Fast**: The server validates environment variables and API keys on startup.
- **Type Safety**: All inputs/outputs use Pydantic models to ensure AI-tool reliability.

## Standards
- **Async First**: No blocking I/O; use `httpx` for external requests.
- **Annotations**: Use `from __future__ import annotations` (except in `server.py` for runtime Pydantic resolution).
- **Testing**: Every tool requires unit tests and, where applicable, property-based tests for edge cases.
- **License**: All source files must include the Apache-2.0 header.

## References
- [Root README](README.md) — Feature overview and quick start.
- [pyproject.toml](pyproject.toml) — Dependencies and metadata.
- [FastMCP Documentation](https://gofastmcp.com)
