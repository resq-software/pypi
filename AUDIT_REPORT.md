# ResQ Software Multi-Registry Audit Report

**Date:** 2026-04-02
**Scope:** `crates`, `pypi`, `npm`, `vcpkg`
**Trigger:** Post-rehaul audit + PyPI org `resq-software` approval

---

## Executive Summary

Audited 4 repos containing **15 packages** across 4 registries. Found **8 critical issues**, **9 high-severity**, and **12 medium/low** issues. The most dangerous findings are publish-blocking misconfigurations (npm export paths, vcpkg missing portfile), CI badge/branch mismatches that hide broken builds, and missing license files that block registry compliance.

| Repo | Packages | Registry | Default Branch | Critical | High | Med/Low |
|------|----------|----------|----------------|----------|------|---------|
| **crates** | 10 | crates.io | `master` | 2 | 3 | 3 |
| **pypi** | 2 | PyPI | `main` | 1 | 2 | 3 |
| **npm** | 2 | npmjs | `master` | 2 | 2 | 4 |
| **vcpkg** | 1 | vcpkg registry | `main` | 3 | 1 | 2 |
| **Total** | **15** | | | **8** | **8** | **12** |

---

## Cross-Repo Mismatch Report

### Branch Strategy Inconsistency
| Repo | Default Branch | CI Branch | Badge Branch |
|------|---------------|-----------|--------------|
| crates | `master` | `master` | **`main`** (WRONG) |
| pypi | `main` | `main` | `main` |
| npm | `master` | `master` | `master` |
| vcpkg | `main` | `main` | `main` |

**Impact:** crates CI badge silently shows "failing" because it queries `?branch=main` but workflows run on `master`.

### Missing Root LICENSE Files
| Repo | LICENSE Present | License Declared |
|------|----------------|-----------------|
| crates | **NO** | Apache-2.0 |
| pypi | **NO** | Apache-2.0 |
| npm | YES (`LICENSE.md`) | Apache-2.0 |
| vcpkg | YES (`LICENSE`) | Apache-2.0 |

### DSA Package Parity (cross-registry)
Each repo has a "DSA" package with zero runtime dependencies:

| Registry | Package | Version | Publish Ready | Tests | CI |
|----------|---------|---------|---------------|-------|-----|
| crates.io | `resq-dsa` | 0.1.0 | YES (`publish=true`) | YES | YES |
| PyPI | `resq-dsa` | 0.1.0 | YES (manual tag) | YES | YES |
| npm | `@resq-sw/dsa` | 0.1.0 | YES (manual tag) | YES | YES |
| vcpkg | `resq-common` | 0.1.0 | **NO** (missing portfile) | YES | YES |

### Documentation Agent Files
| Repo | CLAUDE.md | AGENTS.md | Match? |
|------|-----------|-----------|--------|
| crates | **MISSING** | **MISSING** | N/A |
| pypi | YES | YES | Identical (correct per rules) |
| npm | YES | YES | Identical |
| vcpkg | YES | YES | Identical |

---

## Per-Repo Findings

---

### 1. CRATES (`/home/wombocombo/github/wrk/crates`)

**Packages:** 10 workspace members (resq-tui, resq-cli, resq-deploy-cli, resq-health-checker, resq-log-viewer, resq-perf-monitor, resq-flamegraph, resq-bin-explorer, resq-cleanup, resq-dsa)

#### CRITICAL

| # | Issue | File | Line | Impact |
|---|-------|------|------|--------|
| C1 | CI badge queries `branch=main` but all workflows use `master` | `README.md` | 19 | Badge falsely shows failing |
| C2 | Dockerfile copies `resq-tui` binary but it's lib-only (no bin target) | `Dockerfile` | ~70 | Docker build copies nonexistent binary |

#### HIGH

| # | Issue | File | Line | Impact |
|---|-------|------|------|--------|
| H1 | No root LICENSE file | repo root | - | Blocks crates.io compliance |
| H2 | Version inconsistency: cli=0.2.3, tui=0.1.4, dsa=0.1.0 vs workspace=0.1.6 | `Cargo.toml` (root) | 8 | Confusing version strategy |
| H3 | No CHANGELOG files in any crate | all crates | - | release-plz can't generate notes |

#### MEDIUM/LOW

