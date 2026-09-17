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

"""Connect to resq-mcp and load its tools as LangChain tools.

This is milestone 1 of the agent: prove we are a *consumer* of the MCP
server, not a second copy of the domain logic. Later nodes in the graph call
these tools; they do not reimplement validate / simulate / deploy.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from langchain_mcp_adapters.client import MultiServerMCPClient

if TYPE_CHECKING:
    from langchain_mcp_adapters.sessions import StdioConnection


def resq_mcp_dir() -> Path:
    """Return the sibling ``packages/resq-mcp`` directory.

    Returns:
        Path: Absolute path to the resq-mcp package root.
    """
    return Path(__file__).resolve().parents[3] / "resq-mcp"


def default_mcp_connection(*, safe_mode: bool = True) -> StdioConnection:
    """Build the stdio connection that spawns a local resq-mcp process.

    Safe Mode is set explicitly, never inherited. ``os.environ.copy()`` carries
    the caller's ambient ``RESQ_SAFE_MODE`` into the child, so ``setdefault``
    would let an operator who happens to have ``RESQ_SAFE_MODE=false`` exported
    silently spawn an unguarded server. The value is assigned unconditionally
    so the gate depends on this argument alone.

    Turning the gate off is therefore a deliberate, greppable call rather than
    an accident of the environment, which is what a later human-in-the-loop
    node needs.

    Args:
        safe_mode: When True (the default) the spawned server refuses
            mutations. Pass False only from a node that has obtained human
            approval.

    Returns:
        StdioConnection: Connection dict accepted by ``MultiServerMCPClient``.
    """
    env = os.environ.copy()
    env["RESQ_SAFE_MODE"] = "true" if safe_mode else "false"
    return {
        "transport": "stdio",
        "command": "uv",
        "args": ["run", "--directory", str(resq_mcp_dir()), "resq-mcp"],
        "env": env,
    }


def mcp_client() -> MultiServerMCPClient:
    """Return a client pointed at the local resq-mcp server.

    Returns:
        MultiServerMCPClient: Client named ``resq``.
    """
    return MultiServerMCPClient({"resq": default_mcp_connection()})


async def list_resq_tools(client: MultiServerMCPClient | None = None) -> list[str]:
    """Load resq-mcp tools and return their names, sorted.

    Args:
        client: Optional pre-built client. Tests inject a fake; production
            constructs one via :func:`mcp_client`.

    Returns:
        list[str]: Tool names as advertised by the MCP server.
    """
    owned = client or mcp_client()
    tools = await owned.get_tools()
    return sorted(tool.name for tool in tools)
