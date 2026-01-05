"""Design Foundry MCP server entrypoint.

Stateless, HTTP-streaming MCP server built with the FastMCP helper.
Tools are registered in dedicated modules under ``src/tools``.
"""

from __future__ import annotations

import os
from typing import Any, Iterable

from fastmcp import FastMCP, settings as mcp_settings
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response
import uvicorn
import warnings

# Suppress noisy deprecation warnings from vendored websockets in uvicorn
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"_vendor\.websockets\.legacy.*",
)
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"_vendor\.uvicorn\.protocols\.websockets\.websockets_impl",
)
# Also suppress upstream module paths (non-vendored) that Vercel might use
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"websockets\.legacy.*",
)
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"uvicorn\.protocols\.websockets\.websockets_impl",
)

def create_server(extra_tools: Iterable[Any] | None = None) -> FastMCP:
    """Create and configure the MCP server instance.

    Parameters
    ----------
    extra_tools:
        Optional iterable of callables decorated with ``@server.tool`` that
        should be registered in addition to the built-in tool set. Useful for
        testing or extensions.
    """

    server = FastMCP(name="design-foundry-mcp")

    # Core tool registration is deferred to keep this module minimal.
    # Individual tool modules will import the shared server instance and
    # attach their tools.
    if extra_tools:
        for tool in extra_tools:
            server.add_tool(tool)

    return server


# Create the default server instance and expose FastAPI app for hosting.
server = create_server()

# Register tools by importing modules (side-effect registration via decorator).
# Keep imports near here to avoid import cycles.
from .tools import terminology  # noqa: F401
from .tools import design_rules  # noqa: F401
from .tools import tapeout  # noqa: F401
from .tools import process  # noqa: F401
from .tools import pdk  # noqa: F401
from .tools import communication  # noqa: F401
from .tools import methodology  # noqa: F401


def _build_sse_app() -> Starlette:
    """Create Starlette app that bridges FastMCP over SSE and JSON RPC.

    Provides:
    - GET /          : status JSON
    - POST /         : JSON-RPC (initialize/tools.list/tools.call) via mcp_handler
    - GET /health    : health check
    - GET /sse       : MCP SSE stream
    - POST /messages : MCP SSE message endpoint
    """

    sse = SseServerTransport("/messages")

    async def handle_sse(request: Request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server._mcp_server.run(  # type: ignore[attr-defined]
                streams[0],
                streams[1],
                server._mcp_server.create_initialization_options(),  # type: ignore[attr-defined]
            )

    async def handle_messages(request: Request):
        await sse.handle_post_message(
            request.scope, request.receive, request._send
        )

    async def root_handler(request: Request):
        if request.method == "GET":
            return JSONResponse({"name": "design-foundry-mcp", "version": "1.0.0", "status": "running"})
        # POST -> JSON-RPC fallback (non-SSE HTTP)
        try:
            payload = await request.json()
        except Exception as exc:  # noqa: BLE001
            return JSONResponse(
                {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {exc}"}},
                status_code=400,
            )
        # Lazy import to avoid circular dependency on startup
        from api import mcp_handler

        response = await mcp_handler.dispatch_async(payload if isinstance(payload, dict) else {})
        return JSONResponse(response)

    async def health_handler(request: Request):
        return JSONResponse({"status": "ok"})

    return Starlette(
        debug=mcp_settings.debug,
        routes=[
            Route("/", endpoint=root_handler, methods=["GET", "POST"]),
            Route("/health", endpoint=health_handler, methods=["GET"]),
            Route("/sse", endpoint=handle_sse, methods=["GET"]),
            Route("/messages", endpoint=handle_messages, methods=["POST"]),
            Route("/favicon.ico", endpoint=lambda request: Response(status_code=204)),
            Route("/favicon.png", endpoint=lambda request: Response(status_code=204)),
        ],
    )


# ASGI app for uvicorn entrypoint (uvicorn src.server:app ...)
app = _build_sse_app()


def main() -> None:
    """Run the server (SSE over HTTP by default, stdio optional)."""
    transport = os.getenv("MCP_TRANSPORT", "sse")
    if transport not in ("sse", "stdio"):
        transport = "sse"
    if transport == "stdio":
        server.run(transport="stdio")
        return

    uvicorn.run(
        app,
        host=mcp_settings.host,
        port=mcp_settings.port,
        log_level=mcp_settings.log_level,
    )


if __name__ == "__main__":
    main()


