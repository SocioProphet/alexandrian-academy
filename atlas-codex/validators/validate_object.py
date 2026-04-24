#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple, List

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR = ROOT / "platform-contracts" / "schemas"

SCHEMA_BY_TYPE = {
    "CurriculumPlan": "curriculum-plan.schema.json",
    "UnitMap": "unit-map.schema.json",
    "AssessmentPlan": "assessment-plan.schema.json",
    "LearningLoopRecord": "learning-loop-record.schema.json",
}

def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def build_registry() -> Registry:
    registry = Registry()
    for schema_path in SCHEMAS_DIR.glob("*.schema.json"):
        schema = load_json(schema_path)
        registry = registry.with_resource(
            schema_path.name,
            Resource.from_contents(schema)
        )
    return registry

def schema_for_object(obj: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    header = obj.get("header", {})
    obj_type = header.get("object_type")
    if obj_type not in SCHEMA_BY_TYPE:
        raise ValueError(f"Unsupported or missing object_type: {obj_type!r}. Expected one of: {list(SCHEMA_BY_TYPE.keys())}")
    schema_path = SCHEMAS_DIR / SCHEMA_BY_TYPE[obj_type]
    return obj_type, load_json(schema_path)

def canon_gates(obj: Dict[str, Any]) -> List[str]:
    """
    Hard blockers for Canon acceptance.
    These are *additional* to JSON Schema shape validation.
    """
    errs: List[str] = []
    header = obj.get("header", {})
    status = header.get("status")
    ext = obj.get("extension", {})
    promo = ext.get("promotion_intent", {})
    target_space = promo.get("target_space")

    policy_tags = header.get("policy_tags")
    if not isinstance(policy_tags, list):
        errs.append("Gate G0: header.policy_tags must be a list (non-null).")

    if status == "accepted" and target_space == "canon":
        if "evidence" not in obj or obj.get("evidence") is None:
            errs.append("Gate G1: accepted Canon objects must include evidence (EvidenceBundle).")
        else:
            ev = obj.get("evidence", {})
            spans = ev.get("supporting_span_ids", [])
            arts = ev.get("source_artifact_ids", [])
            if not isinstance(spans, list) or len(spans) < 1:
                errs.append("Gate G1: evidence.supporting_span_ids must have >= 1 item for accepted Canon objects.")
            if not isinstance(arts, list) or len(arts) < 1:
                errs.append("Gate G1: evidence.source_artifact_ids must have >= 1 item for accepted Canon objects.")

        if not ext.get("jurisdiction_id"):
            errs.append("Gate G2: extension.jurisdiction_id is required for accepted Canon objects.")
        if not ext.get("pedagogy_id"):
            errs.append("Gate G2: extension.pedagogy_id is required for accepted Canon objects.")

    return errs

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_object.py <path/to/object.json>", file=sys.stderr)
        return 2

    obj_path = Path(sys.argv[1]).resolve()
    if not obj_path.exists():
        print(f"Not found: {obj_path}", file=sys.stderr)
        return 2

    obj = load_json(obj_path)

    registry = build_registry()
    obj_type, schema = schema_for_object(obj)

    validator = Draft202012Validator(schema, registry=registry)
    schema_errors = sorted(validator.iter_errors(obj), key=lambda e: e.path)

    gate_errors = canon_gates(obj)

    if schema_errors:
        print(f"[FAIL] JSON Schema validation failed for {obj_type}: {obj_path}")
        for e in schema_errors:
            loc = "/".join([str(p) for p in e.path]) or "(root)"
            print(f"  - schema error at {loc}: {e.message}")
    else:
        print(f"[OK] JSON Schema validation passed for {obj_type}: {obj_path}")

    if gate_errors:
        print(f"[FAIL] Canon gates failed: {obj_path}")
        for g in gate_errors:
            print(f"  - {g}")
    else:
        print(f"[OK] Canon gates passed: {obj_path}")

    return 0 if (not schema_errors and not gate_errors) else 1

if __name__ == "__main__":
    raise SystemExit(main())
