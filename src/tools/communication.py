"""Tool: foundry_communication_template

FAE와의 커뮤니케이션 템플릿을 상황별로 생성.
"""

from __future__ import annotations

from typing import Any, Dict

from ..data.templates_db import TEMPLATES
from ..server import server


def _fill(template: str, context: Dict[str, Any]) -> str:
    # Provide safe defaults to avoid KeyError.
    safe_ctx = {
        "project_name": context.get("project_name", "PROJECT"),
        "process": context.get("process", "PROCESS"),
        "issue_description": context.get("issue_description", "Describe issue"),
        "urgency": context.get("urgency", "medium"),
        "sender": context.get("sender", "Team"),
        "rule_id": context.get("rule_id", "RuleID"),
        "location": context.get("location", "Layout location"),
        "netlist_freeze": context.get("netlist_freeze", "YYYY-MM-DD"),
        "signoff_complete": context.get("signoff_complete", "YYYY-MM-DD"),
        "gds_release": context.get("gds_release", "YYYY-MM-DD"),
        "lots": context.get("lots", "N/A"),
        "test_conditions": context.get("test_conditions", "N/A"),
        "impact": context.get("impact", "Impact description"),
    }
    try:
        return template.format(**safe_ctx)
    except Exception:
        return "컨텍스트 치환 중 오류가 발생했습니다. 필드를 확인하세요."


@server.tool(
    name="foundry_communication_template",
    description=(
        "파운드리 FAE와의 커뮤니케이션 템플릿 생성. "
        "communication_type: technical_inquiry/drc_waiver_request/"
        "tapeout_schedule/yield_issue_report/respin_request."
    ),
)
async def foundry_communication_template(
    communication_type: str,
    context: Dict[str, Any],
) -> str:
    """커뮤니케이션 템플릿을 Markdown 텍스트로 반환."""
    ctype = communication_type.lower().strip()
    if not ctype:
        return "입력 오류: communication_type은 필수입니다."
    template = TEMPLATES.get(ctype)
    if not template:
        return (
            f"지원하지 않는 communication_type: `{communication_type}`. "
            "technical_inquiry/drc_waiver_request/tapeout_schedule/"
            "yield_issue_report/respin_request 중 선택하세요."
        )
    body = _fill(template, context)
    return body



