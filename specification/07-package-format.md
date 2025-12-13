# UAPF Package Format (.uapf) — Normative

## Container format
A `.uapf` file MUST be a **ZIP archive**.

- File extension: `.uapf`
- Compression: ZIP (deflate or stored)
- No encryption at the container level

## Root layout
A `.uapf` archive MUST contain exactly one package.

Allowed layouts:
- files at ZIP root
- a single top-level directory containing the package

Disallowed:
- multiple sibling package roots

## Mandatory files
Every `.uapf` package MUST include:

- `uapf.yaml`
- `metadata/ownership.yaml`
- `metadata/lifecycle.yaml`

## Level-specific requirements

### Level 4 (atomic executable)
A Level-4 package MUST include:
- `bpmn/` with ≥1 `.bpmn.xml`
- `resources/mappings.yaml`

### Levels 1–3 (compositional)
Levels 1–3 MAY omit BPMN/DMN/CMMN folders if:
- the package is compositional only
- this is declared via `includes` in the manifest

### Level 0
Level 0 is NOT a `.uapf` package.
It is represented only by an enterprise index in a workspace.

## File naming
Recommended (not required):
- `*.bpmn.xml`
- `*.dmn.xml`
- `*.cmmn.xml`

## Manifest
The manifest file `uapf.yaml` MUST:
- validate against `schemas/uapf-manifest.schema.json`
- declare the package level
- declare cornerstone presence

## Integrity (optional)
A package MAY include:
- `metadata/integrity.yaml` with checksums
- digital signature files

Integrity metadata MUST NOT contradict actual package contents.

## Determinism
Packaging tools SHOULD produce deterministic archives.
If timestamps or ordering vary, implementations MUST rely on content validation, not binary equality.
