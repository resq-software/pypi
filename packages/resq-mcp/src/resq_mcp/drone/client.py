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

"""HTTP client for the fleet-api service.

The MCP server is a *consumer* of fleet state. This module owns the aiohttp
session, maps HTTP status codes onto :class:`ErrorResponse`, and never invents
drone IDs — those come from the API.

A single :class:`aiohttp.ClientSession` is created at server startup and closed
on shutdown so TCP connections are reused. Tests that never run lifespan still
work: the first request lazily opens a session, and they should call
:func:`stop_fleet_session` in teardown.
"""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
from pydantic import ValidationError

from resq_mcp.core.models import ErrorResponse
from resq_mcp.core.timeout import get_default_timeout
from resq_mcp.drone.models import DeploymentStatus, DroneUnit, SwarmStatus

logger = logging.getLogger("resq-mcp")

_session: aiohttp.ClientSession | None = None


def _client_timeout() -> aiohttp.ClientTimeout:
    """Build an aiohttp timeout from the shared ResQ timeout config.

    Returns:
        aiohttp.ClientTimeout: Total, connect, and read budgets.
    """
    cfg = get_default_timeout()
    return aiohttp.ClientTimeout(
        total=cfg.total,
        connect=cfg.connect,
        sock_read=cfg.read,
    )


def _normalize_base_url(base_url: str) -> str:
    """Strip trailing slashes so path joins do not produce ``//``.

    Args:
        base_url: Configured fleet-api origin.

    Returns:
        str: Origin without a trailing slash.
    """
    return base_url.rstrip("/")


async def start_fleet_session() -> None:
    """Open the process-wide aiohttp session if it is not already open."""
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(timeout=_client_timeout())
        logger.debug("Opened fleet-api HTTP session")


async def stop_fleet_session() -> None:
    """Close the process-wide aiohttp session, if any."""
    global _session
    if _session is not None and not _session.closed:
        await _session.close()
        logger.debug("Closed fleet-api HTTP session")
    _session = None


async def _session_handle() -> aiohttp.ClientSession:
    """Return the shared session, creating it on first use.

    Returns:
        aiohttp.ClientSession: The process-wide session.
    """
    await start_fleet_session()
    if _session is None:  # pragma: no cover - start_fleet_session always sets it
        raise RuntimeError("fleet-api HTTP session failed to start")
    return _session


async def _error_from_response(resp: aiohttp.ClientResponse) -> ErrorResponse:
    """Turn a non-success HTTP response into an ErrorResponse.

    Args:
        resp: The fleet-api response.

    Returns:
        ErrorResponse: Message taken from FastAPI ``detail`` when present.
    """
    detail: str | None = None
    try:
        payload: Any = await resp.json()
except (aiohttp.ContentTypeError, ValueError):
        text = await resp.text()
        detail = text.strip() or None
    else:
        if isinstance(payload, dict):
            raw = payload.get("detail")
            if isinstance(raw, str) and raw:
                detail = raw

    if resp.status == 404:
        message = detail or "Fleet API resource not found"
    elif resp.status == 409:
        message = detail or "No drone is available for dispatch"
    else:
        message = detail or f"Fleet API returned HTTP {resp.status}"
    return ErrorResponse(message=message)


async def _request_json(
    method: str,
    base_url: str,
    path: str,
    *,
    json: dict[str, Any] | None = None,
) -> Any | ErrorResponse:
    """Perform a JSON HTTP request against fleet-api.

    Args:
        method: HTTP method (``GET`` or ``POST``).
        base_url: fleet-api origin.
        path: Path beginning with ``/``.
        json: Optional JSON body for POST.

    Returns:
        Any | ErrorResponse: Parsed JSON on 2xx, or an error for HTTP / network
        failures. Callers validate the JSON against a Pydantic model.
    """
    url = f"{_normalize_base_url(base_url)}{path}"
    session = await _session_handle()
    try:
        async with session.request(method, url, json=json) as resp:
            if resp.status >= 400:
                return await _error_from_response(resp)
            try:
                return await resp.json()
            except aiohttp.ContentTypeError:
                return ErrorResponse(message="Fleet API returned a non-JSON body")
    except TimeoutError:
        logger.warning("Fleet API timed out: %s %s", method, url)
        return ErrorResponse(message="Fleet API timed out")
    except aiohttp.ClientError as exc:
        logger.warning("Fleet API unreachable: %s %s (%s)", method, url, exc)
        return ErrorResponse(message=f"Fleet API unreachable: {exc}")


