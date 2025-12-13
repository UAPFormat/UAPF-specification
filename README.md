# UAPF Specification

## Normative entry point

This README is **informational**.

The normative entry point for the UAPF v1 standard is:
- [`specification/00-overview.md`](specification/00-overview.md)

All conformance requirements are defined under `/specification` and `/schemas`.

This repository is the **Single Source of Truth (SSOT)** for **UAPF v1**.

UAPF is a disciplined format for storing and versioning organizational processes as code, and for exporting portable packages that can be bound to AI agents (e.g., via MCP) without losing governance and traceability.

## Cornerstone axioms (normative)

1. **UAPF is both a Package and a Workspace**
   - A **Package** is a portable, versioned unit (`.uapf`).
   - A **Workspace** is a Git repository holding one or more packages.
   - The Git workspace is the **authoritative SSOT**.

2. **UAPF starts at the lowest executable level**
   - The minimal valid UAPF entity is a **Level-4 process**.
   - Higher levels are compositions, never copies.

3. **UAPF is extractable and importable**
   - Any process can be exported as a `.uapf` package.
   - Packages can be imported into MCP to bind processes to AI agents.

4. **Every UAPF process consists of fixed cornerstones**
   - BPMN (process flow)
   - DMN (decision logic)
   - CMMN (case/context logic)
   - Resources + resource mapping (agents, systems, humans)

5. **UAPF uses Levels, not Tiers**
   - Levels describe **scope**, not modeling semantics.
   - Levels are numbered **1–4**.
   - **Level 0** is the enterprise collection index (workspace scope).

6. **Processes are code**
   - Stored in Git, reviewable, releasable.
   - Form a governed digital twin of enterprise operations.

## Specification (normative)
- SSOT boundaries: [`specification/00-ssot.md`](specification/00-ssot.md)
- Concepts & levels: [`specification/01-concepts.md`](specification/01-concepts.md)
- Process cornerstones: [`specification/02-process-cornerstones.md`](specification/02-process-cornerstones.md)
- Packages & workspaces: [`specification/03-packages-and-workspaces.md`](specification/03-packages-and-workspaces.md)
- Folder structure: [`specification/04-folder-structure.md`](specification/04-folder-structure.md)
- Level composition: [`specification/05-level-composition.md`](specification/05-level-composition.md)
- Package format (.uapf): [`specification/07-package-format.md`](specification/07-package-format.md)
- Export/Import/Validation: [`specification/08-export-import-validation.md`](specification/08-export-import-validation.md)
- MCP export & AI binding: [`specification/06-mcp-integration.md`](specification/06-mcp-integration.md)
- Conformance checklist: [`specification/10-conformance-checklist.md`](specification/10-conformance-checklist.md)

## Schemas (normative)
- UAPF manifest schema: [`schemas/uapf-manifest.schema.json`](schemas/uapf-manifest.schema.json)
- Enterprise index schema: [`schemas/enterprise-index.schema.json`](schemas/enterprise-index.schema.json)
- Resource mapping schema: [`schemas/resource-mapping.schema.json`](schemas/resource-mapping.schema.json)

## Normative boundaries
Only the following are normative SSOT for UAPF v1:
- [`/specification`](specification/)
- [`/schemas`](schemas/)

Examples are reference only and must validate against schemas.

## Quick validation (CI parity)
The repository validates examples against schemas via GitHub Actions.
To run locally (optional):
- Install: `pip install pyyaml jsonschema`
- Validate: run the script embedded in `.github/workflows/validate.yml`

## Examples
- Minimal Level-4 package: [`examples/minimal-l4-package`](examples/minimal-l4-package)
- Packed `.uapf` archives: [`examples/archives`](examples/archives)

## Non-goals
- This repository does **not** provide a BPMN/DMN/CMMN editor.
- This repository does **not** standardize organizational operating models beyond the UAPF packaging, governance, and portability rules.

## Versioning
This is **UAPF v1**. All breaking changes require a major version bump and a clear migration note.
