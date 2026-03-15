---
name: mcp-protocol
description: MCP protocol compliance rules for the ResQ MCP server.
---

# MCP Protocol Rules

## Tools

- Tool names are `snake_case`.
- Every tool has a clear, one-sentence `description` that an LLM can use to decide when to call it.
- Input schema is derived from a Pydantic model — never a raw `dict`.
- Tools return `list[TextContent | ImageContent | EmbeddedResource]`. Never return raw strings or dicts directly.
- Side-effecting tools (those that mutate state or trigger real actions) must check `RESQ_SAFE_MODE` and raise `McpError` if enabled.

## Resources

- Resource URIs follow the `resq://` scheme.
- Static resources use `@mcp.resource("resq://path/to/resource")`.
- Dynamic resources use URI templates: `@mcp.resource("resq://simulations/{id}")`.
- Resource handlers return `str` (text) or `bytes` (binary).

## Prompts

- Prompt names are `snake_case`.
- Prompts return `GetPromptResult` with a `messages` list.
- Prompt arguments are typed — use `PromptArgument` with `required=True/False`.

## Error Handling

- Protocol errors (bad input, resource not found): raise `McpError` with an appropriate `ErrorCode`.
- Internal errors (API timeout, parsing failure): log the internal error, raise `McpError` with `INTERNAL_ERROR` code and a user-safe message (no stack traces, no secrets).

## Versioning

- The server version string in `pyproject.toml` drives `python-semantic-release`.
- Never manually edit the version — it is set by CI on merge to `main`.
