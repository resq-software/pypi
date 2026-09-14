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

"""Command-line entry point for resq-agent."""

from __future__ import annotations

import argparse
import asyncio

from resq_agent.mcp import list_resq_tools


def main() -> None:
    """Run ``resq-agent list-tools`` (milestone 1)."""
    parser = argparse.ArgumentParser(description="LangGraph agent that drives resq-mcp")
    parser.add_argument(
        "command",
        choices=["list-tools"],
        help="list-tools: connect to resq-mcp and print advertised tool names",
    )
    args = parser.parse_args()
    if args.command == "list-tools":
        for name in asyncio.run(list_resq_tools()):
            print(name)


if __name__ == "__main__":
    main()
