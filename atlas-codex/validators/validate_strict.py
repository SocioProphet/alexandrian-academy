#!/usr/bin/env python3
"""
Strict validation overlay for Canon promotion.

We treat JSON Schema as necessary but not sufficient.
Strict mode enforces:
- no placeholder IDs/timestamps
- plausible ISO8601 timestamps
- evidence presence (anchors/spans)
- jurisdiction + standards coverage presence for Canon
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

ISO8601_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)

PLACEHOLDER_RE = re.compile(r"(REPLACE|PLACEHOLDER|TBD|TODO)", re.IGNORECASE)

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def find_first(obj, keys):
    for k in keys:
        if isinstance(obj, dict) and k in obj:
            return obj[k]
    return None

def fail(msg: str):
    print(f"[FAIL][STRICT] {msg}", file=sys.stderr)
    raise SystemExit(1)

def check_iso8601(ts: str, label: str):
    if not isinstance(ts, str) or not ts:
        fail(f"{label} missing or not a string")
    if PLACEHOLDER_RE.search(ts):
        fail(f"{label} contains placeholder token: {ts}")
    if not ISO8601_RE.match(ts):
        fail(f"{label} not ISO8601 (expected ...Z or ±HH:MM): {ts}")
    # sanity parse
    try:
        if ts.endswith("Z"):
            datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            datetime.fromisoformat(ts)
    except Exception:
        fail(f"{label} failed datetime parse: {ts}")

def check_id(val: str, label: str):
    if not isinstance(val, str) or not val:
        fail(f"{label} missing or not a string")
    if PLACEHOLDER_RE.search(val):
        fail(f"{label} contains placeholder token: {val}")
    # permissive structural check: allow UUID-like, ULID-like, or our prefixed IDs
    if not re.match(r"^[A-Za-z0-9:\-_]{8,}$", val):
        fail(f"{label} appears malformed: {val}")

def count_evidence_anchors(obj) -> int:
    # Try several likely locations (we keep this resilient to schema evolution)
    evidence = find_first(obj, ["evidence_bundle", "evidenceBundle", "provenance", "evidence"])
    if not isinstance(evidence, dict):
        return 0
    anchors = find_first(evidence, ["anchors", "spans", "evidence_anchors", "evidenceSpans"])
    if isinstance(anchors, list):
        return len(anchors)
    return 0

def count_artifacts(obj) -> int:
    evidence = find_first(obj, ["evidence_bundle", "evidenceBundle", "provenance", "evidence"])
    if not isinstance(evidence, dict):
        return 0
    artifacts = find_first(evidence, ["artifacts", "sources", "items"])
    if isinstance(artifacts, list):
        return len(artifacts)
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="Path to JSON object to strict-validate")
    ap.add_argument("--expect-state", choices=["sandbox", "draft", "canon", "accepted"], default=None)
    args = ap.parse_args()

    p = Path(args.path)
    obj = load_json(p)

    header = find_first(obj, ["header", "meta", "metadata"])
    if not isinstance(header, dict):
        fail("Missing header/meta/metadata object")

    # IDs
    object_id = find_first(header, ["object_id", "id", "objectId"])
    check_id(object_id, "header.object_id")

    # Timestamps
    created_at = find_first(header, ["created_at", "createdAt", "timestamp", "time_created"])
    check_iso8601(created_at, "header.created_at")

    # State
    state = find_first(header, ["state", "lifecycle_state", "status"])
    if not isinstance(state, str) or not state:
        fail("header.state missing")
    if PLACEHOLDER_RE.search(state):
        fail(f"header.state contains placeholder token: {state}")

    if args.expect_state:
        # Compatibility aliases (repo vocabulary evolves; we keep strictness while supporting canonical names)
        # - 'sandbox' is an alias for 'draft'
        # - 'canon' is an alias for 'accepted'
        if args.expect_state == "sandbox" and state in ("sandbox", "draft"):
            pass
        elif args.expect_state == "canon" and state in ("canon", "accepted"):
            pass
        elif state != args.expect_state:
            fail(f"header.state mismatch: expected {args.expect_state}, got {state}")

    # Canon-specific constraints
    if state == "canon" or args.expect_state == "canon":
        jurisdiction_id = find_first(header, ["jurisdiction_id", "jurisdictionId"])
        pedagogy_id = find_first(header, ["pedagogy_id", "pedagogyId"])
        check_id(jurisdiction_id, "header.jurisdiction_id")
        check_id(pedagogy_id, "header.pedagogy_id")

        # Standards coverage must exist somewhere
        standards = find_first(obj, ["standards_coverage", "standardsCoverage", "standards"])
        if not isinstance(standards, list) or len(standards) == 0:
            fail("Canon requires non-empty standards coverage list")

        # Evidence expectations for Canon
        a = count_evidence_anchors(obj)
        r = count_artifacts(obj)
        if a < 1:
            fail("Canon requires at least 1 evidence anchor/span")
        if r < 1:
            fail("Canon requires at least 1 evidence artifact/source")

    print(f"[OK][STRICT] Passed strict checks: {p}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
