#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from serve_learning_loop_explanations import DEFAULT_RECORD_DIR, explanation_for_record_id


def test_explanation_for_existing_learning_loop_record() -> None:
    status, payload = explanation_for_record_id(DEFAULT_RECORD_DIR, "llr_00000001")
    assert status == 200
    assert payload["header"]["object_type"] == "LearningActionExplanation"
    assert payload["learning_loop_record_ref"] == "llr_00000001"
    assert payload["evidence"]["search_refs"] == ["sherlock://learning-search/example-0001"]


def test_explanation_for_missing_learning_loop_record(tmp_path: Path) -> None:
    status, payload = explanation_for_record_id(tmp_path, "missing")
    assert status == 404
    assert payload["record_id"] == "missing"
