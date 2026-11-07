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

# CHANGELOG

<!-- version list -->

## v2.0.0 (2026-11-07)

### Bug Fixes

- Align comments with post-exclusion coverage numbers
  ([#42](https://github.com/resq-software/pypi/pull/42),
  [`09cf4f5`](https://github.com/resq-software/pypi/commit/09cf4f5f792ceba143e68e1ff4427894ac26fa38))

- Resolve failing CI (run 35108048778) ([#119](https://github.com/resq-software/pypi/pull/119),
  [`43bea29`](https://github.com/resq-software/pypi/commit/43bea29d74a5d10741572ac0505fbb1aca14fecb))

- **ci**: Correct size-labeler globs and sync title-derived labels
  ([#95](https://github.com/resq-software/pypi/pull/95),
  [`75e2daf`](https://github.com/resq-software/pypi/commit/75e2daff6dcbe07aee468f1cd007da6ce1ec4e21))

- **ci**: Escape `<` in prose for MDX safety ([#36](https://github.com/resq-software/pypi/pull/36),
  [`7f6dda3`](https://github.com/resq-software/pypi/commit/7f6dda394e2759c6945e6fed14d5bdc9cdb5ff84))

- **ci**: Keep the licence check advisory when a licence is unresolved
  ([#126](https://github.com/resq-software/pypi/pull/126),
  [`0192fb7`](https://github.com/resq-software/pypi/commit/0192fb7b4d6f2430ceeea790de91b577351e1fee))

- **ci**: On a re-run, attach only missing release assets instead of clobbering
  ([#126](https://github.com/resq-software/pypi/pull/126),
  [`0192fb7`](https://github.com/resq-software/pypi/commit/0192fb7b4d6f2430ceeea790de91b577351e1fee))

- **ci**: Pin ai-auditor to Gemini CLI 0.39.1 and gemini-2.5-pro
  ([#125](https://github.com/resq-software/pypi/pull/125),
  [`098ecce`](https://github.com/resq-software/pypi/commit/098ecce0ffe698d2cded5553241c0723779a3276))

- **ci**: Recompile ai-auditor off the blocked gh-aw v0.83.4
  ([#122](https://github.com/resq-software/pypi/pull/122),
  [`fe90311`](https://github.com/resq-software/pypi/commit/fe90311bafab354d16d7fce383391f1180cf6aa6))

- **ci**: Skip security scan on Dependabot PRs to unblock their fix PRs
  ([`ee769e6`](https://github.com/resq-software/pypi/commit/ee769e698c2d6a2d341459b969db13beb57b3835))

- **ci**: Switch lazydocs -> pydoc-markdown for Python 3.13 compat
  ([#32](https://github.com/resq-software/pypi/pull/32),
  [`c485af3`](https://github.com/resq-software/pypi/commit/c485af324ca8c9c6c48207772d1a29d9f6bd812e))

- **ci**: Walk submodules + alphabetize README package list
  ([#33](https://github.com/resq-software/pypi/pull/33),
  [`4c7a495`](https://github.com/resq-software/pypi/commit/4c7a4957bc88bb706cdb535a808a10c83d8f6c73))

- **deps**: Bump pyjwt, urllib3 and multidict locks past OSV advisories
  ([#140](https://github.com/resq-software/pypi/pull/140),
  [`ada4d6a`](https://github.com/resq-software/pypi/commit/ada4d6a6b7f7c377c8eb7dd2e2ac1060a9706c2a))

- **deps**: Floor pyjwt to >=2.14.0 to clear osv-scanner advisory
  ([#131](https://github.com/resq-software/pypi/pull/131),
  [`50ecfd0`](https://github.com/resq-software/pypi/commit/50ecfd0e71be61bbf987bb4068cfff09ff2362af))

- **deps**: Raise security floors past 25 advisories in resq-mcp and resq-agent
  ([#147](https://github.com/resq-software/pypi/pull/147),
  [`9b2b54d`](https://github.com/resq-software/pypi/commit/9b2b54d7770f3e0f420fe81485a9e09b255542f4))

- **hooks**: Adopt granular fail-closed GIT_HOOKS_SKIP
  ([#135](https://github.com/resq-software/pypi/pull/135),
  [`3fe79ce`](https://github.com/resq-software/pypi/commit/3fe79ce504df50f3d1aace3ec72c1a1c413280da))

- **hooks**: Announce prepare-commit-msg skips before they take effect
  ([#135](https://github.com/resq-software/pypi/pull/135),
  [`3fe79ce`](https://github.com/resq-software/pypi/commit/3fe79ce504df50f3d1aace3ec72c1a1c413280da))

- **hooks**: Sync prepare-commit-msg with the canonical template
  ([#135](https://github.com/resq-software/pypi/pull/135),
  [`3fe79ce`](https://github.com/resq-software/pypi/commit/3fe79ce504df50f3d1aace3ec72c1a1c413280da))

- **release**: Categorize release notes by the org C-* taxonomy (not non-existent type:*)
  ([#95](https://github.com/resq-software/pypi/pull/95),
  [`75e2daf`](https://github.com/resq-software/pypi/commit/75e2daff6dcbe07aee468f1cd007da6ce1ec4e21))

- **resq-mcp**: Clear 12 dependency advisories, track uv.lock
  ([#99](https://github.com/resq-software/pypi/pull/99),
  [`833e2f9`](https://github.com/resq-software/pypi/commit/833e2f95942e61a92bb8f2bd4c3af34d035d70f6))

- **resq-mcp**: Correct the changelog-mode claim and re-anchor the exclusion
  ([#146](https://github.com/resq-software/pypi/pull/146),
  [`9ba70f4`](https://github.com/resq-software/pypi/commit/9ba70f4731ea33246307cc8c0a92284587e9ecbe))

- **resq-mcp**: Derive the active-drones resource from the fleet service
  ([#97](https://github.com/resq-software/pypi/pull/97),
  [`6364f1e`](https://github.com/resq-software/pypi/commit/6364f1e7c682036273b6850da2e8f0413081554c))

- **resq-mcp**: Flush telemetry from a finally block so cleanup errors cannot skip it
  ([#84](https://github.com/resq-software/pypi/pull/84),
  [`c105463`](https://github.com/resq-software/pypi/commit/c105463b68f878f1742f788ac026eb3e368882e7))

- **resq-mcp**: Flush telemetry on server shutdown
  ([#84](https://github.com/resq-software/pypi/pull/84),
  [`c105463`](https://github.com/resq-software/pypi/commit/c105463b68f878f1742f788ac026eb3e368882e7))

- **resq-mcp**: Honor RESQ_TRANSPORT/HOST/PORT in server entry point
  ([#58](https://github.com/resq-software/pypi/pull/58),
  [`21f8afd`](https://github.com/resq-software/pypi/commit/21f8afd7724bb9458355362ad9cc050a4ddfefe6))

- **resq-mcp**: Honor RESQ_TRANSPORT/HOST/PORT in server entry point
  ([#54](https://github.com/resq-software/pypi/pull/54),
  [`895f067`](https://github.com/resq-software/pypi/commit/895f067f8d95fa48b51b1936569df84a591aae1b))

- **resq-mcp**: Validate identifiers in drone and PDIE models
  ([#89](https://github.com/resq-software/pypi/pull/89),
  [`911d485`](https://github.com/resq-software/pypi/commit/911d485c5cd64173d8b3355495ad377f1bd1dc4f))

### Chores

- Add PR labeler (npm format) ([#95](https://github.com/resq-software/pypi/pull/95),
  [`75e2daf`](https://github.com/resq-software/pypi/commit/75e2daff6dcbe07aee468f1cd007da6ce1ec4e21))

- Deploy agentic workflows ([#56](https://github.com/resq-software/pypi/pull/56),
  [`c1b1eef`](https://github.com/resq-software/pypi/commit/c1b1eef01ebd9b6e5b9b99097d9f7fd2cabfdcd2))

- Remove fleet-api, relocated to an internal repository
  ([#106](https://github.com/resq-software/pypi/pull/106),
  [`8aa6bb4`](https://github.com/resq-software/pypi/commit/8aa6bb429b5c247ef96226851c4b43fb14f880e3))

- Retrigger ci ([#82](https://github.com/resq-software/pypi/pull/82),
  [`b3b9eb4`](https://github.com/resq-software/pypi/commit/b3b9eb4d30a8fe6a2369a709383741c86d799190))

- Sync from resq-software/resQ@3b483eb ([#27](https://github.com/resq-software/pypi/pull/27),
  [`85ca16d`](https://github.com/resq-software/pypi/commit/85ca16d97ecc779cc6ebccff90d3b3f9c8bad9c5))

- **bootstrap**: Retire duplicate setup scripts, delegate to resq-software/dev
  ([#25](https://github.com/resq-software/pypi/pull/25),
  [`d61dfd9`](https://github.com/resq-software/pypi/commit/d61dfd98361c7fbfed49b2f09627ceec79480792))

- **ci**: SHA-pin third-party GitHub Actions refs
  ([#21](https://github.com/resq-software/pypi/pull/21),
  [`90a4aac`](https://github.com/resq-software/pypi/commit/90a4aac7f94e3c7ae4d2ae608cdb37dc236220c1))

- **compliance**: Security policy, release SBOMs, licence check
  ([#126](https://github.com/resq-software/pypi/pull/126),
  [`0192fb7`](https://github.com/resq-software/pypi/commit/0192fb7b4d6f2430ceeea790de91b577351e1fee))

- **compliance**: SPDX headers for the resq-mcp package
  ([#128](https://github.com/resq-software/pypi/pull/128),
  [`665fae5`](https://github.com/resq-software/pypi/commit/665fae54766587ec3f90da8c24576ebcf9578b9a))

- **deps**: Bump actions/attest-build-provenance
  ([#90](https://github.com/resq-software/pypi/pull/90),
  [`60f4c84`](https://github.com/resq-software/pypi/commit/60f4c84df42a0f1dc7334456017a0019c986dd81))

- **deps**: Bump actions/checkout in the github-actions group
  ([#64](https://github.com/resq-software/pypi/pull/64),
  [`0198109`](https://github.com/resq-software/pypi/commit/0198109d6f18f3e32df8adfb7faf18066157d68a))

- **deps**: Bump anyio ([#120](https://github.com/resq-software/pypi/pull/120),
  [`de277df`](https://github.com/resq-software/pypi/commit/de277df5d0b2fb6906af19f14b732c94f2316d9e))

- **deps**: Bump astral-sh/setup-uv in the github-actions group
  ([#115](https://github.com/resq-software/pypi/pull/115),
  [`966764d`](https://github.com/resq-software/pypi/commit/966764d380367299f03b68df578b2ac5f28703fa))

- **deps**: Bump astral-sh/setup-uv in the github-actions group
  ([#93](https://github.com/resq-software/pypi/pull/93),
  [`6ce129c`](https://github.com/resq-software/pypi/commit/6ce129cc35729ec17bbd43d8930225f1c9800c31))

- **deps**: Bump astral-sh/setup-uv in the github-actions group
  ([#71](https://github.com/resq-software/pypi/pull/71),
  [`b1de407`](https://github.com/resq-software/pypi/commit/b1de407fc686d21eb787185b2e879f260b8277b0))

- **deps**: Bump astral-sh/setup-uv in the github-actions group
  ([#29](https://github.com/resq-software/pypi/pull/29),
  [`78edc4b`](https://github.com/resq-software/pypi/commit/78edc4b041b61e2f1c4ce653e979ee13d8f0e525))

- **deps**: Bump docker/build-push-action ([#121](https://github.com/resq-software/pypi/pull/121),
  [`acb1fbf`](https://github.com/resq-software/pypi/commit/acb1fbf66683d1d940f168fe8273802ebe3336cb))

- **deps**: Bump pygments 2.19.2 → 2.20.0 for GHSA-5239-wwwm-4pmq
  ([#23](https://github.com/resq-software/pypi/pull/23),
  [`2f97c07`](https://github.com/resq-software/pypi/commit/2f97c0763b9301db31710602a9c23fd8c97914ee))

- **deps**: Bump python-semantic-release/python-semantic-release
  ([#103](https://github.com/resq-software/pypi/pull/103),
  [`f17c97b`](https://github.com/resq-software/pypi/commit/f17c97b16ded999f2353c6ee3d56731c8924b01b))

- **deps**: Bump the github-actions group across 1 directory with 4 updates
  ([#66](https://github.com/resq-software/pypi/pull/66),
  [`59d8777`](https://github.com/resq-software/pypi/commit/59d8777972f3b06bcb7637e9e8d66c9bceaca98d))

- **deps**: Bump the github-actions group across 1 directory with 5 updates
  ([#50](https://github.com/resq-software/pypi/pull/50),
  [`4207c7a`](https://github.com/resq-software/pypi/commit/4207c7a39307ddc4396349c84802ad3ba9bd813d))

- **deps**: Bump the github-actions group across 1 directory with 6 updates
  ([#77](https://github.com/resq-software/pypi/pull/77),
  [`e4ebc40`](https://github.com/resq-software/pypi/commit/e4ebc40591aa76a183794dd3262ea27d6ae4b606))

- **deps**: Bump the github-actions group across 1 directory with 9 updates
  ([#143](https://github.com/resq-software/pypi/pull/143),
  [`dd89351`](https://github.com/resq-software/pypi/commit/dd8935150665e558bbdc0a45ca8e2a2755f9c9b0))

- **deps**: Bump the github-actions group with 2 updates
  ([#80](https://github.com/resq-software/pypi/pull/80),
  [`c25ae46`](https://github.com/resq-software/pypi/commit/c25ae461edf4ff21339a3a3e3d9fdf91eb3e2812))

- **deps**: Bump the github-actions group with 2 updates
  ([#55](https://github.com/resq-software/pypi/pull/55),
  [`bd47c77`](https://github.com/resq-software/pypi/commit/bd47c773134f7fde7344b6f9dea44a7cd5e55ecc))

- **deps**: Bump the github-actions group with 4 updates
  ([#69](https://github.com/resq-software/pypi/pull/69),
  [`f7a8edc`](https://github.com/resq-software/pypi/commit/f7a8edc1b585038474dde7526780e0687dec3a75))

- **deps**: Bump the github-actions group with 6 updates
  ([#20](https://github.com/resq-software/pypi/pull/20),
  [`d10f1ae`](https://github.com/resq-software/pypi/commit/d10f1ae55d0a8f1171425009aa88edfe62d9ee37))

- **hooks**: Address review — ref-aware scoping, nested lockfiles, docs
  ([#91](https://github.com/resq-software/pypi/pull/91),
  [`45d4595`](https://github.com/resq-software/pypi/commit/45d45953be710788e1bba1a62655dc6067d23955))

- **hooks**: Restore the canonical git hooks ([#91](https://github.com/resq-software/pypi/pull/91),
  [`45d4595`](https://github.com/resq-software/pypi/commit/45d45953be710788e1bba1a62655dc6067d23955))

- **hooks**: Resync pre-push after the shellcheck fix
  ([#91](https://github.com/resq-software/pypi/pull/91),
  [`45d4595`](https://github.com/resq-software/pypi/commit/45d45953be710788e1bba1a62655dc6067d23955))

- **hooks**: Update the README, pick up the canonical template fixes
  ([#91](https://github.com/resq-software/pypi/pull/91),
  [`45d4595`](https://github.com/resq-software/pypi/commit/45d45953be710788e1bba1a62655dc6067d23955))

- **labeler**: Complete npm-format suite — pr-size + label-sync + labels.yml
  ([#95](https://github.com/resq-software/pypi/pull/95),
  [`75e2daf`](https://github.com/resq-software/pypi/commit/75e2daff6dcbe07aee468f1cd007da6ce1ec4e21))

- **nix**: Bump nixpkgs 24.11 → 25.11 + refresh lock
  ([#24](https://github.com/resq-software/pypi/pull/24),
  [`dd020d8`](https://github.com/resq-software/pypi/commit/dd020d82ee9834c47cb08eb5573e3aca199d8f46))

- **resq-mcp**: Make documented quality gates runnable locally
  ([#82](https://github.com/resq-software/pypi/pull/82),
  [`b3b9eb4`](https://github.com/resq-software/pypi/commit/b3b9eb4d30a8fe6a2369a709383741c86d799190))

- **resq-mcp**: Remove unreachable duplicate modules
  ([#81](https://github.com/resq-software/pypi/pull/81),
  [`ebd4f45`](https://github.com/resq-software/pypi/commit/ebd4f4574a8ccaa3b2dcb8062ddfcc3e1df4e321))

### Code Style

- **resq-mcp**: Apply ruff format to satisfy CI format check
  ([#58](https://github.com/resq-software/pypi/pull/58),
  [`21f8afd`](https://github.com/resq-software/pypi/commit/21f8afd7724bb9458355362ad9cc050a4ddfefe6))

### Continuous Integration

- Add conventional-title labeler (auto C-* change-type -> release notes/changelog)
  ([#95](https://github.com/resq-software/pypi/pull/95),
  [`75e2daf`](https://github.com/resq-software/pypi/commit/75e2daff6dcbe07aee468f1cd007da6ce1ec4e21))

- Add docstring coverage gate via interrogate ([#42](https://github.com/resq-software/pypi/pull/42),
  [`09cf4f5`](https://github.com/resq-software/pypi/commit/09cf4f5f792ceba143e68e1ff4427894ac26fa38))

- Add placeholder `required` status gate alongside existing CI
  ([#26](https://github.com/resq-software/pypi/pull/26),
  [`85db9ce`](https://github.com/resq-software/pypi/commit/85db9ce54b4265868f452468ad87e880bdb58d78))

- Adopt self-hosted runner toggle for safe CI + bot jobs
  ([#129](https://github.com/resq-software/pypi/pull/129),
  [`ddee31d`](https://github.com/resq-software/pypi/commit/ddee31d5ae11a21c4c545294b760cf6d69b1cf41))

- Bump security-scan pin to 73b9edb (actionlint now skips gh-aw locks)
  ([#56](https://github.com/resq-software/pypi/pull/56),
  [`c1b1eef`](https://github.com/resq-software/pypi/commit/c1b1eef01ebd9b6e5b9b99097d9f7fd2cabfdcd2))

- Drop gh-aw agentics-maintenance.yml (generated empty choice fails actionlint; optional
  scaffolding) ([#56](https://github.com/resq-software/pypi/pull/56),
  [`c1b1eef`](https://github.com/resq-software/pypi/commit/c1b1eef01ebd9b6e5b9b99097d9f7fd2cabfdcd2))

- Emit one .md per submodule (sync from docs#34)
  ([#39](https://github.com/resq-software/pypi/pull/39),
  [`52b6449`](https://github.com/resq-software/pypi/commit/52b64493ec324d32d60b46d39134de152d74b7da))

- Emit README.mdx + plaintext package list ([#37](https://github.com/resq-software/pypi/pull/37),
  [`41cdb52`](https://github.com/resq-software/pypi/commit/41cdb5256a47757f0fa1f2cc037eacc36972a699))

- Enforce the lockfiles and cap the MCP dependency majors
  ([#101](https://github.com/resq-software/pypi/pull/101),
  [`fc1ee38`](https://github.com/resq-software/pypi/commit/fc1ee38beb3466c187e5fca3768cbf35444c7db8))

- Gate required on real CI + repo-standards (was placeholder)
  ([#63](https://github.com/resq-software/pypi/pull/63),
  [`63fe12e`](https://github.com/resq-software/pypi/commit/63fe12e55a8411f9c86bcc71bb5a770292233ab3))

- Harden the `required` gate (was a placeholder rubber-stamp)
  ([#63](https://github.com/resq-software/pypi/pull/63),
  [`63fe12e`](https://github.com/resq-software/pypi/commit/63fe12e55a8411f9c86bcc71bb5a770292233ab3))

- Ignore gh-aw generated workflows in actionlint (locks + maintenance)
  ([#56](https://github.com/resq-software/pypi/pull/56),
  [`c1b1eef`](https://github.com/resq-software/pypi/commit/c1b1eef01ebd9b6e5b9b99097d9f7fd2cabfdcd2))

- Remove placeholder required.yml — gate now lives in ci.yml
  ([#63](https://github.com/resq-software/pypi/pull/63),
  [`63fe12e`](https://github.com/resq-software/pypi/commit/63fe12e55a8411f9c86bcc71bb5a770292233ab3))

- Restore gh-aw agentics-maintenance.yml (keeps locks fresh; ignored by actionlint)
  ([#56](https://github.com/resq-software/pypi/pull/56),
  [`c1b1eef`](https://github.com/resq-software/pypi/commit/c1b1eef01ebd9b6e5b9b99097d9f7fd2cabfdcd2))

- Revert api-docs.yml to ubuntu-latest (public repo, hosted-only)
  ([#130](https://github.com/resq-software/pypi/pull/130),
  [`f96957e`](https://github.com/resq-software/pypi/commit/f96957e4b2c5d05f131162134f94ea40f9871799))

- Revert ci.yml to ubuntu-latest (public repo, hosted-only)
  ([#130](https://github.com/resq-software/pypi/pull/130),
  [`f96957e`](https://github.com/resq-software/pypi/commit/f96957e4b2c5d05f131162134f94ea40f9871799))

- Revert conventional-title-labeler.yml to ubuntu-latest (public repo, hosted-only)
  ([#130](https://github.com/resq-software/pypi/pull/130),
  [`f96957e`](https://github.com/resq-software/pypi/commit/f96957e4b2c5d05f131162134f94ea40f9871799))

- Revert dependency-review.yml to ubuntu-latest (public repo, hosted-only)
  ([#130](https://github.com/resq-software/pypi/pull/130),
  [`f96957e`](https://github.com/resq-software/pypi/commit/f96957e4b2c5d05f131162134f94ea40f9871799))

- Revert label-sync.yml to ubuntu-latest (public repo, hosted-only)
  ([#130](https://github.com/resq-software/pypi/pull/130),
  [`f96957e`](https://github.com/resq-software/pypi/commit/f96957e4b2c5d05f131162134f94ea40f9871799))

- Revert labeler.yml to ubuntu-latest (public repo, hosted-only)
  ([#130](https://github.com/resq-software/pypi/pull/130),
  [`f96957e`](https://github.com/resq-software/pypi/commit/f96957e4b2c5d05f131162134f94ea40f9871799))

- Revert pr-size-labeler.yml to ubuntu-latest (public repo, hosted-only)
  ([#130](https://github.com/resq-software/pypi/pull/130),
  [`f96957e`](https://github.com/resq-software/pypi/commit/f96957e4b2c5d05f131162134f94ea40f9871799))

- Revert self-hosted toggle on this public repo (hosted-only)
  ([#130](https://github.com/resq-software/pypi/pull/130),
  [`f96957e`](https://github.com/resq-software/pypi/commit/f96957e4b2c5d05f131162134f94ea40f9871799))

- Route api-docs.yml to self-hosted runner ([#129](https://github.com/resq-software/pypi/pull/129),
  [`ddee31d`](https://github.com/resq-software/pypi/commit/ddee31d5ae11a21c4c545294b760cf6d69b1cf41))

- Route ci.yml to self-hosted runner ([#129](https://github.com/resq-software/pypi/pull/129),
  [`ddee31d`](https://github.com/resq-software/pypi/commit/ddee31d5ae11a21c4c545294b760cf6d69b1cf41))

- Route conventional-title-labeler.yml to self-hosted runner
  ([#129](https://github.com/resq-software/pypi/pull/129),
  [`ddee31d`](https://github.com/resq-software/pypi/commit/ddee31d5ae11a21c4c545294b760cf6d69b1cf41))

- Route dependency-review.yml to self-hosted runner
  ([#129](https://github.com/resq-software/pypi/pull/129),
  [`ddee31d`](https://github.com/resq-software/pypi/commit/ddee31d5ae11a21c4c545294b760cf6d69b1cf41))

- Route label-sync.yml to self-hosted runner
  ([#129](https://github.com/resq-software/pypi/pull/129),
  [`ddee31d`](https://github.com/resq-software/pypi/commit/ddee31d5ae11a21c4c545294b760cf6d69b1cf41))

- Route labeler.yml to self-hosted runner ([#129](https://github.com/resq-software/pypi/pull/129),
  [`ddee31d`](https://github.com/resq-software/pypi/commit/ddee31d5ae11a21c4c545294b760cf6d69b1cf41))

- Route pr-size-labeler.yml to self-hosted runner
  ([#129](https://github.com/resq-software/pypi/pull/129),
  [`ddee31d`](https://github.com/resq-software/pypi/commit/ddee31d5ae11a21c4c545294b760cf6d69b1cf41))

- Stop recurring Release + security workflow failures on main
  ([#47](https://github.com/resq-software/pypi/pull/47),
  [`e5fd1e2`](https://github.com/resq-software/pypi/commit/e5fd1e2f84043a2491f6bc5ac299bfd33fde0a40))

- Wire org-wide security-scan + dependabot + CODEOWNERS
  ([#19](https://github.com/resq-software/pypi/pull/19),
  [`9a3c888`](https://github.com/resq-software/pypi/commit/9a3c88830485872ef804223b46b2910881cb722d))

- **ai-auditor**: Re-run audit on PR updates, not just on open
  ([#88](https://github.com/resq-software/pypi/pull/88),
  [`d771812`](https://github.com/resq-software/pypi/commit/d77181239e1e24d4a71441d3bbeae418810aafaa))

- **ai-auditor**: Switch engine to gemini (avoid Copilot utility-model 429)
  ([#56](https://github.com/resq-software/pypi/pull/56),
  [`c1b1eef`](https://github.com/resq-software/pypi/commit/c1b1eef01ebd9b6e5b9b99097d9f7fd2cabfdcd2))

- **api-docs**: Cross-link package overview re-export stubs
  ([#41](https://github.com/resq-software/pypi/pull/41),
  [`ece8971`](https://github.com/resq-software/pypi/commit/ece897168699e52ef60522342b03c20f7b504c2f))

- **api-docs**: Disable uv cache to close cache-poisoning alert (#44)
  ([#48](https://github.com/resq-software/pypi/pull/48),
  [`de461aa`](https://github.com/resq-software/pypi/commit/de461aa4a8be8f0d546ca37efda15137e354fe0b))

- **api-docs**: Include docs.json in PR add-paths
  ([#40](https://github.com/resq-software/pypi/pull/40),
  [`85b41cf`](https://github.com/resq-software/pypi/commit/85b41cfe66c5b3278f63e9ff242cdb9745e325ec))

- **api-docs**: Sync workflow from resq-software/docs
  ([#46](https://github.com/resq-software/pypi/pull/46),
  [`5adde56`](https://github.com/resq-software/pypi/commit/5adde5630d7262c6ecf6729d0d4d9c5bbe887a68))

- **api-docs**: Sync workflow from resq-software/docs
  ([#45](https://github.com/resq-software/pypi/pull/45),
  [`096e62c`](https://github.com/resq-software/pypi/commit/096e62cbb86033551943fdbcae55732ac5c3c4a6))

- **api-docs**: Sync workflow from resq-software/docs
  ([#44](https://github.com/resq-software/pypi/pull/44),
  [`6089787`](https://github.com/resq-software/pypi/commit/6089787cc6426c70123961af979cbe5558059a40))

- **api-docs**: Sync workflow from resq-software/docs
  ([#43](https://github.com/resq-software/pypi/pull/43),
  [`a1da2e6`](https://github.com/resq-software/pypi/commit/a1da2e66c6cd49cd7ea13fafe7fd38793a714b0e))

- **dependabot**: Wildcard the gh-aw-actions ignore so it actually matches sub-actions
  ([#56](https://github.com/resq-software/pypi/pull/56),
  [`c1b1eef`](https://github.com/resq-software/pypi/commit/c1b1eef01ebd9b6e5b9b99097d9f7fd2cabfdcd2))

- **deps**: Point pip Dependabot at package dirs, not repo root
  ([#53](https://github.com/resq-software/pypi/pull/53),
  [`cae27ad`](https://github.com/resq-software/pypi/commit/cae27ad86f3a41ddc8c2113aa382a258d5e3f7c9))

- **docs**: Add api-docs workflow rendering lazydocs output
  ([#30](https://github.com/resq-software/pypi/pull/30),
  [`3e2b71e`](https://github.com/resq-software/pypi/commit/3e2b71e38972c349d069ab69cb6e0953ff1d4965))

- **docs**: Splice _pages.json into docs.json nav
  ([#38](https://github.com/resq-software/pypi/pull/38),
  [`360b329`](https://github.com/resq-software/pypi/commit/360b329ec84c504ff0f442536d17fe094a4ce0a6))

- **docs**: Sync template fixes from resq-software/docs#18
  ([#31](https://github.com/resq-software/pypi/pull/31),
  [`bb21dab`](https://github.com/resq-software/pypi/commit/bb21dab73c99e1044865f2c42074d5b4a3b340b7))

- **release**: Prepare releases through a PR instead of a blocked push
  ([#149](https://github.com/resq-software/pypi/pull/149),
  [`90ed6e8`](https://github.com/resq-software/pypi/commit/90ed6e8c4bb815dbc3648acda65667081c0b44bc))

- **security**: Enable Semgrep SAST ([#22](https://github.com/resq-software/pypi/pull/22),
  [`86c8027`](https://github.com/resq-software/pypi/commit/86c80278f58e28ee096914dcd4ee3c65c959bc33))

- **security**: Resolve zizmor findings + fix security workflow startup
  ([#34](https://github.com/resq-software/pypi/pull/34),
  [`0c7b1bc`](https://github.com/resq-software/pypi/commit/0c7b1bcc0ade8eaae8fe1778e5cfb98c3ff9c126))

- **security**: Stop declaring advanced CodeQL; default setup owns it
  ([#132](https://github.com/resq-software/pypi/pull/132),
  [`ff7d53a`](https://github.com/resq-software/pypi/commit/ff7d53a26a78fb9d9a05d57b7d59da5bfadcbc00))

- **zizmor**: Suppress template-injection in gh-aw generated workflows
  ([#59](https://github.com/resq-software/pypi/pull/59),
  [`8f8f203`](https://github.com/resq-software/pypi/commit/8f8f20357ad00cc5e4cfbe34c08b9ba38ee2ac1d))

### Documentation

- Polish READMEs with badges, Mermaid diagrams, and expanded examples
  ([`d5d99aa`](https://github.com/resq-software/pypi/commit/d5d99aa77325912f44a4f5e0da644e1f7fd56cb5))

- Reconcile the docs with the machinery, repair the resq shim
  ([#104](https://github.com/resq-software/pypi/pull/104),
  [`91da501`](https://github.com/resq-software/pypi/commit/91da50178d789dbb923a6d30fdbb7f65f91d2cdc))

- Restore verbatim Apache-2.0 license text ([#94](https://github.com/resq-software/pypi/pull/94),
  [`4c8bfcd`](https://github.com/resq-software/pypi/commit/4c8bfcd619dd84f8b5af05ebbbd97cc93d92f042))

- **ci**: Name the changelog aggregator generically in workflow comments
  ([#124](https://github.com/resq-software/pypi/pull/124),
  [`62fbfd1`](https://github.com/resq-software/pypi/commit/62fbfd12a6289dbdc4d4d93325152f705790c90b))

- **resq-mcp**: Correct security/audit/ratelimit docstring claims
  ([#76](https://github.com/resq-software/pypi/pull/76),
  [`5d127c0`](https://github.com/resq-software/pypi/commit/5d127c0daf6e7ee1d562282fa5eda42f3119891e))

- **resq-mcp**: Document telemetry helpers and pin docstring gate at 100
  ([#87](https://github.com/resq-software/pypi/pull/87),
  [`a62e01a`](https://github.com/resq-software/pypi/commit/a62e01abb46ec8591ecb3c404ae858b9003d47b0))

- **resq-mcp**: Drop a cross-repository reference from the changelog
  ([#146](https://github.com/resq-software/pypi/pull/146),
  [`9ba70f4`](https://github.com/resq-software/pypi/commit/9ba70f4731ea33246307cc8c0a92284587e9ecbe))

- **resq-mcp**: Note that denial auditing is conditional on RESQ_AUDIT_ENABLED
  ([#87](https://github.com/resq-software/pypi/pull/87),
  [`a62e01a`](https://github.com/resq-software/pypi/commit/a62e01abb46ec8591ecb3c404ae858b9003d47b0))

- **resq-mcp**: Refine audit hashing caveats per review
  ([#76](https://github.com/resq-software/pypi/pull/76),
  [`5d127c0`](https://github.com/resq-software/pypi/commit/5d127c0daf6e7ee1d562282fa5eda42f3119891e))

### Features

- **fleet-api**: Add drone fleet management API
  ([#98](https://github.com/resq-software/pypi/pull/98),
  [`8bfa77c`](https://github.com/resq-software/pypi/commit/8bfa77c5ae83b0f12e1b363a5170dc7a1a7b2b6c))

- **resq-agent**: Add linear assess → validate → strategy graph
  ([#117](https://github.com/resq-software/pypi/pull/117),
  [`422ed89`](https://github.com/resq-software/pypi/commit/422ed89cdf7cad252aea86865c027a48d5d130ac))

- **resq-agent**: Connect to resq-mcp and list its tools
  ([#116](https://github.com/resq-software/pypi/pull/116),
  [`801ce5e`](https://github.com/resq-software/pypi/commit/801ce5ed3aee9605417cd6c0d0904717bbbb2b04))

- **resq-mcp**: Adopt FastMCP 4 and MCP SDK 2 (protocol 2026-07-28)
  ([#114](https://github.com/resq-software/pypi/pull/114),
  [`e4f1db2`](https://github.com/resq-software/pypi/commit/e4f1db25f548dd3b1641294abe4f807bcd03305d))

- **resq-mcp**: Call fleet-api over HTTP for roster, swarm, and dispatch
  ([#112](https://github.com/resq-software/pypi/pull/112),
  [`613d008`](https://github.com/resq-software/pypi/commit/613d008f072023ac76a0d97e76e4a58bf1b0b30a))

- **resq-mcp**: Expose drone fleet telemetry and deployment tools
  ([#83](https://github.com/resq-software/pypi/pull/83),
  [`b63e098`](https://github.com/resq-software/pypi/commit/b63e098df630f07fd7e52343641928b934365a45))

- **resq-mcp**: Expose PDIE and drone fleet tools
  ([#83](https://github.com/resq-software/pypi/pull/83),
  [`b63e098`](https://github.com/resq-software/pypi/commit/b63e098df630f07fd7e52343641928b934365a45))

- **resq-mcp**: Expose PDIE vulnerability and alert tools
  ([#83](https://github.com/resq-software/pypi/pull/83),
  [`b63e098`](https://github.com/resq-software/pypi/commit/b63e098df630f07fd7e52343641928b934365a45))

- **resq-mcp**: Harden per NSA MCP security guidance (PP-26-1834)
  ([#58](https://github.com/resq-software/pypi/pull/58),
  [`21f8afd`](https://github.com/resq-software/pypi/commit/21f8afd7724bb9458355362ad9cc050a4ddfefe6))

- **resq-mcp**: MCP security hardening per NSA PP-26-1834 + transport env fix
  ([#58](https://github.com/resq-software/pypi/pull/58),
  [`21f8afd`](https://github.com/resq-software/pypi/commit/21f8afd7724bb9458355362ad9cc050a4ddfefe6))

### Refactoring

- **resq-mcp**: Address CodeRabbit review feedback
  ([#58](https://github.com/resq-software/pypi/pull/58),
  [`21f8afd`](https://github.com/resq-software/pypi/commit/21f8afd7724bb9458355362ad9cc050a4ddfefe6))

- **resq-mcp**: Address review feedback on hardening controls
  ([#58](https://github.com/resq-software/pypi/pull/58),
  [`21f8afd`](https://github.com/resq-software/pypi/commit/21f8afd7724bb9458355362ad9cc050a4ddfefe6))

- **resq-mcp**: Hash full result payloads in tool audit records
  ([#86](https://github.com/resq-software/pypi/pull/86),
  [`5e643cc`](https://github.com/resq-software/pypi/commit/5e643cc417268b7d81ba262779b66e23c1607d77))


## v1.3.3 (2026-04-09)

### Bug Fixes

- **ci**: Accept Polynomial in complexity tests, lower coverage to 85%
  ([`a2cb90e`](https://github.com/resq-software/pypi/commit/a2cb90e5e791e29417603291ee21d8df07065b64))

### Chores

- Sync from the internal source repository
  ([`b61e05d`](https://github.com/resq-software/pypi/commit/b61e05d8bd985eeaba732d3673a9de0fbfc8cf90))

- Sync from the internal source repository
  ([`727513e`](https://github.com/resq-software/pypi/commit/727513e5ebe875100c39d0b6ff0d668eb89ca5c1))

### Refactoring

- Restructure into packages/ workspace layout
  ([`447f128`](https://github.com/resq-software/pypi/commit/447f128b80c1c7a6c55847cc92916efcf4bf9bae))


## v1.2.1 (2026-03-28)

### Bug Fixes

- **ci**: Add resq-dsa CI and publish workflow, scope Docker to resq-mcp
  ([`74a84c9`](https://github.com/resq-software/pypi/commit/74a84c92748458cf1e4fed1ac50a397625101958))

- Create publish-dsa.yml for tag-based PyPI publishing of resq-dsa - Create ci-dsa.yml for resq-dsa
  lint/test/typecheck - Add path filters to existing ci.yml to only trigger for resq-mcp changes -
  Docker builds now scoped to resq-mcp changes only

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### Documentation

- Comprehensive workspace README, AGENTS.md, and CLAUDE.md
  ([`377e17e`](https://github.com/resq-software/pypi/commit/377e17e8143ad0bc2b7808c3c3e23b9cb9ffc120))


## v1.2.0 (2026-03-27)

### Bug Fixes

- **ci**: Resolve Python 3.13 OutsideDestinationError for readme path
  ([`09ce6b8`](https://github.com/resq-software/pypi/commit/09ce6b83e96a5f418075d23d615a2c5343d54d98))

### Chores

- Update repo references after rename mcp → pypi
  ([`c826660`](https://github.com/resq-software/pypi/commit/c826660f7b911a9ca973150e4c6064f6afbf430d))

### Features

- Add resq-dsa package — zero-dependency DSA library
  ([`304bf92`](https://github.com/resq-software/pypi/commit/304bf92d6f32ec75f26e9a3a4ec3cbab8711e778))

Bloom filter, Count-Min sketch, Graph (BFS/Dijkstra/A*), Bounded Heap, Trie + Rabin-Karp. Python
  3.11+, zero dependencies.

### Refactoring

- Convert to packages/ workspace layout
  ([`37c8acd`](https://github.com/resq-software/pypi/commit/37c8acde188afb286399c2d83832eec338b6738e))

Move resq-mcp into packages/resq-mcp/ to support multiple Python packages in this repo. All
  workflows updated.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### Testing

- Add algorithmic complexity verification tests
  ([`596d171`](https://github.com/resq-software/pypi/commit/596d1718b1c3b83455164d0f4498fb08373d3de5))

Uses big_o to empirically verify Big-O guarantees: BloomFilter O(1), BoundedHeap O(log n), Graph
  Dijkstra O(E log V), BFS O(V+E), Trie O(L), CountMinSketch O(1).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>


## v1.1.2 (2026-03-23)

### Bug Fixes

- **ci**: Skip TestPyPI publish for dependabot PRs
  ([`1e31d0c`](https://github.com/resq-software/pypi/commit/1e31d0cebd5561fd5bc03d886dba7186179c3dca))

Dependabot PRs only change workflow YAML, not Python code. The OIDC Trusted Publisher on TestPyPI
  isn't configured for dependabot, causing invalid-publisher failures that block CI status checks.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### Chores

- **deps**: Bump pascalgn/size-label-action ([#8](https://github.com/resq-software/pypi/pull/8),
  [`ee8b496`](https://github.com/resq-software/pypi/commit/ee8b496d5481db2434fff8fd6a57340c054d5672))

Bumps the actions-minor-patch group with 1 update:
  [pascalgn/size-label-action](https://github.com/pascalgn/size-label-action).

Updates `pascalgn/size-label-action` from 0.5.5 to 0.5.7 - [Release
  notes](https://github.com/pascalgn/size-label-action/releases) -
  [Commits](https://github.com/pascalgn/size-label-action/compare/f8edde36b3be04b4f65dcfead05dc8691b374348...56b489b027932ec0cf60438a1a5f1a19c8fc71ff)

--- updated-dependencies: - dependency-name: pascalgn/size-label-action dependency-version: 0.5.7

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: actions-minor-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Code Style

- Format test_errors_extended and test_telemetry_extended
  ([`ca9ccfb`](https://github.com/resq-software/pypi/commit/ca9ccfbed97f372f69a21b34b93d1702b5af7d26))

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### Documentation

- Add missing OTEL telemetry env vars to configuration table
  ([`8f4160c`](https://github.com/resq-software/pypi/commit/8f4160cdc92a576b8af9dcb2cdf8e46f2e87b1ee))


## v1.1.1 (2026-03-22)

### Bug Fixes

- Address PR #7 review findings across workflows and source
  ([`d85460d`](https://github.com/resq-software/pypi/commit/d85460dd370d38ab79be64871d4484cb5fd45a83))

Workflows: - publish.yml: gate publish-pypi on sign + attestation completion - publish.yml: SBOM now
  scans built artifacts (dist/) not source tree - ci.yml: skip TestPyPI on fork PRs (OIDC tokens
  unavailable) - sync-to-mono.yml: remove duplicated commit+push step

Source: - errors.py: add default=str to json.dumps to prevent serialization crash - pdie/models.py:
  add Pydantic field constraints (ge/le/gt) on risk scores, probability, and forecast_horizon_hours

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>


## v1.1.0 (2026-03-22)

### Features

- Publish Docker image to GHCR and revamp README
  ([`40b01ab`](https://github.com/resq-software/pypi/commit/40b01abe99925dfb1b37ec2e7bf63ab420546d7d))

Add GHCR login and push tags to the release workflow so the container image appears under the repo's
  Packages sidebar alongside Docker Hub.

Restructure README with Playwright-inspired collapsible client setup sections (VS Code, Claude
  Desktop, Claude Code, Cursor, Windsurf, Docker) and add Docker/GHCR badges.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>


## v1.0.4 (2026-03-21)

### Performance Improvements

- **ci**: Sync directly to monorepo main instead of creating PRs
  ([`5f261f4`](https://github.com/resq-software/pypi/commit/5f261f45c9165bcb5561848a3a746d5b78015b5f))

Eliminates redundant monorepo CI runs on sync PRs. Satellite CI already validates the code before
  sync.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>


## v1.0.3 (2026-03-21)

### Performance Improvements

- **ci**: Enable uv dependency caching in CI
  ([`16f2c16`](https://github.com/resq-software/pypi/commit/16f2c16bde13e9e37f68fb8a5caabcea8603667f))

Adds enable-cache: true to all setup-uv steps, reducing dependency installation time across lint,
  typecheck, security, and test jobs.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>


## v1.0.2 (2026-03-21)

### Bug Fixes

- **test**: Resolve ruff lint violations in test files
  ([`f1e5d71`](https://github.com/resq-software/pypi/commit/f1e5d718dd813bdda00e729d27137f7f4f065195))

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### Documentation

- Add VS Code MCP config and expand README
  ([`497a4cd`](https://github.com/resq-software/pypi/commit/497a4cda968974b8c9924c184fae24edc4058859))

Add .vscode/mcp.json for out-of-the-box MCP server discovery in VS Code and Cursor. Expand README
  with VS Code/Cursor setup guide, module overview, full tool/resource/prompt reference tables, and
  example workflows.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### Testing

- Add tests to reach 90% coverage threshold
  ([`a30d543`](https://github.com/resq-software/pypi/commit/a30d543c6f0c433591d98612495809b9310ec341))

Coverage: 79.78% → 91.61%

New test coverage for: - MCPErrorFormatter: KeyError, TimeoutError, unknown errors, context
  redaction, http_status - Timeout: NaN/inf handling, invalid env var fallback - Telemetry:
  sanitize_attrs, redact_log_message, truncate, NoOp classes, Metrics lazy init, trace decorator
  (sync/async + exceptions), span context manager, log_event, get_trace_context, shutdown - Server:
  _process_simulation (complete, evicted, notify failure, cancelled), lifespan start/stop,
  simulation capacity limit - Resources: failed simulation status

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>


## v1.0.1 (2026-03-21)

### Bug Fixes

- **ci**: Pin actions to SHA hashes and add permissions
  ([`6040035`](https://github.com/resq-software/pypi/commit/6040035a66ef63da44b491dfa786c38aa305ecd7))

Resolves code scanning alerts for unpinned actions and missing permissions blocks.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### Code Style

- Format Python files with ruff
  ([`ce0ef54`](https://github.com/resq-software/pypi/commit/ce0ef545f1405471b2e176a6d8711a325d5adab1))

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>


## v1.0.0 (2026-03-18)

### Features

- 🚀 implement telemetry and harden tool security guards
  ([`48edde3`](https://github.com/resq-software/pypi/commit/48edde32aaae939d28f7d57299933178840ab3ac))

- Integrate OpenTelemetry SDK with OTLP and console backend support - Add TTL-based eviction for
  incidents, missions, and simulations - Implement capacity, conflict, and idempotency guards for
  tools - Harden prompts against injection using incident ID validation - Switch to explicit urgency
  flags for mission risk tolerance

BREAKING CHANGE: get_deployment_strategy now requires incidents to be validated via
  validate_incident before a strategy can be requested.

### Breaking Changes

- Get_deployment_strategy now requires incidents to be validated via validate_incident before a
  strategy can be requested.


## v0.4.0 (2026-03-18)

### Continuous Integration

- Drop Python 3.14-dev from test matrix (not yet supported by uv)
  ([`b41ff8c`](https://github.com/resq-software/pypi/commit/b41ff8c0da34b878d7bc66ada96325544cb16654))

### Features

- **core**: 📡 implement telemetry subsystem and enhance server safety
  ([`46e558b`](https://github.com/resq-software/pypi/commit/46e558b71f0289c27e0696d5500a1a68f35ea2b5))

Implement a comprehensive OpenTelemetry-based telemetry subsystem and strengthen server-side
  operational guards.

- Implement OpenTelemetry subsystem with PII scrubbing and async decorators - Add mission parameter
  tools and idempotency guards for incident validation - Refactor simulation processor for
  concurrent execution and orphan recovery - Introduce capacity limits and TTL-based eviction for
  simulation state - Improve security using timing-attack resistant credential comparison - Overhaul
  documentation including README, AGENTS.md, and CLAUDE.md - Add environment variable validation on
  server startup


## v0.3.4 (2026-03-17)

### Bug Fixes

- **ci**: Use GitHub API directly for release asset uploads (avoids immutable release error)
  ([`92fc25f`](https://github.com/resq-software/pypi/commit/92fc25fb01fb557d0fbfceb03f3063bb4c199d62))


## v0.3.3 (2026-03-17)

### Bug Fixes

- **ci**: Use softprops/action-gh-release for asset uploads
  ([`ba8a0cd`](https://github.com/resq-software/pypi/commit/ba8a0cd0e135d8b2be5933706b95ab29e7b4d4b4))


## v0.3.2 (2026-03-17)

### Bug Fixes

- **ci**: Use --clobber for release asset uploads to handle re-runs
  ([`9390cf2`](https://github.com/resq-software/pypi/commit/9390cf2fe0098301c612d09472b5b4faa353c0a4))


## v0.3.1 (2026-03-17)

### Bug Fixes

- **ci**: Use PYPI_TOKEN for publishing, pin sigstore action version
  ([`39d50cd`](https://github.com/resq-software/pypi/commit/39d50cdd05444c5c0dbbfd6d23476d4b61a39a5a))

- Fall back to PYPI_TOKEN secret until Trusted Publisher is configured on pypi.org for the
  resq-software org - Pin sigstore/gh-action-sigstore-python to v3.2.0 (v3 major tag doesn't exist)

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>


## v0.3.0 (2026-03-17)

### Chores

- **deps**: Bump astral-sh/setup-uv from 5 to 7 ([#4](https://github.com/resq-software/pypi/pull/4),
  [`f0a2b99`](https://github.com/resq-software/pypi/commit/f0a2b99025d58d1bb9c5b0f9cf73121cc6b4f492))

Bumps [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv) from 5 to 7. - [Release
  notes](https://github.com/astral-sh/setup-uv/releases) -
  [Commits](https://github.com/astral-sh/setup-uv/compare/v5...v7)

--- updated-dependencies: - dependency-name: astral-sh/setup-uv dependency-version: '7'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump codecov/codecov-action from 4 to 5
  ([#6](https://github.com/resq-software/pypi/pull/6),
  [`68dc997`](https://github.com/resq-software/pypi/commit/68dc997a7dbcecbe47e720704bbd52ed9510de16))

Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 4 to 5. - [Release
  notes](https://github.com/codecov/codecov-action/releases) -
  [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/codecov/codecov-action/compare/v4...v5)

--- updated-dependencies: - dependency-name: codecov/codecov-action dependency-version: '5'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump docker/login-action from 3 to 4
  ([#5](https://github.com/resq-software/pypi/pull/5),
  [`8fc2f3a`](https://github.com/resq-software/pypi/commit/8fc2f3ade2778ac00533cbb88744434ae173c1d5))

Bumps [docker/login-action](https://github.com/docker/login-action) from 3 to 4. - [Release
  notes](https://github.com/docker/login-action/releases) -
  [Commits](https://github.com/docker/login-action/compare/v3...v4)

--- updated-dependencies: - dependency-name: docker/login-action dependency-version: '4'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Documentation

- Update README with AI-generated content
  ([`03842df`](https://github.com/resq-software/pypi/commit/03842df248556abcab6ecb85d7602143f5729920))

- Update README with AI-generated content
  ([`81ace88`](https://github.com/resq-software/pypi/commit/81ace886419536b925e7b8d4adabceb669ea2dab))

- Update README with AI-generated content
  ([`1af74e4`](https://github.com/resq-software/pypi/commit/1af74e4af68848d6c277d2c3ca219aafa3c24814))

### Features

- Enterprise-grade publishing, CI hardening, test quality & domain restructure
  ([`9de8b21`](https://github.com/resq-software/pypi/commit/9de8b214974bb68693907f88af1e99d8709e2400))

## What changed

### CI/CD & Publishing - OIDC Trusted Publisher for PyPI (no API tokens) - Sigstore artifact signing
  + build attestation with verification - CycloneDX SBOM generation attached to GitHub Releases - CI
  matrix: Python 3.11, 3.12, 3.13, 3.14-dev - Separate lint, typecheck, security gates → test →
  build-verify pipeline - TestPyPI publish on PRs after full pipeline passes - py.typed marker (PEP
  561)

### Test Quality - 94 → 156 tests, 85% → 92% coverage with enforced gate - Hypothesis property-based
  testing for Pydantic models - Integration tests: 3 cross-module workflows - Probabilistic
  distribution tests for drone tools - Edge case tests across all domain modules - Factory fixtures
  in conftest.py

### Domain Restructure - Flat 13-file package → 5 domain packages (core, drone, dtsop, hce, pdie) -
  server.py split into server + resources + prompts - models.py split into domain-specific model
  files - Tests reorganized into unit/, integration/, property/

### Enterprise Utilities - MCPErrorFormatter: structured JSON errors with context redaction -
  Centralized timeout config with env-var override and exponential backoff

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>


## v0.2.0 (2026-03-15)

### Bug Fixes

- **ci**: Harden release and docker publish
  ([`138107f`](https://github.com/resq-software/pypi/commit/138107f2411081b8ab417bccbe2a124036cc3fa4))

- **ci**: Use main branch in release workflow and semantic-release config
  ([`76327fc`](https://github.com/resq-software/pypi/commit/76327fc124d4a6928bdb40497aafff83568b1dd5))

- **release**: Install uv in PSR Docker container before building
  ([`412b17b`](https://github.com/resq-software/pypi/commit/412b17bed10388e959c957967c6214a5957c7828))

The python-semantic-release action runs in an isolated Docker container where the uv binary (set up
  by setup-uv on the runner) is not available. Prepend `pip install uv` to the build_command so uv
  is present at build time.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Chores

- Add dev tooling — hooks, skills, agents, codecov, dependabot
  ([`98740d8`](https://github.com/resq-software/pypi/commit/98740d873f7bd20ce17918de432931e79e68d70a))

- Add .git-hooks/ (pre-commit, commit-msg, prepare-commit-msg, post-checkout, post-merge, pre-push)
  with resq-cli delegation, OSV scan, secrets scan, and ruff check/format - Add scripts/setup.sh
  with core.hooksPath wiring and Nix bootstrap - Add bootstrap.sh root alias for scripts/setup.sh -
  Add flake.nix devShell with osv-scanner, Python 3.12, and uv - Add .github/skills/
  (feynman-auditor, nemesis-auditor, state-inconsistency-auditor) - Add .github/agents/,
  .github/commands/, .github/rules/ for FastMCP context - Add .github/dependabot.yml with pip +
  github-actions and minor/patch grouping - Add .github/workflows/auto-merge.yml for Dependabot PRs
  - Update .github/workflows/ci.yml with pytest --cov and Codecov upload - Add CLAUDE.md + AGENTS.md
  agent guide - Add agent-sync.sh to keep AGENTS.md and CLAUDE.md in sync

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- **deps**: Bump actions/checkout from 4 to 6 ([#3](https://github.com/resq-software/pypi/pull/3),
  [`13a86b1`](https://github.com/resq-software/pypi/commit/13a86b13e086db79ef7d05cf666e3ebf7e2ca6cf))

Bumps [actions/checkout](https://github.com/actions/checkout) from 4 to 6. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/actions/checkout/compare/v4...v6)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump docker/build-push-action from 6 to 7
  ([#2](https://github.com/resq-software/pypi/pull/2),
  [`ddd2abf`](https://github.com/resq-software/pypi/commit/ddd2abf47d4fe2176b148eec939a9d6e1ded82f7))

Bumps [docker/build-push-action](https://github.com/docker/build-push-action) from 6 to 7. -
  [Release notes](https://github.com/docker/build-push-action/releases) -
  [Commits](https://github.com/docker/build-push-action/compare/v6...v7)

--- updated-dependencies: - dependency-name: docker/build-push-action dependency-version: '7'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump python-semantic-release/publish-action from 9 to 10
  ([#1](https://github.com/resq-software/pypi/pull/1),
  [`9744bdc`](https://github.com/resq-software/pypi/commit/9744bdcc28d70c3eff3fe77aac045d365c7336ec))

Bumps
  [python-semantic-release/publish-action](https://github.com/python-semantic-release/publish-action)
  from 9 to 10. - [Release
  notes](https://github.com/python-semantic-release/publish-action/releases) -
  [Changelog](https://github.com/python-semantic-release/publish-action/blob/main/releaserc.toml) -
  [Commits](https://github.com/python-semantic-release/publish-action/compare/v9...v10)

--- updated-dependencies: - dependency-name: python-semantic-release/publish-action
  dependency-version: '10'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Continuous Integration

- Add PR labeler and label-sync workflows
  ([`e9a8f64`](https://github.com/resq-software/pypi/commit/e9a8f64e599debf453ba916ca9d8b7ba79927d80))

- .github/labels.yml — standardized label definitions - .github/labeler.yml — path-based PR labels
  per area - workflows/labeler.yml — actions/labeler@v6 on PR open/sync - workflows/label-sync.yml —
  EndBug/label-sync@v2 on labels.yml change - workflows/pr-size-labeler.yml — XS/S/M/L/XL size
  labels ignoring uv.lock

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Auto-release with python-semantic-release on push to master
  ([`5f64574`](https://github.com/resq-software/pypi/commit/5f64574e726f53d8b694edef7f7cf3701851ba45))

### Features

- **ci**: Inbound sync — create PR in resQ monorepo on push to main
  ([`7feb7c6`](https://github.com/resq-software/pypi/commit/7feb7c6393b4172a22e03c60dc642055914275f0))

Requires SYNC_TOKEN secret with repo write access to resq-software/resQ.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


## v0.1.0 (2026-03-12)

### Bug Fixes

- **ci**: Remove invalid job-level if conditions using secrets context
  ([`f873a67`](https://github.com/resq-software/pypi/commit/f873a6788890553cf6311f2d90debcc1e39688ff))

secrets.* is not supported in job-level if: conditions for push-triggered workflows — it causes a
  workflow parse error. Reverted to plain jobs; publish will fail with auth errors until secrets are
  configured.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- **ci**: Remove monorepo-internal dep, fix Dockerfile README copy
  ([`dd69e1b`](https://github.com/resq-software/pypi/commit/dd69e1b468fedfe6f85d0bbeedd91488f87a0b51))

- **ci**: Replace monorepo resq.exceptions with local ConfigurationError
  ([`424eb76`](https://github.com/resq-software/pypi/commit/424eb76f2a02b3a1620cbd358621f270212f3757))

- **ci**: Skip publish jobs when secrets are not configured
  ([`2a37638`](https://github.com/resq-software/pypi/commit/2a37638b0a17df3229d89b3aa7d8c0caac5aa3dc))

Guard publish-pypi and publish-docker jobs with if conditions so the workflow doesn't fail when
  PYPI_TOKEN / DOCKERHUB credentials haven't been added as repo secrets yet.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- **tests**: Replace deprecated FastMCP .fn attribute with direct calls
  ([`20dfc4e`](https://github.com/resq-software/pypi/commit/20dfc4e226e33b90b7e172fe3dcf98d93c062732))

FastMCP no longer wraps decorated functions with a .fn attribute — the decorators now return the
  original async function unchanged, so calling .fn raised AttributeError. Updated
  TestGetSimulationStatus and TestValidateIncident to call functions directly.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Continuous Integration

- Test, docker build, and PyPI + Docker Hub publish workflows
  ([`aff9460`](https://github.com/resq-software/pypi/commit/aff9460c6b5dc8b25363ce72248e5b1c8ba05b15))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Features

- Initial ResQ MCP server
  ([`ccdb37a`](https://github.com/resq-software/pypi/commit/ccdb37a0387ef8aae3e4465c079341085eed585f))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
