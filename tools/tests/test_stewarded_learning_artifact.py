#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "atlas-codex" / "validators" / "validate_object.py"
VALID_FIXTURE = ROOT / "examples" / "stewarded-learning-artifact.valid.json"
REJECTED_FIXTURE = ROOT / "examples" / "stewarded-learning-artifact.rejected.no-keeper.json"


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_stewarded_learning_artifact_valid_fixture_passes() -> None:
    result = run_validator(VALID_FIXTURE)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "[OK] JSON Schema validation passed" in result.stdout
    assert "[OK] Semantic gates passed" in result.stdout


def test_stewarded_learning_artifact_rejected_fixture_fails_semantic_gates() -> None:
    result = run_validator(REJECTED_FIXTURE)
    assert result.returncode != 0
    combined = result.stdout + result.stderr
    assert "[OK] JSON Schema validation passed" in combined
    assert "[FAIL] Semantic gates failed" in combined
    assert "IOES S2" in combined
    assert "IOES S3" in combined
    assert "IOES S4" in combined
    assert "IOES S5" in combined
    assert "IOES S6" in combined


def main() -> int:
    test_stewarded_learning_artifact_valid_fixture_passes()
    test_stewarded_learning_artifact_rejected_fixture_fails_semantic_gates()
    print("[OK] stewarded learning artifact IOES validation tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
