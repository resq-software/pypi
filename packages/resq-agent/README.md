# resq-agent

LangGraph incident-response agent that **consumes** [resq-mcp](../resq-mcp) tools.

MCP is the tool-provider side. This package is the tool-consumer side: it
decides *when* to call validate / strategy / simulate / deploy, and it pauses
for a human before anything Safe Mode would block.

## Milestone 1 (this PR)

Connect to a running `resq-mcp` over stdio and list its tools. No LLM yet.

```bash
cd packages/resq-agent
uv sync
uv run resq-agent list-tools
```

That spawns `uv run resq-mcp` from `packages/resq-mcp` with `RESQ_SAFE_MODE=true`.

## Later milestones

1. Linear graph: assess → `validate_incident` → `get_deployment_strategy`
2. `run_simulation` + poll `resq://simulations/{id}` until complete
3. LangGraph interrupt before `update_mission_params` (the Safe Mode gate)
4. README example with a real model provider (`openai` / `anthropic` extras)

## Tests

```bash
uv run pytest
uv run ruff check src/ tests/
uv run mypy src/
```

Tool listing is tested with a fake MCP client so CI does not spawn the server
or need API keys.
