# Changelog

## [2.1.0] - 2026-05-17

### Added
- Cornerstone diagram interchange is now mandatory. Cornerstone BPMN/DMN/CMMN
  files MUST include valid OMG diagram interchange (`bpmndi:BPMNDiagram` /
  `dmndi:DMNDI` / `cmmndi:CMMNDI`). New normative section in
  `07-package-format.md` ("Diagram interchange") and new validation rule
  `SEM-011` in `11-semantic-validation.md` (ERROR severity, MUST-validate).
  DMN files whose decision logic is table/literal-expression only, with no
  Decision Requirements Diagram, are exempt from the DMN DI requirement.

  Rationale: a cornerstone is the authoritative and *inspectable* artifact of
  a process. Diagram interchange is the modeler-default representation of
  layout — every conforming OMG modeler emits it on save — so requiring it
  imposes no burden on a normal authoring workflow and only rejects
  hand-authored, logic-only XML that was never modeled. Implementations MUST
  NOT treat automatic layout generation as a substitute for authored DI.

### Note
- This is an additive normative requirement (new MUST + new SEM rule), not a
  change to existing structure — hence a minor bump. Existing packages whose
  cornerstones were produced by a modeler already comply. Packages with
  hand-authored, DI-less cornerstones must add diagram interchange.


## [2.0.0] - 2026-05-17

### Changed (BREAKING)
- Cornerstone file naming: BPMN/DMN/CMMN files MUST now use the OMG-standard
  extensions `.bpmn`, `.dmn`, `.cmmn` — previously `.bpmn.xml`, `.dmn.xml`,
  `.cmmn.xml`. (`specification/07-package-format.md`,
  `specification/11-semantic-validation.md`.)

  Rationale: UAPF does not redefine BPMN/DMN/CMMN — those standards, and
  their serialization, are owned by OMG. Cornerstone files are now named
  with the extensions the OMG tool ecosystem recognizes, so a UAPF
  cornerstone opens unmodified in any conforming OMG modeler or viewer
  (Camunda Modeler, bpmn-js/dmn-js, IDE plugins). This also removes a prior
  internal contradiction in 07-package-format.md, where the Level-4 rule
  required `.bpmn.xml` while the file-naming section called the same
  convention "recommended (not required)."

### Migration
- Rename cornerstone files: `*.bpmn.xml` -> `*.bpmn`, `*.dmn.xml` -> `*.dmn`,
  `*.cmmn.xml` -> `*.cmmn`.
- Manifests (`uapf.yaml`) reference cornerstone *folders*, not individual
  files, and therefore do NOT change.
- The `uapf-manifest` JSON Schema has no filename constraint and does NOT
  change.
- Bundled examples (`approve-expense-l4`, `minimal-l4-package`,
  `minimal-workspace`) have been renamed accordingly.


## [1.1.0] - 2025-01-10

### Added
- `schemas/ownership.schema.json` - Ownership metadata schema
- `schemas/lifecycle.schema.json` - Lifecycle metadata schema
- `schemas/policies.schema.json` - Policy definitions schema
- `schemas/mcp-tools.schema.json` - Normative MCP tool input/output schemas
- `specification/09-dependencies.md` - Dependency resolution and versioning rules
- `specification/11-semantic-validation.md` - Semantic validation rules beyond JSON Schema
- `specification/12-yaml-guidelines.md` - YAML authoring safety guidelines
- Resource binding contracts with input/output schemas, timeouts, and fallbacks
- Lock file specification for reproducible builds
- Circular dependency detection requirement
- MCP error code taxonomy

### Changed
- `schemas/resource-mapping.schema.json` - Extended with contracts, timeouts, fallbacks, and capability matching
- `schemas/uapf-manifest.schema.json` - Added structured `dependencies` field
- Enhanced `specification/06-mcp-integration.md` with tool schema references

### Fixed
- YAML type coercion issues documented with required quoting rules

## [1.0.0] — Initial Stable Release

This release defines the first stable version of the UAPF standard.

### Included
- Normative specification for UAPF v1
- Stable `.uapf` package format (ZIP-based)
- Levels 0–4 composition model
- BPMN, DMN, CMMN cornerstones
- Resource and agent binding model
- Export, import, and validation rules
- JSON Schemas for validation
- Reference examples and CLI tooling

### Compatibility
- This release establishes the v1 compatibility baseline.
- All v1.x releases MUST remain backward compatible.
