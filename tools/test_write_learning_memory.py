#!/usr/bin/env python3
from __future__ import annotations

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from write_learning_memory import memoryd_payload, post_memoryd_write

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "platform-contracts" / "examples" / "learning-memory-record.example.json"


class FakeMemorydHandler(BaseHTTPRequestHandler):
    received: dict[str, Any] | None = None

    def do_POST(self) -> None:  # noqa: N802 - stdlib callback name
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        FakeMemorydHandler.received = json.loads(body)
        response = {"event_id": "event.fake.0001", "backend_memory_ids": ["memory.fake.0001"], "stored_locally": True}
        payload = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        return


class WriteLearningMemoryTests(unittest.TestCase):
    def test_memoryd_payload_extracts_write_payload(self) -> None:
        record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        payload = memoryd_payload(record)
        self.assertEqual(payload["memory_class"], "decision")
        self.assertEqual(payload["envelope"]["source_interface"], "alexandrian-academy")

    def test_post_memoryd_write_to_fake_server(self) -> None:
        FakeMemorydHandler.received = None
        server = ThreadingHTTPServer(("127.0.0.1", 0), FakeMemorydHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            result = post_memoryd_write(f"http://127.0.0.1:{server.server_port}", memoryd_payload(record))
        finally:
            server.shutdown()
            thread.join(timeout=5)
        self.assertEqual(result["event_id"], "event.fake.0001")
        self.assertIsNotNone(FakeMemorydHandler.received)
        assert FakeMemorydHandler.received is not None
        self.assertEqual(FakeMemorydHandler.received["memory_class"], "decision")


if __name__ == "__main__":
    unittest.main()
