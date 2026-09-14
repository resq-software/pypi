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

"""Tests for the CLI entry point."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from resq_agent.__main__ import main


def test_list_tools_prints_names(capsys: pytest.CaptureFixture[str]) -> None:
    """The CLI is a thin wrapper around list_resq_tools."""

    async def fake_list() -> list[str]:
        return ["validate_incident", "run_simulation"]

    with (
        patch("sys.argv", ["resq-agent", "list-tools"]),
        patch("resq_agent.__main__.list_resq_tools", fake_list),
    ):
        main()
    captured = capsys.readouterr()
    assert captured.out.splitlines() == ["validate_incident", "run_simulation"]


def test_run_prints_json_state(capsys: pytest.CaptureFixture[str]) -> None:
    """The run command dumps the final graph state as JSON."""

    async def fake_run(
        incident: dict[str, object],
        tools: object | None = None,
    ) -> dict[str, object]:
        return {**incident, "assessment": "ok"}

    with (
        patch("sys.argv", ["resq-agent", "run", "--incident-id", "INC-1"]),
        patch("resq_agent.__main__.run_incident", fake_run),
    ):
        main()
    captured = capsys.readouterr()
    assert '"incident_id": "INC-1"' in captured.out
    assert '"assessment": "ok"' in captured.out
