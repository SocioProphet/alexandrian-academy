# Mnemosyne Forge

Mnemosyne Forge produces **accessible, reproducible derivatives** from raw artifacts in Aegis Vault. This includes transcripts, closed captions, timed segments, and alternative-modality representations of media. All derivatives are generated deterministically from their source artifacts, so they can be regenerated if lost or updated.

## Why accessibility derivatives matter

Accessible learning is not optional. WCAG 2.1 AA compliance, captioned media, and alternative text are legal requirements in many jurisdictions and ethical requirements everywhere. Mnemosyne Forge makes accessibility a first-class, versioned, auditable output rather than an afterthought.

Pedagogical adaptation also depends on derivatives: a learner who needs a read-along transcript, a segmented audio clip, or a summarized section is served by derivatives, not the raw artifact.

## What lives here

| Derivative type | Description |
|----------------|-------------|
| Transcript | Full text of spoken audio, timestamped |
| Caption / subtitle | Time-coded caption file (e.g., VTT, SRT) |
| Segment | A bounded slice of media (audio or video chunk) aligned to an anchor span |
| Alternative modality | Text description of an image, simplified reading level version, etc. |

Derivatives are identified with `MN-` prefixed object IDs and reference their source Aegis Vault artifact.

## Relationships to other modules

- **Aegis Vault** provides the source artifacts.
- **Ariadne's Thread** provides the span boundaries used for segmentation and alignment.
- **Atlas Codex** references derivatives in learning objects that require accessible media.
- **Policy** enforces that canon learning objects with public media require captions and transcripts (per `policy-parameter-sheet.v1.json`).

## Accessibility policy defaults

From [`policy/parameters/policy-parameter-sheet.v1.json`](../policy/parameters/policy-parameter-sheet.v1.json):
- WCAG profile: `WCAG2.1-AA`
- Public media requires captions: `true`
- Public media requires transcripts: `true`
- Assessment alternative modalities required: `true`

## Key references

- Architecture: [`docs/architecture/agentic-learning-teaching.md`](../docs/architecture/agentic-learning-teaching.md)
- Policy parameters: [`policy/parameters/policy-parameter-sheet.v1.json`](../policy/parameters/policy-parameter-sheet.v1.json)
- Diagram specs: [`docs/diagrams/specs/`](../docs/diagrams/specs/)
