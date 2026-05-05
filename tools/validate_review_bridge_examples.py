#!/usr/bin/env python3
"""Validate Alexandrian review-bridge example objects.

This helper is intentionally narrow. It validates only the M1/M2/M3
constitutional review bridge examples introduced with the review-layer schema
tranche. It avoids changing the core object validator until these object types
are accepted into the main validation registry.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "platform-contracts" / "schemas"
EXAMPLES_DIR = ROOT / "platform-contracts" / "examples"

EXAMPLE_TO_SCHEMA = {
    "moderation-event.example.json": "moderation-event.schema.json",
    "metamoderation-event.example.json": "metamoderation-event.schema.json",
    "constitutional-review-event.example.json": "constitutional-review-event.schema.json",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_registry() -> Registry:
    registry = Registry()
    for schema_path in SCHEMAS_DIR.glob("*.schema.json"):
        schema = load_json(schema_path)
        registry = registry.with_resource(schema_path.name, Resource.from_contents(schema))
    return registry


def validate_one(example_name: str, schema_name: str, registry: Registry) -> int:
    example_path = EXAMPLES_DIR / example_name
    schema_path = SCHEMAS_DIR / schema_name

    if not example_path.exists():
        print(f"[FAIL] missing example: {example_path}")
        return 1
    if not schema_path.exists():
        print(f"[FAIL] missing schema: {schema_path}")
        return 1

    example = load_json(example_path)
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(example), key=lambda e: e.path)

    if errors:
        print(f"[FAIL] {example_name} against {schema_name}")
        for err in errors:
            loc = "/".join([str(p) for p in err.path]) or "(root)"
            print(f"  - {loc}: {err.message}")
        return 1

    print(f"[OK] {example_name} validates against {schema_name}")
    return 0


def main() -> int:
    registry = build_registry()
    failures = 0
    for example_name, schema_name in EXAMPLE_TO_SCHEMA.items():
        failures += validate_one(example_name, schema_name, registry)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
