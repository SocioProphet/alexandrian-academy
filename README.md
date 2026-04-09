# Alexandrian Academy

[![CI](https://github.com/SocioProphet/alexandrian-academy/actions/workflows/ci.yml/badge.svg)](https://github.com/SocioProphet/alexandrian-academy/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Alexandrian Academy** is an open, policy-governed platform for building and delivering curriculum at scale. It binds evidence-based learning objects to jurisdiction constraints, pedagogy profiles, and omnichannel delivery — with full provenance, accessibility, and governance baked in at the data layer.

Designed for K-12, higher education, and lifelong learning, the platform lets communities author, review, and promote curriculum through a reproducible, append-only governance loop rather than ad-hoc content management.

---

## Why this exists

Most learning platforms separate _content_ from _evidence_, _policy_, and _provenance_. Alexandrian Academy treats them as inseparable:

- Every artifact is immutable and content-addressed.
- Every claim cites a verifiable anchor.
- Every curriculum object carries jurisdiction constraints and a pedagogy profile.
- Every promotion from draft to canon passes an explicit governance gate.
- Every evaluation is reproducible and policy-snapshotted.

The result is a platform that can explain _why_ a learner should do something next, hold that explanation to a standards citation, and adapt it to any delivery channel.

---

## Architecture overview

```
Learner/Teacher
      |
      v
+--------------+     +------------------+     +------------------+
|  Aegis Vault |---->| Ariadne's Thread |---->| Mnemosyne Forge  |
|  (immutable  |     |  (anchors/spans  |     |  (transcripts,   |
|   evidence)  |     |   into evidence) |     |   captions,      |
+--------------+     +------------------+     |   derivatives)   |
                                              +--------+---------+
                                                       |
                                          Policy + Authoring
                                                       |
                                                       v
                                           +------------------+
                                           |   Atlas Codex    |
                                           |  (Sandbox/Canon  |
                                           |  learning objects)|
                                           +------+-----------+
                                                  |
                              +-------------------+-----------------+
                              v                   v                 v
                   +------------------+  +----------------+  +-------------+
                   | Oracle of Delphi |  |  Moirai Ledger |  |  NBA Engine |
                   |  (evaluations,   |->|  (ChangeSets,  |  | (next-best- |
                   |   detectors)     |  |   governance)  |  |  action)    |
                   +------------------+  +----------------+  +------+------+
                                                                     |
                                                             +-------v-------+
                                                             |   Renderers   |
                                                             | phone - chat  |
                                                             | email - other |
                                                             +---------------+
```

Full narrative: [`docs/architecture/agentic-learning-teaching.md`](docs/architecture/agentic-learning-teaching.md)

---

## Bounded contexts (monorepo modules)

| Module | Purpose | Key artifacts |
|--------|---------|---------------|
| [`aegis-vault/`](aegis-vault/) | Immutable, content-addressed evidence artifacts | Raw source files, hashed blobs |
| [`ariadnes-thread/`](ariadnes-thread/) | Anchors and precise spans into artifacts | Span pointers, citation records |
| [`mnemosyne-forge/`](mnemosyne-forge/) | Accessible derivatives: transcripts, captions, segments | WCAG-compliant media derivatives |
| [`atlas-codex/`](atlas-codex/) | Learning objects (CurriculumPlan, UnitMap, AssessmentPlan) with Sandbox/Canon separation | JSON learning objects, validators |
| [`moirai-ledger/`](moirai-ledger/) | Append-only governance: ChangeSets, corrections, contribution records | ChangeSet JSON, promotion history |
| [`oracle-of-delphi/`](oracle-of-delphi/) | Evaluations, detector findings, policy-parameter snapshots | Evaluation records, detector output |
| [`platform-contracts/`](platform-contracts/) | Shared JSON schemas and enums for all modules | JSON Schema (Draft 2020-12) |
| [`policy/`](policy/) | Jurisdiction profiles and policy parameter sheets | US-PA profile, WCAG/FERPA/COPPA parameters |
| [`templates/`](templates/) | Starter templates for curriculum builders and NBA policies | curriculum-plan, unit-map, assessment-plan |
| [`tools/`](tools/) | CLI utilities: ID generation, diagram verification | `idgen.py`, `verify_diagrams.py` |

---

## Key concepts

**Sandbox vs. Canon**
Learning objects start as _sandbox_ drafts. Promotion to _canon_ requires passing Oracle of Delphi evaluations and creating a Moirai ChangeSet — an explicit, reversible governance record.

**Evidence-first provenance**
All curriculum objects must cite immutable artifacts (Aegis Vault) via precise anchors (Ariadne's Thread). Claims require verifiable citations, not assertions.

**Jurisdiction + pedagogy profiles**
Every CurriculumPlan carries a `jurisdiction_id` (e.g., `US-PA`) and a `pedagogy_id` (e.g., `montessori.v1`). Jurisdiction constraints encode privacy mode (FERPA/COPPA), required standards references, and accessibility requirements. Pedagogy parameters control pacing, advancement rules, and learner agency.

**Standards identifier grammar**
Standards are referenced with deterministic IDs:
```
STD::<COUNTRY>::<JURISDICTION>::<STANDARD_SET>::<VERSION>::<PATH>
# e.g. STD::US::PA::PA-ELA::v1::K:Reading:FoundationalSkills:RF.1.1
```
See [`docs/standards/standards-id-grammar.md`](docs/standards/standards-id-grammar.md).

**Omnichannel NBA**
The Next Best Action engine emits channel-agnostic action contracts. Renderers adapt them to phone, chat, messaging, email, or other surfaces.

---

## Data contracts

All shared object types are defined in [`platform-contracts/schemas/`](platform-contracts/schemas/) using JSON Schema Draft 2020-12:

| Schema | Covers |
|--------|--------|
| `universal-header.schema.json` | Object identity, versioning, status lifecycle, policy tags |
| `curriculum-plan.schema.json` | Program-level curriculum intent + LOM metadata |
| `unit-map.schema.json` | Learning graph nodes and edges |
| `assessment-plan.schema.json` | Evaluation schema and mastery thresholds |
| `evidence-bundle.schema.json` | Provenance anchors and derivation metadata |
| `changeset.schema.json` | Governance mutation records |

Object status lifecycle: `draft` -> `proposed` -> `reviewed` -> `accepted` -> `deprecated` / `retracted`

---

## Quick start

### Prerequisites
- Python 3.12+
- `make`

### Setup and validate

```bash
# Create virtual environment and install dependencies
make deps

# Validate example objects against their schemas
make validate-examples

# Run all validation (diagrams + examples + templates)
make validate
```

### Generate a unique object ID

```bash
python3 tools/idgen.py
# Outputs a ULID (Universally Unique Lexicographically Sortable Identifier)
```

### Validate a single object

```bash
python3 atlas-codex/validators/validate_object.py path/to/my-object.json
```

### Validate with strict Canon gates

```bash
python3 atlas-codex/validators/validate_strict.py path/to/object.json --expect-state accepted
```

---

## Interoperability

Alexandrian Academy maps to established learning technology standards:

| Standard | Notes | Mapping |
|----------|-------|---------|
| IEEE LOM | Learning Object Metadata — used as the interoperability surface for import/export | [`docs/interoperability/lom-mapping.md`](docs/interoperability/lom-mapping.md) |
| edX/OLX | Open Learning XML — course packaging format used by Open edX | [`docs/interoperability/edx-structure-mapping.md`](docs/interoperability/edx-structure-mapping.md) |
| OCW / Coursera-style MOOCs | Sequencing, video, transcript, and next-best-action patterns | [`docs/interoperability/ocw-coursera-parallels.md`](docs/interoperability/ocw-coursera-parallels.md) |

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for development setup, naming conventions, validation workflow, and the Sandbox -> Canon promotion process.

---

## License

MIT — community-owned contributions with permissive reuse. See [`LICENSE`](LICENSE).

---

## Topics / discoverability keywords

`education` `curriculum` `learning-management` `edtech` `k-12` `higher-education`
`montessori` `json-schema` `provenance` `governance` `accessibility` `wcag`
`ferpa` `coppa` `lom` `competency-based` `mastery-learning` `omnichannel`
`knowledge-graph` `open-education` `next-best-action` `monorepo`
