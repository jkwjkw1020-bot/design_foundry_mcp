"""MCP request handling for Vercel serverless runtime.

This module exposes a small JSON-RPC-ish surface compatible with the MCP
protocol (initialize, tools/list, tools/call) and bridges to the existing
tool functions under ``src.tools``.
"""

from __future__ import annotations

import asyncio
import inspect
from typing import Any, Callable, Dict, List

from src.tools.terminology import explain_foundry_term
from src.tools.design_rules import design_rule_qa
from src.tools.tapeout import tapeout_checklist
from src.tools.process import compare_process_nodes
from src.tools.pdk import pdk_document_guide
from src.tools.communication import foundry_communication_template
from src.tools.methodology import design_methodology_guide

# Tool registry
TOOLS: Dict[str, Callable[..., Any]] = {
    "explain_foundry_term": explain_foundry_term,
    "design_rule_qa": design_rule_qa,
    "tapeout_checklist": tapeout_checklist,
    "compare_process_nodes": compare_process_nodes,
    "pdk_document_guide": pdk_document_guide,
    "foundry_communication_template": foundry_communication_template,
    "design_methodology_guide": design_methodology_guide,
}

# Tool definitions for tools/list
TOOL_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "name": "explain_foundry_term",
        "description": "반도체 파운드리 관련 전문 용어를 설명합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "term": {"type": "string", "description": "설명이 필요한 용어"},
                "foundry": {
                    "type": "string",
                    "description": "파운드리 이름 (예: TSMC/Samsung/general)",
                    "default": "general",
                },
                "context": {
                    "type": "string",
                    "description": "추가 맥락",
                    "default": "",
                },
            },
            "required": ["term"],
        },
    },
    {
        "name": "design_rule_qa",
        "description": "공정 노드/카테고리별 디자인 룰 Q&A.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "process_node": {"type": "string"},
                "rule_category": {"type": "string"},
                "question": {"type": "string"},
                "foundry": {"type": "string", "default": "general"},
            },
            "required": ["process_node", "rule_category", "question"],
        },
    },
    {
        "name": "tapeout_checklist",
        "description": "Tape-out 전 점검 체크리스트를 생성합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "design_type": {"type": "string"},
                "process_node": {"type": "string"},
                "checklist_category": {"type": "string", "default": "all"},
            },
            "required": ["design_type", "process_node"],
        },
    },
    {
        "name": "compare_process_nodes",
        "description": "두 공정 노드를 주요 관점에서 비교합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "node1": {"type": "string"},
                "node2": {"type": "string"},
                "comparison_aspects": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["performance", "power", "area", "cost"],
                },
            },
            "required": ["node1", "node2"],
        },
    },
    {
        "name": "pdk_document_guide",
        "description": "PDK 문서 타입별 구조와 활용 팁을 안내합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "document_type": {"type": "string"},
                "specific_topic": {"type": "string", "default": ""},
            },
            "required": ["document_type"],
        },
    },
    {
        "name": "foundry_communication_template",
        "description": "FAE 커뮤니케이션 템플릿을 생성합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "communication_type": {"type": "string"},
                "context": {"type": "object"},
            },
            "required": ["communication_type", "context"],
        },
    },
    {
        "name": "design_methodology_guide",
        "description": "공정 분류와 주제별 설계 방법론 가이드를 제공합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "methodology_topic": {"type": "string"},
                "process_node": {"type": "string", "default": "advanced"},
            },
            "required": ["methodology_topic"],
        },
    },
]


def handle_initialize(request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "result": {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "design-foundry-mcp", "version": "1.0.0"},
            "capabilities": {"tools": {}},
        },
    }


def handle_tools_list(request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "result": {"tools": TOOL_DEFINITIONS},
    }


def _error_response(request_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


async def _call_tool_async(name: str, arguments: Dict[str, Any]) -> Any:
    tool = TOOLS.get(name)
    if not tool:
        raise ValueError(f"Unknown tool: {name}")

    # Run sync or async functions accordingly.
    if inspect.iscoroutinefunction(tool):
        return await tool(**arguments)
    result = tool(**arguments)
    if inspect.iscoroutine(result):
        return await result
    return result


async def handle_tools_call_async(request: Dict[str, Any]) -> Dict[str, Any]:
    params = request.get("params", {})
    tool_name = params.get("name")
    arguments = params.get("arguments", {}) or {}

    if not tool_name:
        return _error_response(request.get("id"), -32602, "Missing tool name")

    try:
        result = await _call_tool_async(tool_name, arguments)
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {"content": [{"type": "text", "text": result}]},
        }
    except Exception as exc:  # noqa: BLE001
        return _error_response(request.get("id"), -32603, str(exc))


async def dispatch_async(request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method", "")
    if method == "initialize":
        return handle_initialize(request)
    if method == "tools/list":
        return handle_tools_list(request)
    if method == "tools/call":
        return await handle_tools_call_async(request)
    return _error_response(request.get("id"), -32601, "Method not found")


def dispatch(request: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous wrapper for environments without an event loop."""
    return asyncio.run(dispatch_async(request))



