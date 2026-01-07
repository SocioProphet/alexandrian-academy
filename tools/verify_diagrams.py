#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "diagrams" / "rendered" / "manifest.v1.json"

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    if not MANIFEST.exists():
        print(f"[FAIL] Missing manifest: {MANIFEST}", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rendered_dir = MANIFEST.parent

    required = manifest.get("required_diagrams", [])
    if not required:
        print("[FAIL] Manifest has no required_diagrams.", file=sys.stderr)
        return 2

    failures = 0
    for item in required:
        fname = item.get("filename")
        if not fname:
            print("[FAIL] Manifest entry missing filename.", file=sys.stderr)
            failures += 1
            continue

        # (Workaround for strictness; keep path simple)
        fp = rendered_dir / fname

        if not fp.exists():
            print(f"[FAIL] Missing rendered diagram: {fp}")
            failures += 1
            continue

        digest = sha256_file(fp)
        expected = item.get("sha256", "")
        if expected == "REPLACE_AFTER_RENDER":
            print(f"[WARN] sha256 not set for {fname}. Current sha256={digest}")
        else:
            if digest != expected:
                print(f"[FAIL] sha256 mismatch for {fname}: expected={expected} actual={digest}")
                failures += 1
            else:
                print(f"[OK] {fname} sha256 matches.")

    if failures:
        print(f"[FAIL] Diagram verification failures: {failures}", file=sys.stderr)
        return 1

    print("[OK] Diagram verification passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
