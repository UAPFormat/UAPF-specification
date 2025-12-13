# Export, Import, and Validation (Normative)

## Conformance levels
An implementation MAY claim:
- **Package conformance**: can validate and read/write `.uapf` packages.
- **Workspace conformance**: can index and resolve workspace references.
- **MCP binding conformance**: can produce MCP-compatible bindings from resource mappings.

## Export (workspace → .uapf)
Export MUST:
1. Collect `uapf.yaml` and all referenced files/folders for the package scope.
2. Resolve `includes`:
   - either embed included packages, OR
   - preserve references and declare them as external dependencies.
3. Create a ZIP archive with `.uapf` extension.
4. Preserve relative paths.

## Import (.uapf → workspace or runtime)
Import MUST:
1. Unzip and locate `uapf.yaml`.
2. Validate manifest schema and required files for the declared level.
3. Validate resource mapping schema if present.
4. Report unresolved `includes` as an error unless external dependency resolution is configured.

## Validation rules (baseline)
A conformant validator MUST:
- validate `uapf.yaml` against `schemas/uapf-manifest.schema.json`
- validate `enterprise.yaml` against `schemas/enterprise-index.schema.json` (Level 0)
- validate `resources/mappings.yaml` against `schemas/resource-mapping.schema.json` when present

A validator SHOULD also:
- check that Level 4 has `/bpmn` and at least one `.bpmn.xml`
- check that mappings reference existing BPMN/DMN/CMMN element identifiers (best-effort)
- check that includes paths are resolvable in a workspace context

## BPMN/DMN/CMMN semantic validation (optional)
UAPF packaging validation is distinct from BPMN/DMN/CMMN engine validation.
Implementations MAY integrate engine validators (e.g., Camunda/Zeebe tooling) but UAPF does not require a specific engine.
