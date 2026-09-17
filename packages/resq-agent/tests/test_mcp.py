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

"""Tests for the resq-mcp client wrapper."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest

from resq_agent.mcp import default_mcp_connection, list_resq_tools, resq_mcp_dir


class _FakeClient:
    """Stand-in for MultiServerMCPClient that never opens a subprocess."""

    def __init__(self, names: list[str]) -> None:
        self._names = names

    async def get_tools(self) -> list[Any]:
        """Return objects that only need a ``name`` attribute."""
        return [SimpleNamespace(name=name) for name in self._names]


def test_resq_mcp_dir_points_at_the_sibling_package() -> None:
    """The stdio spawn must run the real resq-mcp package, not a copy of it."""
    path = resq_mcp_dir()
    assert path.name == "resq-mcp"
    assert (path / "pyproject.toml").is_file()


def test_default_connection_uses_stdio_and_safe_mode() -> None:
    """Mutations stay blocked until a later HITL node turns Safe Mode off."""
    conn = default_mcp_connection()
    assert conn["transport"] == "stdio"
    assert conn["command"] == "uv"
    assert conn["args"][0] == "run"
    assert conn["env"]["RESQ_SAFE_MODE"] == "true"


def test_ambient_safe_mode_false_does_not_reach_the_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An exported RESQ_SAFE_MODE=false must not disarm the spawned server.

    The connection copies os.environ, so a caller who happens to have the gate
    disabled in their own shell would otherwise hand that straight to the
    child process. The safe default has to win over the ambient value.
    """
    monkeypatch.setenv("RESQ_SAFE_MODE", "false")
    conn = default_mcp_connection()
    assert conn["env"]["RESQ_SAFE_MODE"] == "true"


def test_safe_mode_can_be_disabled_only_explicitly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Turning the gate off is an argument, not an environment variable."""
    monkeypatch.setenv("RESQ_SAFE_MODE", "true")
    conn = default_mcp_connection(safe_mode=False)
    assert conn["env"]["RESQ_SAFE_MODE"] == "false"


async def test_list_resq_tools_returns_sorted_names() -> None:
    """Names come from the MCP client, sorted so the CLI output is stable."""
    client = _FakeClient(["run_simulation", "validate_incident", "get_deployment_strategy"])
    names = await list_resq_tools(client)  # type: ignore[arg-type]
    assert names == [
        "get_deployment_strategy",
        "run_simulation",
        "validate_incident",
    ]


async def test_load_tool_map_keys_tools_by_name() -> None:
    """The graph looks up tools by name, so the map must use tool.name as keys."""
    from resq_agent.mcp import load_tool_map

    client = _FakeClient(["validate_incident", "get_deployment_strategy"])
    tools = await load_tool_map(client)  # type: ignore[arg-type]
    assert set(tools) == {"validate_incident", "get_deployment_strategy"}


async def test_list_resq_tools_constructs_a_client_when_none_is_passed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Omitting the client still goes through MultiServerMCPClient."""
    fake = _FakeClient(["scan_current_sector"])
    monkeypatch.setattr("resq_agent.mcp.mcp_client", lambda: fake)
    names = await list_resq_tools()
    assert names == ["scan_current_sector"]


async def test_mcp_client_wraps_the_default_connection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """mcp_client() must pass the stdio connection through, not a hardcoded URL."""
    captured: dict[str, Any] = {}

    class _Recorder:
        def __init__(self, connections: dict[str, Any]) -> None:
            captured.update(connections)

        get_tools = AsyncMock(return_value=[])

    monkeypatch.setattr("resq_agent.mcp.MultiServerMCPClient", _Recorder)
    from resq_agent.mcp import mcp_client

    client = mcp_client()
    assert "resq" in captured
    assert captured["resq"]["transport"] == "stdio"
    assert client is not None
