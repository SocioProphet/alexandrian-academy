# Alexandrian Academy Evaluation Fabric Alignment

Status: draft
Owner: Alexandrian Academy
Consumes:
- SocioProphet/socioprophet-standards-knowledge: `standards/evaluation-fabric-standard.v1.md`
- SocioProphet/socioprophet-standards-knowledge: `standards/agent-education-equivalence-standard.v1.md`
- SocioProphet/socioprophet-standards-knowledge: `standards/foundational-training-cycle-standard.v1.md`
- SocioProphet/socioprophet-standards-storage: `standards/open-courseware-corpus-standard.v1.md`
- SocioProphet/socioprophet-standards-storage: `standards/evaluation-record-standard.v1.md`
- SocioProphet/sociosphere: `standards/angel-of-the-lord/README.md`

## Purpose

Alexandrian Academy is the teaching and curriculum layer for SocioProphet. It converts systems-learning loops, public courseware corpora, platform standards, MLOps lessons, ontology patterns, SourceOS lifecycle work, and Atlas orchestration patterns into structured human and agent education.

This document aligns Academy modules with the SocioProphet evaluation fabric so that completion, mastery, transfer, and progression claims are evidence-backed, regression-checked, and adversarially reviewed where required.

## Scope

This alignment applies to:

- human education modules;
- Michael-agent degree-equivalent education tracks;
- SocioProphet agent learning modules;
- systems-learning-loop curriculum;
- MLOps/model-serving curriculum;
- ontology/knowledge-graph curriculum;
- SourceOS/SociOS lifecycle curriculum;
- Prophet Platform and Atlas orchestration curriculum.

## Academy evaluation loop

Each module should follow:

```text
principle -> worked example -> assignment/lab/test/exam/project -> evidence -> rubric/metric -> feedback -> reinforcement -> transfer task -> prior regression check -> Angel review where required -> completion/remediation
```

## Regenerative curriculum loop

Academy curriculum must not be static. Each pass should enrich the corpus and curriculum while preserving prior accepted performance.

```text
capture refs and courseware -> generate curriculum map -> run tests/evaluations -> apply Angel hardening -> capture learnings -> enrich refs/rubrics/tasks -> regenerate curriculum -> rerun prior regression checks
```

Each pass should emit:

- updated curriculum source references;
- CoursewareCorpus or SourceRecord references;
- CurriculumCorpusSnapshot references where applicable;
- CurriculumEnrichmentDelta records where applicable;
- EvaluationRecords;
- EpochRegressionChecks for epoch-bearing tracks;
- AngelEpochGrades where required;
- remediation records;
- updated transfer tasks.

## Required module structure

```yaml
id: stable module identifier
title: human readable title
track: systems_learning | mlops | ontology | sourceos | platform | atlas | agent_education | other
level: introductory | intermediate | advanced | graduate_equivalent | professional
learning_objectives: list
source_corpora: CoursewareCorpus or SourceRecord references
lessons: list of lesson references
worked_examples: list
assignments: list
labs: list
published_tests_or_exams: list where applicable
project_or_transfer_task: required for advanced modules
rubric: Rubric reference
metrics: Metric references where applicable
evidence_required: EvidenceRequirement references
monotonicity_policy: MonotonicProgressPolicy reference for epoch-bearing modules
angel_required: true | false | conditional
completion_rule: pass | pass_with_findings | remediation_required | blocked
```

## Michael-agent education rule

When a module is used for Michael-agent degree-equivalent education:

1. primary course material should come from public institutional sources where available;
2. published assignments, tests, exams, labs, and projects should be used as assessment corpora where lawful;
3. Michael must produce an AssessmentAttempt record;
4. the attempt must be stored in an EvidenceBundle;
5. prior accepted tests, exams, projects, and transfer tasks must remain non-regressed within the monotonic progress policy;
6. a transfer task must demonstrate application to SocioProphet work;
7. the epoch must receive Angel of the Lord grading;
8. unresolved blocker or material high findings prevent completion.

## Human education rule

Human learners may complete modules through assignments, labs, tests, exams, projects, reviews, and transfer tasks. Human-only institutional credentials remain outside the Academy unless separately and truthfully documented.

Human tracks should still use regression and reinforcement checks where the learning path claims continuous mastery.

## Transfer tasks

Every advanced module should include a transfer task. Examples:

- convert an institutional learning-loop case study into a Prophet Platform primitive;
- map a public course to an agent education requirement;
- implement a Ray Serve/KubeRay serving-loop evaluation plan;
- build an ontology diff and SHACL validation plan;
- produce a SourceOS release-set evaluation record;
- write an Angel of the Lord remediation report;
- regenerate a curriculum module after evaluation findings and prove no regression.

## Courseware corpus handling

Academy modules should prefer primary public courseware and public course catalogs when mapping degree-equivalent requirements. Do not redistribute materials unless their license permits redistribution. Store metadata, citations, evidence records, and learner/agent outputs.

Published exams and tests may be used as assessment corpora where terms permit. Answer keys or solutions may support practice and review, but they are not proof of mastery without independent attempts, review, transfer tasks, and regression checks.

## Evaluation artifacts

Accepted module completion should emit:

- EvaluationRecord;
- EvaluationAttempt records;
- EvidenceBundle;
- RemediationRecord when needed;
- TransferEvaluationRecord for advanced modules;
- EpochRegressionCheck for epoch-bearing modules;
- AngelEpochGrade when Michael-agent or high-consequence platform work is involved.

## Initial curriculum adapters

The first Academy adapters should be:

```text
courses/systems-learning-loops/
courses/michael-agent-foundations/
courses/mlops-and-model-serving/
courses/ontology-and-knowledge-systems/
courses/sourceos-lifecycle/
courses/platform-governance/
```

## Non-hand-waving rule

No Academy module may claim completion, mastery, transfer, or progression unless its evaluation artifacts exist and satisfy the evaluation fabric standard.

No regeneration pass may claim improvement if it hides regression against prior accepted grades, tests, projects, transfer tasks, or Angel findings.
