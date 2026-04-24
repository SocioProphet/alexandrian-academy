#!/usr/bin/env python3
from __future__ import annotations

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from publish_learning_explanation_bundle import build_bundle
from publish_learning_search_record import post_search_record
from write_learning_memory import post_memoryd_write

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "platform-contracts" / "examples" / "learning-loop-record.example.json"


class FakeSearchHandler(BaseHTTPRequestHandler):
    received: dict[str, Any] | None = None

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        FakeSearchHandler.received = json.loads(self.rfile.read(length).decode("utf-8"))
        body = json.dumps({"accepted": True, "result_id": FakeSearchHandler.received["header"]["object_id"]}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


class FakeMemoryHandler(BaseHTTPRequestHandler):
    received: dict[str, Any] | None = None

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        FakeMemoryHandler.received = json.loads(self.rfile.read(length).decode("utf-8"))
        body = json.dumps({"event_id": "event.fake.0001", "backend_memory_ids": ["memory.fake.0001"], "stored_locally": True}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def start_server(handler: type[BaseHTTPRequestHandler]) -> tuple[ThreadingHTTPServer, threading.Thread]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


class PublishLearningExplanationBundleE2ETests(unittest.TestCase):
    def test_bundle_publishes_search_and_memory_payloads_to_explicit_endpoints(self) -> None:
        FakeSearchHandler.received = None
        FakeMemoryHandler.received = None
        search_server, search_thread = start_server(FakeSearchHandler)
        memory_server, memory_thread = start_server(FakeMemoryHandler)
        try:
            record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            bundle = build_bundle(record)
            search_result = post_search_record(
                f"http://127.0.0.1:{search_server.server_port}/v1/search/ingest/academy",
                bundle["learning_search_record"],
            )
            memory_result = post_memoryd_write(
                f"http://127.0.0.1:{memory_server.server_port}",
                bundle["learning_memory_record"]["memoryd_write"],
            )
        finally:
            search_server.shutdown()
            memory_server.shutdown()
            search_thread.join(timeout=5)
            memory_thread.join(timeout=5)

        self.assertTrue(search_result["accepted"])
        self.assertEqual(memory_result["event_id"], "event.fake.0001")
        self.assertIsNotNone(FakeSearchHandler.received)
        self.assertIsNotNone(FakeMemoryHandler.received)
        assert FakeSearchHandler.received is not None
        assert FakeMemoryHandler.received is not None
        self.assertEqual(FakeSearchHandler.received["source"], "ALEXANDRIAN_ACADEMY")
        self.assertEqual(FakeMemoryHandler.received["memory_class"], "decision")
        self.assertEqual(FakeMemoryHandler.received["envelope"]["source_interface"], "alexandrian-academy")


if __name__ == "__main__":
    unittest.main()
