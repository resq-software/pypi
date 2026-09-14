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

"""Linear incident-response graph: assess → validate → strategy.

No mutations. Safe Mode can stay on. Later milestones add simulation polling
and a human interrupt before ``update_mission_params``.
"""

from __future__ import annotations

from typing import Any, Literal, NotRequired, TypedDict

from langchain_core.runnables import RunnableConfig  # noqa: TC002
from langgraph.graph import END, START, StateGraph

from resq_agent.mcp import load_tool_map

VALIDATE_TOOL = "validate_incident"
STRATEGY_TOOL = "get_deployment_strategy"


class IncidentState(TypedDict):
    """Shared state that flows through the linear graph."""

    incident_id: str
    sector_id: str
    detected_type: str
    confidence: float
    is_confirmed: bool
    notes: str
    assessment: NotRequired[str]
    validation: NotRequired[str]
    strategy: NotRequired[str]
    errors: NotRequired[list[str]]


def _tools(config: RunnableConfig) -> dict[str, Any]:
    """Read the injected tool map from the LangGraph config.

    Args:
        config: The runnable config passed to ``ainvoke``.

    Returns:
        dict[str, Any]: Tools keyed by name.

    Raises:
        RuntimeError: If the caller forgot to inject tools.
    """
    configurable = config.get("configurable") or {}
    tools = configurable.get("tools")
    if not isinstance(tools, dict) or not tools:
        raise RuntimeError("incident graph requires configurable.tools")
    return tools


async def _ainvoke_tool(tool: Any, payload: dict[str, Any]) -> str:
    """Call a LangChain/MCP tool and stringify the result.

    Args:
        tool: Object with ``ainvoke``.
        payload: Tool arguments.

    Returns:
        str: Tool output, stringified.
    """
    result = await tool.ainvoke(payload)
    return result if isinstance(result, str) else str(result)


async def assess(state: IncidentState) -> dict[str, Any]:
    """Record a one-line assessment. Does not call any MCP tool.

    Args:
        state: Incoming incident.

    Returns:
        dict[str, Any]: Partial state update with ``assessment``.
    """
    return {
        "assessment": (
            f"Incident {state['incident_id']} in {state['sector_id']}: "
            f"{state['detected_type']} (confidence {state['confidence']:.2f})"
        )
    }


async def validate(state: IncidentState, config: RunnableConfig) -> dict[str, Any]:
    """Call ``validate_incident``. Skip strategy when the report is rejected.

    Args:
        state: Incident plus assessment.
        config: Must carry ``configurable.tools``.

    Returns:
        dict[str, Any]: Validation text, or an error if the tool is missing.
    """
    tools = _tools(config)
    tool = tools.get(VALIDATE_TOOL)
    if tool is None:
        return {"errors": [f"MCP tool {VALIDATE_TOOL!r} is not loaded"]}
    text = await _ainvoke_tool(
        tool,
        {
            "incident_id": state["incident_id"],
            "is_confirmed": state["is_confirmed"],
            "validation_source": "resq-agent",
            "notes": state["notes"],
        },
    )
    return {"validation": text}


def after_validate(state: IncidentState) -> Literal["strategy", "done"]:
    """Route to strategy only when validation succeeded and confirmed.

    Args:
        state: State after the validate node.

    Returns:
        Literal["strategy", "done"]: Next hop.
    """
    if state.get("errors"):
        return "done"
    if not state["is_confirmed"]:
        return "done"
    return "strategy"


async def strategy(state: IncidentState, config: RunnableConfig) -> dict[str, Any]:
    """Call ``get_deployment_strategy`` for a confirmed incident.

    Args:
        state: Confirmed incident.
        config: Must carry ``configurable.tools``.

    Returns:
        dict[str, Any]: Strategy payload, or an error if the tool is missing.
    """
    tools = _tools(config)
    tool = tools.get(STRATEGY_TOOL)
    if tool is None:
        return {"errors": [f"MCP tool {STRATEGY_TOOL!r} is not loaded"]}
    text = await _ainvoke_tool(tool, {"incident_id": state["incident_id"]})
    return {"strategy": text}


def build_incident_graph() -> Any:
    """Compile the assess → validate → strategy graph.

    Returns:
        CompiledStateGraph: Ready for ``ainvoke``.
    """
    builder: StateGraph[IncidentState] = StateGraph(IncidentState)
    builder.add_node("assess", assess)
    builder.add_node("validate", validate)
    builder.add_node("strategy", strategy)
    builder.add_edge(START, "assess")
    builder.add_edge("assess", "validate")
    builder.add_conditional_edges(
        "validate",
        after_validate,
        {"strategy": "strategy", "done": END},
    )
    builder.add_edge("strategy", END)
    return builder.compile()


async def run_incident(
    incident: IncidentState,
    tools: dict[str, Any] | None = None,
) -> IncidentState:
    """Run the linear graph for one incident.

    Args:
        incident: Required incident fields.
        tools: Optional injected tool map. When omitted, tools are loaded
            from a live resq-mcp process.

    Returns:
        IncidentState: Final graph state.
    """
    resolved = tools if tools is not None else await load_tool_map()
    graph = build_incident_graph()
    result = await graph.ainvoke(incident, {"configurable": {"tools": resolved}})
    return result  # type: ignore[no-any-return]
