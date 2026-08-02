#!/usr/bin/env python3
"""Tests for the Moirai Ledger ChangeSet `external_provenance` extension.

Covers the CHRONOS carrier-alignment additive extension to
`platform-contracts/schemas/changeset.schema.json` and the external-carrier
promotion gate in `atlas-codex/validators/validate_changeset.py`:

  - a pre-existing, purely-internal ChangeSet still validates unchanged
    (no regression from adding the optional `external_provenance` field);
  - a neuro-symbolic-sourced ChangeSet with proper provenance (grounded,
    validated, non-authority-declared) is admitted;
  - a neuro-symbolic-sourced ChangeSet missing sufficient grounding/
    validation is rejected by the external-carrier gate;
  - a neuro-symbolic-sourced ChangeSet that improperly claims canonization
    authority is rejected (at the schema level, since
    `owning_authority_non_claim` is a hard `const: true`).

Follows this repo's existing subprocess-based validator test convention
(see tools/tests/test_stewarded_learning_artifact.py).
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "atlas-codex" / "validators" / "validate_changeset.py"
CHANGESET_EXAMPLES = ROOT / "moirai-ledger" / "changesets" / "examples"

PRE_EXISTING_INTERNAL_CHANGESET = CHANGESET_EXAMPLES / "changeset-0001.promote-curriculum-plan.json"
VALID_NEUROSYMBOLIC_CHANGESET = CHANGESET_EXAMPLES / "changeset-0002.neurosymbolic-candidate.valid.json"
REJECTED_MISSING_PROVENANCE_CHANGESET = (
    CHANGESET_EXAMPLES / "changeset-0003.neurosymbolic-candidate.rejected.missing-provenance.json"
)
REJECTED_CLAIMS_AUTHORITY_CHANGESET = (
    CHANGESET_EXAMPLES / "changeset-0004.neurosymbolic-candidate.rejected.claims-authority.json"
)


def run_validator(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class ChangesetProvenanceExtensionTest(unittest.TestCase):
    def test_pre_existing_internal_changeset_still_passes_unchanged(self) -> None:
        """A ChangeSet with no `external_provenance` is completely unaffected."""
        result = run_validator(PRE_EXISTING_INTERNAL_CHANGESET)
        combined = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, combined)
        self.assertIn("[OK] ChangeSet JSON Schema validation passed", combined)
        # The external-carrier gate must not even mention itself for an
        # internal ChangeSet -- it is a silent no-op, not a vacuous pass.
        self.assertNotIn("External-carrier promotion gate", combined)

    def test_neurosymbolic_candidate_with_proper_provenance_is_admitted(self) -> None:
        result = run_validator(VALID_NEUROSYMBOLIC_CHANGESET)
        combined = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, combined)
        self.assertIn("[OK] ChangeSet JSON Schema validation passed", combined)
        self.assertIn("[OK] External-carrier promotion gate passed", combined)

    def test_neurosymbolic_candidate_missing_grounding_is_rejected(self) -> None:
        result = run_validator(REJECTED_MISSING_PROVENANCE_CHANGESET)
        combined = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[OK] ChangeSet JSON Schema validation passed", combined)
        self.assertIn("[FAIL] External-carrier promotion gate failed", combined)
        self.assertIn("grounding_status='ungrounded'", combined)
        self.assertIn("validation_status='pending'", combined)

    def test_neurosymbolic_candidate_claiming_authority_is_rejected(self) -> None:
        result = run_validator(REJECTED_CLAIMS_AUTHORITY_CHANGESET)
        combined = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[FAIL] ChangeSet JSON Schema validation failed", combined)
        self.assertIn("owning_authority_non_claim", combined)


def main() -> int:
    suite = unittest.TestLoader().loadTestsFromTestCase(ChangesetProvenanceExtensionTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
