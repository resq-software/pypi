# resq-agent

LangGraph incident-response agent that **consumes** [resq-mcp](../resq-mcp) tools.

MCP is the tool-provider side. This package is the tool-consumer side: it
decides *when* to call validate / strategy / simulate / deploy, and it pauses
for a human before anything Safe Mode would block.

## Setup

```bash
cd packages/resq-agent
uv sync
```

## Milestone 1 — list tools

```bash
uv run resq-agent list-tools
```

Spawns `uv run resq-mcp` from `packages/resq-mcp` with `RESQ_SAFE_MODE=true`.

## Milestone 2 — linear graph (no mutations)

```
assess → validate_incident → get_deployment_strategy
```

The graph **is** the control flow. It does not ask an LLM which tool to call.
Rejected incidents stop after validate and never request a strategy.

```bash
uv run resq-agent run --incident-id INC-DEMO-1 --sector-id Sector-1
uv run resq-agent run --incident-id INC-DEMO-1 --reject
```

## Later milestones

1. `run_simulation` + poll `resq://simulations/{id}` until complete
2. LangGraph interrupt before `update_mission_params` (the Safe Mode gate)
3. Optional model-provider extras (`openai` / `anthropic`)

## Tests

```bash
uv run pytest
uv run ruff check src/ tests/
uv run mypy src/
```

CI uses fake MCP tools so it does not spawn the server or need API keys.
