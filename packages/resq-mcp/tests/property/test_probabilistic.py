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

"""Probabilistic behavior tests for the drone feed module."""

from __future__ import annotations

import random

from resq_mcp.core.models import ErrorResponse
from resq_mcp.drone.models import DeploymentStatus, SectorAnalysis
from resq_mcp.drone.service import (
    get_drone_swarm_status,
    request_drone_deployment,
    scan_current_sector,
)


class TestProbabilisticBehavior:
    def test_disaster_detection_rate_approximately_30_percent(self) -> None:
        random.seed(42)
        n_runs = 1000
        detections = 0
        for _ in range(n_runs):
            result = scan_current_sector("Sector-1")
            if isinstance(result, SectorAnalysis) and result.status == "CRITICAL_ALERT":
                detections += 1
        rate = detections / n_runs
        assert 0.20 <= rate <= 0.40, f"Detection rate {rate:.2%} outside expected range"

    async def test_deployment_eta_within_documented_range(self) -> None:
        random.seed(42)
        for _ in range(100):
            result = await request_drone_deployment("Sector-1", "high")
            # Assert the type rather than guarding on it: with FLEET_API_URL
            # unset the service falls back to the in-memory mock, so
            # DeploymentStatus is the only correct outcome. A guard would let a
            # regression returning ErrorResponse 100 times pass silently.
            assert isinstance(result, DeploymentStatus)
            assert 30 <= result.eta_seconds <= 120

    async def test_drone_id_is_a_roster_member(self) -> None:
        random.seed(42)
        from resq_mcp.drone.service import FLEET_ROSTER

        known = {unit.drone_id for unit in FLEET_ROSTER}
        for _ in range(100):
            result = await request_drone_deployment("Sector-2", "critical")
            assert isinstance(result, DeploymentStatus)
            assert result.drone_id in known, f"Bad drone ID: {result.drone_id}"

    async def test_swarm_battery_within_range(self) -> None:
        random.seed(42)
        for _ in range(100):
            status = await get_drone_swarm_status()
            assert not isinstance(status, ErrorResponse)
            assert 60 <= status.average_battery <= 100
