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
- `bpmn/` with ≥1 `.bpmn` file
- `resources/mappings.yaml`

### Levels 1–3 (compositional)
Levels 1–3 MAY omit BPMN/DMN/CMMN folders if:
- the package is compositional only
- this is declared via `includes` in the manifest

### Level 0
Level 0 is NOT a `.uapf` package.
It is represented only by an enterprise index in a workspace.

## File naming

Cornerstone files MUST use the file extensions defined by their respective
OMG standards:

- BPMN files MUST use `.bpmn`
- DMN files MUST use `.dmn`
- CMMN files MUST use `.cmmn`

Rationale: UAPF does not redefine BPMN/DMN/CMMN; their semantics and their
serialization are owned by OMG. UAPF cornerstone files are therefore named
with the extensions the OMG tool ecosystem recognizes (`.bpmn`, `.dmn`,
`.cmmn`), so that a UAPF cornerstone opens, unmodified, in any conforming
OMG modeler or viewer. The files remain XML documents; the extension
identifies the modeling standard, not the serialization.

## Diagram interchange

Cornerstone BPMN, DMN and CMMN files MUST include valid OMG diagram
interchange (DI):

- BPMN files MUST contain a `<bpmndi:BPMNDiagram>` element, with the
  `bpmndi`, `dc` and `di` namespaces declared.
- DMN files MUST contain a `<dmndi:DMNDI>` element where the decision
  model defines a Decision Requirements Diagram (DRD). A DMN file whose
  only decision logic is one or more decision tables or literal
  expressions, with no DRD, is exempt.
- CMMN files MUST contain a `<cmmndi:CMMNDI>` element, with the
  `cmmndi`, `dc` and `di` namespaces declared.

Rationale: a UAPF cornerstone is the authoritative *and inspectable*
artifact of a process. Diagram interchange is the standard, modeler-default
representation of a BPMN/DMN/CMMN model's layout — every conforming OMG
modeler (Camunda Modeler, bpmn-js/dmn-js/cmmn-js, Eclipse) produces it on
save. A cornerstone without DI is therefore an artifact that was never
modeled, only hand-authored as logic; it cannot be opened and reviewed
visually in any conforming tool. Requiring DI imposes no burden on a normal
authoring workflow — the modeler already emits it — and guarantees that a
cornerstone renders identically across the OMG tool ecosystem.

An implementation MUST NOT rely on automatic layout generation as a
substitute for authored DI: a generated layout is not the authored layout
and is not deterministic across tools.

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
