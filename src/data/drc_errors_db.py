DRC_ERRORS_KNOWLEDGE = {
    "spacing": {
        "description": "두 도형 사이의 간격이 최소 규칙보다 작은 경우 발생",
        "common_causes": [
            "자동 배치/배선 후 수동 수정 시 간격 미확인",
            "IP 블록 간 인터페이스 영역에서 발생",
            "Metal fill 자동 생성 후 기존 패턴과 충돌",
        ],
        "solutions": {
            "step1": "에러 위치 확인 및 관련 도형 식별",
            "step2": "도형 이동 또는 크기 조정으로 간격 확보",
            "step3": "자동 수정 불가 시 배선 재작업 고려",
            "step4": "반복 발생 영역은 placement 제약 추가",
        },
        "prevention_tips": [
            "배치 후 incremental DRC 수시 확인",
            "Critical net 주변에 routing blockage 설정",
            "Metal fill 전 DRC clean 상태 확보",
        ],
        "layer_specific": {
            "M1": "Lower metal은 spacing이 tight하므로 주의. Standard cell 경계 확인",
            "VIA1": "Via 간 spacing은 enclosure와 함께 확인 필요",
            "POLY": "Poly spacing은 gate length에 영향. Litho 제약 고려",
        },
    },
    "width": {
        "description": "도형의 폭이 최소 규칙보다 작은 경우 발생",
        "common_causes": [
            "수동 편집 시 실수로 폭 축소",
            "Custom cell 설계 시 규칙 미숙지",
            "기존 설계를 다른 공정으로 마이그레이션 시",
        ],
        "solutions": {
            "step1": "에러 도형의 현재 width 확인",
            "step2": "해당 레이어의 minimum width 규칙 확인",
            "step3": "도형 폭을 규칙 이상으로 확장",
            "step4": "확장 시 인접 도형과의 spacing 재확인",
        },
        "prevention_tips": [
            "설계 시작 전 Design Rule Manual 숙지",
            "Grid 설정을 minimum width의 배수로 설정",
            "Template 또는 Pcell 활용",
        ],
        "layer_specific": {
            "M1": "M1 min width는 EM rule과 연관. Current density 고려",
            "POLY": "Poly width = gate length. Transistor 성능에 직결",
            "DIFF": "Diffusion width는 transistor width와 연관",
        },
    },
    "enclosure": {
        "description": "Via/Contact이 상하위 Metal에 충분히 둘러싸이지 않은 경우",
        "common_causes": [
            "Via 위치가 Metal 가장자리에 너무 가까움",
            "Metal 폭이 Via enclosure를 만족하기에 부족",
            "자동 배선 후 Metal 수동 수정 시 Via 위치 미조정",
        ],
        "solutions": {
            "step1": "Via와 상하위 Metal의 overlap 영역 확인",
            "step2": "Metal 확장 또는 Via 위치 이동",
            "step3": "Metal 확장 어려우면 Via 개수 조정 고려",
            "step4": "심한 경우 배선 경로 재설계",
        },
        "prevention_tips": [
            "Via 배치 시 enclosure margin 여유 확보",
            "Narrow metal 구간에서는 via 배치 지양",
            "Auto-via 기능 활용 시 규칙 자동 준수",
        ],
        "layer_specific": {
            "VIA1": "M1-VIA1-M2 enclosure 동시 만족 필요",
            "VIA2": "상위 Via로 갈수록 enclosure 규칙 완화되는 경향",
            "CO": "Contact enclosure은 Poly/Diffusion 양쪽 확인",
        },
    },
    "density": {
        "description": "특정 영역의 Metal/Poly 밀도가 규정 범위를 벗어난 경우",
        "common_causes": [
            "로직 밀도가 낮은 영역에서 under-density",
            "매크로/메모리 주변 영역 불균형",
            "Metal fill 미적용 또는 부적절한 적용",
        ],
        "solutions": {
            "step1": "Density map으로 violation 영역 파악",
            "step2": "Under-density: Metal fill 추가",
            "step3": "Over-density: Fill 제거 또는 설계 재배치",
            "step4": "Critical area는 fill 제외 영역으로 설정",
        },
        "prevention_tips": [
            "Floorplan 단계에서 density 균형 고려",
            "주기적으로 density check 수행",
            "Fill insertion은 timing closure 후 수행",
        ],
        "layer_specific": {
            "M1": "Lower metal density가 CMP 균일성에 가장 큰 영향",
            "POLY": "Poly density는 gate patterning 품질에 영향",
            "general": "각 레이어별 min/max density 범위 확인 필요",
        },
    },
    "antenna": {
        "description": "Gate에 연결된 Metal 면적이 과다하여 공정 중 손상 위험",
        "common_causes": [
            "긴 Metal 배선이 Gate에 직접 연결",
            "Metal 레이어 변경 없이 장거리 배선",
            "Via 개수 대비 Metal 면적 과다",
        ],
        "solutions": {
            "step1": "Antenna ratio 계산으로 violation 정도 파악",
            "step2": "배선 중간에 layer 점프(via) 추가",
            "step3": "Antenna diode 삽입",
            "step4": "심한 경우 배선 경로 재설계",
        },
        "prevention_tips": [
            "Router의 antenna-aware 옵션 활성화",
            "Long wire는 자동으로 layer 변경하도록 설정",
            "Critical gate 근처에 diode 사전 배치",
        ],
        "layer_specific": {
            "M1": "M1에서 발생 시 diode 삽입이 효과적",
            "upper_metal": "상위 metal에서는 layer jump로 해결",
            "POLY": "Poly antenna는 가장 치명적. 우선 해결 필요",
        },
    },
    "overlap": {
        "description": "서로 다른 레이어가 규칙에 맞지 않게 중첩된 경우",
        "common_causes": [
            "Well/Implant 영역 정의 오류",
            "다른 타입의 소자가 너무 가깝게 배치",
            "Custom layout 시 레이어 간 관계 미숙지",
        ],
        "solutions": {
            "step1": "Overlap 영역의 레이어 구성 확인",
            "step2": "불필요한 레이어 제거 또는 영역 조정",
            "step3": "소자 간 간격 확보",
            "step4": "Well/Implant 경계 재정의",
        },
        "prevention_tips": [
            "레이어 간 허용/금지 overlap 규칙 숙지",
            "DRC rule deck 문서의 overlap 섹션 참조",
            "Pcell 사용으로 규칙 자동 준수",
        ],
        "layer_specific": {
            "NWELL_PWELL": "Well overlap은 latchup 위험. 절대 금지",
            "DIFF_POLY": "Transistor 형성 영역. 의도된 overlap만 허용",
            "IMP": "Implant overlap은 threshold voltage에 영향",
        },
    },
    "extension": {
        "description": "도형이 다른 도형을 충분히 넘어서 확장되지 않은 경우",
        "common_causes": [
            "Poly가 Diffusion을 충분히 넘지 않음",
            "Metal이 Via 너머로 충분히 연장되지 않음",
            "End-of-line 규칙 미준수",
        ],
        "solutions": {
            "step1": "Extension 규칙 수치 확인",
            "step2": "해당 도형을 규칙만큼 연장",
            "step3": "연장 시 인접 도형과의 spacing 확인",
            "step4": "연장 불가 시 도형 재배치",
        },
        "prevention_tips": [
            "Transistor 설계 시 poly extension 기본 마진 확보",
            "Via 배치 시 metal extension 자동 확인",
            "End-of-line 규칙은 advanced node에서 특히 중요",
        ],
        "layer_specific": {
            "POLY": "Poly-over-diffusion extension은 device 특성에 영향",
            "METAL": "Metal extension은 via reliability와 연관",
            "general": "Extension 부족은 공정 변이에 취약",
        },
    },
}

