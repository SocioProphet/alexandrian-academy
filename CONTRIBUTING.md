# Contributing to Alexandrian Academy

Thank you for considering a contribution. This guide covers the development workflow, naming conventions, and how learning objects move from sandbox to canon.

---

## Table of contents

1. [Development setup](#development-setup)
2. [Repository layout](#repository-layout)
3. [Naming and ID conventions](#naming-and-id-conventions)
4. [JSON object authoring](#json-object-authoring)
5. [Validation workflow](#validation-workflow)
6. [Sandbox → Canon promotion](#sandbox--canon-promotion)
7. [Pull request guidelines](#pull-request-guidelines)
8. [Adding a jurisdiction](#adding-a-jurisdiction)

---

## Development setup

```bash
# Clone the repository
git clone https://github.com/SocioProphet/alexandrian-academy.git
cd alexandrian-academy

# Create a virtual environment and install Python dependencies
make deps

# Run all validation to confirm a clean baseline
make validate
```

Python 3.12+ is required. No other runtimes are needed for schema validation and tooling.

---

## Repository layout

```
aegis-vault/          Immutable source artifacts
ariadnes-thread/      Anchors and spans into artifacts
mnemosyne-forge/      Accessible derivatives (transcripts, captions)
atlas-codex/          Learning objects + validators
  validators/         Python validators (validate_object.py, validate_strict.py)
moirai-ledger/        Governance ChangeSets
  changesets/         ChangeSet records and examples
oracle-of-delphi/     Evaluations and detector findings
platform-contracts/   Shared JSON schemas and enums
  schemas/            JSON Schema Draft 2020-12 files
  examples/           Worked example objects (validated in CI)
  enums/              Shared enumeration files
policy/               Jurisdiction profiles and policy parameters
  jurisdictions/      One directory per jurisdiction (e.g. US-PA/)
  parameters/         Policy parameter sheets
templates/            Starter templates for new objects
tools/                CLI utilities
docs/                 Architecture, interoperability, standards docs
```

---

## Naming and ID conventions

### Object IDs

Object IDs use a prefix that indicates the bounded context, followed by an uppercase type token and a ULID or descriptive slug:

| Prefix | Context |
|--------|---------|
| `AE-` | Aegis Vault artifact |
| `AR-` | Ariadne's Thread anchor/span |
| `MN-` | Mnemosyne Forge derivative |
| `AT-` | Atlas Codex learning object |
| `MO-` | Moirai Ledger ChangeSet |
| `DE-` | Oracle of Delphi evaluation |
| `CONTRIB-` | Contributor identifier |

Generate a ULID for new objects:

```bash
python3 tools/idgen.py
```

Examples: `AT-CURRPLAN-01J8KQ...`, `MO-CHANGESET-01J8KR...`

### Standards references

Standards use the canonical grammar:

```
STD::<COUNTRY>::<JURISDICTION>::<STANDARD_SET>::<VERSION>::<PATH>
```

Example: `STD::US::PA::PA-ELA::v1::K:Reading:FoundationalSkills:RF.1.1`

See [`docs/standards/standards-id-grammar.md`](docs/standards/standards-id-grammar.md).

### File names

- JSON objects: `<object-id>.json` or descriptive `<type>.<state>.json`
- Schema files: `<type>.schema.json`
- Template files: `<type>.template.json`
- Policy files: `<name>.v<N>.json`

---

## JSON object authoring

All objects include a `header` conforming to `universal-header.schema.json`. Required fields:

```json
{
  "header": {
    "object_id": "AT-CURRPLAN-<ULID>",
    "object_type": "CurriculumPlan",
    "object_version": "0.1",
    "created_at": "2026-01-01T00:00:00Z",
    "created_by_contributor_id": "CONTRIB-<you>",
    "created_by_role": "author",
    "status": "draft",
    "policy_tags": ["restricted_private"]
  }
}
```

Valid roles: `author`, `editor`, `reviewer`, `curator`, `transcriber`, `captioner`, `segmenter`, `system`

Valid status values (in order): `draft` → `proposed` → `reviewed` → `accepted` → `deprecated` / `retracted`

Valid policy tags include: `public_commons`, `restricted_private`, `restricted_pii`, `restricted_third_party`

Starter templates are in [`templates/curriculum-builder/v1/`](templates/curriculum-builder/v1/).

---

## Validation workflow

### Validate a single object

```bash
python3 atlas-codex/validators/validate_object.py path/to/object.json
```

This validates the object against its schema (derived from `header.object_type`).

### Strict Canon-gate validation

```bash
python3 atlas-codex/validators/validate_strict.py path/to/object.json --expect-state accepted
```

Strict validation applies additional gates (evidence bundle required, jurisdiction + pedagogy IDs present, policy tags present) that must pass before Canon promotion.

### Full suite (used in CI)

```bash
make validate
```

This runs diagram verification, example validation, and template validation.

### CI

Every push and pull request runs the full validation suite via GitHub Actions (`.github/workflows/ci.yml`).

---

## Sandbox → Canon promotion

Learning objects live in one of two spaces:

| Space | Meaning |
|-------|---------|
| `sandbox` | Draft or work-in-progress; not authoritative |
| `canon` | Peer-reviewed, policy-compliant, authoritative |

### Promotion process

1. **Author** creates or updates a learning object with `status: "draft"` and `target_space: "sandbox"`.
2. **Reviewer** runs `validate_object.py` to confirm schema compliance.
3. **Curator** runs `validate_strict.py --expect-state accepted` to confirm all Canon gates pass.
4. **Author or curator** creates a Moirai ChangeSet record (see [`moirai-ledger/changesets/changeset.template.json`](moirai-ledger/changesets/changeset.template.json)) documenting the promotion:
   - Operation: `PROMOTE_SANDBOX_TO_CANON`
   - Before/after content hashes
   - Supporting span IDs and source artifact IDs
5. **PR** — submit the changed object + ChangeSet as a single PR.

Canon objects must have:
- A valid `EvidenceBundle` with at least one span and artifact reference.
- `jurisdiction_id` and `pedagogy_id` set.
- `policy_tags` as a non-empty list.
- `status: "accepted"`.

---

## Pull request guidelines

- Keep PRs focused: one learning object or one feature per PR when practical.
- Include a ChangeSet record for any Canon promotion.
- Run `make validate` before opening a PR; CI will also run it.
- Use descriptive commit messages: `feat(atlas-codex): add US-PA Kindergarten ELA curriculum plan`.
- Reference relevant standards IDs or jurisdiction profiles in the PR description when applicable.

---

## Adding a jurisdiction

1. Create a directory: `policy/jurisdictions/<COUNTRY>-<REGION>/`
2. Add a `jurisdiction.profile.v<N>.json` following the existing [`US-PA`](policy/jurisdictions/US-PA/jurisdiction.profile.v1.json) pattern.
3. Add a `standards.registry.v<N>.json` listing the standards sets for that jurisdiction.
4. Reference the new jurisdiction in any CurriculumPlan objects via `extension.jurisdiction_id`.
5. Update the jurisdiction index in [`policy/`](policy/) if one exists.

Use the standards ID grammar (`STD::<COUNTRY>::<REGION>::...`) for all standards references.
