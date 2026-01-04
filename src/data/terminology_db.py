"""Lightweight terminology knowledge base for foundry/PDK terms.

본 데이터는 공개적으로 알려진 일반 개념만 포함하며, NDA 정보는 포함하지 않습니다.
필요시 이후 단계에서 안전하게 확장할 수 있도록 딕셔너리 구조를 유지합니다.
"""

from __future__ import annotations

from typing import Dict, List, TypedDict


class ProcessRelevance(TypedDict, total=False):
    advanced: str  # 7nm 이하 등 첨단 공정
    mature: str  # 28nm 이상 등 성숙 공정


class TermEntry(TypedDict, total=False):
    full_name: str
    description: str
    related_terms: List[str]
    practical_tips: str
    process_relevance: ProcessRelevance


FOUNDRY_TERMINOLOGY: Dict[str, TermEntry] = {
    "PODE": {
        "full_name": "Poly on Diffusion Edge",
        "description": (
            "확산 영역 가장자리에 폴리실리콘이 겹치는 트랜지스터 구조. "
            "폴리-확산 정렬 정밀도가 중요하며 포토 공정 편차에 민감하다."
        ),
        "related_terms": ["CPODE", "Poly Cut", "Continuous Poly"],
        "practical_tips": (
            "고성능 공정에서 드라이브 강도 확보에 유리하지만, "
            "게이트-소스/드레인 오버랩과 CD 편차를 DRC로 엄격히 확인해야 한다."
        ),
        "process_relevance": {
            "advanced": "FinFET/CFET 등에서 필수 고려, DRC/OPC 제약이 큼",
            "mature": "플래너 공정에서는 적용 빈도가 낮음",
        },
    },
    "CPODE": {
        "full_name": "Continuous Poly on Diffusion Edge",
        "description": (
            "연속된 폴리 라인이 확산 영역을 가로지르는 구조. "
            "멀티 핑거 트랜지스터에서 균일한 CD 확보에 사용된다."
        ),
        "related_terms": ["PODE", "Poly Cut"],
        "practical_tips": "Dummy poly와 함께 사용해 CD 균일성 및 스트레스 밸런스를 확보한다.",
        "process_relevance": {
            "advanced": "멀티 패터닝으로 인한 color 제약을 함께 검토",
            "mature": "CMP/스트레스 영향이 상대적으로 작음",
        },
    },
    "Metal Fill": {
        "full_name": "Metal Dummy Fill",
        "description": (
            "CMP 평탄도와 메탈 밀도 균일성을 위해 삽입하는 더미 메탈 패턴. "
            "IR/EM에는 직접 기여하지 않지만 커플링/근접 효과를 줄 수 있다."
        ),
        "related_terms": ["Density Rule", "CMP", "Dummy Pattern"],
        "practical_tips": (
            "민감한 아날로그 경로에서는 keep-out 설정, "
            "클럭/고속 IO 라우트에는 메탈 필 간격과 레이어 선택을 조정한다."
        ),
        "process_relevance": {
            "advanced": "밀도 윈도우가 좁고 레이어별 fill shape 제약이 많음",
            "mature": "밀도 조건이 비교적 완화되나 필수 체크 대상",
        },
    },
    "Antenna Rule": {
        "full_name": "Plasma Induced Gate Damage Rule",
        "description": (
            "플라즈마 식각 시 긴 금속 라인이 게이트 산화막에 전하를 축적해 "
            "손상시키는 것을 방지하기 위한 규칙."
        ),
        "related_terms": ["Antenna Diode", "Metal Jump", "Partial Ratio"],
        "practical_tips": (
            "게이트 연결 전 메탈을 상위 레이어로 점프하거나, "
            "Antenna 다이오드를 삽입해 총 면적 비를 규격 이하로 낮춘다."
        ),
        "process_relevance": {
            "advanced": "고κ/금속 게이트에서 산화막이 얇아 규칙이 더 엄격",
            "mature": "규칙이 비교적 완화되지만 장거리 라우팅은 주의",
        },
    },
    "Dummy Gate": {
        "full_name": "Dummy Poly/Gate",
        "description": (
            "활성 트랜지스터 양 끝에 배치해 패터닝/스트레스 균일성을 높이는 더미 게이트."
        ),
        "related_terms": ["OD Dummy", "Dummy Active", "OPC"],
        "practical_tips": "아날로그 매칭을 위해 좌우 대칭으로 배치하고, DRC에서 더미 인식 여부 확인.",
    },
}



