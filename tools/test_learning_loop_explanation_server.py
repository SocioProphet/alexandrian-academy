#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from serve_learning_loop_explanations import DEFAULT_RECORD_DIR, explanation_for_record_id


class LearningLoopExplanationServerTests(unittest.TestCase):
    def test_explanation_for_existing_learning_loop_record(self) -> None:
        status, payload = explanation_for_record_id(DEFAULT_RECORD_DIR, "llr_00000001")
        self.assertEqual(status, 200)
        self.assertEqual(payload["header"]["object_type"], "LearningActionExplanation")
        self.assertEqual(payload["learning_loop_record_ref"], "llr_00000001")
        self.assertEqual(payload["evidence"]["search_refs"], ["sherlock://learning-search/example-0001"])

    def test_explanation_for_missing_learning_loop_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status, payload = explanation_for_record_id(Path(tmp), "missing")
        self.assertEqual(status, 404)
        self.assertEqual(payload["record_id"], "missing")


if __name__ == "__main__":
    unittest.main()
