# 12 — YAML Authoring Guidelines (Normative)

## 12.0 Purpose

YAML is used for UAPF manifest and metadata files. This chapter defines authoring rules to prevent common YAML pitfalls.

## 12.1 Required Quoting

The following values MUST be quoted as strings:

### 12.1.1 Version Numbers

```yaml
# WRONG - becomes float 1.0
version: 1.0

# CORRECT
version: "1.0.0"
```

### 12.1.2 Boolean-like Strings

```yaml
# WRONG - becomes boolean
enabled: yes
country: NO

# CORRECT
enabled: "yes"
country: "NO"
```

### 12.1.3 Time-like Strings

```yaml
# WRONG - becomes integer (seconds)
time: 12:30

# CORRECT
time: "12:30"
```

### 12.1.4 Numeric Strings

```yaml
# WRONG - becomes integer
zipcode: 01234

# CORRECT
zipcode: "01234"
```

## 12.2 Safe Value Patterns

| Field Type | Safe Pattern | Example |
|------------|--------------|---------|
| version | Always quote | `"1.0.0"` |
| id | Use snake_case/kebab-case | `my-process-id` |
| ref | Always quote | `"Task_1"` |
| timeout | Use duration suffix | `"30s"` |

## 12.3 Validation Requirement

Implementations MUST:
- Validate that `version` fields are strings
- Validate that boolean fields (`enabled`, `runnable`) are actual booleans
- Reject manifests where version appears as a number

## 12.4 YAML Version

UAPF files MUST be valid YAML 1.2.

## 12.5 Encoding

All YAML files MUST be UTF-8 encoded without BOM.
