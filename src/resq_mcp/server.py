# Copyright 2026 ResQ
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ResQ MCP Server - Model Context Protocol server for disaster response coordination.

This module provides the main FastMCP server implementation for ResQ, offering:
- Simulation management via resources and tools
- Drone fleet status and deployment
- Incident validation and response planning

The server uses a lifespan context manager to manage background tasks for
simulation processing and notification delivery.
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here
# because FastMCP/Pydantic needs to resolve the type annotations at runtime
# for tool parameter validation. Using PEP 563 postponed annotations causes
# NameError when FastMCP tries to evaluate the forward references.

import asyncio
import contextlib
import logging
import time
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from fastmcp import FastMCP

from resq_mcp.core.config import settings, validate_environment
from resq_mcp.core.telemetry import setup_telemetry

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

# Setup Logging
logging.basicConfig(level=logging.INFO if not settings.DEBUG else logging.DEBUG)
logger = logging.getLogger("resq-mcp")

# Initialize Telemetry
setup_telemetry()

# --- Capacity & TTL limits ---
MAX_SIMULATIONS: int = 500
COMPLETED_TTL_SECONDS: int = 300  # evict completed sims after 5 minutes

# --- Mock Data Store ---
simulations: "dict[str, dict[str, Any]]" = {}
incidents: "dict[str, dict[str, Any]]" = {}

# Keep strong references to per-simulation tasks so they aren't garbage-collected
# before completion (required by asyncio task semantics per RUF006).
_sim_tasks: "set[asyncio.Task[None]]" = set()

# Track which sim_ids currently have an active completion task so the poll loop
# can recover orphaned "processing" sims (e.g. created directly in tests or if
# a hypothetical partial-state reload leaves sims in "processing" without tasks).
_active_processing: "set[str]" = set()


@asynccontextmanager
async def lifespan(server: FastMCP) -> "AsyncGenerator[None, None]":
    """Lifespan context manager for the MCP server with background tasks.

    Manages the lifecycle of background processing tasks that run for the
    duration of the server. Ensures clean startup and shutdown with proper
    task cancellation and resource cleanup.

    Background Tasks Started:
        - simulation_processor: Mock simulation state machine that transitions
          simulations from pending -> processing -> completed and sends SSE
          notifications to subscribed clients.

    Lifecycle:
        1. Startup: Log initialization, create background tasks
        2. Running: Yield control to FastMCP server
        3. Shutdown: Cancel tasks, suppress CancelledError, log shutdown

    Args:
        server: The FastMCP server instance for notification dispatch.

    Yields:
        None: Control returns to FastMCP for request handling.

    Note:
        In production, background tasks would interface with actual
        simulation clusters, message queues (Redis/RabbitMQ), and
        maintain persistent connections to drone telemetry streams.
    """
    logger.info("Starting resQ MCP Server...")
    task = asyncio.create_task(simulation_processor(server))
    yield
    logger.info("Shutting down resQ MCP Server...")
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task


# Initialize FastMCP
mcp = FastMCP(
    settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)


# --- Background Tasks ---


def _cleanup_old_simulations() -> None:
    """Evict completed simulations older than COMPLETED_TTL_SECONDS.

    Prevents unbounded memory growth in the simulations store by removing
    entries that are both completed and past their TTL.
    """
    now = time.monotonic()
    to_delete = [
        sid
        for sid, data in list(simulations.items())
        if data.get("status") == "completed"
        and now - data.get("completed_at", now) > COMPLETED_TTL_SECONDS
    ]
    for sid in to_delete:
        del simulations[sid]
        logger.debug("Evicted completed simulation %s", sid)


async def _process_simulation(server: FastMCP, sim_id: str, data: "dict[str, Any]") -> None:
    """Async task: complete one simulation after a processing delay.

    Runs concurrently per simulation so the main poll loop is never blocked
    by a single job's 3-second processing window (fixes the sequential-sleep DoS).

    State Machine:
        processing -> completed (after 3 s)
        processing -> failed    (on CancelledError, e.g. server shutdown mid-run)
    """
    _active_processing.add(sim_id)
    try:
        await asyncio.sleep(3)
        # Guard: entry may have been evicted if server restarted or was flushed
        if simulations.get(sim_id) is not data:
            return
        data["status"] = "completed"
        data["progress"] = 1.0
        data["result_url"] = f"neofs://sim_results/{sim_id}.json"
        data["completed_at"] = time.monotonic()
        logger.info("Simulation %s COMPLETED", sim_id)
        try:
            await server.notify_resource_updated(f"resq://simulations/{sim_id}")  # type: ignore[attr-defined]
        except Exception:
            logger.debug("Failed to notify for %s", sim_id, exc_info=True)
    except asyncio.CancelledError:
        # Mark failed so clients don't poll forever on a zombie entry
        if simulations.get(sim_id) is data:
            data["status"] = "failed"
        raise
    finally:
        _active_processing.discard(sim_id)


async def simulation_processor(server: FastMCP) -> None:
    """Background processor for simulation state transitions and notifications.

    Polls for pending simulations every 2 s and spawns an independent async
    task per simulation so that no single job's delay blocks the others.

    State Machine:
        pending    -> processing (immediate, 50% progress, task spawned)
        processing -> completed  (after 3 s inside _process_simulation)
        processing -> failed     (on server shutdown mid-run)

    Notifications:
        SSE resource update notifications are sent on each state transition.

    Note:
        Production would replace this with a real job queue integration
        (Celery / RQ) and Unity/Unreal Engine status polling.
    """
    while True:
        await asyncio.sleep(2)
        _cleanup_old_simulations()
        for sim_id, data in list(simulations.items()):
            if data["status"] == "pending":
                data["status"] = "processing"
                data["progress"] = 0.5
                logger.info("Simulation %s moved to PROCESSING", sim_id)
                task = asyncio.create_task(_process_simulation(server, sim_id, data))
                _sim_tasks.add(task)
                task.add_done_callback(_sim_tasks.discard)
                try:
                    await server.notify_resource_updated(f"resq://simulations/{sim_id}")  # type: ignore[attr-defined]
                except Exception:
                    logger.debug("Failed to notify for %s", sim_id, exc_info=True)
            elif data["status"] == "processing" and sim_id not in _active_processing:
                # Orphan recovery: a sim is in "processing" with no active task
                # (e.g. created directly in tests or after partial-state replay).
                logger.debug("Recovering orphaned processing simulation %s", sim_id)
                task = asyncio.create_task(_process_simulation(server, sim_id, data))
                _sim_tasks.add(task)
                task.add_done_callback(_sim_tasks.discard)


# Register tools, resources, and prompts
import resq_mcp.dtsop.tools  # noqa: E402
import resq_mcp.hce.tools  # noqa: E402
import resq_mcp.prompts  # noqa: E402
import resq_mcp.resources  # noqa: F401, E402


def main() -> None:
    """Console script entry point for the ResQ MCP server."""
    validate_environment()
    mcp.run()


if __name__ == "__main__":
    main()
