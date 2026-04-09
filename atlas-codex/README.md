# Atlas Codex

Atlas Codex is the **learning object store** for Alexandrian Academy. It holds CurriculumPlans, UnitMaps, and AssessmentPlans — the canonical authored artifacts that define what learners do, in what order, to what standard.

Objects exist in one of two spaces:

| Space | Meaning |
|-------|---------|
| **Sandbox** | Draft or work-in-progress; not yet authoritative |
| **Canon** | Peer-reviewed, policy-compliant, authoritative |

Promotion from Sandbox to Canon requires passing Oracle of Delphi evaluations and creating a Moirai ChangeSet — an explicit, reversible governance record.

## Learning object types

### CurriculumPlan

A program-level intent document that defines:
- What will be taught (standards references, topic coverage)
- Who it is for (audience, jurisdiction constraints)
- How it will be taught (pedagogy profile: pacing model, advancement rules, learner agency)
- Privacy and accessibility requirements (FERPA, COPPA, WCAG modes)
- Promotion intent (Sandbox vs. Canon target)

Schema: [`platform-contracts/schemas/curriculum-plan.schema.json`](../platform-contracts/schemas/curriculum-plan.schema.json)
Template: [`templates/curriculum-builder/v1/curriculum-plan.template.json`](../templates/curriculum-builder/v1/curriculum-plan.template.json)
Example: [`platform-contracts/examples/curriculum-plan.sandbox.json`](../platform-contracts/examples/curriculum-plan.sandbox.json)

### UnitMap

A directed graph of learning nodes and their relationships (prerequisites, sequences, alternatives). Nodes are tagged with standards references using the `STD::` grammar.

Schema: [`platform-contracts/schemas/unit-map.schema.json`](../platform-contracts/schemas/unit-map.schema.json)
Template: [`templates/curriculum-builder/v1/unit-map.template.json`](../templates/curriculum-builder/v1/unit-map.template.json)

### AssessmentPlan

A definition of evaluation methods, mastery thresholds, and alternative modality requirements for a curriculum unit.

Schema: [`platform-contracts/schemas/assessment-plan.schema.json`](../platform-contracts/schemas/assessment-plan.schema.json)
Template: [`templates/curriculum-builder/v1/assessment-plan.template.json`](../templates/curriculum-builder/v1/assessment-plan.template.json)

## Validators

| Script | Purpose |
|--------|---------|
| `validators/validate_object.py` | Validate an object against its JSON Schema |
| `validators/validate_strict.py` | Validate + apply Canon gates (evidence, jurisdiction, pedagogy, policy tags) |

```bash
# Standard validation
python3 atlas-codex/validators/validate_object.py path/to/object.json

# Strict Canon-gate validation
python3 atlas-codex/validators/validate_strict.py path/to/object.json --expect-state accepted
```

## Canon gates

Beyond schema validity, Canon objects must satisfy:
- **G0** — `header.policy_tags` is a non-empty list
- **G1** — If `status: accepted` and `target_space: canon`, an `EvidenceBundle` with at least one span and one artifact reference must be present
- **G2** — `extension.jurisdiction_id` and `extension.pedagogy_id` must be set

## Relationships to other modules

- Cites **Aegis Vault** artifacts and **Ariadne's Thread** spans through `EvidenceBundle`.
- Is evaluated by **Oracle of Delphi** before Canon promotion.
- Promotion to Canon is recorded in **Moirai Ledger**.
- Feeds the **NBA Engine** via UnitMap and AssessmentPlan outputs.

## Key references

- Architecture: [`docs/architecture/agentic-learning-teaching.md`](../docs/architecture/agentic-learning-teaching.md)
- LOM mapping: [`docs/interoperability/lom-mapping.md`](../docs/interoperability/lom-mapping.md)
- Standards grammar: [`docs/standards/standards-id-grammar.md`](../docs/standards/standards-id-grammar.md)
- Diagram specs: [`docs/diagrams/specs/`](../docs/diagrams/specs/)
