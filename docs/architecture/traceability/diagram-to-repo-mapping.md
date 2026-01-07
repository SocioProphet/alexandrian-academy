# Traceability: Diagram Specs → Bounded Contexts → Contracts → Cadence

We treat diagram specs as architectural requirements. Every labeled box in Diagram 01 maps to:
- a bounded context directory,
- at least one contract schema or template,
- and an operational responsibility in the cadence.

## Diagram 01 box mappings

| Diagram Box | Repo Directory | Key Contracts/Templates |
|---|---|---|
| Aegis Vault (Immutable Evidence) | aegis-vault/ | EvidenceBundle (indirect), future artifact manifest schemas |
| Ariadne’s Thread (Anchors & Spans) | ariadnes-thread/ | EvidenceBundle supporting_span_ids semantics |
| Mnemosyne Forge (Accessible Derivatives) | mnemosyne-forge/ | future transcript/segment schemas |
| Atlas Codex (Sandbox/Canon) | atlas-codex/ | CurriculumPlan/UnitMap/AssessmentPlan schemas |
| Moirai Ledger (ChangeSets) | moirai-ledger/ | ChangeSet template (promotion intent) |
| Oracle of Delphi (Evaluations) | oracle-of-delphi/ | policy parameter sheet + future detector outputs |
| Curriculum Builder | templates/curriculum-builder/v1/ | object templates (PA-first) |
| NBA Engine | templates/nba/v1/ | NBA policy template |
| Renderers | docs/architecture/channels/ | channel mapping + action contract |

## Contract files already present

- platform-contracts/schemas/universal-header.schema.json
- platform-contracts/schemas/evidence-bundle.schema.json
- platform-contracts/schemas/curriculum-plan.schema.json
- platform-contracts/schemas/unit-map.schema.json
- platform-contracts/schemas/assessment-plan.schema.json
