# Changelog

## [2.5.0] - 2026-05-21

### Removed (breaking)
- The sidecar location `tests/algorithms/<card-id>.test.yaml` is
  REMOVED as a valid location for algorithm card tests. Conforming
  implementations MUST NOT load algorithm card tests from this
  location. (Sidecar tests under `tests/` remain valid for BPMN,
  DMN, and CMMN cornerstones — only algorithm cards are affected.)

### Added (breaking)
- A new REQUIRED top-level `tests` array on every algorithm card
  (`algorithm-card.schema.json`). The array MUST contain at least
  two entries (`minItems: 2`). Each entry has the shape
  `{ name, description?, inputs, expected_outputs, tolerance? }`.
  The viewer minimum of two is intentional: a single-case sample
  browser hides failure modes.
- New validation rule SEM-014 (ERROR): every algorithm card MUST
  carry the embedded `tests` array with at least two entries.
- New validation rule SEM-015 (WARN): test `inputs.*` and
  `expected_outputs.*` keys SHOULD match the Card's declared
  `io.inputs[].id` and `io.outputs[].id` respectively. Misaligned
  keys are a known footgun (the sample browser can't match against
  test cases whose input keys don't align with the IO contract).
- New chapter 13.15 (Migration guide from v2.4.0) — mechanical
  steps for moving sidecar tests into the Card.
- New chapter 13.16 (informative — Algorithm Card viewer) — defines
  the recommended Preview-tab viewer contract: polymorphic
  rendering on `implementation.type`, common metadata + IO header
  and sample-browser footer, per-language inline visualisers
  (regex highlight, FEEL evaluator, dmn link-out to cornerstone),
  external "sample browser" with string-equality matching against
  embedded tests, composite call-tree. Risk-class dot derivation
  matches chapter 13.10. Click-through from a BPMN algorithm task
  overlay opens the viewer as a side-panel drawer over the BPMN.

### Changed
- Chapter 13.12 (Testing) rewritten: tests are embedded, not sidecar.
- Chapter 13.11 (Manifest declaration) lost its "(unchanged from
  prior text — kept here for reading flow.)" note; promoted to a
  first-class section.
- `specification/10-conformance-checklist.md` extended with three
  new bullets covering SEM-014, SEM-015, and the sidecar removal.

### Migration notes
- v2.4.0 packages MUST migrate per chapter 13.15 before upgrading
  to v2.5.0. The migration is mechanical for the data shape but
  requires editorial judgment when fewer than two cases exist —
  the author MUST add at least one more case before SEM-014 will
  pass. UAPFormat/dokumenta-semantiska-analize ships its own v3.2.0
  with embedded tests in lockstep with this release; treat it as
  the reference migration.

## [2.4.0] - 2026-05-20

### Changed (breaking — but no production deployments affected, see Note below)
- The integration point for Algorithm Cards has moved. v2.3.0 placed
  `algorithm_card` on the resource target in `resources/mappings.yaml`.
  v2.4.0 places `uapf:algorithmCardRef` on the BPMN task itself.
  This reversal is deliberate: when the card lives on the resource
  target the algorithm becomes invisible at the BPMN diagram level,
  defeating the purpose of having a process notation. The algorithm
  card belongs on the task because the task IS the invocation of the
  algorithm.

### Added
- New BPMN extension namespace `https://uapf.dev/bpmn/v2.4` and
  attribute `uapf:algorithmCardRef` valid on `bpmn:serviceTask`,
  `bpmn:businessRuleTask`, and `bpmn:task`. Value MUST be a Card id
  matching `^algo\.[a-z0-9][a-z0-9._-]+$`.
- New `schemas/bpmn-extension.schema.json` defining the extension
  attribute formally.
- New chapter 13.9 (BPMN IO specification from the Card) — a card-
  referencing task SHOULD also carry a synthesized
  `<bpmn:ioSpecification>` block so downstream gateways branching on
  algorithm outputs are visually traceable.
- New chapter 13.10 (visual rendering — informative) — defines the
  recommended visual treatment: custom algorithm icon, card identity
  line, metadata line, risk-class dot, and data-object IO. This is
  what makes the diagram self-explanatory: anyone reading the BPMN
  can see which algorithm fires at each step, what risk class it
  carries, and which outputs feed the next gateway.
- New validation rule `SEM-013` (ERROR, advisory): the BPMN
  `<bpmn:ioSpecification>` on a card-referencing task SHOULD match
  the Card's `io` block.

