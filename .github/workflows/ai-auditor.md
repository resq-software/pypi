---
# Trigger - when should this workflow run?
on:
  pull_request:
    # `synchronize` and `reopened` are required, not optional: the audit's job
    # results are recorded against the head SHA. With `opened` alone, pushing any
    # follow-up commit leaves the new SHA without them, and because these jobs are
    # required by the branch ruleset the PR becomes permanently unmergeable.
    types: [opened, synchronize, reopened]
  workflow_dispatch:  # Manual trigger

# Permissions - what can this workflow access?
permissions:
  contents: read
  issues: read
  pull-requests: read

# AI engine - Gemini (free Google AI Studio tier; avoids Copilot utility-model rate limits).
# The model is pinned: left unpinned the proxy steers to whatever its alias globs
# resolve to, which since 2026-08-10 has been `gemini-3.1-flash-tts-preview` — a
# text-to-speech model with no entry in the AI-credits pricing table.
model: gemini-2.5-pro
engine:
  id: gemini
  # Pinned. gh-aw v0.88.7 otherwise picks Gemini CLI 0.55.1, which rejects the
  # auth this workflow supplies, and the agent job dies before doing any work:
  #     Invalid auth method selected.
  #     [gemini-harness] attempt 1: process exit event exitCode=41
  # GEMINI_API_KEY (the org secret) is wired the same either way, so the break
  # is inside the CLI. Unpin only together with whatever auth change 0.5x wants.
  version: "0.39.1"

# Network access
network: defaults

# Outputs - what APIs and tools can the AI use?
safe-outputs:
  report-failure-as-issue: false
  add-comment:
    max: 10

---

# ai-auditor

Audit the changes in this pull request for security vulnerabilities, logic bugs, or performance issues.

## Instructions

1.  Review all file changes in the current pull request.
2.  Identify potential security vulnerabilities (e.g., SQL injection, hardcoded secrets, insecure defaults).
3.  Look for logic bugs, edge cases, or potential runtime errors.
4.  Check for performance bottlenecks or inefficient code patterns.
5.  For each identified issue, provide a concise and constructive comment explaining the problem and suggesting a fix.
6.  Use the `add-comment` tool to post your feedback directly on the PR.

Be thorough but focus on high-impact issues. If no issues are found, post a brief summary comment stating that the audit passed.

## Setup

This workflow uses the Gemini engine and requires the `GEMINI_API_KEY` repository secret (free key from https://aistudio.google.com).