| # | Issue | File | Impact |
|---|-------|------|--------|
| M1 | No CLAUDE.md/AGENTS.md | repo root | Inconsistent with other repos |
| M2 | No `.cargo/config.toml` | repo root | No custom build config |
| M3 | `bin_explorer` binary name doesn't match `resq-bin` pattern | `bin-explorer/Cargo.toml` | Inconsistent naming |

---

### 2. PYPI (`/home/wombocombo/github/wrk/pypi`)

**Packages:** 2 (resq-mcp v1.2.0, resq-dsa v0.1.0)

#### CRITICAL

| # | Issue | File | Line | Impact |
|---|-------|------|------|--------|
| C1 | resq-dsa missing `py.typed` marker | `packages/resq-dsa/src/resq_dsa/` | - | PEP 561: type hints invisible to consumers |

#### HIGH

| # | Issue | File | Line | Impact |
|---|-------|------|------|--------|
| H1 | No root LICENSE file | repo root | - | Package metadata references Apache-2.0 but no file |
| H2 | resq-dsa has no automated versioning (manual tag + bump) | `publish-dsa.yml` | - | Error-prone releases |

#### MEDIUM/LOW

| # | Issue | File | Impact |
|---|-------|------|--------|
| M1 | resq-dsa publish has no attestation/SBOM (unlike resq-mcp) | `.github/workflows/publish-dsa.yml` | Security parity gap |
| M2 | resq-dsa README has no CI/PyPI badges | `packages/resq-dsa/README.md` | Poor discoverability |
| M3 | resq-dsa has no CHANGELOG.md | `packages/resq-dsa/` | No release history |

---

### 3. NPM (`/home/wombocombo/github/wrk/npm`)

**Packages:** 2 (@resq-sw/ui v0.9.0, @resq-sw/dsa v0.1.0)

#### CRITICAL

| # | Issue | File | Line | Impact |
|---|-------|------|------|--------|
| C1 | `release.yml` checks wrong package name for GitHub Packages (`@resq-software/npm` vs `@resq-sw/ui`) | `.github/workflows/release.yml` | 113 | Always re-publishes; wasted CI |
| C2 | UI `./lib/utils` export has double path (`lib/lib/utils.js`) | `packages/ui/package.json` | 296-300 | `import { cn } from "@resq-sw/ui/lib/utils"` fails |

#### HIGH

| # | Issue | File | Line | Impact |
|---|-------|------|------|--------|
| H1 | Per-package READMEs missing (referenced in CLAUDE.md) | `packages/ui/`, `packages/dsa/` | - | Published packages have no docs |
| H2 | Inconsistent build tooling: UI uses tsdown, DSA uses tsc | both packages | - | Maintenance burden |

#### MEDIUM/LOW

| # | Issue | File | Impact |
|---|-------|------|--------|
| M1 | No `.npmignore` files | both packages | May publish unnecessary files |
| M2 | No per-package LICENSE files | both packages | npm best practice violation |
| M3 | AGENTS.md duplicates CLAUDE.md | repo root | Redundant |
| M4 | UI tsconfig sets `noEmit: true` but tsdown produces output | `packages/ui/tsconfig.json` | Confusing for maintainers |

---

### 4. VCPKG (`/home/wombocombo/github/wrk/vcpkg`)

**Packages:** 1 (resq-common v0.1.0)

#### CRITICAL

| # | Issue | File | Line | Impact |
|---|-------|------|------|--------|
| C1 | **No `portfile.cmake`** | `packages/resq-common/` | - | vcpkg cannot install this port at all |
| C2 | **No `versions/` directory** | repo root | - | No version tracking; not a valid registry |
| C3 | **No `baseline.json`** | repo root | - | Cannot establish default versions |

#### HIGH

| # | Issue | File | Line | Impact |
|---|-------|------|------|--------|
| H1 | `env_utils.hpp` has MIT license header, rest is Apache-2.0 | `packages/resq-common/include/resq/env_utils.hpp` | 1-10 | License inconsistency vs vcpkg.json |

#### MEDIUM/LOW

| # | Issue | File | Impact |
|---|-------|------|--------|
| M1 | CI has no vcpkg-specific test steps | `.github/workflows/ci.yml` | Never validates vcpkg install path |
| M2 | No `supports` field in vcpkg.json | `packages/resq-common/vcpkg.json` | Platform constraints undefined |

---

## Misplacement Report

