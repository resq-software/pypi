<!--
  Copyright 2026 ResQ

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->

# Security Policy & Threat Model

## Threat Model

### Components
- **MCP Client**: Untrusted agent/LLM.
- **MCP Server**: This service.
- **Backend (Mocked)**: Internal trusted networks.

### Threats & Mitigations
1.  **Prompt Injection**:
    - **Risk**: malicious input manipulating backend commands.
    - **Mitigation**: Strict Pydantic schemas. Inputs are typed. No raw shell execution.

2.  **Unathorized Access**:
    - **Risk**: Random internet traffic accessing the SSE endpoint.
    - **Mitigation**: Bearer Token Auth (Mocked for now via `RESQ_API_KEY`). In prod, use OIDC.

3.  **Confused Deputy**:
    - **Risk**: LLM tricked into performing actions user didn't intend.
    - **Mitigation**: "Safe Mode" defaults. High-impact tools (Run Simulation) require explicit parameters.

4.  **SSRF (Server Side Request Forgery)**:
    - **Risk**: Server calling arbitrary URLs.
    - **Mitigation**: Outbound URLs generated are strictly internal schemas (`neofs://`). No user-supplied URLs are fetched.

## Reporting
Report vulnerabilities to `security@resq.internal`.
