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

A package containing Algorithm Cards SHOULD declare:

```yaml
algorithm_cards: true
paths:
  algorithms: algorithms
```

## 13.12 Testing (embedded; v2.5.0+)

**Breaking change in v2.5.0.** Per-Card tests MUST now be embedded
directly in the Card under the top-level `tests` array. The previous
sidecar location `tests/algorithms/<card-id>.test.yaml` is **removed**
as a valid location for algorithm card tests. (Sidecar tests under
`tests/` remain valid for BPMN, DMN, and CMMN cornerstones — only
algorithm cards are affected by this change.)

A Card MUST declare at least two test cases. The Algorithm Card
viewer (chapter 13.16) renders these as the primary interaction
surface, so two is a viewer-driven minimum, not an arbitrary count;
single-case test corpora hide failure modes and produce sample
browsers with only one row.

Each entry has a uniform shape regardless of `algorithm_kind` or
`implementation.type`:

```yaml
tests:
  - name: "Latvian personas kods in plain text"
    description: "Standard 11-digit personal ID code with hyphen"
    inputs:
      content: "Personas kods: 010101-12345 saskaņā ar likumu."
    expected_outputs:
      redacted_content: "Personas kods: [REDACTED] saskaņā ar likumu."
      personas_koda_present: true
      detected_entity_types: ["PERSONAS_KODS"]
    tolerance:                   # optional, for stochastic outputs
      ai_confidence_score: 0.05

  - name: "no PII present"
    inputs:
      content: "Vakar bija saulains laiks."
    expected_outputs:
      redacted_content: "Vakar bija saulains laiks."
      personas_koda_present: false
      detected_entity_types: []
```

Fields:

* `name` (REQUIRED) — short label, used as the tab/row label in the viewer.
* `description` (OPTIONAL) — longer explanation; shown on expand.
* `inputs` (REQUIRED) — concrete values keyed by `io.inputs[].id`.
  The viewer's sample browser matches user-entered values against
  these by exact string equality (per SEM-015 the keys SHOULD match
  the Card's declared input ids).
* `expected_outputs` (REQUIRED) — expected values keyed by
  `io.outputs[].id`. For deterministic cards this is a hard assertion;
  for stochastic cards, see `tolerance`.
* `tolerance` (OPTIONAL) — per-output absolute delta for stochastic
  outputs. Numeric values mean ±delta; test runners that do not
  implement tolerance MAY skip those assertions but MUST still load
  the case.

A passing test run is the operational definition of validation
(unchanged from v2.4.0).

## 13.13 Cards in MCP export

When a package is exported to MCP per chapter 06, Cards MUST be
exposable as resources under `uapf://algorithms/...` and queryable
via `uapf.list` and `uapf.get_artifact`.

The `uapf.resolve_resources` tool MUST include the Card reference
in the resolved binding when a target's task carries one.

## 13.14 Conformance

See chapter 10 for the Algorithm Cards conformance section.

## 13.15 Migration guide from v2.4.0

Existing v2.4.0 packages with sidecar tests under
`tests/algorithms/<card-id>.test.yaml` MUST migrate to embedded
tests when upgrading to v2.5.0. Mechanical migration:

1. For each `algorithms/<id>.card.yaml`, find any
   `tests/algorithms/<id>.test.yaml` sidecar.
2. Copy each sidecar test case under the Card's new top-level
   `tests:` array. Field names map 1:1 (`inputs`, `expected_outputs`,
   `tolerance`).
3. Delete the sidecar `.test.yaml` file.
4. If the resulting `tests:` array has fewer than two entries, the
   author MUST add at least one more case (e.g. a negative or
   edge-case input). SEM-014 will fail otherwise.

The migration is mechanical for the data shape but requires editorial
judgment when fewer than two cases exist. The viewer minimum of two
is intentional — see 13.12.

## 13.16 Algorithm Card viewer (informative; v2.5.0+)

This subsection is INFORMATIVE — it does not mandate viewer
behaviour, but defines the recommended viewer contract so multiple
implementations stay consistent. A conforming viewer renders an
algorithm card as the Preview tab on `*.card.yaml` files, alongside
the host's existing Edit File and View Source tabs.

The Preview tab is polymorphic on `implementation.type` plus the
relevant sub-field (`impl_inline.language` or `impl_external.medium`).
All Preview renderings share a common header (card metadata strip,
IO contract panel, risk-class dot per chapter 13.10) and a common
footer (sample browser driven by the embedded `tests` array). The
middle section varies by implementation type:

* `implementation.type: external` — the card is a black box. The
  viewer renders the IO contract and a **sample browser**: the user
  edits input values, the viewer matches by exact string equality
  against `tests[].inputs`, and on match displays the corresponding
  `expected_outputs`. On no match, the viewer displays the recorded
  samples as a curated dropdown without claiming to predict the
  output of arbitrary inputs.
* `implementation.type: inline` — the card carries its logic
  literally. The viewer renders the source per `impl_inline.language`:
  * `regex` — pattern shown; sample text from `tests[].inputs`
    interactively highlights matches.
  * `feel` — expression shown; user-editable input fields evaluate
    the expression client-side; result displayed live.
  * `dmn` — link out to the corresponding `dmn/<id>.dmn` cornerstone
    file rather than re-rendering it in the algorithm viewer
    (DMN has its own cornerstone visualiser).
  * `rego`, `sql`, `wasm` — syntax-highlighted source with the
    sample browser; live evaluation is implementation-defined.
* `implementation.type: composite` — call-tree graph of the
  composed Card references, each node clickable to navigate into
  that Card's viewer.

The risk-class dot uses the same derivation as chapter 13.10
(green for deterministic / minimal-risk, amber for stochastic or
limited-risk-with-oversight, red for high-risk or
mandatory-oversight). The dot appears in the metadata strip.

Click-through from the BPMN diagram's algorithm task overlay
(chapter 13.10) SHOULD open the Algorithm Card viewer as a
side-panel drawer over the BPMN, preserving process context rather
than navigating away.
