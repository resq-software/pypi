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
import json

from resq_agent.graph import IncidentState, run_incident
from resq_agent.mcp import list_resq_tools


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser.

    Returns:
        argparse.ArgumentParser: Parser with ``list-tools`` and ``run``.
    """
    parser = argparse.ArgumentParser(description="LangGraph agent that drives resq-mcp")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-tools", help="connect to resq-mcp and print advertised tool names")

    run_cmd = sub.add_parser("run", help="run assess → validate → strategy (no mutations)")
    run_cmd.add_argument("--incident-id", required=True)
    run_cmd.add_argument("--sector-id", default="Sector-1")
    run_cmd.add_argument("--detected-type", default="wildfire")
    run_cmd.add_argument("--confidence", type=float, default=0.9)
    run_cmd.add_argument(
        "--reject",
        action="store_true",
        help="submit a rejection instead of a confirm",
    )
    run_cmd.add_argument("--notes", default="Assessed by resq-agent linear graph")
    return parser


def main() -> None:
    """Run ``resq-agent list-tools`` or ``resq-agent run``."""
    args = _build_parser().parse_args()
    if args.command == "list-tools":
        for name in asyncio.run(list_resq_tools()):
            print(name)
        return

    incident: IncidentState = {
        "incident_id": args.incident_id,
        "sector_id": args.sector_id,
        "detected_type": args.detected_type,
        "confidence": args.confidence,
        "is_confirmed": not args.reject,
        "notes": args.notes,
    }
    result = asyncio.run(run_incident(incident))
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
