"""Tool: design_methodology_guide

공정 분류(advanced/mature)와 주제별 설계 방법론 가이드.
"""

from __future__ import annotations

from typing import Dict, List

from ..server import server


GUIDES: Dict[str, Dict[str, List[str]]] = {
    "floorplan": {
        "advanced": [
            "Macro edge keep-out으로 double patterning 충돌 완화",
            "Power grid를 early stage에 확정하고 congestion map으로 검증",
            "Clock spine/mesh 영역 확보",
        ],
        "mature": [
            "IR-drop 취약 영역에 stripe 증설",
            "IO/analog 근접 시 크로스톡/EMI 거리 확보",
        ],
    },
    "power_grid": {
        "advanced": [
            "EM/IR 동시 해석 기준으로 strap pitch/width 설정",
            "Local vs global grid hierarchy 분리",
        ],
        "mature": [
            "Corner 온도/전압 변화에 따른 IR margin 확인",
            "Pad ring 전원 분리와 decap 배치",
        ],
    },
    "clock_tree": {
        "advanced": [
            "Mesh/Hybrid 구조로 OCV 민감도 감소",
            "Useful skew를 CTS 단계에서 제한적으로 적용",
        ],
        "mature": [
            "Buffer set 제한으로 skew/latency 균형",
            "Jitter budget을 PLL/deskew와 함께 정의",
        ],
    },
    "placement": {
        "advanced": [
            "Color-aware placement 옵션 활용",
            "Multi-bit flops로 클럭 부하/면적 절감",
        ],
        "mature": [
            "논리 근접도 기반 클러스터링으로 배선 혼잡 완화",
            "Don't touch 영역 최소화, 리오더 유연성 확보",
        ],
    },
    "routing": {
        "advanced": [
            "Double patterning 친화적 track 기반 라우팅",
            "High-speed nets는 상위 레이어 직선화, via count 최소화",
        ],
        "mature": [
            "Congestion hotspot 회피를 위해 layer assignment 조정",
            "EM 민감 경로는 폭/병렬 라우트로 보강",
        ],
    },
    "timing_closure": {
        "advanced": [
            "AOCV/POCV 기반 여유 분석, STA와 ECO 루프 자동화",
            "Hold fixing은 상위 레이어 via 최소화 전략 병행",
        ],
        "mature": [
            "Critical path에 size/swap, 유휴 경로에는 인덕티브 noise 주의",
            "Late ECO 대비 여유 버짓 문서화",
        ],
    },
    "low_power": {
        "advanced": [
            "Multi-Vt 셀 혼용 + MTCMOS gating으로 leakage 억제",
            "Power gating 영역 경계 IR/ground bounce 해석",
        ],
        "mature": [
            "Clock gating 적용 범위 확대, retention flops 최소화",
            "DVFS 적용 시 corner 라이브러리 일관성 확인",
        ],
    },
    "multi_voltage": {
        "advanced": [
            "Level shifter/detector 자동 배치 규칙 정의",
            "Island 간 클럭/리셋 도메인 CDC 계획",
        ],
        "mature": [
            "LS 위치/방향 고정으로 라우팅 예측성 확보",
            "Power-up/down 시퀀스 검증",
        ],
    },
}


@server.tool(
    name="design_methodology_guide",
    description=(
        "공정 분류(advanced/mature)와 주제별 설계 방법론 가이드 제공. "
        "methodology_topic: floorplan/power_grid/clock_tree/placement/"
        "routing/timing_closure/low_power/multi_voltage."
    ),
)
async def design_methodology_guide(
    methodology_topic: str,
    process_node: str = "advanced",
) -> str:
    """공정별 설계 방법론 가이드를 제공합니다."""
    topic = methodology_topic.lower().strip()
    proc = "advanced" if process_node.lower().startswith("adv") else "mature"

    if not topic:
        return "입력 오류: methodology_topic은 필수입니다."

    info = GUIDES.get(topic)
    if not info:
        return (
            f"지원하지 않는 topic: `{methodology_topic}`. "
            "floorplan/power_grid/clock_tree/placement/routing/"
            "timing_closure/low_power/multi_voltage 중 선택하세요."
        )

    tips = info.get(proc) or []
    if not tips:
        return "가이드를 찾지 못했습니다. 입력을 다시 확인하세요."

    lines = [f"### Design Methodology: {methodology_topic} ({proc})"]
    for t in tips[:8]:
        lines.append(f"- {t}")
    lines.append("\n> 공정/파운드리별 수치는 FAE 가이드를 따르세요.")
    return "\n".join(lines)



