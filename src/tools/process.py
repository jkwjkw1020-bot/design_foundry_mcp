"""Tool: compare_process_nodes

두 공정 노드를 주요 관점별로 비교하는 경량 도구. 공개 정보 기반 일반화.
"""

from __future__ import annotations

from typing import Dict, List

from ..server import server


ALLOWED_ASPECTS = {
    "performance": "Switching speed / fmax 예상 경향",
    "power": "동적/정적 전력 경향",
    "area": "셀/배선 밀도 경향",
    "cost": "웨이퍼 비용 및 NRE 상대 경향",
    "maturity": "IP/PDK 성숙도",
    "availability": "MPW/production 리드타임",
}


def _aspect_note(aspect: str, node: str) -> str:
    aspect = aspect.lower()
    if aspect == "performance":
        return f"{node}: 공정이 미세할수록 fmax 잠재력↑, RC/변동성 관리 필요"
    if aspect == "power":
        return f"{node}: 전력은 축소 경향이나 leakage는 노드/온도에 민감"
    if aspect == "area":
        return f"{node}: 셀/배선 pitch 축소로 면적↓, 레이아웃 제약/격자 제약↑"
    if aspect == "cost":
        return f"{node}: 더 미세한 노드는 웨이퍼/마스크 비용↑, mask count 증가"
    if aspect == "maturity":
        return f"{node}: 성숙도는 PDK/라이브러리/실투입 양산 사례에 좌우"
    if aspect == "availability":
        return f"{node}: MPW 가용성과 양산 슬롯 리드타임을 파운드리별 확인"
    return f"{node}: 일반적 비교 정보 부족"


def _build_table(node1: str, node2: str, aspects: List[str]) -> str:
    lines = ["### Process Node Comparison", "", "| Aspect | " + node1 + " | " + node2 + " |", "| --- | --- | --- |"]
    for a in aspects:
        lines.append(f"| {a} | {_aspect_note(a, node1)} | {_aspect_note(a, node2)} |")
    return "\n".join(lines)


@server.tool(
    name="compare_process_nodes",
    description=(
        "두 공정 노드를 성능/전력/면적/비용/성숙도/가용성 관점에서 비교. "
        "응답은 Markdown 테이블과 간단한 메모."
    ),
)
async def compare_process_nodes(
    node1: str,
    node2: str,
    comparison_aspects: List[str] | None = None,
) -> str:
    """두 공정 노드의 특징을 비교합니다."""
    if not node1.strip() or not node2.strip():
        return "입력 오류: node1, node2는 필수입니다."

    aspects = comparison_aspects or ["performance", "power", "area", "cost"]
    cleaned = [a.lower() for a in aspects if a.lower() in ALLOWED_ASPECTS]
    if not cleaned:
        cleaned = ["performance", "power", "area", "cost"]

    table = _build_table(node1, node2, cleaned)
    bullet = "\n".join(f"- {a}: {ALLOWED_ASPECTS[a]}" for a in cleaned)
    note = "\n> NDA 정보는 포함하지 않으며, 파운드리별 수치는 FAE 확인 권장."
    return "\n".join([table, "", "요약 메모:", bullet, note])



