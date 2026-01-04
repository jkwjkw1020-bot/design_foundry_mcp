"""Design Foundry MCP server entrypoint.

Stateless, HTTP-streaming MCP server built with the FastMCP helper.
Tools are registered in dedicated modules under ``src/tools``.
"""

from __future__ import annotations

import os
from typing import Any, Iterable

from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
import uvicorn


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
    """Create Starlette app that bridges FastMCP over SSE.

    This mirrors fastmcp's internal SSE setup but avoids nested asyncio.run
    calls by letting uvicorn own the event loop.
    """

    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server._mcp_server.run(  # type: ignore[attr-defined]
                streams[0],
                streams[1],
                server._mcp_server.create_initialization_options(),  # type: ignore[attr-defined]
            )

    async def handle_messages(request):
        await sse.handle_post_message(
            request.scope, request.receive, request._send
        )

    return Starlette(
        debug=server.settings.debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Route("/messages", endpoint=handle_messages, methods=["POST"]),
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
        host=server.settings.host,
        port=server.settings.port,
        log_level=server.settings.log_level,
    )


if __name__ == "__main__":
    main()


