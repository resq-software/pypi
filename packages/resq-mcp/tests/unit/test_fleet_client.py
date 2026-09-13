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

"""HTTP-backend tests for the drone fleet service.

These tests point ``RESQ_FLEET_API_URL`` at a loopback aiohttp server that
stands in for fleet-api. They never talk to a real fleet-api process.

aioresponses is a project dependency but is currently incompatible with aiohttp
3.14 (ClientResponse requires ``stream_writer``). A loopback server exercises
the same ClientSession path without depending on that mock's internals.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

import pytest
from aiohttp import web

from resq_mcp.core.config import settings
from resq_mcp.core.models import ErrorResponse
from resq_mcp.core.timeout import TimeoutConfig
from resq_mcp.drone.client import stop_fleet_session
from resq_mcp.drone.models import DeploymentStatus, DroneUnit, SwarmStatus
from resq_mcp.drone.service import (
    get_drone_swarm_status,
    get_fleet_roster,
    request_drone_deployment,
)

RouteHandler = Callable[[web.Request], Awaitable[web.StreamResponse]]


@asynccontextmanager
async def _serve(routes: dict[tuple[str, str], RouteHandler]) -> AsyncIterator[str]:
    """Bind a loopback fleet-api stand-in and yield its origin URL."""
    app = web.Application()
    for (method, path), handler in routes.items():
        app.router.add_route(method, path, handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    server = site._server
    assert server is not None
    sockets = getattr(server, "sockets", None)
    assert sockets
    port: int = sockets[0].getsockname()[1]
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        await runner.cleanup()


@pytest.fixture
async def _close_session() -> AsyncIterator[None]:
    """Guarantee the shared ClientSession does not leak between cases."""
    try:
        yield
    finally:
        await stop_fleet_session()


def _status_payload(**overrides: Any) -> dict[str, Any]:
    """Build a fleet-api ``GET /fleet/status`` body."""
    payload: dict[str, Any] = {
        "total_drones": 3,
        "active_drones": 2,
        "average_battery": 77,
        "network_status": "operational",
        "timestamp": "2026-09-13T00:00:00+00:00",
    }
    payload.update(overrides)
    return payload


def _roster_payload() -> list[dict[str, Any]]:
    """Build a fleet-api ``GET /drones`` body."""
    return [
        {
            "drone_id": "DRONE-Alpha",
            "role": "Surveillance",
            "home_sector": "Sector-4",
            "battery_percent": 78,
            "is_active": True,
        },
        {
            "drone_id": "DRONE-Beta",
            "role": "Payload",
            "home_sector": "Sector-2",
            "battery_percent": 64,
            "is_active": True,
        },
    ]


def _deployment_payload(**overrides: Any) -> dict[str, Any]:
    """Build a fleet-api ``POST /deployments`` body."""
    payload: dict[str, Any] = {
        "deployment_id": "DEP-ABCDEF12",
        "drone_id": "DRONE-Alpha",
        "sector_id": "Sector-2",
        "priority": "high",
        "status": "deployed",
        "eta_seconds": 30,
        "created_at": "2026-09-13T00:00:00+00:00",
    }
    payload.update(overrides)
    return payload


@pytest.mark.usefixtures("_close_session")
class TestFetchSwarmStatusHttp:
    """``get_drone_swarm_status`` against a loopback fleet-api."""

    async def test_maps_fleet_status_onto_swarm_status(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A 200 from ``/fleet/status`` becomes a SwarmStatus with the same figures."""

        async def status(_request: web.Request) -> web.Response:
            return web.json_response(_status_payload())

        async with _serve({("GET", "/fleet/status"): status}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await get_drone_swarm_status()

        assert isinstance(result, SwarmStatus)
        assert result.total_drones == 3
        assert result.active_drones == 2
        assert result.average_battery == 77
        assert result.network_status == "operational"

    async def test_timeout_returns_error_response(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A hung fleet-api must not crash the MCP tool — it becomes ErrorResponse."""

        async def hang(_request: web.Request) -> web.Response:
            await asyncio.sleep(5)
            return web.json_response(_status_payload())

        monkeypatch.setattr(
            "resq_mcp.drone.client.get_default_timeout",
            lambda: TimeoutConfig(total=0.05, connect=0.05, read=0.05),
        )
        async with _serve({("GET", "/fleet/status"): hang}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await get_drone_swarm_status()

        assert isinstance(result, ErrorResponse)
        assert "timed out" in result.message.lower()

    async def test_connection_error_returns_error_response(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A down fleet-api is reported as unreachable, not a stack trace."""
        monkeypatch.setattr(settings, "FLEET_API_URL", "http://127.0.0.1:1")
        result = await get_drone_swarm_status()

        assert isinstance(result, ErrorResponse)
        assert "unreachable" in result.message.lower()


@pytest.mark.usefixtures("_close_session")
class TestFetchRosterHttp:
    """``get_fleet_roster`` against a loopback fleet-api."""

    async def test_maps_drone_list_and_ignores_telemetry_fields(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """``battery_percent`` is fleet-api telemetry; MCP DroneUnit drops it."""

        async def drones(_request: web.Request) -> web.Response:
            return web.json_response(_roster_payload())

        async with _serve({("GET", "/drones"): drones}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await get_fleet_roster()

        assert not isinstance(result, ErrorResponse)
        assert [unit.drone_id for unit in result] == ["DRONE-Alpha", "DRONE-Beta"]
        assert all(isinstance(unit, DroneUnit) for unit in result)
        assert not hasattr(result[0], "battery_percent")

    async def test_http_error_returns_error_response(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A 500 from fleet-api becomes ErrorResponse for the tool layer to raise."""

        async def boom(_request: web.Request) -> web.Response:
            return web.json_response({"detail": "store unavailable"}, status=500)

        async with _serve({("GET", "/drones"): boom}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await get_fleet_roster()

        assert isinstance(result, ErrorResponse)
        assert "store unavailable" in result.message


@pytest.mark.usefixtures("_close_session")
class TestCreateDeploymentHttp:
    """``request_drone_deployment`` against a loopback fleet-api."""

    async def test_assigns_the_drone_id_fleet_api_returned(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Regression: dispatch must not invent UNIT- ids the fleet has never heard of."""

        async def deploy(request: web.Request) -> web.Response:
            body = await request.json()
            return web.json_response(
                _deployment_payload(
                    drone_id="DRONE-Beta",
                    sector_id=body["sector_id"],
                    priority=body["priority"],
                ),
                status=201,
            )

        async with _serve({("POST", "/deployments"): deploy}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await request_drone_deployment("Sector-2", priority="high")

        assert isinstance(result, DeploymentStatus)
        assert result.drone_id == "DRONE-Beta"
        assert result.sector_id == "Sector-2"
        assert result.eta_seconds == 30

    async def test_unknown_sector_is_404(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """fleet-api 404 (unmonitored sector) maps onto ErrorResponse."""

        async def missing(_request: web.Request) -> web.Response:
            return web.json_response(
                {"detail": "Sector Sector-9 is not monitored. Known sectors: Sector-1"},
                status=404,
            )

        async with _serve({("POST", "/deployments"): missing}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await request_drone_deployment("Sector-9")

        assert isinstance(result, ErrorResponse)
        assert "not monitored" in result.message

    async def test_no_eligible_drone_is_409(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """fleet-api 409 (valid request, no drone) is a distinct failure from 404."""

        async def conflict(_request: web.Request) -> web.Response:
            return web.json_response(
                {"detail": "No drone is available for dispatch"},
                status=409,
            )

        async with _serve({("POST", "/deployments"): conflict}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await request_drone_deployment("Sector-1")

        assert isinstance(result, ErrorResponse)
        assert "No drone is available" in result.message


@pytest.mark.usefixtures("_close_session")
class TestMalformedBodies:
    """fleet-api sending a body the client cannot parse must still yield ErrorResponse.

    These are the paths that matter when the upstream misbehaves rather than
    simply failing. A stack trace escaping here would reach the agent instead of
    an actionable message.
    """

    async def test_truncated_json_on_success_is_an_error_response(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A 200 labelled application/json over a truncated body must not raise.

        ``resp.json()`` raises JSONDecodeError here, which is a ValueError and
        NOT an aiohttp.ContentTypeError, so catching only the latter lets it
        escape ``_request_json``.
        """

        async def truncated(_request: web.Request) -> web.Response:
            return web.Response(body=b'{"total_drones": 3', content_type="application/json")

        async with _serve({("GET", "/fleet/status"): truncated}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await get_drone_swarm_status()

        assert isinstance(result, ErrorResponse)
        assert "non-JSON" in result.message

    async def test_error_status_with_non_json_body_uses_the_text(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A 502 carrying plain text still produces a message, not a crash.

        Exercises the fallback in ``_error_from_response`` that reads ``text()``
        when the body will not parse as JSON.
        """

        async def gateway(_request: web.Request) -> web.Response:
            return web.Response(text="upstream gateway failed", status=502)

        async with _serve({("GET", "/drones"): gateway}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await get_fleet_roster()

        assert isinstance(result, ErrorResponse)
        assert "upstream gateway failed" in result.message

    async def test_error_status_with_empty_body_falls_back_to_status(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """An error with no usable detail still names the status code."""

        async def empty(_request: web.Request) -> web.Response:
            return web.Response(status=503)

        async with _serve({("GET", "/drones"): empty}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await get_fleet_roster()

        assert isinstance(result, ErrorResponse)
        assert "503" in result.message

    async def test_schema_violation_becomes_an_error_response(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Well-formed JSON of the wrong shape is a validation failure, not a crash."""

        async def wrong_shape(_request: web.Request) -> web.Response:
            return web.json_response(_status_payload(total_drones="not-an-integer"))

        async with _serve({("GET", "/fleet/status"): wrong_shape}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await get_drone_swarm_status()

        assert isinstance(result, ErrorResponse)
        assert "invalid" in result.message.lower()

    async def test_roster_that_is_not_an_array_is_an_error_response(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """``/drones`` returning an object instead of a list is rejected by shape."""

        async def not_a_list(_request: web.Request) -> web.Response:
            return web.json_response({"drones": []})

        async with _serve({("GET", "/drones"): not_a_list}) as origin:
            monkeypatch.setattr(settings, "FLEET_API_URL", origin)
            result = await get_fleet_roster()

        assert isinstance(result, ErrorResponse)
        assert "non-array" in result.message
