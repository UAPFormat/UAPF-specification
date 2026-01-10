# UAPF v1 — Specification Overview (Normative)

## Scope
This specification defines **UAPF v1**, a standard for representing, versioning, packaging, and exporting organizational processes as code, and for binding those processes to execution targets (including AI agents).

UAPF standardizes:
- process packaging and structure
- composition across organizational scope
- governance metadata
- portability via `.uapf` packages
- deterministic export/import rules

UAPF does NOT standardize:
- BPMN, DMN, or CMMN semantics
- workflow execution engines
- AI agent internal reasoning or prompting
- organizational operating models

## Intended audience
This specification is intended for:
- tool builders implementing UAPF validators, packagers, or importers
- enterprises maintaining process repositories as code
- platforms binding processes to AI agents (e.g., via MCP)

## Normative boundaries
The following are normative and define conformance:
- `/specification/**`
- `/schemas/**`

All other content (examples, tools, websites) is informative only.

The formal checklist for verifying UAPF conformance is captured in:
- [`specification/10-conformance-checklist.md`](10-conformance-checklist.md)

## Chapter list

The core chapters of the specification are:

1. [`00-ssot.md`](00-ssot.md) — SSOT rules
2. [`01-concepts.md`](01-concepts.md) — core concepts
3. [`02-process-cornerstones.md`](02-process-cornerstones.md) — BPMN/DMN/CMMN cornerstones
4. [`03-packages-and-workspaces.md`](03-packages-and-workspaces.md) — artifact types
5. [`04-folder-structure.md`](04-folder-structure.md) — repository layout
6. [`05-level-composition.md`](05-level-composition.md) — levels and composition
7. [`06-mcp-integration.md`](06-mcp-integration.md) — MCP export and agentic integrations
8. [`07-package-format.md`](07-package-format.md) — package container format
9. [`08-export-import-validation.md`](08-export-import-validation.md) — export/import rules
10. [`09-dependencies.md`](09-dependencies.md) — dependency resolution
11. [`10-conformance-checklist.md`](10-conformance-checklist.md) — conformance checklist
12. [`11-semantic-validation.md`](11-semantic-validation.md) — semantic validation rules
13. [`12-yaml-guidelines.md`](12-yaml-guidelines.md) — YAML authoring guidelines
14. [`99-versioning-and-evolution.md`](99-versioning-and-evolution.md) — versioning rules

## Conformance levels
An implementation MAY claim conformance at one or more levels:

1. **Package conformance**
   - validates `.uapf` packages
   - understands manifests and required structure

2. **Workspace conformance**
   - resolves Level 0–4 composition
   - validates enterprise indexes and includes

3. **Export/Import conformance**
   - produces and consumes `.uapf` archives

4. **Agent binding conformance**
   - interprets resource mappings
   - produces derived bindings (e.g., MCP artifacts)

An implementation MUST clearly state which conformance level(s) it supports.

## Terminology
The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 2119.
