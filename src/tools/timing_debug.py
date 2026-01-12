from __future__ import annotations

from typing import List

from src.data.timing_violations_db import TIMING_VIOLATIONS_KNOWLEDGE


def _section(title: str, items: List[str]) -> List[str]:
    lines: List[str] = []
    if items:
        lines.append(f"\n**{title}**")
        for it in items:
            lines.append(f"- {it}")
    return lines


def timing_violation_debug(
    violation_type: str,
    severity: str = "medium",
    context: str = "",
) -> str:
    """
    Timing violation 유형별 디버깅 방법과 해결 전략을 제공합니다.
    """
    vt = (violation_type or "").strip().lower()
    sev = (severity or "medium").strip().lower()
    if not vt:
        return "입력 오류: violation_type은 필수입니다."

    data = TIMING_VIOLATIONS_KNOWLEDGE.get(vt)
    if not data:
        available = ", ".join(sorted(TIMING_VIOLATIONS_KNOWLEDGE.keys()))
        return f"지원하지 않는 timing violation 유형입니다: `{violation_type}`. 사용 가능: {available}"

    lines: List[str] = [
        f"### Timing Violation Debug: {violation_type} (severity: {sev})",
        f"- What it is: {data.get('description','')}",
    ]
    if context:
        lines.append(f"- Context: {context}")

    lines += _section("Root causes", data.get("root_causes", []))

    debug_flow = data.get("debug_flow", {})
    if debug_flow:
        lines.append("\n**Debug flow**")
        for key in sorted(debug_flow.keys()):
            lines.append(f"- {debug_flow[key]}")

    solutions = data.get("solutions", {})
    if solutions:
        lines.append("\n**Solutions**")
        for cat, items in solutions.items():
            lines.append(f"- {cat}:")
            for it in items:
                lines.append(f"  - {it}")

    if "severity_guide" in data:
        guide = data["severity_guide"]
        note = guide.get(sev) or guide.get("medium")
        if note:
            lines.append(f"\n**Severity guide ({sev})**: {note}")

    if data.get("caution"):
        lines.append(f"\n> Caution: {data['caution']}")
    if data.get("impact"):
        lines.append(f"\n> Impact: {data['impact']}")

    return "\n".join(lines)

