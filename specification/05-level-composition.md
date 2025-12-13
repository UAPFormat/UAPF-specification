# Level Composition

## Purpose
Levels 1–3 provide composition and governance without duplicating executable content.

## Composition includes
A package manifest MAY specify:

- `includes`: list of package references (relative paths within workspace OR stable package IDs)

### Reference forms
A reference MUST be one of:
- `../relative/path/to/package`
- `package:<id>@<semver-range>`

Examples:
- `../processes/L4-invoice-validation`
- `package:uapf.proc.invoice.validation@^1.0.0`

## No duplication rule (normative)
If a Level 2 package includes a Level 4 package, the Level 2 package MUST NOT copy the Level 4 BPMN/DMN/CMMN artifacts into its own folders.

Instead, Level 2 uses `includes` and provides:
- additional metadata/governance,
- additional resource bindings,
- higher-level documentation and traceability.
