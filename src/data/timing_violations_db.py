TIMING_VIOLATIONS_KNOWLEDGE = {
    "setup": {
        "description": "데이터가 clock edge 전에 충분히 안정되지 않은 경우",
        "root_causes": [
            "Data path가 너무 긴 경우 (logic level 과다)",
            "Clock path가 너무 빠른 경우 (clock skew)",
            "High fanout net으로 인한 지연",
            "Slow cell 사용 또는 부적절한 cell sizing",
            "Routing detour로 인한 wire delay 증가",
        ],
        "debug_flow": {
            "step1": "Timing report에서 critical path 확인",
            "step2": "Path의 logic level 수 확인",
            "step3": "각 stage의 cell delay와 wire delay 분석",
            "step4": "Dominant delay 요소 파악 (cell vs wire)",
            "step5": "Clock path skew 영향 확인",
        },
        "solutions": {
            "logic_optimization": [
                "Logic restructuring으로 level 감소",
                "Critical path에 faster cell 사용",
                "Redundant logic 제거",
            ],
            "cell_sizing": [
                "Critical path cell을 HVT→SVT→LVT로 변경",
                "Driving cell의 size 증가",
                "Load cell의 size 조정",
            ],
            "clock_optimization": [
                "Useful skew 활용",
                "Clock buffer 조정",
                "Clock gate 위치 최적화",
            ],
            "physical_optimization": [
                "Critical cell을 가깝게 배치",
                "Routing detour 제거",
                "Buffer insertion",
            ],
        },
        "severity_guide": {
            "critical": "WNS < -500ps: Architecture 수정 또는 clock frequency 조정 검토",
            "medium": "WNS -100~-500ps: Cell sizing, VT swap으로 해결 가능",
            "minor": "WNS > -100ps: 약간의 optimization으로 해결",
        },
    },
    "hold": {
        "description": "데이터가 clock edge 후에 너무 빨리 변하는 경우",
        "root_causes": [
            "Data path가 너무 짧은 경우",
            "Clock path가 너무 느린 경우",
            "동일 clock의 인접 flip-flop 간 경로",
            "Clock skew로 인해 capture clock이 늦게 도착",
        ],
        "debug_flow": {
            "step1": "Hold violation path 확인",
            "step2": "Launch/Capture clock의 arrival time 비교",
            "step3": "Data path delay 분석",
            "step4": "Clock skew 기여도 확인",
            "step5": "인접 cell 간 경로인지 확인",
        },
        "solutions": {
            "delay_insertion": [
                "Data path에 delay buffer 삽입",
                "Hold fixing cell 자동 삽입",
                "Slower cell로 교체",
            ],
            "clock_optimization": [
                "Clock skew 균형 조정",
                "Clock tree 재합성",
                "Hold time이 작은 flip-flop 사용",
            ],
            "physical_adjustment": [
                "Cell 배치 조정으로 wire delay 추가",
                "Routing을 일부러 길게 (비권장)",
            ],
        },
        "severity_guide": {
            "critical": "대량의 hold violation: Clock tree 구조 점검 필요",
            "medium": "특정 영역 집중: 해당 영역 clock skew 확인",
            "minor": "산발적 발생: Buffer insertion으로 해결",
        },
        "caution": "Hold fixing은 setup에 영향을 줄 수 있으므로 iterative하게 진행",
    },
    "max_transition": {
        "description": "신호의 rise/fall 시간이 허용 최대값을 초과",
        "root_causes": [
            "Driving cell의 구동 능력 부족",
            "Output load (capacitance)가 너무 큼",
            "Long wire로 인한 RC delay",
            "High fanout으로 인한 과부하",
        ],
        "debug_flow": {
            "step1": "Violation net과 driving cell 확인",
            "step2": "Output capacitance 분석",
            "step3": "Fanout 수 확인",
            "step4": "Wire length 확인",
            "step5": "Transition value와 limit 비교",
        },
        "solutions": {
            "driver_sizing": [
                "Driving cell size 증가",
                "Stronger drive strength cell로 교체",
                "Buffer insertion으로 구간 분리",
            ],
            "load_reduction": [
                "Fanout 분리 (load balancing)",
                "Wire length 단축 (cell 재배치)",
                "Sink cell size 축소 (입력 capacitance 감소)",
            ],
            "buffer_insertion": [
                "Long wire 중간에 repeater 삽입",
                "High fanout net에 buffer tree 구성",
            ],
        },
        "impact": "Max transition 위반은 signal integrity, noise margin, downstream timing에 영향",
    },
    "max_capacitance": {
        "description": "Net의 총 capacitance가 허용 최대값을 초과",
        "root_causes": [
            "너무 많은 sink에 연결 (high fanout)",
            "Long wire로 인한 wire capacitance",
            "Large sink cell들의 input capacitance 합",
        ],
        "debug_flow": {
            "step1": "Violation net 확인",
            "step2": "Total capacitance breakdown (wire + pin)",
            "step3": "Fanout 수와 각 sink의 input cap 확인",
            "step4": "Wire length 확인",
            "step5": "Max cap limit 대비 초과량 확인",
        },
        "solutions": {
            "fanout_splitting": [
                "Buffer tree로 fanout 분산",
                "Logical하게 독립적인 그룹으로 분리",
                "Critical path와 non-critical path 분리",
            ],
            "cell_sizing": [
                "Sink cell을 smaller input cap cell로 교체",
                "Driving cell을 higher drive로 교체",
            ],
            "physical_optimization": [
                "Cell 재배치로 wire length 감소",
                "Higher metal layer 사용 (lower capacitance)",
            ],
        },
        "impact": "Max cap 위반은 transition 위반으로 이어지고, timing과 power에 영향",
    },
    "max_fanout": {
        "description": "하나의 output이 연결된 input 수가 허용치 초과",
        "root_causes": [
            "Control signal (enable, reset 등)의 과다 연결",
            "Clock gating cell의 fanout",
            "Test signal의 광범위 분배",
        ],
        "debug_flow": {
            "step1": "High fanout net 식별",
            "step2": "연결된 sink cell 목록 확인",
            "step3": "Signal 특성 파악 (clock, reset, data)",
            "step4": "Physical distribution 확인",
        },
        "solutions": {
            "buffer_tree": [
                "계층적 buffer tree 구성",
                "Balanced fanout으로 분배",
                "Physical location 고려한 분배",
            ],
            "architectural": [
                "Local reset/enable 생성",
                "Hierarchical control 구조",
                "필요 시 RTL 수정",
            ],
        },
        "impact": "Fanout 과다는 transition violation, timing degradation, power 증가 유발",
    },
    "clock_skew": {
        "description": "동일 clock domain 내 flip-flop 간 clock 도착 시간 차이",
        "root_causes": [
            "Clock tree balancing 미흡",
            "서로 다른 영역에 위치한 flip-flop",
            "Clock buffer 특성 차이",
            "On-chip variation (OCV)",
        ],
        "debug_flow": {
            "step1": "Clock tree report로 skew 확인",
            "step2": "Max skew 발생 flip-flop pair 확인",
            "step3": "Clock tree 경로 비교",
            "step4": "Physical location 확인",
            "step5": "Buffer stage 수 비교",
        },
        "solutions": {
            "cts_optimization": [
                "Clock tree 재합성",
                "Target skew 조정",
                "Buffer/inverter selection 조정",
            ],
            "useful_skew": [
                "Timing critical path에 intentional skew 적용",
                "Setup/Hold 균형 조정",
            ],
            "physical": [
                "Clock sink 재배치",
                "Clock routing 조정",
            ],
        },
        "impact": "과도한 skew는 setup/hold margin 감소, uncertainty 증가",
    },
    "recovery": {
        "description": "Asynchronous control signal 해제 후 clock까지의 시간 부족",
        "root_causes": [
            "Reset/Set 신호의 deassertion이 clock에 너무 가까움",
            "Async signal path가 너무 느림",
            "Clock skew로 인한 margin 감소",
        ],
        "solutions": {
            "path_optimization": [
                "Reset path 최적화",
                "Reset synchronizer 검토",
                "Buffer insertion",
            ],
            "timing_adjustment": [
                "Reset deassertion timing 조정",
                "Clock phase 조정",
            ],
        },
    },
    "removal": {
        "description": "Clock edge 후 asynchronous control signal이 너무 빨리 변함",
        "root_causes": [
            "Async signal이 clock 직후에 변화",
            "Async signal path가 너무 빠름",
            "Clock의 늦은 도착",
        ],
        "solutions": {
            "delay_insertion": [
                "Async signal path에 delay 추가",
                "Synchronizer 검토",
            ],
            "timing_adjustment": [
                "Signal assertion/deassertion timing 조정",
            ],
        },
    },
}

