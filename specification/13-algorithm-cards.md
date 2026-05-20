# 13 — Algorithm Cards (Normative)

## 13.0 Purpose

This chapter defines the **Algorithm Card** artifact: a typed, versioned
governance wrapper for a single algorithm invoked behind a resource target.
A Card supplies the metadata required to identify, audit, validate, and
replace an algorithm without requiring the algorithm's implementation to
live inside the UAPF package.

Algorithm Cards extend the Resources cornerstone (see chapter 02). They
do NOT constitute a new cornerstone. The four cornerstones — BPMN, DMN,
CMMN, Resources + Mapping — defined in chapter 02 remain authoritative
and unchanged.

## 13.1 Scope

The Resources cornerstone declares *where* work is dispatched
(`ai_agent`, `human_role`, `system_api`, `mcp_tool`, `external_service`).
It does NOT declare *what* the dispatched algorithm does, who is
accountable for it, when it was last validated, or how it behaves under
uncertainty. Algorithm Cards fill that gap.

A Card is OPTIONAL. Packages whose resource targets are sufficiently
described by their existing target declaration MAY omit Cards entirely.
Packages whose targets invoke probabilistic models, learned classifiers,
third-party services, or any algorithm whose behaviour is not self-evident
from the target declaration alone SHOULD provide a Card per such target.

UAPF does NOT standardize through this chapter:
- the source language or representation of algorithms,
- the runtime that executes them,
- the format of training data, model weights, or external services
  referenced by a Card,
- any specific AI, ML, cryptographic, or privacy technique.

A Card describes; it does not implement.

## 13.2 The Algorithm Card artifact

A Card MUST be a YAML file under the package's `algorithms/` folder.

The folder location is configured by `paths.algorithms` in the manifest;
the default value is `algorithms`.

A Card MUST validate against `schemas/algorithm-card.schema.json`.

A Card file MUST use the suffix `.card.yaml`.

## 13.3 Required fields

Every Card MUST declare:

| Field | Constraint |
|---|---|
| `kind` | The literal string `uapf.algorithm.card` |
| `id` | Globally unique identifier, pattern `^algo\.[a-z0-9][a-z0-9._-]+$` |
| `version` | Semantic version string (chapter 12 quoting rules apply) |
| `name` | Human-readable title |
| `intent` | Plain-language description of what the algorithm does |
| `algorithm_kind` | One of: `formula`, `classifier`, `extractor`, `ml_model`, `rule_table`, `crypto`, `redactor`, `router`, `validator`, `aggregator`, `transformer`, `emitter`, `other` |
| `io` | Typed input/output contract |
| `implementation` | Discriminated by `type`: `inline`, `external`, or `composite` |
| `owners` | At least one owner, structurally consistent with `metadata/ownership.yaml` |
| `lifecycle` | Status, structurally consistent with `metadata/lifecycle.yaml` |

## 13.4 Implementation forms

The `implementation` block declares where the algorithm body lives. It is
a discriminated union on the `type` field.

### 13.4.1 `inline`

The algorithm body is present in the Card. Used when the algorithm is
declaratively expressible in a supported language. The Card MUST declare:

- `type`: the literal `inline`
- `language`: one of `feel`, `dmn`, `rego`, `regex`, `sql`, `wasm`
- `body`: the algorithm body as a string, OR
- `body_ref`: a path to a file in the package containing the body

Exactly one of `body` or `body_ref` MUST be present.

### 13.4.2 `external`

The algorithm body lives outside the package. The Card MUST declare:

- `type`: the literal `external`
- `medium`: one of `llm_prompt`, `ml_model`, `http_api`, `mcp_tool`,
  `native_binary`, `crypto_module`, `vendor_saas`
- `uri`: addressable reference (URL, file path, registry reference)
- `hash`: SHA-256 of the referenced artifact, format `sha256:<hex>`
- `runtime`: OPTIONAL medium-specific runtime configuration

### 13.4.3 `composite`

The Card refers to two or more other Cards composed together. The Card
MUST declare:

- `type`: the literal `composite`
- `composed_of`: ordered list of `{ ref, version }` referencing other
  Cards by `id`

Composite resolution is recursive. Implementations MUST detect cycles
(see SEM-008 in chapter 11).

## 13.5 IO contract

