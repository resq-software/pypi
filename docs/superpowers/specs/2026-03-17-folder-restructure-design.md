# Folder Restructure: Flat to Domain-Organized

**Date:** 2026-03-17
**Status:** Approved
**Approach:** Full domain packages with core/ for cross-cutting concerns

---

## Overview

Restructure resq-mcp from 13 flat source files to domain-organized packages.
Each subsystem (DTSOP, HCE, PDIE, Drone) becomes a self-contained package
with its own models, service logic, and MCP tool registrations. Cross-cutting
concerns move to `core/`. Tests reorganize into unit/integration/property.

Pure refactoring — no behavior changes. Public API stays identical.

---

## Source Layout

```
src/resq_mcp/
├── __init__.py            # Public API re-exports (preserved)
├── __main__.py            # python -m entry point (unchanged)
├── py.typed               # PEP 561 marker (unchanged)
├── server.py              # FastMCP init, lifespan, background tasks, simulations dict
│                          # Bottom-of-file imports trigger tool/resource/prompt registration
├── resources.py           # @mcp.resource(): simulation status, active drones
├── prompts.py             # @mcp.prompt(): incident_response_plan
├── core/
│   ├── __init__.py        # Re-exports: settings, MCPErrorFormatter, verify_api_key, etc.
│   ├── config.py          # Settings, validate_environment, ConfigurationError
│   ├── errors.py          # MCPErrorFormatter
│   ├── models.py          # Shared: Coordinates, Sector, ErrorResponse, DetectedObject,
│   │                      # DisasterScenario, _utc_now()
│   ├── security.py        # verify_api_key, security_scheme
│   ├── telemetry.py       # setup_telemetry, trace
│   └── timeout.py         # TimeoutConfig, get_default_timeout, get_polling_interval
├── drone/
│   ├── __init__.py
│   ├── models.py          # SectorAnalysis, SectorStatusSummary, NetworkStatus,
│   │                      # SwarmStatus, DeploymentRequest, DeploymentStatus
│   └── service.py         # scan_current_sector, get_all_sectors_status,
│                          # get_drone_swarm_status, request_drone_deployment
│                          # Plus: DRONE_SECTORS, DISASTER_SCENARIOS constants
├── dtsop/
│   ├── __init__.py
│   ├── models.py          # SimulationRequest, OptimizationStrategy
│   ├── service.py         # run_simulation, get_optimization_strategy
│   │                      # Plus: _STRATEGY_TEMPLATES constant
│   └── tools.py           # @mcp.tool(): run_simulation, get_deployment_strategy
├── hce/
│   ├── __init__.py
│   ├── models.py          # IncidentReport, IncidentValidation, MissionParameters
│   ├── service.py         # validate_incident, update_mission_params
│   │                      # Plus: _AUTO_CONFIRM_THRESHOLD constant
│   └── tools.py           # @mcp.tool(): validate_incident
└── pdie/
    ├── __init__.py
    ├── models.py          # VulnerabilityMap, PreAlert
    └── service.py         # get_vulnerability_map, get_predictive_alerts
                           # Plus: VULNERABILITY_DB, threshold constants
```

### Import Chain (no circular deps)

```
core/models.py  ← drone/models.py, hce/models.py, etc.
core/config.py  ← server.py
server.py       → creates mcp, then bottom-of-file imports:
                  dtsop/tools.py, hce/tools.py, resources.py, prompts.py
dtsop/tools.py  → imports mcp from server, imports from dtsop/service.py
```

### server.py Responsibilities (slimmed)

- `mcp = FastMCP(...)` initialization
- `lifespan()` context manager
- `simulation_processor()` background task
- `simulations` dict (global state)
- Bottom-of-file: `import resq_mcp.resources`, `import resq_mcp.prompts`,
  `import resq_mcp.dtsop.tools`, `import resq_mcp.hce.tools`

### Tool Registration Pattern

Each domain `tools.py` imports `mcp` from `server` and registers tools:

```python
# dtsop/tools.py
from resq_mcp.server import mcp
from .service import run_simulation as trigger_sim, get_optimization_strategy

@mcp.tool()
async def run_simulation(request: SimulationRequest, ctx: Context | None = None) -> str:
    ...
```

---

## Test Layout

```
tests/
├── conftest.py                # Shared: factory fixtures, reset_random_seed
├── unit/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── test_config.py
│   │   ├── test_errors.py
│   │   ├── test_security.py
│   │   ├── test_telemetry.py
│   │   └── test_timeout.py
│   ├── test_server.py         # Background processor, simulation status
│   ├── test_resources.py      # list_active_drones
│   ├── test_prompts.py        # incident_response_plan
│   ├── test_drone.py          # scan, swarm, deployment + edge cases
│   ├── test_dtsop.py          # simulation, strategy + edge cases
│   ├── test_hce.py            # validate, mission params + edge cases + validate_incident tool
│   └── test_pdie.py           # vulnerability, alerts + edge cases
├── integration/
│   ├── __init__.py
│   └── test_flows.py          # 3 cross-module flows
└── property/
    ├── __init__.py
    ├── test_models.py          # Hypothesis: Coordinates, DeploymentRequest, IncidentReport
    └── test_probabilistic.py   # Detection rate, ETA, battery, drone ID stats
```

### Test merges

- `test_validate_incident.py` merges into `unit/test_hce.py`
- `test_tools.py` probabilistic tests → `property/test_probabilistic.py`
- `test_tools.py` unit tests → `unit/test_drone.py`
- `test_models.py` hypothesis tests → `property/test_models.py`
- `test_models.py` unit tests stay in a new `unit/test_models.py` or distribute into domain test files
- `test_server.py` resource tests → `unit/test_resources.py`
- `test_server.py` prompt tests → `unit/test_prompts.py`

---

## Migration Strategy

Pure refactoring. No behavior changes. Each step is a commit.

1. Create directory structure and `__init__.py` files
2. Split `models.py` → `core/models.py` + domain `models.py` files
3. Move cross-cutting modules → `core/` (config, errors, security, telemetry, timeout)
4. Move domain logic → domain `service.py` files (dtsop, hce, pdie, drone)
5. Split `server.py` → `server.py` + `resources.py` + `prompts.py`
6. Create domain `tools.py` files with @mcp.tool() registrations
7. Update `__init__.py` re-exports to preserve public API
8. Reorganize tests into `unit/`, `integration/`, `property/`
9. Update all imports across test files
10. Update `pyproject.toml`, `CLAUDE.md`, `AGENTS.md`
11. Run full suite: lint + mypy + 148 tests + coverage gate

### Files Changed

| Current File | Destination |
|---|---|
| `config.py` | `core/config.py` |
| `errors.py` | `core/errors.py` |
| `security.py` | `core/security.py` |
| `telemetry.py` | `core/telemetry.py` |
| `timeout.py` | `core/timeout.py` |
| `models.py` | Split → `core/models.py` + `drone/models.py` + `dtsop/models.py` + `hce/models.py` + `pdie/models.py` |
| `tools.py` | `drone/service.py` |
| `dtsop.py` | `dtsop/service.py` |
| `hce.py` | `hce/service.py` |
| `pdie.py` | `pdie/service.py` |
| `server.py` | Split → `server.py` + `resources.py` + `prompts.py` + `dtsop/tools.py` + `hce/tools.py` |
