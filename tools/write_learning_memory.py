#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from explain_learning_action import load_json


def memoryd_payload(record: dict[str, Any]) -> dict[str, Any]:
    payload = record.get("memoryd_write")
    if not isinstance(payload, dict):
        raise ValueError("LearningMemoryRecord missing memoryd_write object")
    return payload


def post_memoryd_write(endpoint: str, payload: dict[str, Any], api_key: str | None = None, timeout: float = 10.0) -> dict[str, Any]:
    url = endpoint.rstrip("/") + "/v1/write"
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
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
        raise RuntimeError(f"memoryd write failed: HTTP {exc.code}: {detail}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a LearningMemoryRecord payload to memoryd /v1/write")
    parser.add_argument("record", help="Path to LearningMemoryRecord JSON")
    parser.add_argument("--endpoint", help="memoryd endpoint, for example http://127.0.0.1:8080")
    parser.add_argument("--api-key", help="optional memoryd API key")
    parser.add_argument("--dry-run", action="store_true", help="print the memoryd payload without sending")
    args = parser.parse_args()

    record = load_json(Path(args.record))
    payload = memoryd_payload(record)

    if args.dry_run or not args.endpoint:
        print(json.dumps(payload, indent=2, sort_keys=False))
        return 0

    result = post_memoryd_write(args.endpoint, payload, args.api_key)
    print(json.dumps(result, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
