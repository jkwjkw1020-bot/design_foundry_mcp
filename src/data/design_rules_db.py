"""Design rule knowledge base (public, generic info only).

NDA 대상 정보는 포함하지 않으며, 공개적으로 알려진 일반 경향만 담습니다.
"""

from __future__ import annotations

from typing import Dict, List, TypedDict


class RuleCategoryEntry(TypedDict, total=False):
    min_width: str
    min_spacing: str
    enclosure: str
    notes: List[str]
    practical_considerations: List[str]


class NodeRules(TypedDict, total=False):
    metal: RuleCategoryEntry
    via: RuleCategoryEntry
    poly: RuleCategoryEntry
    well: RuleCategoryEntry
    antenna: RuleCategoryEntry
    density: RuleCategoryEntry
    esd: RuleCategoryEntry
    general: RuleCategoryEntry


DESIGN_RULES_KNOWLEDGE: Dict[str, NodeRules] = {
    "5nm": {
        "metal": {
            "min_width": "M1 약 18-20nm 수준, 멀티 패터닝 기반",
            "min_spacing": "동일 레이어 간 20nm대, coloring 제약 영향",
            "practical_considerations": [
                "SADP/SAQP 컬러 충돌을 피하도록 router coloring 설정 확인",
                "EM 한계가 낮아 전력망은 상위 레이어 폭/갯수 늘려 보강",
            ],
        },
        "via": {
            "enclosure": "Self-aligned via로 enclosure 규칙 단순하지만 cut 수량 제한 존재",
            "practical_considerations": [
                "중요 전류 경로는 듀얼·어레이 via 적용",
                "상하층 pitch 불일치로 인한 router constraint 반영",
            ],
        },
        "antenna": {
            "notes": ["고κ/금속 게이트에서 게이트 산화막 얇아 규칙이 엄격"],
            "practical_considerations": [
                "게이트 연결 전 상위 레이어 점프로 partial ratio 감소",
                "표준셀 내부 안테나 다이오드 활용 여부 확인",
            ],
        },
        "density": {
            "notes": ["레이어별 밀도 윈도우가 좁고 fill shape 제약이 많음"],
            "practical_considerations": [
                "아날로그 영역은 fill keep-out 정의",
                "클럭/IO는 커플링 영향 최소화하도록 fill 간격 조정",
            ],
        },
    },
    "28nm": {
        "metal": {
            "min_width": "M1 약 60-80nm 수준 (파운드리별 상이)",
            "min_spacing": "80-100nm대가 일반적",
            "practical_considerations": [
                "EM 기준은 상대적으로 완화되지만 전력망 폭/중첩 확보",
                "메탈 density 윈도우는 존재하므로 fill 검증 필수",
            ],
        },
        "poly": {
            "min_spacing": "Poly pitch ~140-190nm 범위",
            "practical_considerations": [
                "아날로그 매칭 시 dummy poly 삽입으로 CD 균일성 확보",
            ],
        },
        "antenna": {
            "practical_considerations": [
                "긴 글로벌 라우트는 상위 레이어 점프로 면적 비 축소",
                "필요 시 표준셀 안테나 다이오드 활용",
            ],
        },
    },
    "65nm": {
        "general": {
            "notes": [
                "성숙 공정으로 룰이 비교적 관대하나 density, latch-up, ESD는 여전히 관리 필요",
            ],
            "practical_considerations": [
                "IO/ESD 셀 애플리케이션 노트 준수",
                "디카플링/IR-drop 검토는 파운드리 레퍼런스 플로우 참고",
            ],
        }
    },
}



