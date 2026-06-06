#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
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
    "LearningActionExplanation": "learning-action-explanation.schema.json",
    "LearningSearchRecord": "learning-search-record.schema.json",
    "LearningMemoryRecord": "learning-memory-record.schema.json",
    "StewardedLearningArtifact": "stewarded-learning-artifact.schema.json",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_registry() -> Registry:
    registry = Registry()
    for schema_path in SCHEMAS_DIR.glob("*.schema.json"):
        schema = load_json(schema_path)
        schema_id = schema.get("$id", schema_path.name)
        resource = Resource.from_contents(schema)
        registry = registry.with_resource(schema_path.name, resource)
        registry = registry.with_resource(schema_id, resource)
    return registry


def schema_for_object(obj: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    header = obj.get("header", {})
    obj_type = header.get("object_type")
    if obj_type not in SCHEMA_BY_TYPE:
        raise ValueError(f"Unsupported or missing object_type: {obj_type!r}. Expected one of: {list(SCHEMA_BY_TYPE.keys())}")
    schema_path = SCHEMAS_DIR / SCHEMA_BY_TYPE[obj_type]
    return obj_type, load_json(schema_path)


def parse_dt(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        return None


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


def stewarded_learning_artifact_gates(obj: Dict[str, Any]) -> List[str]:
    """IOES semantic gates for StewardedLearningArtifact objects."""
    errs: List[str] = []
    header = obj.get("header", {})
    status = header.get("status")
    stewardship_status = obj.get("stewardship_status")
    primary_keeper = obj.get("primary_keeper_ref")
    successor_refs = obj.get("successor_refs", [])
    succession = obj.get("succession", {})
    succession_posture = succession.get("posture")
    succession_successors = succession.get("successor_refs", [])
    last_reviewed_at = parse_dt(obj.get("last_reviewed_at"))
    review_interval_days = obj.get("review_interval_days")

    if stewardship_status == "active" and not primary_keeper:
        errs.append("IOES S1: active stewardship requires primary_keeper_ref.")

    if status == "accepted" and stewardship_status != "active":
        errs.append("IOES S2: accepted learning artifacts require active stewardship.")

    if status == "accepted" and succession_posture not in {"defined", "emergency_only"}:
        errs.append("IOES S3: accepted learning artifacts require defined or emergency_only succession posture.")

    if status == "accepted" and not successor_refs and not succession_successors:
        errs.append("IOES S4: accepted learning artifacts require at least one successor reference.")

    if stewardship_status == "orphaned" and status in {"reviewed", "accepted"}:
        errs.append("IOES S5: orphaned artifacts must not be reviewed or accepted without repair.")

    if succession_posture == "missing" and status in {"reviewed", "accepted"}:
        errs.append("IOES S6: missing succession blocks reviewed or accepted status.")

    if isinstance(review_interval_days, int) and last_reviewed_at is not None:
        # Use a stable policy date so fixtures remain deterministic.
        policy_now = datetime(2026, 6, 6, tzinfo=timezone.utc)
        age_days = (policy_now - last_reviewed_at).days
        if status == "accepted" and age_days > review_interval_days:
            errs.append("IOES S7: accepted artifacts must not be past review interval.")

    disallowed = obj.get("projection_constraints", {}).get("disallowed_uses", [])
    if status == "accepted" and isinstance(disallowed, list):
        lowered = {str(item).strip().lower() for item in disallowed}
        if "canon promotion" in lowered:
            errs.append("IOES S8: accepted artifacts cannot simultaneously disallow canon promotion.")

    return errs


def semantic_gates(obj_type: str, obj: Dict[str, Any]) -> List[str]:
    errs = canon_gates(obj)
    if obj_type == "StewardedLearningArtifact":
        errs.extend(stewarded_learning_artifact_gates(obj))
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

    gate_errors = semantic_gates(obj_type, obj)

    if schema_errors:
        print(f"[FAIL] JSON Schema validation failed for {obj_type}: {obj_path}")
        for e in schema_errors:
            loc = "/".join([str(p) for p in e.path]) or "(root)"
            print(f"  - schema error at {loc}: {e.message}")
    else:
        print(f"[OK] JSON Schema validation passed for {obj_type}: {obj_path}")

    if gate_errors:
        print(f"[FAIL] Semantic gates failed: {obj_path}")
        for g in gate_errors:
            print(f"  - {g}")
    else:
        print(f"[OK] Semantic gates passed: {obj_path}")

    return 0 if (not schema_errors and not gate_errors) else 1


if __name__ == "__main__":
    raise SystemExit(main())