### Removed (breaking)
- `target.algorithm_card` is removed from `schemas/resource-mapping.schema.json`.
  Resource targets describe *where* a task is dispatched — they do
  not declare algorithm identity. The card belongs on the task, not
  on the dispatch endpoint.

### Changed
- Validation rule `SEM-012` reworded: the rule now governs BPMN
  attribute resolution (`uapf:algorithmCardRef` -> `algorithms/`)
  rather than resource-target attribute resolution.
- `specification/02-process-cornerstones.md` extension note updated.
- `specification/10-conformance-checklist.md` updated to require
  recognition of the BPMN namespace and the new validation rules.
- `examples/approve-expense-l4`: the BPMN file gains
  `xmlns:uapf` + `uapf:algorithmCardRef` on the appropriate
  serviceTask plus a synthesized `<bpmn:ioSpecification>`. The
  corresponding `algorithm_card` is removed from
  `resources/mappings.yaml`. Archive re-packed.

### Note
- This is a deliberate reversal of a decision made in v2.3.0.
  v2.3.0 was published and merged earlier on the same day as this
  release; the dependent ecosystem at the time of revision was a
  single in-flight implementation package
  (`dokumenta-semantiska-analize` v3.0.0) which is being updated to
  v3.1.0 in lockstep. No widely-deployed code depended on
  `target.algorithm_card`, so the field is removed rather than
  deprecated. Future external implementations that adopted v2.3.0
  should migrate by moving the `algorithm_card` value from each
  resource target to the corresponding BPMN task as
  `uapf:algorithmCardRef`, and optionally adding a
  `<bpmn:ioSpecification>` synthesized from the Card.

## [2.3.0] - 2026-05-20

### Added
- New OPTIONAL artifact category — Algorithm Cards — defined in
  `specification/13-algorithm-cards.md` and validated by
  `schemas/algorithm-card.schema.json`. A Card is a typed, versioned
  governance wrapper for a single algorithm invoked behind a resource
  target. Cards live in the package's `algorithms/` folder (path
  configurable via `paths.algorithms`) and supply intent, IO contract,
  ownership, lifecycle, validation history, and OPTIONAL extensions
  for ML, crypto, privacy, risk, and prompt-based implementations.
- Manifest schema gains two OPTIONAL top-level properties:
  `algorithm_cards` (boolean) and `paths.algorithms` (string). Neither
  is required; both live outside the closed `cornerstones` block.
- Resource mapping schema gains one OPTIONAL `algorithm_card` property
  per target, referencing a Card by `id` or relative path.
- New validation rule `SEM-012` (ERROR): Algorithm Card reference does
  not resolve.
- New OPTIONAL conformance block in `10-conformance-checklist.md` for
  implementations that support Algorithm Cards.
- New example `examples/approve-expense-l4` now demonstrates a Card
  attached to one of its resource targets.

### Note
- Fully additive, backward-compatible. Every package valid under 2.2.x
  remains valid under 2.3.0. Algorithm Cards extend the Resources
  cornerstone — they do NOT become a fifth cornerstone. The four
  cornerstones (BPMN, DMN, CMMN, Resources + Mapping) remain
  authoritative and unchanged. Hence a minor bump.

## [2.2.0] - 2026-05-17

### Added
- Manifest schema (`schemas/uapf-manifest.schema.json`) extended to model the
  full real-world manifest vocabulary. New optional top-level fields:
  - `artifacts` — per-cornerstone inventory with `role`/`description` per file
  - `inputs` / `outputs` — logical process I/O names
  - `requires_capabilities` — UAPF-IP host capabilities the package requires
  - `profiles_supported` — UAPF-IP integration profiles supported
  - `guardrails` — path to the package guardrails file
- `exposure.mcp.exposedEntrypoints` items may now be either a bare
  process/decision id (string) or an object `{decision|process, tool}` mapping
  an entrypoint to an explicit MCP tool name — previously string-only.

### Note
- Additive, backward-compatible schema change (new optional properties, a
  widened item type) — hence a minor bump. Manifests valid under 2.1.x stay
  valid. Prior to 2.2.0 the schema modelled neither the richer
  `artifacts`/`inputs`/`outputs` form nor the UAPF-IP
  `requires_capabilities`/`profiles_supported`/`guardrails` fields, even though
  real packages used them; this release closes that gap.

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
