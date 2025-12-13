# Versioning and Evolution — Normative

## Specification versioning
UAPF follows semantic versioning:

- MAJOR: breaking changes
- MINOR: backward-compatible additions
- PATCH: clarifications and fixes

This repository defines **UAPF v1.x**.

## Package compatibility
A `.uapf` package MUST declare a format version.
Implementations MUST reject packages requiring a higher major version.

## Backward compatibility
- Minor versions MUST NOT invalidate existing packages.
- Major versions MAY introduce breaking changes.

## Migration
If a future UAPF version introduces breaking changes:
- a migration guide MUST be provided
- tooling SHOULD assist automated migration where feasible

## Deprecation
Deprecated fields or structures:
- MUST remain valid for at least one major version
- MUST be clearly documented
