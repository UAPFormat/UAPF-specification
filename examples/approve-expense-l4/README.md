# Approve Expense (Level 4)

Concrete Level-4 example showing:
- BPMN executable flow (`bpmn/approve-expense.bpmn.xml`)
- DMN decision placeholder (`dmn/approval-policy.dmn.xml`)
- Resource definitions and task/decision bindings (`resources/mappings.yaml`)
- Governance metadata (`metadata/*`)

This example is intended to validate the package format and mapping model.

## Packed archive
A packed `.uapf` version of this package is committed at:

- `examples/archives/approve-expense-l4.uapf`

You can reproduce it with:
```bash
python tools/uapf-cli/uapf.py pack examples/approve-expense-l4 examples/archives/approve-expense-l4.uapf
```
