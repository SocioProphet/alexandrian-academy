#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

from publish_learning_explanation_bundle import build_bundle

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "platform-contracts" / "examples" / "learning-loop-record.example.json"


class PublishLearningExplanationBundleTests(unittest.TestCase):
    def test_build_bundle_contains_explanation_search_and_memory_records(self) -> None:
        record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        bundle = build_bundle(record)
        self.assertEqual(bundle["learning_action_explanation"]["header"]["object_type"], "LearningActionExplanation")
        self.assertEqual(bundle["learning_search_record"]["header"]["object_type"], "LearningSearchRecord")
        self.assertEqual(bundle["learning_memory_record"]["header"]["object_type"], "LearningMemoryRecord")
        self.assertEqual(bundle["learning_memory_record"]["memoryd_write"]["memory_class"], "decision")


if __name__ == "__main__":
    unittest.main()
