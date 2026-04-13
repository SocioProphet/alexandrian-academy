# Support Learning Objectives and Pedagogic Quality Integration

## Purpose

This document defines how `alexandrian-academy` participates in the governed support, premium-support, query, and operational-intelligence loop.

The Academy is the normative learning lane. It evaluates explanation quality, pedagogic clarity, progression quality, prerequisite coverage, and learning-objective fitness for support assets, runbooks, guided remediation, and customer-facing educational materials.

## Repository role

`alexandrian-academy` contributes:

- learning-objective definitions for support and explanation quality
- curriculum-backed support and enablement objects
- pedagogic-quality metrics for support artifacts and runbooks
- governed improvement signals about confusion, prerequisite gaps, sequencing issues, and explanation fitness
- channel-agnostic learning objects that can be surfaced through support, self-service, or Matrix-assisted workflows

It does not own:

- ops-domain anomaly and metering normalization (`global-devsecops-intelligence`)
- canonical query orchestration (`sherlock-search`)
- long-horizon retained memory (`memory-mesh`)
- base ontology semantics (`ontogenesis`)

## Core learning-linked classes

The Academy should align to the shared semantic model through at least:

- `LearningObjective`
- `CurriculumObject`
- `ExplanationLink`
- `PedagogicQualityMetric`
- `SupportLearningAssessment`

## Support-oriented learning objectives

Learning objectives for support should include, at minimum:

- explanation clarity
- prerequisite coverage
- confusion reduction
- task completion readiness
- escalation readiness when self-service is insufficient
- progressive understanding across repeated interactions

These objectives should apply to:

- support assets
- runbooks
- guided remediation content
- premium-support explanations
- self-service educational flows
- operator-facing support guidance

## Pedagogic-quality loop

The pedagogic-quality loop should evaluate:

1. whether a support explanation is understandable
2. whether required prerequisites were surfaced in time
3. whether the user or operator was guided through a coherent sequence
4. whether the artifact should be revised, expanded, split, or retired
5. whether a curriculum-backed object should be added to the reusable asset graph

## Integration points

### With Sherlock
Sherlock should be able to query Academy-backed curriculum and explanation objects when assembling support and self-service responses.

### With Memory Mesh
`memory-mesh` should retain which support explanations worked, failed, caused confusion, or led to later escalations.

### With AI4IT operational intelligence
Operational-intelligence findings can reveal recurring confusion or repeated support patterns; these should become learning-objective inputs and Academy-backed improvement targets.

### With support and premium support
Standard support may use canonical curriculum-backed explanation objects.
Premium support may use deeper, tenant-aware overlays while still evaluating explanation quality against shared learning objectives.

## Immediate implementation tranche

1. Define support-oriented learning-objective families.
2. Define pedagogic-quality metrics for support artifacts and guided remediation.
3. Link curriculum-backed objects to support and self-service surfaces.
4. Feed learning-quality findings back into memory, query, and asset-improvement workflows.

## Outcome

When implemented correctly, `alexandrian-academy` becomes the normative learning and explanation-quality loop for support, premium support, self-service, and guided remediation rather than remaining a separate educational island.
