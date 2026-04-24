# Sherlock and Lampstand Ingestion Manifest for Learning Search Records

## Purpose

This manifest defines how Alexandrian Academy exports `LearningSearchRecord` objects for Sherlock Search and Lampstand-style indexing.

The export is read-only. It does not promote curriculum, execute learner actions, grant authority, or bypass Canon/Sandbox governance.

## Source

- `source`: `ALEXANDRIAN_ACADEMY`
- Primary entity type: `LEARNING_ACTION_EXPLANATION`
- Secondary entity type: `LEARNING_LOOP_RECORD`

## Source objects

`LearningSearchRecord` is generated from `LearningActionExplanation`, which is generated from `LearningLoopRecord`.

The record must preserve:

- target learning-loop reference;
- evidence anchor references;
- memory-mesh references;
- Sherlock retrieval references;
- Oracle evaluation references;
- Moirai ChangeSet references;
- policy-fabric decision references;
- AgentPlane run references.

## Index fields

| Field | Required | Notes |
| --- | --- | --- |
| `header.object_id` | yes | Stable Academy object identity. |
| `source` | yes | Must be `ALEXANDRIAN_ACADEMY`. |
| `entity_type` | yes | `LEARNING_ACTION_EXPLANATION` or `LEARNING_LOOP_RECORD`. |
| `title` | yes | Human-readable search title. |
| `text` | yes | Searchable explanation text. |
| `target_ref` | yes | Learning-loop or related Academy object reference. |
| `evidence_ref_ids` | yes | Evidence anchors remain visible. |
| `memory_ref_ids` | yes | Recall references remain visible. |
| `search_ref_ids` | yes | Sherlock retrieval trail remains visible. |
| `governance_ref_ids` | yes | Oracle, Moirai, and policy refs remain visible. |
| `agentplane_run_ref_ids` | optional | Reproducible run references where available. |
| `final_score` | optional | Ranking hint only; not truth authority. |

## Permission boundary

Search consumers must treat `LearningSearchRecord` as an indexable explanation artifact, not as an authorization grant.

The search result may reveal only references already allowed by the caller's Academy, jurisdiction, learner, workspace, and policy context.

The following are not allowed through this manifest:

- Canon promotion;
- learner action execution;
- private learner data disclosure outside allowed scope;
- policy grant creation;
- trace opening;
- revocation;
- modification of memory-mesh state.

## Display requirements

A search result should display:

1. recommended action summary;
2. curriculum or learning-loop target;
3. evidence anchors;
4. memory references;
5. Sherlock retrieval references;
6. governance references;
7. AgentPlane run refs when present.

## Recall handoff

If a downstream system wants memory recall/writeback, it must use `LearningMemoryRecord` and the guarded memoryd write helper, not `LearningSearchRecord`.

`LearningSearchRecord` is for discovery and retrieval. `LearningMemoryRecord` is for memoryd-compatible write payloads.
