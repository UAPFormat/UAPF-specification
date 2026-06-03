# Appendix — Per-package MCP execution binding (`exposure.mcp`)

This appendix is informative. It explains how a UAPF package controls the
**execution** MCP surface defined normatively in chapter 06, using the
`exposure.mcp` block already present in the package manifest. It does not add
new normative requirements.

## Where the binding lives

The binding is the `exposure.mcp` object in a package's `uapf.yaml`. There is
**no separate integration file** — `exposure.mcp` is the single source of truth
for how a package is surfaced over MCP. Its standalone schema is
`schemas/uapf-mcp-binding.schema.json` (mirroring the embedded definition in
`uapf-manifest.schema.json`).

```yaml
exposure:
  mcp:
    enabled: true        # expose this package over MCP at all
    runnable: true        # expose execution entrypoints, not only read tools
    exposedEntrypoints:    # filter + naming (omit to expose all by default)
      - "iesnieguma-izskatisana"                 # bare process id -> default tool
      - tool: "izskatit_iesniegumu"               # explicit tool name...
        process: "iesnieguma-izskatisana"          # ...bound to this BPMN process
      - tool: "noteikt_prioritati"
        decision: "determine-priority"             # ...bound to this DMN decision
    exposedArtifacts: ["manifest", "bpmn", "dmn", "docs"]
```

## How it maps to the chapter-06 tools

A conforming UAPF→MCP implementation exposes the normative execution tools
(`uapf.run_process`, `uapf.evaluate_decision`, `uapf.describe`, `uapf.list`,
`uapf.resolve_resources`, `uapf.get_artifact`, `uapf.validate`).

- **No `exposedEntrypoints`** → every runnable process/decision is callable
  through the default tools.
- **Bare ids** → only those entrypoints are exposed (a filter).
- **`{tool, process|decision}`** → the entrypoint is exposed under an explicit,
  package-defined tool name (a rename), which is useful for agent platforms that
  present one tool per action (e.g. Microsoft Copilot Studio).

Decisions are always evaluated deterministically by the engine via the
evaluate-decision surface; the agent never interprets the decision tables.

## Capability hosts

A package declares the capabilities it needs at manifest top level
(`requires_capabilities`, e.g. `ai.redact@1`). The MCP server builds the engine
`hostManifest` from that list at session start and routes each capability to the
configured capability host (an LLM gateway for `ai.*`). **Where** the host runs
is deployment configuration, not package configuration, and so is intentionally
absent from `exposure.mcp`.

## Reference implementations

- `UAPFormat/uapf-mcp` (TypeScript) and `UAPFormat/uapf-mcp-go` (Go, embeddable)
  read this binding and expose the package's execution surface in front of a
  UAPF engine.
- ProcessGit serves the binding per repository at
  `/{owner}/{repo}/uapf-mcp` (execution), alongside `/{owner}/{repo}/mcp`
  (read/knowledge) and `/{owner}/{repo}/uapf-ip` (package descriptor).
