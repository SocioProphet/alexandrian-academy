#!/usr/bin/env python3
from __future__ import annotations

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from publish_learning_search_record import post_search_record, search_payload

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "platform-contracts" / "examples" / "learning-search-record.example.json"


class FakeSearchIngestHandler(BaseHTTPRequestHandler):
    received: dict[str, Any] | None = None

    def do_POST(self) -> None:  # noqa: N802 - stdlib callback name
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        FakeSearchIngestHandler.received = json.loads(body)
        response = {"accepted": True, "result_id": FakeSearchIngestHandler.received["header"]["object_id"]}
        payload = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        return


class PublishLearningSearchRecordTests(unittest.TestCase):
    def test_search_payload_requires_learning_search_record(self) -> None:
        record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        payload = search_payload(record)
        self.assertEqual(payload["source"], "ALEXANDRIAN_ACADEMY")
        self.assertEqual(payload["entity_type"], "LEARNING_ACTION_EXPLANATION")

    def test_post_search_record_to_fake_server(self) -> None:
        FakeSearchIngestHandler.received = None
        server = ThreadingHTTPServer(("127.0.0.1", 0), FakeSearchIngestHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            result = post_search_record(f"http://127.0.0.1:{server.server_port}/ingest", search_payload(record))
        finally:
            server.shutdown()
            thread.join(timeout=5)
        self.assertTrue(result["accepted"])
        self.assertIsNotNone(FakeSearchIngestHandler.received)
        assert FakeSearchIngestHandler.received is not None
        self.assertEqual(FakeSearchIngestHandler.received["source"], "ALEXANDRIAN_ACADEMY")


if __name__ == "__main__":
    unittest.main()
