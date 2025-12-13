# UAPF Package Format (.uapf) — Normative

## Container
A `.uapf` file MUST be a **ZIP archive**.

- File extension: `.uapf`
- Compression: standard ZIP (deflate is acceptable)
- The ZIP MUST preserve relative paths and file names.

## Root directory rule
A `.uapf` archive MUST contain **exactly one** root package directory OR place package files at the ZIP root.

Allowed:
- `my-package/uapf.yaml` (single top folder)
- `uapf.yaml` at archive root

Not allowed:
- multiple sibling package roots in one `.uapf`

## Required files and folders
A UAPF package MUST include:

- `uapf.yaml` (manifest) — REQUIRED
- `metadata/ownership.yaml` — REQUIRED
- `metadata/lifecycle.yaml` — REQUIRED

For **Level 4** packages, it MUST include:
- `bpmn/` with at least one `.bpmn.xml` file — REQUIRED
- `resources/` with `mappings.yaml` — REQUIRED

For higher-level packages (Levels 1–3), BPMN/DMN/CMMN folders MAY be absent if the package is purely compositional and declares that in the manifest.

## File naming conventions
- BPMN files SHOULD use: `*.bpmn.xml`
- DMN files SHOULD use: `*.dmn.xml`
- CMMN files SHOULD use: `*.cmmn.xml`

## Manifest schema
The `uapf.yaml` manifest MUST validate against:
- `schemas/uapf-manifest.schema.json`

Resource mappings MUST validate against:
- `schemas/resource-mapping.schema.json`

Enterprise indexes MUST validate against:
- `schemas/enterprise-index.schema.json`

## Integrity and traceability (optional, recommended)
A package MAY include:
- `metadata/integrity.yaml` containing checksums (sha256) for included artifacts.
- `metadata/signature.*` for digital signing.

If present, integrity documents MUST NOT contradict the actual package contents.
