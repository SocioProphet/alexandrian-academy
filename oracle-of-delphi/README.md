# Oracle of Delphi

Oracle of Delphi is the **evaluation and detector layer** for Alexandrian Academy. It runs automated and human-assisted checks on curriculum objects before they are promoted to Canon, and it records the policy-parameter snapshot under which each evaluation was performed — so evaluations are reproducible.

## Why reproducible evaluation matters

A curriculum object that "passed review" last year under one policy version may not pass today. Oracle of Delphi snapshots the policy parameters in force at evaluation time, so every finding is auditable: you can always answer "what rules were in effect when this was approved?"

Detectors also catch structural problems — missing evidence bundles, broken standards references, inaccessible media — that schema validation alone cannot catch.

## What lives here

| Record type | Description |
|------------|-------------|
| Evaluation | A structured assessment of an Atlas Codex object against Canon gates and policy rules |
| Detector finding | A machine-generated signal (schema error, broken reference, accessibility violation, etc.) |
| Policy snapshot | The state of `policy-parameter-sheet.v<N>.json` at evaluation time |

Evaluation records are identified with `DE-` prefixed object IDs.

## Evaluation process

1. A candidate object is submitted to Oracle of Delphi (manually or via automation).
2. Detectors run checks: schema validity, Canon gate conditions, standards reference integrity, accessibility requirements.
3. Results are recorded as an Evaluation with findings and a policy-parameter snapshot reference.
4. If all gates pass, the Evaluation authorizes a Moirai ChangeSet for Canon promotion.
5. If any gate fails, the findings are returned to the author for remediation.

## Policy-parameter snapshot

Every evaluation references the policy parameter sheet version in force at evaluation time:

```json
{
  "policy_parameter_version_ref": "policy/parameters/policy-parameter-sheet.v1.json"
}
```

Policy sheet: [`policy/parameters/policy-parameter-sheet.v1.json`](../policy/parameters/policy-parameter-sheet.v1.json)

Key defaults enforced:
- Canon requires an evidence bundle (`canon_requires_evidence: true`)
- Canon requires jurisdiction and pedagogy IDs (`canon_requires_jurisdiction_and_pedagogy: true`)
- Accepted objects require policy tags (`accepted_requires_policy_tags: true`)
- Accessibility baseline: WCAG 2.1 AA

## Relationships to other modules

- Evaluates **Atlas Codex** objects against Canon gates.
- Snapshots **Policy** parameters at evaluation time.
- Authorizes **Moirai Ledger** ChangeSets on passing evaluations.
- Findings reference **Ariadne's Thread** spans and **Aegis Vault** artifacts as evidence.

## Key references

- Architecture: [`docs/architecture/agentic-learning-teaching.md`](../docs/architecture/agentic-learning-teaching.md)
- Policy parameter sheet: [`policy/parameters/policy-parameter-sheet.v1.json`](../policy/parameters/policy-parameter-sheet.v1.json)
- Diagram specs: [`docs/diagrams/specs/`](../docs/diagrams/specs/)
