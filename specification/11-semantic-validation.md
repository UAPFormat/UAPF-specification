# 11 — Semantic Validation Rules (Normative)

## 11.0 Purpose

JSON Schema validation ensures structural correctness. This chapter defines semantic validation rules that ensure logical correctness.

## 11.1 Reference Integrity

### 11.1.1 BPMN Element References

All `source.ref` values in resource mappings MUST reference existing BPMN element IDs.

**Validation Rule SEM-001:**
```
FOR EACH binding IN mappings.bindings:
  IF binding.source.type STARTS WITH "bpmn.":
    ASSERT binding.source.ref EXISTS IN bpmn/*.bpmn as element @id
```

### 11.1.2 DMN Element References

**Validation Rule SEM-002:**
```
FOR EACH binding IN mappings.bindings:
  IF binding.source.type == "dmn.decision":
    ASSERT binding.source.ref EXISTS IN dmn/*.dmn as decision @id
```

### 11.1.3 Target References

**Validation Rule SEM-003:**
```
FOR EACH binding IN mappings.bindings:
  ASSERT binding.targetId EXISTS IN mappings.targets[].id
```

## 11.2 Completeness Rules

### 11.2.1 Level 4 Binding Coverage

**Validation Rule SEM-004:**
```
FOR Level 4 packages:
  FOR EACH userTask IN bpmn/*.bpmn:
    WARN IF userTask.@id NOT IN any binding.source.ref
```

### 11.2.2 Unused Targets

**Validation Rule SEM-005:**
```
FOR EACH target IN mappings.targets:
  WARN IF target.id NOT IN any binding.targetId
```

## 11.3 Consistency Rules

### 11.3.1 Capability Matching

**Validation Rule SEM-006:**
```
FOR EACH binding WITH requiredCapabilities:
  LET target = FIND target WHERE target.id == binding.targetId
  FOR EACH capability IN binding.requiredCapabilities:
    WARN IF capability NOT IN target.capabilities
```

### 11.3.2 Level Consistency

**Validation Rule SEM-007:**
```
FOR EACH include IN manifest.includes:
  LET target = RESOLVE include
  ASSERT target.level > manifest.level
  // Lower levels can only include higher-numbered levels
```

### 11.3.3 Diagram Interchange Presence

Cornerstone BPMN/DMN/CMMN files MUST carry valid OMG diagram interchange
(see 07-package-format, "Diagram interchange").

**Validation Rule SEM-011:**
```
FOR EACH file IN bpmn/*.bpmn:
  ASSERT file CONTAINS <bpmndi:BPMNDiagram>
FOR EACH file IN cmmn/*.cmmn:
  ASSERT file CONTAINS <cmmndi:CMMNDI>
FOR EACH file IN dmn/*.dmn:
  IF file DEFINES a Decision Requirements Diagram (DRD):
    ASSERT file CONTAINS <dmndi:DMNDI>
```


### 11.3.4 Algorithm Card Reference Integrity

When a BPMN task carries a `uapf:algorithmCardRef` attribute, the
referenced Card MUST resolve.

**Validation Rule SEM-012:**
```
FOR EACH bpmn:serviceTask | bpmn:businessRuleTask | bpmn:task IN cornerstones/bpmn/*:
  IF task HAS attribute uapf:algorithmCardRef:
    ASSERT uapf:algorithmCardRef MATCHES /^algo\.[a-z0-9][a-z0-9._-]+$/
    ASSERT uapf:algorithmCardRef EXISTS as id IN any algorithms/*.card.yaml
```

### 11.3.5 BPMN IO Specification Matches Card IO

When a BPMN task carries `uapf:algorithmCardRef` AND a
`<bpmn:ioSpecification>` is present, the IO specification SHOULD
match the referenced Card's `io` block.

**Validation Rule SEM-013:**
```
FOR EACH task WITH uapf:algorithmCardRef AND <bpmn:ioSpecification>:
  card = LOAD algorithms/{algorithmCardRef}.card.yaml
  FOR EACH dataInput IN ioSpecification:
    ASSERT EXISTS matching card.io.inputs[].id
  FOR EACH dataOutput IN ioSpecification:
    ASSERT EXISTS matching card.io.outputs[].id
```

SEM-013 is an advisory error — auto-fixable by regenerating the IO
specification from the Card.

### 11.3.6 Algorithm Card Embedded Tests (v2.5.0+)

Every algorithm card MUST carry at least two embedded test cases
under its top-level `tests` array (see chapter 13.12).

**Validation Rule SEM-014:**
```
FOR EACH card IN algorithms/*.card.yaml:
  ASSERT card.tests IS PRESENT
  ASSERT card.tests IS array
  ASSERT card.tests.length >= 2
```

SEM-014 is an ERROR. v2.4.0 cards that pass schema validation but
fail SEM-014 are non-conformant in v2.5.0+ and MUST be migrated per
the chapter 13.15 migration guide before upgrading.

### 11.3.7 Algorithm Card Test Key Resolution

The keys used in `tests[].inputs` and `tests[].expected_outputs`
SHOULD match the Card's declared `io.inputs[].id` and
`io.outputs[].id` respectively. Misaligned keys produce viewer
behaviour that looks like silent test passes (the viewer cannot
match user-entered inputs against test cases that don't share input
keys).

**Validation Rule SEM-015:**
```
FOR EACH card IN algorithms/*.card.yaml:
  declared_input_ids = SET(card.io.inputs[].id)
  declared_output_ids = SET(card.io.outputs[].id)
  FOR EACH test IN card.tests:
    FOR EACH input_key IN test.inputs:
      WARN IF input_key NOT IN declared_input_ids
    FOR EACH output_key IN test.expected_outputs:
      WARN IF output_key NOT IN declared_output_ids
```

SEM-015 is an ADVISORY warning (level: warn). It does not block
conformance, but it surfaces a class of footgun where a Card author
adds a new IO field but forgets to update existing test cases (or
vice versa).

## 11.4 Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| SEM-001 | ERROR | BPMN element reference not found |
| SEM-002 | ERROR | DMN decision reference not found |
| SEM-003 | ERROR | Target ID not found in targets list |
| SEM-004 | WARNING | User task has no binding |
| SEM-005 | WARNING | Target defined but never used |
| SEM-006 | WARNING | Required capability not declared |
| SEM-007 | ERROR | Invalid level composition |
| SEM-008 | ERROR | Circular dependency detected |
| SEM-009 | ERROR | Duplicate binding for same source |
| SEM-010 | WARNING | Fallback target not defined |
| SEM-011 | ERROR | Cornerstone file missing diagram interchange (DI) |
| SEM-012 | ERROR | Algorithm Card reference (uapf:algorithmCardRef) does not resolve |
| SEM-013 | ERROR | BPMN ioSpecification does not match referenced Card's io block |
| SEM-014 | ERROR | Algorithm card lacks embedded tests array, or has fewer than 2 entries (v2.5.0+) |
| SEM-015 | WARN  | Algorithm card test input/output keys do not match declared io.inputs/io.outputs ids (v2.5.0+) |

## 11.5 Conformance

- Implementations MUST validate SEM-001 through SEM-003, SEM-007 through SEM-009, SEM-011, SEM-012, SEM-013, SEM-014, and SEM-015
- Implementations SHOULD validate SEM-004 through SEM-006 and SEM-010
- Implementations MUST report error codes with messages
