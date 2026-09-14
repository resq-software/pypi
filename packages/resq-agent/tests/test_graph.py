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

"""Tests for the linear incident graph."""

from __future__ import annotations

from typing import Any

from resq_agent.graph import IncidentState, run_incident


class FakeTool:
    """Records ainvoke payloads and returns a canned string."""

    def __init__(self, name: str, result: str) -> None:
        self.name = name
        self.calls: list[dict[str, Any]] = []
        self._result = result

    async def ainvoke(self, payload: dict[str, Any], config: object | None = None) -> str:
        """Record ``payload`` and return the canned result."""
        self.calls.append(payload)
        return self._result


def _incident(*, confirmed: bool = True) -> IncidentState:
    """Build a minimal incident payload."""
    return {
        "incident_id": "INC-DEMO-1",
        "sector_id": "Sector-1",
        "detected_type": "wildfire",
        "confidence": 0.95,
        "is_confirmed": confirmed,
        "notes": "video plus ground reports",
    }


async def test_confirmed_incident_runs_validate_then_strategy() -> None:
    """A confirmed report must call both read-only MCP tools, in order."""
    validate = FakeTool("validate_incident", "Incident INC-DEMO-1 successfully CONFIRMED.")
    strategy = FakeTool("get_deployment_strategy", "strategy_id=STRAT-1 drones=2")
    result = await run_incident(
        _incident(confirmed=True),
        tools={validate.name: validate, strategy.name: strategy},
    )

    assert "INC-DEMO-1" in (result.get("assessment") or "")
    assert result.get("validation") == validate._result
    assert result.get("strategy") == strategy._result
    assert validate.calls[0]["incident_id"] == "INC-DEMO-1"
    assert validate.calls[0]["is_confirmed"] is True
    assert strategy.calls[0] == {"incident_id": "INC-DEMO-1"}


async def test_rejected_incident_skips_strategy() -> None:
    """A rejected report must not ask for a deployment strategy."""
    validate = FakeTool("validate_incident", "Incident INC-DEMO-1 successfully REJECTED.")
    strategy = FakeTool("get_deployment_strategy", "should-not-run")
    result = await run_incident(
        _incident(confirmed=False),
        tools={validate.name: validate, strategy.name: strategy},
    )

    assert result.get("strategy") is None
    assert strategy.calls == []
    assert "REJECTED" in (result.get("validation") or "")


async def test_missing_validate_tool_records_an_error() -> None:
    """A graph with no validate tool must fail closed, not invent a result."""
    result = await run_incident(_incident(), tools={"get_deployment_strategy": FakeTool("x", "")})

    assert result.get("strategy") is None
    errors = result.get("errors") or []
    assert any("validate_incident" in item for item in errors)
