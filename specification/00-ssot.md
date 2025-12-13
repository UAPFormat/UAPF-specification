# SSOT and Normative Boundaries

## Single Source of Truth
The **Git workspace** is the Single Source of Truth (SSOT) for UAPF artifacts.

In this repository, the SSOT for the UAPF standard is:

- `/specification/**` (normative text)
- `/schemas/**` (normative validation rules)

## Normative vs Informative
- **Normative** content uses terms like MUST, MUST NOT, REQUIRED, SHOULD, MAY.
- **Informative** content is explanatory only and MUST NOT redefine any structure, schema, or rule.

## Conflict resolution
If any conflict exists between:
- an example/template and the specification, or
- a website/blog post and the specification,

then the content in `/specification/**` and `/schemas/**` is authoritative.

## Derived artifacts
Exports such as `.uapf` archives, generated catalogs, published documentation, and MCP conversion outputs are **derived artifacts** and MUST NOT be treated as SSOT.
