#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from explain_learning_action import build_explanation, load_json

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORD_DIR = ROOT / "platform-contracts" / "examples"


def find_record(record_dir: Path, record_id: str) -> dict[str, Any] | None:
    for path in sorted(record_dir.glob("*.json")):
        try:
            data = load_json(path)
        except Exception:
            continue
        header = data.get("header", {})
        if header.get("object_type") == "LearningLoopRecord" and header.get("object_id") == record_id:
            return data
    return None


def explanation_for_record_id(record_dir: Path, record_id: str) -> tuple[int, dict[str, Any]]:
    record = find_record(record_dir, record_id)
    if record is None:
        return 404, {"error": "learning loop record not found", "record_id": record_id}
    return 200, build_explanation(record)


class LearningLoopExplanationHandler(BaseHTTPRequestHandler):
    record_dir = DEFAULT_RECORD_DIR

    def do_GET(self) -> None:  # noqa: N802 - stdlib callback name
        parsed = urlparse(self.path)
        prefix = "/v1/learning-loop/"
        suffix = "/explanation"
        if not parsed.path.startswith(prefix) or not parsed.path.endswith(suffix):
            self._write_json(404, {"error": "not found"})
            return

        record_id = parsed.path[len(prefix):-len(suffix)].strip("/")
        if not record_id:
            self._write_json(400, {"error": "missing learning loop record id"})
            return

        status, payload = explanation_for_record_id(self.record_dir, record_id)
        self._write_json(status, payload)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, indent=2, sort_keys=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    host = "127.0.0.1"
    port = 8788
    record_dir = DEFAULT_RECORD_DIR

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if len(sys.argv) > 2:
        record_dir = Path(sys.argv[2]).resolve()

    LearningLoopExplanationHandler.record_dir = record_dir
    server = ThreadingHTTPServer((host, port), LearningLoopExplanationHandler)
    print(f"serving learning-loop explanations on http://{host}:{port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