async def fetch_swarm_status(base_url: str) -> SwarmStatus | ErrorResponse:
    """GET /fleet/status and map it onto :class:`SwarmStatus`.

    Args:
        base_url: fleet-api origin.

    Returns:
        SwarmStatus | ErrorResponse: Live aggregates, or an error if the
        request or payload is unusable.
    """
    payload = await _request_json("GET", base_url, "/fleet/status")
    if isinstance(payload, ErrorResponse):
        return payload
    if not isinstance(payload, dict):
        return ErrorResponse(message="Fleet API /fleet/status returned a non-object body")
    try:
        fields: dict[str, Any] = {
            "total_drones": payload.get("total_drones"),
            "active_drones": payload.get("active_drones"),
            "average_battery": payload.get("average_battery"),
            "network_status": payload.get("network_status"),
        }
        if payload.get("timestamp") is not None:
            fields["last_sync"] = payload["timestamp"]
        return SwarmStatus.model_validate(fields)
    except ValidationError as exc:
        logger.warning("Fleet API /fleet/status failed validation: %s", exc)
        return ErrorResponse(message="Fleet API /fleet/status payload was invalid")


async def fetch_fleet_roster(base_url: str) -> tuple[DroneUnit, ...] | ErrorResponse:
    """GET /drones and map each row onto :class:`DroneUnit`.

    Extra fields such as ``battery_percent`` are ignored so the MCP model can
    stay a composition record rather than a telemetry sample.

    Args:
        base_url: fleet-api origin.

    Returns:
        tuple[DroneUnit, ...] | ErrorResponse: The roster, or an error.
    """
    payload = await _request_json("GET", base_url, "/drones")
    if isinstance(payload, ErrorResponse):
        return payload
    if not isinstance(payload, list):
        return ErrorResponse(message="Fleet API /drones returned a non-array body")
    try:
        return tuple(DroneUnit.model_validate(item) for item in payload)
    except ValidationError as exc:
        logger.warning("Fleet API /drones failed validation: %s", exc)
        return ErrorResponse(message="Fleet API /drones payload was invalid")


async def create_deployment(
    base_url: str,
    sector_id: str,
    priority: str,
) -> DeploymentStatus | ErrorResponse:
    """POST /deployments and map the 201 body onto :class:`DeploymentStatus`.

    Args:
        base_url: fleet-api origin.
        sector_id: Target sector.
        priority: Mission urgency as accepted by fleet-api.

    Returns:
        DeploymentStatus | ErrorResponse: The dispatch record, or an error
        (404 unknown sector, 409 no eligible drone, network failure).
    """
    payload = await _request_json(
        "POST",
        base_url,
        "/deployments",
        json={"sector_id": sector_id, "priority": priority},
    )
    if isinstance(payload, ErrorResponse):
        return payload
    if not isinstance(payload, dict):
        return ErrorResponse(message="Fleet API /deployments returned a non-object body")
    try:
        fields: dict[str, Any] = {
            "status": payload.get("status"),
            "sector_id": payload.get("sector_id"),
            "priority": payload.get("priority"),
            "drone_id": payload.get("drone_id"),
            "eta_seconds": payload.get("eta_seconds"),
        }
        if payload.get("created_at") is not None:
            fields["timestamp"] = payload["created_at"]
        return DeploymentStatus.model_validate(fields)
    except ValidationError as exc:
        logger.warning("Fleet API /deployments failed validation: %s", exc)
        return ErrorResponse(message="Fleet API /deployments payload was invalid")
