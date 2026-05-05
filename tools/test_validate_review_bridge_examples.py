#!/usr/bin/env python3
"""Tests for the review bridge example validator."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_review_bridge_examples.py"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_review_bridge_examples", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load validate_review_bridge_examples module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReviewBridgeExampleValidationTest(unittest.TestCase):
    def test_review_bridge_examples_validate(self) -> None:
        module = load_validator_module()
        self.assertEqual(module.main(), 0)


if __name__ == "__main__":
    unittest.main()
