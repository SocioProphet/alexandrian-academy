#!/usr/bin/env python3
"""Validator for Moirai Ledger ChangeSet records.

Validates a ChangeSet JSON file against
`platform-contracts/schemas/changeset.schema.json` and applies the
external-carrier promotion gate for ChangeSets that carry an
`external_provenance` block.

`external_provenance` is how a Moirai Ledger ChangeSet records that its
candidate originated outside Alexandrian Academy's own authoring flow via a
neuro-symbolic method (CHRONOS carrier alignment -- see
sociosphere/docs/integration/neurosymbolic-chronos-alignment.md). It is
OPTIONAL: purely-internal ChangeSets omit it entirely and are validated
exactly as before -- this module is additive, it does not touch the existing
required fields or their meaning.

When `external_provenance` IS present, the external-carrier gate below
enforces (in addition to JSON Schema shape validation):
  - the source must carry a source evidence reference (reuses the existing
    `evidence_refs` field rather than duplicating it under a new name);
  - the source must explicitly disclaim canonization authority
    (`owning_authority_non_claim: true` -- also enforced at the schema level
    via `const: true`, so an authority-claiming candidate fails even before
    this gate runs);
  - for an actual `PROMOTE_SANDBOX_TO_CANON` operation, the candidate must
    have reached `grounded`/`verified` grounding status and `validated`
    validation status before Alexandrian Academy's gate admits it.

This is invoked both directly (as a CLI, one ChangeSet file per run) and from
`validate_object_strict.py`'s Canon-promotion gate, which locates the
ChangeSet referenced by an accepted Canon object's `changeset_id` and runs
this same validation against it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "platform-contracts" / "schemas" / "changeset.schema.json"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_changeset_schema() -> Dict[str, Any]:
    return load_json(SCHEMA_PATH)


def schema_errors(cs_obj: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> List[str]:
    schema = schema or load_changeset_schema()
    validator = Draft202012Validator(schema)
    errs = sorted(validator.iter_errors(cs_obj), key=lambda e: list(e.path))
    return [f"{'/'.join(str(p) for p in e.path) or '(root)'}: {e.message}" for e in errs]


def external_carrier_gate_errors(cs_obj: Dict[str, Any]) -> List[str]:
    """Promotion gate for externally-sourced neuro-symbolic candidates.

    No-op when `external_provenance` is absent -- purely-internal ChangeSets
    are unaffected by this gate.
    """
    ext = cs_obj.get("external_provenance")
    if ext is None:
        return []
    if not isinstance(ext, dict):
        return ["External-carrier gate: external_provenance must be an object."]

    errs: List[str] = []

    if ext.get("owning_authority_non_claim") is not True:
        errs.append(
            "External-carrier gate: external_provenance.owning_authority_non_claim "
            "must be true -- an external neuro-symbolic source must never claim "
            "canonization authority over Alexandrian Academy's own promotion gate."
        )

    evidence_refs = cs_obj.get("evidence_refs") or []
    if not isinstance(evidence_refs, list) or len(evidence_refs) < 1:
        errs.append(
            "External-carrier gate: evidence_refs must be non-empty when "
            "external_provenance is present (CHRONOS carrier boundary requires "
            "a source evidence reference)."
        )

    if cs_obj.get("operation") == "PROMOTE_SANDBOX_TO_CANON":
        grounding = ext.get("grounding_status")
        if grounding not in {"grounded", "verified"}:
            errs.append(
                f"External-carrier gate: grounding_status={grounding!r} is "
                "insufficient for Canon promotion (requires 'grounded' or 'verified')."
            )
        validation = ext.get("validation_status")
        if validation != "validated":
            errs.append(
                f"External-carrier gate: validation_status={validation!r} is "
                "insufficient for Canon promotion (requires 'validated')."
            )

    return errs


def validate_changeset_object(cs_obj: Dict[str, Any]) -> List[str]:
    """Full validation of an in-memory ChangeSet object.

    Returns a combined list of errors (schema errors first). Semantic
    external-carrier gate errors are only evaluated when schema validation
    did not already fail, to avoid confusing double-reporting of the same
    problem (e.g. a schema-level const:true violation on
    owning_authority_non_claim).
    """
    s_errors = schema_errors(cs_obj)
    if s_errors:
        return s_errors
    return external_carrier_gate_errors(cs_obj)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_changeset.py <changeset.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        print(f"Not found: {path}", file=sys.stderr)
        return 2

    cs_obj = load_json(path)

    s_errors = schema_errors(cs_obj)
    if s_errors:
        print(f"[FAIL] ChangeSet JSON Schema validation failed: {path}")
        for e in s_errors:
            print(f"  - schema error at {e}")
    else:
        print(f"[OK] ChangeSet JSON Schema validation passed: {path}")

    has_external_provenance = isinstance(cs_obj.get("external_provenance"), dict)
    g_errors = external_carrier_gate_errors(cs_obj) if not s_errors else []

    if g_errors:
        print(f"[FAIL] External-carrier promotion gate failed: {path}")
        for e in g_errors:
            print(f"  - {e}")
    elif not s_errors and has_external_provenance:
        print(f"[OK] External-carrier promotion gate passed: {path}")

    return 0 if (not s_errors and not g_errors) else 1


if __name__ == "__main__":
    raise SystemExit(main())
