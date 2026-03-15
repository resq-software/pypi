<h1 align="center">resQ MCP</h1>

<p align="center">
  FastMCP server exposing ResQ platform capabilities — simulations, drone coordination, and incident response — to AI clients.
</p>

<p align="center">
  <a href="https://github.com/resq-software/mcp/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/resq-software/mcp/ci.yml?branch=main&label=ci&style=flat-square" alt="CI" />
  </a>
  <a href="https://pypi.org/project/resq-mcp/">
    <img src="https://img.shields.io/pypi/v/resq-mcp?style=flat-square" alt="PyPI" />
  </a>
  <a href="https://codecov.io/gh/resq-software/mcp">
    <img src="https://codecov.io/gh/resq-software/mcp/graph/badge.svg" alt="Coverage" />
  </a>
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg?style=flat-square" alt="License: Apache-2.0" />
  </a>
</p>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Install](#install)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Overview

`resq-mcp` is a [Model Context Protocol](https://modelcontextprotocol.io) server built with [FastMCP](https://github.com/jlowin/fastmcp). It exposes the [ResQ platform](https://resq.software) — Digital Twin Simulations (DTSOP), Hybrid Coordination Engine (HCE), and real-time drone telemetry — as structured tools, resources, and prompts that AI clients (Claude Desktop, Cursor, MCP Inspector) can call directly.

**Related projects:**

| Repo | Description |
|------|-------------|
| [resq-software/resQ](https://github.com/resq-software/resQ) | Core platform monorepo |
| [resq-software/cli](https://github.com/resq-software/cli) | CLI tooling |
| [resq-software/dotnet-sdk](https://github.com/resq-software/dotnet-sdk) | .NET SDK |

---

## Features

- **Tools** — trigger simulations, fetch deployment strategies, validate incidents
- **Resources** — real-time drone status (`resq://drones/active`), simulation monitoring (`resq://simulations/{id}`)
- **Prompts** — standardised incident response analysis templates
- **Async notifications** — subscription support for long-running simulation jobs
- **Dual transport** — STDIO (Claude Desktop / MCP Inspector) and SSE / HTTP (networked clients)
- **Pydantic validation** — all inputs fully typed and validated

---

## Install

### PyPI

```sh
uv add resq-mcp
# or: pip install resq-mcp
```

### From source

```sh
git clone https://github.com/resq-software/mcp.git
cd mcp
uv sync
```

### Docker

```sh
docker build -t resq-mcp .
docker run -p 8000:8000 resq-mcp
```

### Dev environment (Nix)

```sh
nix develop        # Python 3.12, uv
# or:
./scripts/setup.sh # installs Nix + Docker; runs uv sync
```

---

## Quick Start

**STDIO** (Claude Desktop, MCP Inspector):

```sh
uv run resq-mcp
# or after install:
resq-mcp
```

**SSE / HTTP** (networked clients, port 8000):

```sh
RESQ_HOST=0.0.0.0 RESQ_PORT=8000 uv run resq-mcp
```

Add to Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "resq": {
      "command": "uv",
      "args": ["run", "resq-mcp"],
      "env": { "RESQ_API_KEY": "your-key" }
    }
  }
}
```

---

## Usage

### Trigger a simulation

```
Tool: trigger_simulation
Args: { "incident_type": "wildfire", "location": { "lat": 37.77, "lon": -122.41 } }
```

### Get active drone status

```
Resource: resq://drones/active
```

### Incident response prompt

```
Prompt: incident_response_analysis
Args: { "incident_id": "INC-2026-0042" }
```

Full API reference: [`src/resq_mcp/`](./src/resq_mcp/)

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `RESQ_API_KEY` | `resq-dev-token` | Bearer token for authenticated endpoints |
| `RESQ_SAFE_MODE` | `true` | Disables side-effecting tools in safe mode |
| `RESQ_HOST` | `127.0.0.1` | Host to bind (SSE transport) |
| `RESQ_PORT` | `8000` | Port to listen on (SSE transport) |
| `RESQ_DEBUG` | `false` | Enable debug logging |
| `RESQ_PROJECT_NAME` | `resQ MCP` | Display name reported to MCP clients |

Copy `.env.example` to `.env` and override as needed. All settings are validated via Pydantic on startup.

---

## Contributing

We welcome contributions. Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) before opening a PR.

**Local setup:**

```sh
git clone https://github.com/resq-software/mcp.git
cd mcp
./scripts/setup.sh   # installs Nix + Docker; runs uv sync
```

**Run tests:**

```sh
uv run pytest
```

**Lint and type-check:**

```sh
uv run ruff check .
uv run mypy src/
```

**Commit convention:** This project uses [Conventional Commits](https://www.conventionalcommits.org/).
All PRs must follow the `type(scope): subject` format — see the table below.

| Prefix | Effect on version |
|--------|------------------|
| `feat:` | Minor bump (`0.x.0`) |
| `fix:` / `perf:` | Patch bump (`0.0.x`) |
| `BREAKING CHANGE` footer or `!` suffix | Major bump (`x.0.0`) |
| `docs:` `style:` `refactor:` `test:` `chore:` | No version bump |

Releases are automated via [python-semantic-release](https://python-semantic-release.readthedocs.io/) on merge to `main`.

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the full release history.

---

## License

Copyright 2026 ResQ

Licensed under the [Apache License, Version 2.0](./LICENSE).
