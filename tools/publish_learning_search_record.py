#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from explain_learning_action import load_json


def search_payload(record: dict[str, Any]) -> dict[str, Any]:
    header = record.get("header", {})
    if header.get("object_type") != "LearningSearchRecord":
        raise ValueError("expected LearningSearchRecord")
    return record


def post_search_record(endpoint: str, payload: dict[str, Any], api_key: str | None = None, timeout: float = 10.0) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key
    request = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read().decode("utf-8")
            if not data:
                return {"status": response.status}
            parsed = json.loads(data)
            if isinstance(parsed, dict):
                return parsed
            return {"response": parsed}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8")
        raise RuntimeError(f"search publish failed: HTTP {exc.code}: {detail}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish a LearningSearchRecord to an explicit Sherlock or Lampstand ingestion endpoint")
    parser.add_argument("record", help="Path to LearningSearchRecord JSON")
    parser.add_argument("--endpoint", help="full ingestion endpoint URL")
    parser.add_argument("--api-key", help="optional API key")
    parser.add_argument("--dry-run", action="store_true", help="print the search payload without sending")
    args = parser.parse_args()

    record = load_json(Path(args.record))
    payload = search_payload(record)

    if args.dry_run or not args.endpoint:
        print(json.dumps(payload, indent=2, sort_keys=False))
        return 0

    result = post_search_record(args.endpoint, payload, args.api_key)
    print(json.dumps(result, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
