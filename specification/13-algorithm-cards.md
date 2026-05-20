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

## 13.8 Relationship to Resource targets

A resource target in `resources/mappings.yaml` MAY reference a Card via
the optional `algorithm_card` property. The reference is the Card's `id`
or a relative path to the Card file.

```yaml
targets:
  - id: classifier_x
    type: ai_agent
    name: "Generic classifier"
    algorithm_card: algo.example.classifier_x
```

The Card and the target describe complementary facets of the same
resource: the target describes the *binding surface* (how to reach the
algorithm), the Card describes the *algorithmic surface* (what the
algorithm does, with what guarantees).

A target MAY reference at most one Card. Multiple targets MAY reference
the same Card. Implementations MUST resolve Card references during
validation; unresolved references MUST raise SEM-012.

## 13.9 Manifest declaration

A package containing Algorithm Cards SHOULD declare:

```yaml
algorithm_cards: true
paths:
  algorithms: algorithms
```

`algorithm_cards` is a manifest-level boolean declaring intent.
`paths.algorithms` declares the folder name if not the default. Both
fields are OPTIONAL and live at manifest top level — not inside the
closed `cornerstones` block.

## 13.10 Testing

Per-Card tests SHOULD be stored under
`tests/algorithms/<card-id>.test.yaml`.

Tests carry a uniform shape regardless of Card `algorithm_kind` or
`implementation.type`: input cases, expected outputs, and a tolerance
declaration. Deterministic algorithms use exact-match tolerance;
stochastic algorithms use distributional tolerance with explicit
pass-rate thresholds.

A passing test run is the operational definition of validation. CI
SHOULD update `validation.last_validated` on the Card when the test
suite passes against the current `implementation.hash` (for external)
or `body_ref` content hash (for inline).

The detailed test format is non-normative and lives in implementation
guides.

## 13.11 Cards in MCP export

When a package is exported to MCP per chapter 06, Cards MUST be
exposable as resources under `uapf://algorithms/...` and queryable via
`uapf.list` and `uapf.get_artifact`.

The `uapf.resolve_resources` tool MUST include the Card reference in
the resolved binding when a target's `algorithm_card` is present.

## 13.12 Conformance

See chapter 10 for the Algorithm Cards conformance section.
