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
    ASSERT binding.source.ref EXISTS IN bpmn/*.bpmn.xml as element @id
```

### 11.1.2 DMN Element References

**Validation Rule SEM-002:**
```
FOR EACH binding IN mappings.bindings:
  IF binding.source.type == "dmn.decision":
    ASSERT binding.source.ref EXISTS IN dmn/*.dmn.xml as decision @id
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
  FOR EACH userTask IN bpmn/*.bpmn.xml:
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

## 11.5 Conformance

- Implementations MUST validate SEM-001 through SEM-003 and SEM-007 through SEM-009
- Implementations SHOULD validate SEM-004 through SEM-006 and SEM-010
- Implementations MUST report error codes with messages
