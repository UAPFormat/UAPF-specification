# MCP Export and AI Binding

## Goal
UAPF packages can be exported and imported into MCP-driven tooling to bind processes to AI agents.

## Export
A UAPF export operation:
- MUST produce a `.uapf` archive that preserves paths,
- MUST include `uapf.yaml`,
- MUST include all referenced cornerstone artifacts for the exported scope.

If exporting a higher-level package that includes lower-level packages, the exporter MUST either:
- (A) embed the included packages into the archive, or
- (B) produce a manifest with resolvable external package references.

## AI Binding
Resource mapping binds executable elements to execution targets.

Mappings MAY bind to:
- AI agents (by ID/capability),
- humans/roles,
- systems/APIs,
- MCP tools or endpoints.

A Level-4 package MUST provide at least one mapping target per executable task, OR explicitly mark tasks as "unbound" for later binding.

## Derived artifact rule
MCP conversion outputs (tool descriptors, prompts, agent cards, etc.) are derived and MUST NOT be treated as SSOT.
