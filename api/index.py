from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from typing import Any, Dict

# Add project root to import path for src.*
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from api import mcp_handler  # noqa: E402


class handler(BaseHTTPRequestHandler):
    """Vercel Python Serverless entrypoint for MCP over HTTP."""

    def _write_json(self, status: int, payload: Dict[str, Any]) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self):  # noqa: N802
        """Health/status endpoint."""
        self._write_json(
            200,
            {
                "name": "design-foundry-mcp",
                "version": "1.0.0",
                "status": "running",
            },
        )

    def do_POST(self):  # noqa: N802
        """Handle MCP JSON-RPC requests."""
        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length) if content_length else b"{}"
        try:
            request = json.loads(raw.decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            self._write_json(
                400,
                {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {exc}"},
                },
            )
            return

        response = mcp_handler.dispatch(request if isinstance(request, dict) else {})
        self._write_json(200, response)


# Vercel Python runtime entrypoint expects "handler" symbol at module level

