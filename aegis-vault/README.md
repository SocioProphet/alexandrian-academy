# Aegis Vault

Aegis Vault is the **immutable evidence store** for Alexandrian Academy. Every source artifact — video, audio, document, transcript, assessment record — enters the platform here and is never modified in place. Immutability is the foundation for trustworthy citations and reproducible evaluations.

## Why immutability matters

Learning claims and curriculum objects must cite evidence that cannot be silently changed after the fact. Content-addressing (hashing) each artifact means any downstream anchor or span can verify its source has not drifted. This eliminates the "I updated the file" problem that makes most citation systems untrustworthy.

## What lives here

| Artifact type | Examples |
|--------------|---------|
| Media | Video recordings, audio files, lecture captures |
| Documents | PDFs, HTML readings, assignment instructions |
| Assessment records | Rubrics, test blueprints, scoring guides |
| Ingested third-party sources | OCW dumps, MOOC exports (referenced, not re-hosted) |

Each artifact is identified by a content hash and an `AE-` prefixed object ID.

## Relationships to other modules

- **Ariadne's Thread** points precise anchors and spans _into_ Aegis Vault artifacts.
- **Mnemosyne Forge** derives accessible derivatives (transcripts, captions) _from_ Aegis Vault artifacts.
- **Atlas Codex** learning objects cite Aegis Vault artifacts through an `EvidenceBundle`.

## Key references

- Architecture: [`docs/architecture/agentic-learning-teaching.md`](../docs/architecture/agentic-learning-teaching.md)
- Evidence bundle schema: [`platform-contracts/schemas/evidence-bundle.schema.json`](../platform-contracts/schemas/evidence-bundle.schema.json)
- Diagram specs: [`docs/diagrams/specs/`](../docs/diagrams/specs/)
