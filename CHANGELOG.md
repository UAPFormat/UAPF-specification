# Changelog

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
