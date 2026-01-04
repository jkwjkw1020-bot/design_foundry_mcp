"""Tool: tapeout_checklist

Tape-out 전 점검 체크리스트를 Markdown 체크박스 형태로 생성.
"""

from __future__ import annotations

from typing import List

from ..data.checklist_db import CATEGORY_ALIASES, CHECKLIST_ITEMS
from ..server import server


def _gather_items(design_type: str, checklist_category: str) -> List[str]:
    dt = design_type.lower()
    cat = checklist_category.lower()

    data = CHECKLIST_ITEMS.get(dt)
    if not data:
        return []

    if cat == "all":
        categories = CATEGORY_ALIASES["all"]
    else:
        categories = [cat]

    items: List[str] = []
    for c in categories:
        section = data.get(c)
        if not section:
            continue
        items.extend(section)
    return items


@server.tool(
    name="tapeout_checklist",
    description=(
        "Tape-out 전 체크리스트를 Markdown 체크박스 형태로 생성. "
        "design_type: digital/analog/mixed_signal/memory/io. "
        "checklist_category: all/drc_lvs/timing/power/signal_integrity/documentation."
    ),
)
async def tapeout_checklist(
    design_type: str,
    process_node: str,
    checklist_category: str = "all",
) -> str:
    """Tape-out 전 체크리스트를 생성합니다."""
    if not design_type.strip() or not process_node.strip():
        return "입력 오류: design_type과 process_node는 필수입니다."

    items = _gather_items(design_type, checklist_category)
    if not items:
        return (
            f"`{design_type}` 유형이나 `{checklist_category}` 카테고리를 찾을 수 없습니다. "
            "지원 값: design_type=digital/analog/mixed_signal/memory/io, "
            "category=all/drc_lvs/timing/power/signal_integrity/documentation."
        )

    lines = [f"### Tape-out Checklist ({design_type}, {process_node})"]
    for it in items:
        lines.append(f"- [ ] {it}")
    return "\n".join(lines)



