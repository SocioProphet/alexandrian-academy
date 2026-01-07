# LOM Mapping to Alexandrian Academy Learning Objects

We align to IEEE LOM conceptually, but we do not copy any vendor schemas. We map LOM categories into our CurriculumPlan / UnitMap / AssessmentPlan envelopes.

## LOM General → Atlas Codex
- Identifier → object_id (+ optional alias_ids)
- Title → title
- Language → language
- Description → description
- Keyword → tags[]
- Coverage → jurisdiction_profile_id + audience constraints

## LOM Lifecycle → Moirai Ledger
- Version → version (semantic)
- Status → status (sandbox/canon)
- Contribute → actor + roles in ChangeSet(s)

## LOM Meta-Metadata → Ariadne’s Thread
- Metadata schema → schema_id
- Language → metadata.language
- Contribute → changeset_id / governance trail

## LOM Technical → Mnemosyne Forge
- Format → media.format
- Location → renderer targets (phone/chat/email/messaging/other)
- Requirements → accessibility + device/channel constraints

## LOM Educational → Curriculum Builder
- Learning Resource Type → unit.type
- Interactivity Type/Level → pedagogy_profile_id overlays
- Difficulty → difficulty band
- Typical Learning Time → duration estimates

## LOM Rights → Community MIT + Attribution
We are MIT-licensed at the community level, but provenance remains mandatory:
- accountability (who changed),
- provenance (what evidence supports),
- credit,
- governance (rollback).

These are enforced through Canon gates + ChangeSets.
