# IOES Learning Artifact Stewardship

## Purpose

This document aligns Alexandrian Academy with the IOES stewardship stack.

IOES means Identity, Ontogenesis, Ecology, and Stewardship.

Alexandrian Academy already treats content, evidence, policy, provenance, accessibility, and governance as inseparable. This document adds the keeper relation: learning artifacts are not merely authored, stored, delivered, or promoted. They are stewarded.

## Core thesis

A learning artifact is a developmental object inside a transmission chain.

It carries evidence, pedagogy, jurisdiction, accessibility requirements, learner context, and canon status. It also requires keepers: people, communities, institutions, or authorized agents responsible for preserving, reviewing, correcting, transmitting, and retiring it.

Ownership does not imply stewardship.

Stewardship does not imply ownership.

Canon status does not imply final truth.

A learning artifact remains alive only while its evidence, pedagogy, accessibility, and keeper chain remain reviewable.

## Stewarded learning artifact

A StewardedLearningArtifact should record at least:

artifact_id

title

artifact_type

status

evidence_bundle_refs

curriculum_object_refs

jurisdiction_refs

pedagogy_refs

accessibility_refs

primary_keeper_ref

successor_refs

mentor_refs

apprentice_refs

review_interval

last_reviewed_at

stewardship_status

projection_constraints

policy_snapshot_refs

changeset_refs

## Stewardship statuses

candidate: stewardship proposed but not yet accepted.

active: keeper accepted responsibility.

needs_review: review interval expired or evidence changed.

contested: authority, accuracy, pedagogy, jurisdiction, or evidence is disputed.

handoff_pending: successor has been nominated but transfer is incomplete.

orphaned: no active keeper is present.

retired: artifact is intentionally withdrawn from active use but preserved.

archived: artifact is preserved for history and not recommended for active learning.

## Relationship to Sandbox and Canon

Sandbox artifacts may have provisional keepers.

Canon artifacts require active stewardship.

A canon artifact without an active keeper or successor posture should become needs_review or orphaned, not remain silently canonical.

A correction or retraction must preserve the prior state through Moirai Ledger rather than overwriting history.

## Mentorship and succession

Alexandrian Academy should model mentor and apprentice relations around learning artifacts.

A mentor relation means responsibility to help another entity understand, teach, review, or maintain the artifact.

An apprentice relation means a candidate successor is learning the artifact and its evidence chain.

A successor relation means a future keeper can assume stewardship under explicit handoff or abandonment conditions.

## Evidence discipline

Every claim in a learning artifact must remain anchored to evidence.

Every stewardship decision should cite evidence, authority, and policy posture.

Model-generated summaries may assist review but must not become canonical claims without citation and review.

## Ontogenesis of learning artifacts

Learning artifacts have developmental phases.

seed: initial idea, not yet instructionally reliable.

sandbox: draft object under active construction.

reviewed: passed local review but not canon.

canon: accepted for governed use.

revised: canon object updated through governance.

contested: reliability or applicability disputed.

retired: no longer recommended for active use.

archived: preserved for historical reference.

This lifecycle must be append-only and replayable.

## Gaia context

Learning artifacts depend on communities, standards bodies, languages, media infrastructure, accessibility tooling, educators, learners, and evidence sources.

When material, a learning artifact should record dependency context:

standards dependency

language dependency

technology dependency

community dependency

evidence-source dependency

accessibility dependency

jurisdiction dependency

This prevents curriculum from pretending to float in the void like a smug PDF balloon.

## First fixture target

The first fixture should demonstrate:

A sandbox learning artifact with evidence anchors.

A primary keeper accepting responsibility.

A successor candidate listed.

A policy snapshot requiring review before canon promotion.

A Moirai ChangeSet recording the proposed promotion.

A blocked example where canon promotion is rejected because no active keeper exists.

## Non-goals

This document does not change existing schemas.

It does not implement a StewardedLearningArtifact schema yet.

It defines the alignment target for the first IOES-aware Alexandrian Academy fixture and validator tranche.

## Next implementation targets

Create `platform-contracts/schemas/stewarded-learning-artifact.schema.json`.

Create valid and rejected examples.

Add validator coverage.

Add a Moirai Ledger ChangeSet example for stewardship handoff.

Bind the fixture to Policy Fabric protected-value veto posture and AgentPlane execution evidence.
