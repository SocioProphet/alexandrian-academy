#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from explain_learning_action import build_explanation, load_json
from export_learning_memory_record import build_memory_record
from export_learning_search_record import build_search_record
from publish_learning_search_record import post_search_record
from write_learning_memory import post_memoryd_write


def build_bundle(record: dict[str, Any]) -> dict[str, Any]:
    explanation = build_explanation(record)
    search_record = build_search_record(explanation)
    memory_record = build_memory_record(explanation)
    return {
        "learning_loop_record": record,
        "learning_action_explanation": explanation,
        "learning_search_record": search_record,
        "learning_memory_record": memory_record,
    }


def maybe_write_json(path: str | None, payload: dict[str, Any]) -> None:
    if path:
        Path(path).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate and optionally publish an Alexandrian learning explanation bundle")
    parser.add_argument("record", help="Path to LearningLoopRecord JSON")
    parser.add_argument("--out", help="optional output path for the generated bundle JSON")
    parser.add_argument("--search-endpoint", help="optional explicit Sherlock or Lampstand ingestion endpoint")
    parser.add_argument("--memory-endpoint", help="optional explicit memoryd endpoint")
    parser.add_argument("--api-key", help="optional API key used for both publish endpoints")
    parser.add_argument("--dry-run", action="store_true", help="generate and print the bundle without publishing")
    args = parser.parse_args()

    record = load_json(Path(args.record))
    bundle = build_bundle(record)
    maybe_write_json(args.out, bundle)

    results: dict[str, Any] = {"bundle": bundle, "published": {}}
    if not args.dry_run and args.search_endpoint:
        results["published"]["search"] = post_search_record(args.search_endpoint, bundle["learning_search_record"], args.api_key)
    if not args.dry_run and args.memory_endpoint:
        results["published"]["memory"] = post_memoryd_write(args.memory_endpoint, bundle["learning_memory_record"]["memoryd_write"], args.api_key)

    print(json.dumps(results, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
