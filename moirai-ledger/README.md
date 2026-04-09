# Moirai Ledger

Moirai Ledger is the **append-only governance layer** for Alexandrian Academy. Every mutation to Canon — a promotion, a correction, a retraction — is recorded as a ChangeSet. The ledger is never rewritten; bad decisions are corrected by new ChangeSets, not by erasing the old ones.

## Why append-only governance matters

Accountability requires a record of who decided what, when, and on what evidence. Editability without a trail is the root cause of most "how did we get here?" problems in content management. By making every Canon mutation an explicit, auditable event, the ledger gives communities the ability to:
- Reconstruct the state of the curriculum at any point in time.
- Identify who promoted a disputed object and why.
- Reverse a bad promotion with a corresponding retraction ChangeSet.

## What lives here

| Record type | Description |
|------------|-------------|
| ChangeSet | A governance record describing one or more mutations to Canon objects |
| Correction | A ChangeSet that applies an erratum to a previously accepted object |
| Retraction | A ChangeSet that moves an accepted object to `retracted` status |

ChangeSets are identified with `MO-` prefixed object IDs.

## ChangeSet structure

Every ChangeSet includes:
- A `header` (standard `UniversalHeader` with `status: proposed`)
- A list of `changes` (operations: `PROMOTE_SANDBOX_TO_CANON`, `RETRACT`, `CORRECT`, etc.)
- A `justification` block: supporting span IDs, source artifact IDs, derivation activity, confidence score, and rationale text

Template: [`changesets/changeset.template.json`](changesets/changeset.template.json)
Example: [`changesets/examples/changeset-0001.promote-curriculum-plan.json`](changesets/examples/changeset-0001.promote-curriculum-plan.json)
Schema: [`platform-contracts/schemas/changeset.schema.json`](../platform-contracts/schemas/changeset.schema.json)

## Promotion workflow

1. Oracle of Delphi evaluates the candidate object and confirms it passes all gates.
2. Author or curator creates a ChangeSet with `operation: PROMOTE_SANDBOX_TO_CANON`.
3. ChangeSet includes the `before_hash` and `after_hash` of the object.
4. ChangeSet is submitted alongside the object in a pull request.
5. On merge, the object's `status` becomes `accepted` and its `promotion_intent.target_space` becomes `canon`.

See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for the full step-by-step process.

## Relationships to other modules

- **Atlas Codex** objects are the targets of ChangeSet operations.
- **Oracle of Delphi** evaluations are cited in ChangeSet justifications.
- **Ariadne's Thread** span IDs are referenced in `justification.supporting_span_ids`.
- **Aegis Vault** artifact IDs are referenced in `justification.source_artifact_ids`.

## Key references

- Architecture: [`docs/architecture/agentic-learning-teaching.md`](../docs/architecture/agentic-learning-teaching.md)
- ChangeSet schema: [`platform-contracts/schemas/changeset.schema.json`](../platform-contracts/schemas/changeset.schema.json)
- Diagram specs: [`docs/diagrams/specs/`](../docs/diagrams/specs/)