The `io` block MUST contain `inputs` and `outputs`, each a list of
field declarations. Each field MUST declare `id` and `type`. Each field
MAY declare `schema` (path to JSON Schema for complex types), `unit`
(SI unit, ISO 4217 currency, or domain-specific symbol), `cardinality`
(`single` | `optional` | `array` | `stream`; default `single`), and
`constraints` (a JSON Schema constraint subset).

## 13.6 Optional fields

A Card MAY declare:

| Field | Purpose |
|---|---|
| `determinism` | `deterministic` (default), `stochastic`, `learned` |
| `confidence` | Uncertainty model: `type`, `threshold`, `below_threshold` action |
| `side_effects` | `pure` (default), `reads_state`, `writes_state`, `external_call` |
| `complexity` | Latency and complexity-class declarations |
| `failure_mode` | Behaviour when output cannot be produced |
| `limitations` | Free-text list of known limitations |
| `reference` | Legal / methodology / standard citation |
| `validation` | `last_validated`, `test_suite`, `validator`, `methodology`, `metrics` |
| `audit` | Logging configuration: `log_inputs`, `log_outputs`, `retention` |

## 13.7 Type-specific extensions

A Card MAY include OPTIONAL extension blocks. Extensions are scoped by
`algorithm_kind` and carry domain-specific metadata that does not fit the
universal core. The following extensions are defined in this version:

- `ml` — applies when `algorithm_kind` is `ml_model` or `classifier`
  with an ML implementation. Links to Model Card URL, training data
  reference, fairness analysis.
- `crypto` — applies when `algorithm_kind` is `crypto`. FIPS certificate,
  algorithm identifier, key length, quantum-resistance flag.
- `privacy` — applies when the algorithm processes personal data.
  Technique, parameters, re-identification risk class.
- `risk` — algorithmic risk classification and human-oversight
  requirements.
- `prompt` — applies when `implementation.medium` is `llm_prompt`.
  Model identifier, prompt hash, temperature, max tokens.

Implementations MUST ignore extensions they do not understand.
Extensions MUST NOT contradict the universal core.

## 13.8 BPMN integration

A BPMN task that invokes an algorithm MUST declare it via the
`uapf:algorithmCardRef` attribute. The attribute value is the Card's
`id` (matching the pattern `^algo\.[a-z0-9][a-z0-9._-]+$`).

The UAPF BPMN namespace URI is `https://uapf.dev/bpmn/v2.4` and MUST
be bound to some XML namespace prefix on `<bpmn:definitions>`. The
recommended prefix is `uapf`. When the prefix `uapf` is already bound
to a different namespace on the same document (e.g., to a legacy
engine namespace such as `https://uapf.dev/bpmn-ext/v1` used for
`uapf:capability` / `uapf:decision`), implementations MUST choose a
different prefix for the v2.4 namespace (e.g., `uapfv24`, `uapfa`).
Renderers and validators MUST resolve attributes by namespace URI +
local name, not by literal prefix.

```xml
<bpmn:definitions
    xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:uapf="https://uapf.dev/bpmn/v2.4"
    ...>
  <bpmn:process id="Process_X">
    <bpmn:serviceTask id="Task_DetectPii"
                      name="Detect and redact PII"
                      uapf:algorithmCardRef="algo.example.pii_redactor">
      ...
    </bpmn:serviceTask>
  </bpmn:process>
</bpmn:definitions>
```

`uapf:algorithmCardRef` is valid on `bpmn:serviceTask`,
`bpmn:businessRuleTask`, and `bpmn:task`. It is NOT valid on user
tasks (a card describes an algorithm — user tasks invoke humans).
The attribute is declarative and authoritative: it is the canonical
statement that "this task invokes algorithm X."

A task MAY reference at most one Card. Multiple tasks MAY reference
the same Card. Implementations MUST resolve every
`uapf:algorithmCardRef` to a Card in `algorithms/`; unresolved
references MUST raise SEM-012.

Resource targets in `resources/mappings.yaml` describe *where* a task
is dispatched (the operational endpoint). They do NOT carry algorithm
identity. UAPF v2.3.0 placed `algorithm_card` on the resource target;
v2.4.0 reverses this — see the CHANGELOG for the rationale.

## 13.9 BPMN IO specification from the Card

A task that carries `uapf:algorithmCardRef` SHOULD ALSO carry a
`<bpmn:ioSpecification>` whose `dataInput` and `dataOutput` entries
correspond one-to-one with the Card's `io.inputs` and `io.outputs`.

