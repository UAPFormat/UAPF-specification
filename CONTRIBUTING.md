# Contributing to UAPF-specification (SSOT)

## Normative boundaries
This repository is SSOT. Only the following are normative:
- `/specification/**`
- `/schemas/**`

Everything else is informative and MUST NOT redefine rules, file structures, schema meanings, or level definitions.

## Change policy
- Any change that affects structure, semantics, required fields, or validation MUST update:
  1) `/specification/**` (prose), and
  2) `/schemas/**` (validation),
  3) plus at least one example under `/examples/**`.

## Pull request checklist
- [ ] I updated spec prose if I changed behavior/structure.
- [ ] I updated schema(s) if I changed required fields or formats.
- [ ] I updated examples and CI passes.
- [ ] I did not introduce MUST/SHALL language outside `/specification/**`.
