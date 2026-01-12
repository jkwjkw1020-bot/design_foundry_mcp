from __future__ import annotations

from typing import List

from src.data.acronyms_db import SEMICONDUCTOR_ACRONYMS


def acronym_decoder(
    acronym: str,
    context: str = "general",
) -> str:
    """
    반도체 업계에서 사용되는 약어와 축약어를 해석합니다.
    """
    key = (acronym or "").strip().upper()
    ctx = (context or "general").strip().lower()
    if not key:
        return "입력 오류: acronym은 필수입니다."

    data = SEMICONDUCTOR_ACRONYMS.get(key)
    if not data:
        return f"등록되지 않은 약어입니다: `{acronym}`. 다른 표현을 시도하거나 맥락을 알려주세요."

    cat = data.get("category", "general")
    lines: List[str] = [
        f"### Acronym Decoder: {key}",
        f"- Full name: {data.get('full_name','')}",
        f"- Category: {cat}",
        f"- Description: {data.get('description','')}",
    ]

    if ctx != "general" and ctx != cat:
        lines.append(f"- Note: 요청 맥락 `{ctx}`과 등록된 카테고리 `{cat}`가 다릅니다. 실제 사용 맥락을 다시 확인하세요.")

    related = data.get("related", [])
    if related:
        lines.append("- Related: " + ", ".join(related))

    if data.get("usage_example"):
        lines.append(f"- Usage: {data['usage_example']}")

    return "\n".join(lines)

