# 09 — Dependencies and Version Resolution (Normative)

## 9.0 Purpose

This chapter defines how UAPF packages reference and resolve dependencies on other packages.

## 9.1 Dependency Declaration

### 9.1.1 In Manifest

A package MAY declare dependencies via the `includes` field:

```yaml
includes:
  - ../relative/path/to/package           # Workspace-relative
  - package:org.proc.shared@^1.0.0        # Registry reference with version
  - package:org.proc.utils@>=2.0.0,<3.0.0 # Range constraint
```

### 9.1.2 Reference Formats

| Format | Example | Resolution |
|--------|---------|------------|
| Relative path | `../shared/auth` | Resolved within workspace |
| Package exact | `package:id@1.2.3` | Exact version required |
| Package caret | `package:id@^1.2.0` | Compatible with 1.x.x (>=1.2.0 <2.0.0) |
| Package tilde | `package:id@~1.2.0` | Patch updates only (>=1.2.0 <1.3.0) |
| Package range | `package:id@>=1.0.0,<2.0.0` | Explicit range |
| Package latest | `package:id@latest` | Latest stable version |

## 9.2 Version Semantics

UAPF uses Semantic Versioning 2.0.0 (semver.org).

### 9.2.1 Version Format

```
MAJOR.MINOR.PATCH[-prerelease][+build]
```

- **MAJOR**: Breaking changes to process contracts, resource bindings, or execution behavior
- **MINOR**: New capabilities, optional fields, backward-compatible additions
- **PATCH**: Bug fixes, documentation, non-behavioral changes

### 9.2.2 Breaking Changes (MAJOR bump required)

The following changes MUST increment MAJOR version:
- Removing or renaming BPMN tasks/gateways that external packages reference
- Changing input/output contracts of exposed processes
- Removing resource binding targets
- Changing execution semantics that callers depend on

## 9.3 Resolution Algorithm

### 9.3.1 Workspace Resolution

For relative paths:
1. Resolve path relative to current package location
2. Validate target contains valid `uapf.yaml`
3. Fail if path does not exist or is invalid

### 9.3.2 Registry Resolution

For `package:` references:
1. Query configured registries in order
2. Find all versions matching constraint
3. Select highest matching version (prefer stable over prerelease)
4. Download and cache package
5. Fail if no matching version exists

### 9.3.3 Conflict Resolution

When multiple packages require different versions of the same dependency:

1. **Compatible ranges**: Use highest version satisfying all constraints
2. **Incompatible ranges**: FAIL with clear error listing conflicts
3. **Override mechanism**: Workspace-level `uapf-lock.yaml` MAY force specific versions

## 9.4 Lock File (RECOMMENDED)

### 9.4.1 Purpose

A `uapf-lock.yaml` file at workspace root MAY capture resolved dependency versions for reproducibility.

### 9.4.2 Format

```yaml
kind: uapf.lock
generated: "2025-01-10T12:00:00Z"
packages:
  - id: org.proc.shared
    version: 1.2.3
    resolved: "https://registry.uapf.dev/org.proc.shared/1.2.3"
    integrity: sha256-abc123...
    dependencies:
      - org.proc.utils@2.0.1
  - id: org.proc.utils
    version: 2.0.1
    resolved: "../shared/utils"
    integrity: sha256-def456...
```

### 9.4.3 Behavior

- If lock file exists, implementations SHOULD use locked versions
- `--update` or equivalent flag MAY refresh lock file
- Lock file SHOULD be committed to version control

## 9.5 Circular Dependency Detection

### 9.5.1 Rule

Circular dependencies are **NOT ALLOWED**.

A package A includes B, B includes C, C includes A = **NON-CONFORMANT**.

### 9.5.2 Detection

Implementations MUST:
1. Build dependency graph during resolution
2. Detect cycles using DFS or equivalent
3. FAIL with clear error showing the cycle path

## 9.6 Export Behavior

When exporting a package with dependencies:

| Mode | Behavior |
|------|----------|
| `--embed` | Include all dependencies in archive |
| `--reference` | Keep `package:` references, require runtime resolution |
| `--flatten` | Resolve and inline at export time (creates standalone package) |

Default: `--reference`

## 9.7 Conformance Requirements

- [ ] Implementations MUST parse all reference formats in 9.1.2
- [ ] Implementations MUST support semver range constraints
- [ ] Implementations MUST detect and reject circular dependencies
- [ ] Implementations SHOULD support lock files
- [ ] Implementations MUST fail clearly on unresolvable dependencies
