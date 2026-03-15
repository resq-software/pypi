---
name: type-safety
description: Type safety and async rules for the ResQ MCP server codebase.
---

# Type Safety Rules

## Typing

- All functions must have complete type annotations — parameters and return types.
- `mypy` must pass with `strict = true` in `pyproject.toml`. No `# type: ignore` without an explanatory comment.
- No `Any` types in tool/resource/prompt signatures or Pydantic models.
- Use `TypeAlias` for complex repeated types.

## Pydantic

- Input models for tools use `model_config = ConfigDict(frozen=True, extra="forbid")`.
- Never use bare `dict` or `list` in tool signatures — always a named Pydantic model.
- Validate environment config via `pydantic-settings` `BaseSettings` — fail fast on startup if required vars are missing.

## Async

- All I/O must be `async` — never use `requests`, `open()`, `time.sleep()`, or any blocking stdlib call in a coroutine.
- Use `httpx.AsyncClient` for outbound HTTP.
- Use `asyncio.gather` for concurrent tasks, not `asyncio.wait` in a loop.
- Use `contextlib.asynccontextmanager` for async resource cleanup — never `finally` with awaited calls that might not run.

## No Sync I/O in Handlers

The MCP server runs in an async event loop. Blocking the loop stalls ALL tools, resources, and prompts for every connected client. This is treated as a critical bug.

## Security

- `RESQ_API_KEY` and any bearer tokens must not appear in log output, error messages, or Pydantic model `repr`.
- Mark secret fields with `model_config = ConfigDict(...)` and `Field(repr=False)`.
- Validate all user-supplied URLs against an allowlist before making outbound requests.
