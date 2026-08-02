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

## External-carrier provenance (CHRONOS alignment)

`sociosphere/docs/integration/neurosymbolic-chronos-alignment.md` names Alexandrian Academy the owning authority plane for "Learning/canonization." That document requires a CHRONOS carrier that references neuro-symbolic reasoning to record method family, source evidence, grounding status, validation status, and an explicit non-authority declaration before the owning plane admits it.

A ChangeSet may optionally carry an `external_provenance` block recording this for a candidate that originated outside Alexandrian Academy's own authoring flow (e.g. a Deep-Ontological-Network-inferred ontology relation, a dILP-style learned rule, or a KAIROS-style induced event schema proposed by Ontogenesis or another CHRONOS-adjacent repo). This is purely additive:

- **Purely-internal ChangeSets omit `external_provenance` entirely** and are validated exactly as before — nothing about the existing required fields changes.
- When present, `external_provenance` requires `method_family`, `grounding_status`, `validation_status`, and `owning_authority_non_claim: true` (the schema hard-fails any value other than `true` — an external source can never claim canonization authority through this field). It reuses the existing `evidence_refs` field for the CHRONOS "source evidence reference" concept rather than duplicating it.
- The external-carrier promotion gate in [`atlas-codex/validators/validate_changeset.py`](../atlas-codex/validators/validate_changeset.py) additionally requires, for an actual `PROMOTE_SANDBOX_TO_CANON` operation, `grounding_status` to be `grounded` or `verified` and `validation_status` to be `validated` before the candidate is admitted.
- Canonization authority never moves: Alexandrian Academy's own promotion gate remains the sole admitting authority for Atlas Codex Canon, regardless of what an external `external_provenance` block declares.

Examples: [`changesets/examples/changeset-0002.neurosymbolic-candidate.valid.json`](changesets/examples/changeset-0002.neurosymbolic-candidate.valid.json) (admitted), [`changesets/examples/changeset-0003.neurosymbolic-candidate.rejected.missing-provenance.json`](changesets/examples/changeset-0003.neurosymbolic-candidate.rejected.missing-provenance.json) and [`changesets/examples/changeset-0004.neurosymbolic-candidate.rejected.claims-authority.json`](changesets/examples/changeset-0004.neurosymbolic-candidate.rejected.claims-authority.json) (both rejected).

## Relationships to other modules

- **Atlas Codex** objects are the targets of ChangeSet operations.
- **Oracle of Delphi** evaluations are cited in ChangeSet justifications.
- **Ariadne's Thread** span IDs are referenced in `justification.supporting_span_ids`.
- **Aegis Vault** artifact IDs are referenced in `justification.source_artifact_ids`.

## Key references

- Architecture: [`docs/architecture/agentic-learning-teaching.md`](../docs/architecture/agentic-learning-teaching.md)
- ChangeSet schema: [`platform-contracts/schemas/changeset.schema.json`](../platform-contracts/schemas/changeset.schema.json)
- Diagram specs: [`docs/diagrams/specs/`](../docs/diagrams/specs/)