The IO specification serves a single load-bearing purpose: making the
algorithm's data interface VISIBLE on the rendered diagram, so that
downstream gateways branching on an output (e.g. a DMN decision
keyed on `ai_confidence_score`) can be visually traced to the
algorithm that produces it.

```xml
<bpmn:serviceTask id="Task_DetectPii"
                  name="Detect and redact PII"
                  uapf:algorithmCardRef="algo.example.pii_redactor">
  <bpmn:ioSpecification>
    <bpmn:dataInput  id="Task_DetectPii_in_content"
                     name="content : string"/>
    <bpmn:dataOutput id="Task_DetectPii_out_redacted_content"
                     name="redacted_content : string"/>
    <bpmn:dataOutput id="Task_DetectPii_out_pii_present"
                     name="personas_koda_present : boolean"/>
    <bpmn:inputSet>
      <bpmn:dataInputRefs>Task_DetectPii_in_content</bpmn:dataInputRefs>
    </bpmn:inputSet>
    <bpmn:outputSet>
      <bpmn:dataOutputRefs>Task_DetectPii_out_redacted_content</bpmn:dataOutputRefs>
      <bpmn:dataOutputRefs>Task_DetectPii_out_pii_present</bpmn:dataOutputRefs>
    </bpmn:outputSet>
  </bpmn:ioSpecification>
</bpmn:serviceTask>
```

The Card's `io` block is the source of truth. The BPMN
`<bpmn:ioSpecification>` is a denormalisation for rendering and MAY
be synthesized by tooling at build time or rewrite time.
Implementations MUST detect mismatches and raise SEM-013 (advisory
error — auto-fixable by regeneration from the Card).

`dataInput.name` and `dataOutput.name` use the convention
`"{io_field.id} : {io_field.type}"` so renderers can show both the
name and the type in a single label.

## 13.10 Visual rendering (informative)

This subsection is INFORMATIVE — it does not mandate renderer
behaviour, but defines the recommended visual contract so multiple
implementations stay consistent.

Renderers that understand `uapf:algorithmCardRef` SHOULD draw a
serviceTask that carries it with the following visual elements,
overlaid on the standard BPMN serviceTask rectangle:

1. **Algorithm icon** in the top-left corner, replacing the default
   `serviceTask` gear marker. The recommended icon is a small stack
   of three offset rounded rectangles ("cards") with the letter
   `ƒ` centred in the top card — the metaphor is "algorithm card."
2. **Card identity line** rendered below the task's display name:
   the Card's `id` in a muted secondary color.
3. **Metadata line** rendered below the card identity: the Card's
   `version`, `algorithm_kind`, and `determinism` joined by a
   middle-dot separator.
4. **Risk-class dot** in the top-right corner, colored:
   * green for `risk.aiActRiskClass: minimal` or
     `determinism: deterministic` with no risk extension,
   * amber for `risk.aiActRiskClass: limited` or
     `determinism: stochastic`,
   * red for `risk.aiActRiskClass: high` or any card with
     `risk.humanOversight: mandatory`.
5. **Data objects** from the synthesized `<bpmn:ioSpecification>` —
   renderers SHOULD let bpmn-js (or equivalent) draw the inputs on
   the left of the task and the outputs on the right, so the data
   flow into downstream gateways is visible.

Click-through on the task body SHOULD open a panel showing the full
Card YAML.

Renderers that do NOT understand the UAPF extension MUST still
render the underlying `serviceTask` correctly — the extension
attribute is namespaced and ignored by conformant BPMN tooling.

## 13.11 Manifest declaration

(unchanged from prior text — kept here for reading flow.)

A package containing Algorithm Cards SHOULD declare:

```yaml
algorithm_cards: true
paths:
  algorithms: algorithms
```

## 13.12 Testing

Per-Card tests SHOULD be stored under
`tests/algorithms/<card-id>.test.yaml`.

Tests carry a uniform shape regardless of Card `algorithm_kind` or
`implementation.type`: input cases, expected outputs, and a tolerance
declaration. A passing test run is the operational definition of
validation.

## 13.13 Cards in MCP export

When a package is exported to MCP per chapter 06, Cards MUST be
exposable as resources under `uapf://algorithms/...` and queryable
via `uapf.list` and `uapf.get_artifact`.

The `uapf.resolve_resources` tool MUST include the Card reference
in the resolved binding when a target's task carries one.

## 13.14 Conformance

See chapter 10 for the Algorithm Cards conformance section.
