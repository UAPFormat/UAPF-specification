# Packages and Workspaces

## Package: portability unit
A package is a directory with:
- `uapf.yaml` (manifest)
- cornerstone folders (`/bpmn`, `/dmn`, `/cmmn`, `/resources`)
- `/metadata` for governance

A package MUST be independently validatable using the schemas in `/schemas`.

A package MAY be exported to a `.uapf` archive. Exporting MUST preserve file paths and the manifest.

## Workspace: Git SSOT unit
A workspace is a Git repository holding:
- Level 0 enterprise index (`enterprise/enterprise.yaml`)
- one or more packages
- optional tooling, templates, and examples

A workspace SHOULD enforce change governance using:
- pull requests / merge requests,
- review rules (CODEOWNERS),
- CI schema validation,
- tagged releases.

## Composition rule
Higher-level packages (Levels 1–3) MUST reference lower-level packages using includes/references. They MUST NOT copy lower-level artifacts.

## Release rule
Git tags/releases represent immutable snapshots of the workspace SSOT at a point in time.
