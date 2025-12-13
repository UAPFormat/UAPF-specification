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
