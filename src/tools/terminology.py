"""Tool: explain_foundry_term

반도체 파운드리/PDK 용어 설명 도구. Markdown 텍스트를 반환하며
Tool 응답 크기를 작게 유지하도록 핵심 정보 위주로 구성한다.
"""

from __future__ import annotations

from typing import List

from ..data.terminology_db import FOUNDRY_TERMINOLOGY, TermEntry
from ..server import server


def _format_term_entry(term: str, entry: TermEntry, foundry: str) -> str:
    """Format a term entry as Markdown within size budget."""
    lines: List[str] = []
    title = entry.get("full_name") or term
    lines.append(f"### {title} ({term})")
    lines.append(f"- Foundry context: {foundry or 'general'}")
    if desc := entry.get("description"):
        lines.append(f"- What it means: {desc}")
    if tips := entry.get("practical_tips"):
        lines.append(f"- Practical tips: {tips}")
    if rel := entry.get("process_relevance"):
        adv = rel.get("advanced")
        mat = rel.get("mature")
        if adv or mat:
            lines.append("- Process relevance:")
            if adv:
                lines.append(f"  - Advanced: {adv}")
            if mat:
                lines.append(f"  - Mature: {mat}")
    if related := entry.get("related_terms"):
        lines.append(f"- Related terms: {', '.join(related)}")
    return "\n".join(lines)


@server.tool(
    name="explain_foundry_term",
    description=(
        "파운드리/PDK 전문 용어를 설명하고 실무 팁을 제공하는 도구. "
        "term은 필수, foundry는 'TSMC', 'Samsung', 'GlobalFoundries', "
        "또는 'general'을 권장. 응답은 Markdown 텍스트로 제공."
    ),
)
async def explain_foundry_term(
    term: str,
    foundry: str = "general",
    context: str = "",
) -> str:
    """반도체 파운드리 관련 전문 용어를 설명합니다.

    반환값은 Markdown 텍스트이며 24KB 미만으로 유지됩니다.
    """
    term_key = term.strip()
    if not term_key:
        return "입력 오류: term을 비워둘 수 없습니다."

    entry = FOUNDRY_TERMINOLOGY.get(term_key) or FOUNDRY_TERMINOLOGY.get(term_key.upper())
    if not entry:
        return (
            f"아직 등록되지 않은 용어입니다: `{term}`.\n"
            "- 공개 정보 범위에서 일반적인 설명이 필요하면 term을 다시 입력하세요.\n"
            "- 특정 파운드리 규칙은 NDA 대상일 수 있으므로 FAE 확인을 권장합니다."
        )

    body = _format_term_entry(term_key, entry, foundry)

    if context:
        body += "\n- Given context: " + context.strip()

    return body



