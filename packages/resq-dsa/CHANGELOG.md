# CHANGELOG

<!-- version list -->

## v2.0.0 (2026-11-07)

### Bug Fixes

- Align comments with post-exclusion coverage numbers
  ([`09cf4f5`](https://github.com/resq-software/pypi/commit/09cf4f5f792ceba143e68e1ff4427894ac26fa38))

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


## v1.3.4 (2026-04-14)

### Bug Fixes

- **git-hooks**: Run ruff per-package (no root pyproject.toml)
  ([`8844892`](https://github.com/resq-software/pypi/commit/8844892522e3d712272e73dde231bda384133f2d))

### Chores

- **deps-dev**: Bump pytest
  ([`c48b2f9`](https://github.com/resq-software/pypi/commit/c48b2f905f6a415ad04a9082595c96f384af1d8e))

### Documentation

- **AGENTS**: Link canonical git-hooks contract + ruff check on pre-push
  ([`5275a27`](https://github.com/resq-software/pypi/commit/5275a27f49af2a0d6695655a4fb2388476aab810))


## v0.1.0 (2025-03-27)

### Features

- BloomFilter for space-efficient probabilistic set membership testing
- CountMinSketch for probabilistic frequency estimation
- Graph with BFS, Dijkstra, and A* pathfinding
- BoundedHeap for top-k queries
- Trie for prefix-based string storage and retrieval
- Rabin-Karp rolling hash string pattern matching
