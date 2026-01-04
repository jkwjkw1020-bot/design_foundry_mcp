"""Tool: design_rule_qa

공정 노드/카테고리별 디자인 룰 Q&A. 공개 일반 정보만 제공하며, 응답은
Markdown 텍스트로 24KB 미만을 유지합니다.
"""

from __future__ import annotations

from typing import List

from ..data.design_rules_db import DESIGN_RULES_KNOWLEDGE, NodeRules, RuleCategoryEntry
from ..server import server


def _format_rule(node: str, category: str, entry: RuleCategoryEntry) -> str:
    lines: List[str] = []
    lines.append(f"### Design Rule: {node} / {category}")
    if mw := entry.get("min_width"):
        lines.append(f"- Min width: {mw}")
    if ms := entry.get("min_spacing"):
        lines.append(f"- Min spacing: {ms}")
    if enc := entry.get("enclosure"):
        lines.append(f"- Enclosure: {enc}")
    if notes := entry.get("notes"):
        lines.append("- Notes:")
        for n in notes[:4]:
            lines.append(f"  - {n}")
    if tips := entry.get("practical_considerations"):
        lines.append("- Practical tips:")
        for t in tips[:6]:
            lines.append(f"  - {t}")
    return "\n".join(lines)


@server.tool(
    name="design_rule_qa",
    description=(
        "공정 노드/카테고리별 디자인 룰 질의응답. "
        "process_node 예: '5nm','7nm','28nm','65nm'. "
        "rule_category 예: metal/via/poly/well/antenna/density/esd/general. "
        "응답은 Markdown 텍스트."
    ),
)
async def design_rule_qa(
    process_node: str,
    rule_category: str,
    question: str,
    foundry: str = "general",
) -> str:
    """Design Rule 관련 질문에 답변합니다. 반환은 Markdown 텍스트."""
    node_key = process_node.strip().lower()
    cat_key = rule_category.strip().lower()

    if not node_key or not cat_key or not question.strip():
        return "입력 오류: process_node, rule_category, question은 필수입니다."

    node_data: NodeRules | None = DESIGN_RULES_KNOWLEDGE.get(node_key) or DESIGN_RULES_KNOWLEDGE.get(process_node)
    if not node_data:
        return (
            f"지원되지 않는 공정 노드입니다: `{process_node}`.\n"
            "- 공개 정보 기반 일반 답변만 제공하며, 미등록 노드는 파운드리 FAE 확인을 권장합니다."
        )

    entry: RuleCategoryEntry | None = node_data.get(cat_key)  # type: ignore[index]
    if not entry:
        return (
            f"`{process_node}` 노드에 대한 `{rule_category}` 카테고리 정보가 없습니다.\n"
            "- 카테고리는 metal/via/poly/well/antenna/density/esd/general 중 하나로 입력하세요."
        )

    body = _format_rule(process_node, rule_category, entry)

    body += "\n- Foundry context: " + (foundry or "general")
    body += "\n- Question: " + question.strip()

    body += "\n\n> 불확실하거나 NDA 대상 세부치는 파운드리 FAE에 확인을 권장합니다."
    return body



