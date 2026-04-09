# Ariadne's Thread

Ariadne's Thread provides **precise, verifiable anchors and spans** into immutable artifacts stored in Aegis Vault. Where Aegis Vault holds the evidence, Ariadne's Thread pins the exact location — a time offset in a video, a paragraph range in a document, a segment of an assessment record — so that citations are specific and falsifiable.

## Why precise anchoring matters

A citation that points to an entire document is almost as weak as no citation at all. "See Smith (2023)" is not the same as "see Smith (2023), section 3.2, paragraph 1, lines 4-7." Ariadne's Thread enforces the latter, making every curriculum claim as specific as the evidence supports.

## What lives here

| Record type | Description |
|------------|-------------|
| Anchor | A named pointer to an artifact (by `AE-` ID) |
| Span | A bounded region within an artifact (time range, byte range, paragraph index, etc.) |
| Citation record | A span linked to the claim or curriculum node it supports |

Spans are identified with `AR-` prefixed object IDs.

## Relationships to other modules

- **Aegis Vault** provides the immutable artifacts that spans point into.
- **Mnemosyne Forge** uses spans to align transcripts and captions to source media.
- **Atlas Codex** references spans in `EvidenceBundle.supporting_span_ids`.
- **Moirai Ledger** ChangeSets cite spans to justify governance decisions.

## Key references

- Architecture: [`docs/architecture/agentic-learning-teaching.md`](../docs/architecture/agentic-learning-teaching.md)
- Evidence bundle schema: [`platform-contracts/schemas/evidence-bundle.schema.json`](../platform-contracts/schemas/evidence-bundle.schema.json)
- Diagram specs: [`docs/diagrams/specs/`](../docs/diagrams/specs/)
