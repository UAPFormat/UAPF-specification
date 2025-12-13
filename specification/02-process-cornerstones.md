# Process Cornerstones

Every UAPF process package (any Level 1–4) is defined around fixed cornerstones.

## Cornerstones (normative)
A UAPF package MUST define its process scope using the following cornerstone artifact categories:

1. **BPMN** (process flow) — REQUIRED for Level 4.
2. **DMN** (decision logic) — OPTIONAL, first-class.
3. **CMMN** (case/context logic) — OPTIONAL, first-class.
4. **Resources + Mapping** — REQUIRED for Level 4; RECOMMENDED for higher levels.

## BPMN
- Stored as BPMN XML files under `/bpmn`.
- A Level-4 package MUST include at least one BPMN XML file.

## DMN
- Stored as DMN XML files under `/dmn`.
- DMN is used to express decision logic referenced by BPMN tasks/gateways.

## CMMN
- Stored as CMMN XML files under `/cmmn`.
- CMMN is used where case-driven behavior exists.

## Resources and Mapping
Resources describe who/what executes work and how tasks bind to those resources.

- Resource definitions MUST be stored under `/resources`.
- Mapping MUST provide an executable binding target for tasks/decisions/case steps.
- Mapping MAY bind to:
  - AI agents,
  - humans/roles,
  - systems/APIs,
  - MCP tools/endpoints.

UAPF does not redefine BPMN/DMN/CMMN semantics; it packages them with governance and bindings.
