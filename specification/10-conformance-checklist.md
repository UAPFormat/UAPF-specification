# UAPF v1 Conformance Checklist (Normative)

An implementation claiming UAPF conformance MUST satisfy the following.

## Package conformance
- [ ] Accepts ZIP-based `.uapf` archives
- [ ] Locates and parses `uapf.yaml`
- [ ] Validates manifest against schema
- [ ] Enforces level-specific requirements

## Level 4 requirements
- [ ] At least one BPMN file present
- [ ] Resource mappings present
- [ ] Manifest declares cornerstones correctly

## Workspace conformance
- [ ] Supports Level 0 enterprise index
- [ ] Resolves includes across levels
- [ ] Rejects duplicated executable artifacts

## Export / import
- [ ] Produces `.uapf` archives per spec
- [ ] Rejects invalid or incomplete packages
- [ ] Reports unresolved dependencies

## MCP Export and Agentic Integrations (06)

- [ ] The implementation supports **Package → MCP** (import any valid `.uapf` and expose MCP surface).
- [ ] The implementation supports **Workspace → MCP** (map a Workspace repo to an MCP surface reflecting SSOT).
- [ ] The MCP surface exposes required tools:
  - [ ] `uapf.describe`
  - [ ] `uapf.list`
  - [ ] `uapf.run_process`
  - [ ] `uapf.evaluate_decision`
  - [ ] `uapf.resolve_resources`
  - [ ] `uapf.get_artifact`
  - [ ] `uapf.validate` (MUST in Workspace mode; RECOMMENDED in Package mode)
- [ ] The MCP surface exposes required resource categories:
  - [ ] `uapf://manifest/...`
  - [ ] `uapf://bpmn/...`
  - [ ] `uapf://dmn/...`
  - [ ] `uapf://cmmn/...`
  - [ ] `uapf://policies/...` (if policies exist)
  - [ ] `uapf://bindings/...`
- [ ] Resource binding is first-class: the implementation returns explicit resolved bindings or explicit “unbound” results (no invented bindings).
- [ ] Level-handling: Level 1–3 packages that are not runnable fail clearly unless a runnable entrypoint is resolved.

## Governance
- [ ] Reads ownership metadata
- [ ] Reads lifecycle metadata

## Agent binding (optional)
- [ ] Interprets resource mappings
- [ ] Produces derived agent bindings

## Dependency resolution (09)
- [ ] Parses all reference formats (relative, package:, version ranges)
- [ ] Supports semver range constraints (^, ~, >=, <, etc.)
- [ ] Detects and rejects circular dependencies
- [ ] Supports lock file reading (RECOMMENDED)
- [ ] Fails clearly on unresolvable dependencies

## Semantic validation (11)
- [ ] Validates BPMN element references exist
- [ ] Validates DMN decision references exist
- [ ] Validates target IDs exist in targets list
- [ ] Validates level composition rules
- [ ] Reports errors with codes from SEM-xxx taxonomy

## YAML safety (12)
- [ ] Validates version fields are strings, not numbers
- [ ] Rejects invalid type coercions in required fields

An implementation MUST state which sections it supports.
