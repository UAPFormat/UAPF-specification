# Concepts and Levels

## UAPF Package
A **UAPF Package** is a portable directory structure representing a process scope. A package can be zipped and distributed as a `.uapf` archive.

A package MUST contain a `uapf.yaml` manifest.

## UAPF Workspace
A **UAPF Workspace** is a Git repository holding one or more packages and an enterprise index (Level 0). The workspace is the SSOT.

## Levels (scope only)
UAPF defines **Levels** as an aggregation and governance scope. Levels MUST NOT be used to imply modeling semantics.

| Level | Meaning |
|------:|---------|
| 4 | Atomic executable process |
| 3 | Composed subprocess / variant |
| 2 | End-to-end business process |
| 1 | Domain process collection |
| 0 | Enterprise process collection index (workspace-level) |

### Level 0 rule
Level 0 MUST NOT contain executable logic. It is an index and composition map.

### Level 1–3 rule
Levels 1–3 are compositions of other packages. They MUST reference lower-level packages and MUST NOT duplicate lower-level content.

### Level 4 rule
Level 4 is the lowest executable level. A Level-4 package MUST include BPMN and MUST include resources and mappings (even if minimal).
