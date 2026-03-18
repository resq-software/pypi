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

"""MCP tool wrappers for HCE domain."""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here
# because FastMCP/Pydantic needs to resolve the type annotations at runtime
# for tool parameter validation. Using PEP 563 postponed annotations causes
# NameError when FastMCP tries to evaluate the forward references.

import logging
from datetime import UTC, datetime

from resq_mcp.hce.models import IncidentValidation, MissionParameters
from resq_mcp.hce.service import update_mission_params as _update_mission_params
from resq_mcp.server import incidents, mcp

logger = logging.getLogger("resq-mcp")


@mcp.tool()
async def validate_incident(val: IncidentValidation) -> str:
    """Submit validation result for an incident report.

    Used by human operators or automated validation systems (HCE) to
    confirm or reject incident reports before triggering full response.

    Args:
        val: IncidentValidation with:
            - incident_id: ID of incident being validated
            - is_confirmed: True=confirmed, False=rejected/false positive
            - validation_source: Who/what validated (e.g., "Human-Operator")
            - correlated_pre_alert_id: Optional linked PDIE alert
            - notes: Validation reasoning and evidence

    Returns:
        str: Confirmation message indicating action taken:
            "Incident {id} successfully CONFIRMED." or
            "Incident {id} successfully REJECTED."

    Example:
        >>> from resq_mcp.hce.models import IncidentValidation
        >>> validation = IncidentValidation(
        ...     incident_id="INC-123",
        ...     is_confirmed=True,
        ...     validation_source="Human-Operator-Alice",
        ...     notes="Confirmed via video evidence and ground reports"
        ... )
        >>> result = await validate_incident(validation)
        >>> print(result)  # "Incident INC-123 successfully CONFIRMED."

    Workflow:
        1. Edge AI detects incident (low confidence)
        2. HCE cross-references with PDIE/sensors
        3. If ambiguous -> human review required
        4. Operator submits validation via this tool
        5. If confirmed -> trigger response strategy
        6. If rejected -> log as false positive, update ML model

    Audit Trail:
        All validations logged with timestamp, source, and reasoning
        for post-incident analysis and ML model refinement.
    """
    action = "CONFIRMED" if val.is_confirmed else "REJECTED"

    # Idempotency / conflict guard — prevent silent re-validation with opposite result
    if val.incident_id in incidents:
        existing = incidents[val.incident_id]
        if existing["is_confirmed"] != val.is_confirmed:
            existing_action = "CONFIRMED" if existing["is_confirmed"] else "REJECTED"
            return (
                f"Conflict: Incident {val.incident_id} was already {existing_action} "
                f"by {existing['validation_source']}. "
                f"Conflicting re-validation rejected."
            )
        return f"Incident {val.incident_id} already {action} (idempotent)."

    incidents[val.incident_id] = {
        "is_confirmed": val.is_confirmed,
        "validation_source": val.validation_source,
        "notes": val.notes,
        "validated_at": datetime.now(UTC).isoformat(),
    }
    logger.info(
        "Incident %s %s by %s",
        val.incident_id,
        action,
        val.validation_source,
    )
    logger.debug("Incident %s notes: %s", val.incident_id, val.notes)
    return f"Incident {val.incident_id} successfully {action}."


@mcp.tool()
async def update_mission_params(drone_id: str, strategy_id: str) -> MissionParameters:
    """Push authorized mission parameters to a drone for an approved strategy.

    Completes the deployment workflow after a strategy has been approved:
    get_deployment_strategy -> (human approval) -> update_mission_params -> drone executes.

    Args:
        drone_id: Target drone identifier (e.g., "DRONE-Alpha").
        strategy_id: Approved strategy ID from get_deployment_strategy (e.g., "STRAT-X1Y2Z3").

    Returns:
        MissionParameters: Authorized parameter set including mission ID, allowed actions,
            risk tolerance, and a deterministic blockchain-anchored strategy hash.

    Example:
        >>> params = await update_mission_params("DRONE-Alpha", "STRAT-ABCD1234")
        >>> print(params.authorized_actions)
        >>> print(params.strategy_hash)  # 0xSHA256(strategy_id:mission_id)
    """
    logger.info(
        "Pushing mission params to drone %s for strategy %s",
        drone_id,
        strategy_id,
    )
    return _update_mission_params(drone_id, strategy_id)
