---
name: lint
description: Run ruff and mypy for linting and type checking.
---

# /lint

Lint and type-check the ResQ MCP server.

## Steps

1. Run `uv run ruff check .` — report all violations.
2. Run `uv run ruff format --check .` — report formatting issues.
3. Run `uv run mypy src/` — report all type errors.
4. All three must pass with zero errors before a PR can merge.
