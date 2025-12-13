# UAPF v1 Conformance Checklist (Normative)

An implementation claiming UAPF conformance MUST satisfy the following.

## Package conformance
- [ ] Accepts ZIP-based `.uapf` archives
- [ ] Locates and parses `uapf.yaml`
- [ ] Validates manifest against schema
- [ ] Enforces level-specific requirements

## Level 4 requirements
- [ ] At least one BPMN file present
- [ ] Resource mappings present
- [ ] Manifest declares cornerstones correctly

## Workspace conformance
- [ ] Supports Level 0 enterprise index
- [ ] Resolves includes across levels
- [ ] Rejects duplicated executable artifacts

## Export / import
- [ ] Produces `.uapf` archives per spec
- [ ] Rejects invalid or incomplete packages
- [ ] Reports unresolved dependencies

## Governance
- [ ] Reads ownership metadata
- [ ] Reads lifecycle metadata

## Agent binding (optional)
- [ ] Interprets resource mappings
- [ ] Produces derived agent bindings

An implementation MUST state which sections it supports.
