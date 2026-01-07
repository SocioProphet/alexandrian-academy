#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "platform-contracts" / "schemas"
CHANGESET_SCHEMA = SCHEMAS / "changeset.schema.json"
CHANGESET_DIR = ROOT / "moirai-ledger" / "changesets"

PLACEHOLDER_RE = re.compile(r"(REPLACE-|PLACEHOLDER|TBD|TODO)", re.IGNORECASE)

def load_json(p: Path):
  return json.loads(p.read_text(encoding="utf-8"))

def validate_changeset(cs_obj: dict):
  schema = load_json(CHANGESET_SCHEMA)
  v = Draft202012Validator(schema)
  errors = sorted(v.iter_errors(cs_obj), key=lambda e: e.path)
  if errors:
    for e in errors[:25]:
      path = "/".join(str(x) for x in e.path)
      print(f"[FAIL] ChangeSet schema error at '{path}': {e.message}", file=sys.stderr)
    raise SystemExit(2)

def find_changeset_id(obj: dict):
  # Support multiple reasonable placements without forcing a single layout too early.
  for keypath in [
    ("changeset_id",),
    ("meta", "changeset_id"),
    ("header", "changeset_id"),
    ("provenance", "changeset_id"),
    ("governance", "changeset_id"),
  ]:
    cur = obj
    ok = True
    for k in keypath:
      if isinstance(cur, dict) and k in cur:
        cur = cur[k]
      else:
        ok = False
        break
    if ok and isinstance(cur, str) and cur.strip():
      return cur.strip()
  return None

def find_status(obj: dict):
  for keypath in [
    ("status",),
    ("meta", "status"),
    ("header", "status"),
  ]:
    cur = obj
    ok = True
    for k in keypath:
      if isinstance(cur, dict) and k in cur:
        cur = cur[k]
      else:
        ok = False
        break
    if ok and isinstance(cur, str):
      return cur.strip().lower()
  return None

def assert_no_placeholders(obj: dict, path=""):
  if isinstance(obj, dict):
    for k, v in obj.items():
      assert_no_placeholders(v, f"{path}.{k}" if path else k)
  elif isinstance(obj, list):
    for i, v in enumerate(obj):
      assert_no_placeholders(v, f"{path}[{i}]")
  elif isinstance(obj, str):
    if PLACEHOLDER_RE.search(obj):
      raise SystemExit(f"[FAIL] Placeholder token found at '{path}': {obj}")

def locate_changeset_file(changeset_id: str):
  # Simple policy: search examples first; expand later to a registry/index.
  candidates = list(CHANGESET_DIR.rglob("*.json"))
  for c in candidates:
    try:
      o = load_json(c)
      if o.get("changeset_id") == changeset_id:
        return c
    except Exception:
      continue
  return None

def run_base_validator(obj_path: Path):
  # Use the existing validator to preserve current behavior.
  base = ROOT / "atlas-codex" / "validators" / "validate_object.py"
  if not base.exists():
    print(f"[FAIL] Base validator missing: {base}", file=sys.stderr)
    raise SystemExit(2)
  rc = Path(sys.executable)
  # Execute base validator as a subprocess via python -c is messy; do direct import-free exec.
  import runpy
  sys_argv_backup = sys.argv[:]
  try:
    sys.argv = [str(base), str(obj_path)]
    runpy.run_path(str(base), run_name="__main__")
  finally:
    sys.argv = sys_argv_backup

def main():
  if len(sys.argv) != 2:
    print("Usage: validate_object_strict.py <object.json>", file=sys.stderr)
    return 2

  obj_path = Path(sys.argv[1]).resolve()
  if not obj_path.exists():
    print(f"[FAIL] Missing object file: {obj_path}", file=sys.stderr)
    return 2

  # 1) Run existing validator first (schema + current gates)
  run_base_validator(obj_path)

  # 2) Strict Canon enforcement
  obj = load_json(obj_path)
  status = find_status(obj)
  if status != "canon":
    print(f"[OK] Strict Canon gates skipped (status={status}).")
    return 0

  if not CHANGESET_SCHEMA.exists():
    print(f"[FAIL] Missing ChangeSet schema: {CHANGESET_SCHEMA}", file=sys.stderr)
    return 2

  # No placeholders allowed in Canon objects
  assert_no_placeholders(obj)

  cs_id = find_changeset_id(obj)
  if not cs_id:
    print("[FAIL] Canon object missing changeset_id (supported paths: changeset_id, meta/header/provenance/governance.changeset_id).", file=sys.stderr)
    return 2

  cs_file = locate_changeset_file(cs_id)
  if not cs_file:
    print(f"[FAIL] Canon object references ChangeSet '{cs_id}', but no matching ChangeSet JSON found under {CHANGESET_DIR}.", file=sys.stderr)
    return 2

  cs_obj = load_json(cs_file)
  validate_changeset(cs_obj)

  print(f"[OK] Strict Canon gates passed: changeset_id={cs_id} file={cs_file}")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
