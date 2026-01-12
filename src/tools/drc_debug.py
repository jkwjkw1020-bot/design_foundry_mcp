from __future__ import annotations

from typing import List

from src.data.drc_errors_db import DRC_ERRORS_KNOWLEDGE


def _format_steps(solutions: dict) -> List[str]:
    # Preserve insertion order (step1...stepN)
    lines: List[str] = []
    for key in sorted(solutions.keys()):
        lines.append(f"- {solutions[key]}")
    return lines


def drc_error_guide(
    error_type: str,
    layer: str = "general",
    error_description: str = "",
) -> str:
    """
    DRC(Design Rule Check) 에러 유형별 원인 분석과 해결 방법을 제공합니다.
    """
    et = (error_type or "").strip().lower()
    if not et:
        return "입력 오류: error_type은 필수입니다."

    data = DRC_ERRORS_KNOWLEDGE.get(et)
    if not data:
        available = ", ".join(sorted(DRC_ERRORS_KNOWLEDGE.keys()))
        return f"지원하지 않는 DRC 에러 유형입니다: `{error_type}`. 사용 가능: {available}"

    layer_key = (layer or "general").strip()
    lines: List[str] = [
        f"### DRC Error Guide: {error_type} ({layer_key})",
        f"- What it is: {data.get('description','')}",
    ]
    if error_description:
        lines.append(f"- Context: {error_description}")

    lines.append("\n**Common causes**")
    for cause in data.get("common_causes", []):
        lines.append(f"- {cause}")

    solutions = data.get("solutions", {})
    if solutions:
        lines.append("\n**Resolution steps**")
        lines.extend(_format_steps(solutions))

    tips = data.get("prevention_tips", [])
    if tips:
        lines.append("\n**Prevention tips**")
        for tip in tips:
            lines.append(f"- {tip}")

    layer_notes = data.get("layer_specific", {})
    specific = layer_notes.get(layer_key) or layer_notes.get("general")
    if specific:
        lines.append(f"\n**Layer note ({layer_key})**: {specific}")

    return "\n".join(lines)