| Item | Expected Location | Actual Location | Status |
|------|-------------------|-----------------|--------|
| `py.typed` marker (resq-dsa) | `packages/resq-dsa/src/resq_dsa/py.typed` | Not found | **MISSING** |
| Root LICENSE (crates) | `/crates/LICENSE` | Not found | **MISSING** |
| Root LICENSE (pypi) | `/pypi/LICENSE` | Not found | **MISSING** |
| Per-package READMEs (npm) | `packages/ui/README.md`, `packages/dsa/README.md` | Not found | **MISSING** |
| `portfile.cmake` (vcpkg) | `packages/resq-common/portfile.cmake` | Not found | **MISSING** |
| `versions/resq-common.json` (vcpkg) | `versions/r-/resq-common.json` | Not found | **MISSING** |
| `baseline.json` (vcpkg) | `versions/baseline.json` | Not found | **MISSING** |
| CLAUDE.md (crates) | `/crates/CLAUDE.md` | Not found | **MISSING** |
| AGENTS.md (crates) | `/crates/AGENTS.md` | Not found | **MISSING** |
| CHANGELOG.md (resq-dsa, pypi) | `packages/resq-dsa/CHANGELOG.md` | Not found | **MISSING** |
| CHANGELOG.md (all crates) | per-crate directories | Not found | **MISSING** |

---

## Severity-Ranked Remediation Plan

### P0 - Publish Blockers (fix before any release)

1. **vcpkg: Create `portfile.cmake`**
   - File: `packages/resq-common/portfile.cmake`
   - Content: `vcpkg_cmake_configure()`, `vcpkg_cmake_install()`, `vcpkg_cmake_config_fixup()`
   - Also create `versions/baseline.json` and `versions/r-/resq-common.json`

2. **npm: Fix `./lib/utils` export path**
   - File: `packages/ui/package.json` lines 296-300
   - Change `lib/lib/utils.{js,d.ts}` to `lib/utils.{js,d.ts}`

3. **npm: Fix release.yml package name**
   - File: `.github/workflows/release.yml` line 113
   - Change `@resq-software/npm` to `@resq-sw/ui`

4. **pypi: Add `py.typed` marker to resq-dsa**
   - Create empty file: `packages/resq-dsa/src/resq_dsa/py.typed`

### P1 - Compliance & Correctness (fix this week)

5. **crates + pypi: Add root LICENSE files**
   - Copy Apache-2.0 text to `/crates/LICENSE` and `/pypi/LICENSE`

6. **crates: Fix README badge branch**
   - File: `README.md` line 19
   - Change `?branch=main` to `?branch=master`

7. **crates: Remove `resq-tui` from Dockerfile COPY**
   - File: `Dockerfile` ~line 70
   - Remove the line copying nonexistent `resq-tui` binary

8. **vcpkg: Fix license header in `env_utils.hpp`**
   - File: `packages/resq-common/include/resq/env_utils.hpp` lines 1-10
   - Change MIT header to Apache-2.0

### P2 - Documentation & Parity (fix this sprint)

9. **npm: Create per-package READMEs**
   - Create `packages/ui/README.md` and `packages/dsa/README.md`

10. **crates: Add CLAUDE.md and AGENTS.md**
    - Create files matching the pattern from pypi/npm/vcpkg repos

11. **pypi: Add badges to resq-dsa README**
    - Add CI, PyPI version, and license badges

12. **pypi: Add CHANGELOG.md for resq-dsa**
    - Create `packages/resq-dsa/CHANGELOG.md`

### P3 - Automation & Hardening (next cycle)

13. **pypi: Automate resq-dsa versioning**
    - Add semantic-release config to `packages/resq-dsa/pyproject.toml`
    - Or adopt the tag-based workflow with version bump automation

14. **pypi: Add attestation/SBOM to resq-dsa publish**
    - Mirror the Sigstore attestation step from `publish.yml` to `publish-dsa.yml`

15. **npm: Standardize build tooling**
    - Either migrate DSA to tsdown or document the intentional divergence

16. **vcpkg: Add vcpkg install test to CI**
    - Add a CI step that runs `vcpkg install` using the local port overlay

17. **crates: Add CHANGELOG.md files**
    - Configure release-plz to generate per-crate changelogs

---

*Generated by parallel audit agents scanning all manifests, workflows, source layouts, and documentation across the resq-software organization.*
