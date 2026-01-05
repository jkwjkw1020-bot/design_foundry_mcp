"""ASGI entrypoint for Vercel Python runtime using FastMCP SSE transport."""

from __future__ import annotations

import os
import sys

# Ensure project root is on path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Reuse the Starlette app built in src.server (FastMCP SSE transport)
from src.server import app as _app  # noqa: E402

# Vercel detects ASGI by the module-level "app" variable.
app = _app



