---
name: test
description: Run the pytest suite with async support.
---

# /test

Run tests for the ResQ MCP server.

## Usage

```
/test [filter]
```

## Steps

1. Run `uv run pytest` (or `uv run pytest -k <filter>` if given).
2. Report failures with test file, function, and assertion message.
3. Report coverage summary — target is ≥ 80% for `src/resq_mcp/`.
4. If `pytest-asyncio` mode is not set to `auto`, remind to add `asyncio_mode = "auto"` to `pyproject.toml`.
