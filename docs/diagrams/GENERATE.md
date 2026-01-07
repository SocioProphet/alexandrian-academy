# Diagram Generation Workflow (No Sensitive Inputs)

We do not store, upload, or commit sensitive third-party diagrams. We generate repository-original diagrams from specs.

## Inputs
- docs/diagrams/specs/*.spec.md
- docs/diagrams/prompts/dalle-prompts.md

## Outputs
- docs/diagrams/rendered/diagram-01-platform-architecture.png
- docs/diagrams/rendered/diagram-02-core-research-areas.png

## Procedure
1) Use the prompt catalog to generate diagrams with DALL·E (or equivalent generator).
2) Review for:
   - no third-party names,
   - only our semantic labels,
   - clear arrows and readable typography.
3) Commit the generated PNGs into docs/diagrams/rendered/.
4) If the spec changes, increment spec version and regenerate.

## Governance
- Any change to diagram specs is a documentation change that should be reviewed like an architecture change.
