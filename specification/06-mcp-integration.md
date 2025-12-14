# 06 — MCP Export and Agentic Integrations (Normative)

## 6.0 Purpose and scope

UAPF packages and workspaces MUST be exportable to an agent-facing integration surface without losing governance, traceability, and resource bindings.

This chapter defines the normative requirements for exporting UAPF to MCP (Model Context Protocol) as a binding surface for AI agents and agentic runtimes.

This chapter does NOT standardize:
- any specific workflow engine implementation,
- any specific agent runtime,
- any specific DID method or VC format.

Those belong to satellite repositories and/or implementation guides.

## 6.1 SSOT alignment: only two UAPF artifact types

UAPF defines exactly two artifact types for export and binding:

1) **Workspace**
- A Git repository holding one or more UAPF packages and workspace-level indexes/policies.
- The Workspace is the authoritative SSOT.

2) **Package**
- A portable, versioned unit exported as a `.uapf` package (container format defined elsewhere).
- Packages are derived from (or imported into) a Workspace.

All MCP export behavior MUST be definable in terms of these two artifact types.

## 6.2 Two normative MCP transformation modes

UAPF-to-MCP MUST support BOTH transformation modes:

### 6.2.1 Package → MCP (portable import)

A conforming implementation MUST support importing any valid `.uapf` Package and exposing it as an MCP server surface.

This mode is intended for:
- portability (sharing a process externally),
- testing and validation,
- partner distribution,
- local binding to agents without requiring the full Workspace.

### 6.2.2 Workspace → MCP (SSOT repository mapping)

A conforming implementation MUST support mapping a UAPF Workspace (a Git repo) to an MCP server surface.

This mode is intended for:
- enterprise-scale process libraries,
- inventory/search across hundreds or thousands of packages,
- governance, versioning, and controlled rollout,
- binding that always reflects SSOT.

In Workspace → MCP mode, the MCP surface MUST reflect the Workspace as the authoritative source, not any cached exports.

## 6.3 Required MCP surface primitives (minimal contract)

To prevent ecosystem drift, UAPF standardizes a minimal set of MCP Tools and MCP Resources that MUST be exposed by any conforming UAPF→MCP implementation.

### 6.3.1 Required MCP tools (minimal set)

A conforming implementation MUST expose tools equivalent to:

- `uapf.describe`
  - Returns high-level capability metadata for the current mode (Package or Workspace), including supported operations.

- `uapf.list`
  - Workspace mode: lists packages and/or runnable entrypoints (filterable by level/domain/tags if supported).
  - Package mode: returns a singleton list for the current package.

- `uapf.run_process`
  - Executes a BPMN process entrypoint defined by the target package (or resolved from workspace selection).
  - MUST return execution result metadata and references to outputs.

- `uapf.evaluate_decision`
  - Evaluates a DMN decision entrypoint defined by the target package (or resolved from workspace selection).

- `uapf.resolve_resources`
  - Resolves resource bindings for a given package/process/task/decision.
  - MUST return binding targets for systems, humans, and agents (if defined).

- `uapf.get_artifact`
  - Fetches artifacts by reference:
    - manifest
    - BPMN XML
    - DMN XML
    - CMMN XML
    - docs/test artifacts if present

- `uapf.validate`
  - Workspace mode: MUST validate workspace indexes + all referenced packages against schemas.
  - Package mode: MAY validate the current package (RECOMMENDED).

Tool names MAY be prefixed/suffixed for implementation branding, but the canonical tool semantics above MUST be preserved and discoverable.

### 6.3.2 Required MCP resources (minimal set)

A conforming implementation MUST expose resources equivalent to:

- `uapf://manifest/...`
- `uapf://bpmn/...`
- `uapf://dmn/...`
- `uapf://cmmn/...`
- `uapf://policies/...`
  - Required claims / classification / constraints (if present)
- `uapf://bindings/...`
  - The resolved resource mapping output for a target scope

Resource URI structure MAY vary by implementation, but the categories above MUST be available and addressable.

## 6.3.3 Schema conformance

Any MCP export MUST expose only data that conforms to:
- manifest.schema.json
- resource-binding.schema.json
- policies.schema.json

If data cannot be resolved, implementations MUST return explicit `unbound` or `blocked` states.

## 6.4 Level handling rules in MCP export

UAPF Levels describe scope, not execution semantics.

- Level 4 packages typically expose runnable entrypoints directly.
- Higher level packages (Level 1–3) are compositions and MAY:
  - expose navigation tools (list/resolve children),
  - expose runnable orchestration ONLY if the package declares a runnable orchestration contract.

If a Level 1–3 package is not runnable, `uapf.run_process` MUST fail with a clear “not runnable at this level” error unless a runnable entrypoint is resolved (e.g., by selecting a Level 4 child).

## 6.5 Resource binding is first-class (mandatory)

MCP export MUST support binding not only processes/decisions/cases but also the resources they depend on.

A conforming implementation MUST support, at minimum, these resource classes when present in UAPF:

- **System resources** (APIs, queues, databases, services)
- **Human resources** (approvers/operators; human-in-the-loop steps)
- **Agent resources** (AI agents as callable workers or delegates)
- **External org resources** (partner endpoints, registries)

The MCP surface MUST expose resolved bindings via:
- the `uapf.resolve_resources` tool, and
- `uapf://bindings/...` resources.

If resource mappings are absent, implementations MUST return an explicit “unbound” result rather than inventing bindings.

## 6.6 Security, authorization, and verification hooks (profiles)

UAPF does not mandate a single security technology, but MCP export MUST provide policy hooks that prevent unauthorized execution and binding.

### 6.6.1 Capability gates (required)

A conforming implementation MUST support policy-driven gating before:
- executing sensitive processes,
- evaluating sensitive decisions,
- resolving or using sensitive resource bindings.

At minimum, gating MUST be enforceable via:
- workspace policy (preferred), and/or
- package policy.

### 6.6.2 DID/VC verification (optional profile)

If a Workspace or Package declares “required claims” (e.g., role, capability, clearance), an implementation MAY enforce those requirements using DID/VC verification.

If implemented:
- The verifier MUST support issuer allowlists and revocation/status checks where available.
- Failure to satisfy required claims MUST block execution/binding with a clear error.

This profile is OPTIONAL but RECOMMENDED for enterprise and multi-agent deployments.

### 6.6.3 A2A delegation (optional profile)

If a resource binding references an “agent endpoint”, implementations MAY support agent-to-agent delegation by:
- treating another agent as a resource target, and
- allowing tasks/steps to be delegated via a defined endpoint contract.

This profile is OPTIONAL and intended for multi-agent orchestration patterns.

## 6.7 Normative boundaries vs. reference implementations

Normative SSOT requirements are defined ONLY in:
- `/specification`
- `/schemas`

Reference implementations MAY exist in satellite repositories and MUST NOT override this chapter.

## 6.8 Reference implementation targets (non-normative pointers)

The following repositories may provide reference implementations:
- `uapf-engine` (execution/registry plane)
- `uapf-mcp` (MCP adapter plane)

Any behavior differences MUST be resolved in favor of this SSOT repository.

## 6.9 Non-normative implementation layers

The following are explicitly OUTSIDE SSOT scope:
- MCP server lifecycle
- Transport (stdio / HTTP / OAuth)
- DID method selection
- VC formats
- Agent runtime behavior

These belong in satellite repositories and MUST conform to this specification.
