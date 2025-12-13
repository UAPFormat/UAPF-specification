# Folder Structure (Normative)

## Workspace layout (recommended)
A UAPF workspace SHOULD use a structure similar to:

/enterprise
/domains
/processes

Example:

- `enterprise/enterprise.yaml` (Level 0)
- `domains/<domain>/*` (Level 1 compositions)
- `processes/<process>/*` (Levels 2–4 packages)

The exact folder names MAY differ, but references MUST remain resolvable.

## Package layout (required)
Every package MUST follow this internal layout:

/<uapf-package>
  uapf.yaml
  /bpmn
  /dmn
  /cmmn
  /resources
  /metadata

Rules:
- `uapf.yaml` is REQUIRED.
- `/bpmn` is REQUIRED for Level 4.
- `/resources` is REQUIRED for Level 4.
- `/dmn` and `/cmmn` MAY be empty or absent only if the manifest states they are not used.

## Metadata layout
`/metadata` MUST contain:
- `ownership.yaml` (REQUIRED)
- `lifecycle.yaml` (REQUIRED)

Additional metadata files MAY be added.
