# Export, Import, and Validation — Normative

## Export (workspace → .uapf)
An export operation MUST:

1. Locate `uapf.yaml`
2. Validate the manifest schema
3. Collect all referenced files for the package scope
4. Resolve `includes` by either:
   - embedding referenced packages, OR
   - declaring them as external dependencies
5. Produce a ZIP archive with `.uapf` extension

Export MUST fail if:
- required files are missing
- manifest validation fails
- includes cannot be resolved

## Import (.uapf → workspace or runtime)
An import operation MUST:

1. Unpack the archive
2. Locate `uapf.yaml`
3. Validate required files for the declared level
4. Validate schemas
5. Report unresolved dependencies

Import MUST fail if:
- `uapf.yaml` is missing
- schemas fail validation
- Level 4 requirements are not met

## Validation rules

A conformant validator MUST:
- validate manifests against JSON Schema
- validate enterprise indexes at Level 0
- validate resource mappings when present

A validator SHOULD:
- verify BPMN/DMN/CMMN file presence
- warn on unresolved element references
- warn on unused resource targets

## Error severity
- **ERROR**: non-conformant, processing MUST stop
- **WARNING**: valid but potentially incomplete
