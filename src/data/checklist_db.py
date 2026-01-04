"""Tape-out checklist data (public, generic).

NDA 정보 없이 공용 베스트프랙티스 수준의 항목만 포함합니다.
"""

from __future__ import annotations

from typing import Dict, List

# Checklist items are Markdown-ready text (without checkboxes).
CHECKLIST_ITEMS: Dict[str, Dict[str, List[str]]] = {
    "digital": {
        "drc_lvs": [
            "DRC clean (signoff deck 기준) 확인",
            "LVS clean 및 black-box 셀 매핑 확인",
            "Antenna/EM/DFM 추가 체크 완료",
        ],
        "timing": [
            "Setup/Hold 여유 확보 (all corners, OCV/AOCV/POCV)",
            "Clock tree skew/uncertainty 업데이트 반영",
            "Async crossing CDC 보고서 클린",
        ],
        "power": [
            "IR-drop/EM signoff 완료 (static/dynamic)",
            "Power grid 덮음률/strap 폭 검토",
            "Power intent (UPF/CPF) 일치성 확인",
        ],
        "signal_integrity": [
            "Crosstalk/Noise 분석 완료",
            "High-speed IO/SerDes 채널 손실 예산 검토",
        ],
        "documentation": [
            "GDS/DEF, netlist, timing libs, SDC 패키징",
            "ECO log, waiver 리스트, 릴리스 노트 포함",
        ],
    },
    "analog": {
        "drc_lvs": [
            "Matching/대칭 구조 DRC 예외 검토",
            "LVS with device parameters (W/L/multiplier) clean",
        ],
        "power": [
            "IR-drop/ground bounce 민감 노드 검토",
            "ESD 파스/클램프 연결 경로 확인",
        ],
        "signal_integrity": [
            "Noise coupling (substrate/metal) 분석",
            "시뮬레이션 모델과 레이아웃 관성 차이 확인",
        ],
        "documentation": [
            "Bias 조건, 코너 정의, 시뮬레이션 스윕 범위 문서화",
            "Measured/expected spec 테이블 제공",
        ],
    },
    "mixed_signal": {
        "drc_lvs": [
            "Digitally-assisted analog 영역 DRC waiver 목록 정리",
            "LVS black-box/abstract 경계 확인",
        ],
        "timing": [
            "Mixed-signal boundary handshake 타이밍 확인",
            "Clock/Reset domain interface CDC clean",
        ],
        "power": [
            "아날로그/디지털 분리 전원, guard ring/guard trace 확인",
            "Power-up/down 시퀀스 문서화",
        ],
        "signal_integrity": [
            "크로스톡/EMI 민감 경로 쉴딩 검토",
            "ADC/DAC 레퍼런스 노드 격리 확인",
        ],
        "documentation": [
            "Top-level integration 가이드와 테스트 모드 정의",
        ],
    },
    "memory": {
        "drc_lvs": [
            "Embedded memory compiler 릴리스 버전/patch 확인",
            "LVS black-box/시그니처 일치",
        ],
        "power": [
            "IR-drop/di/dt 이벤트에 대한 droop 완화",
            "Retention/standby 전류 측정 계획",
        ],
        "signal_integrity": [
            "Read/Write disturb 조건 검토",
            "배선 skew와 sense amp 타이밍 여유 확인",
        ],
        "documentation": [
            "Fuse/repair 플로우, BIST 절차 문서화",
        ],
    },
    "io": {
        "drc_lvs": [
            "ESD 셀 연결/클램프 배선 검증",
            "Pad ring DRC/LVS clean",
        ],
        "power": [
            "IO supply decap 배치, return path 검토",
            "Hot-plug/ESD 이벤트 시 전류 경로 확인",
        ],
        "signal_integrity": [
            "SI/PI 해석 (package + board 추정) 완료",
            "ESD 보호에 따른 RC 영향 확인",
        ],
        "documentation": [
            "Package 핀맵/ballmap, IBIS/AMI 모델 제공",
            "전기적 spec (Vih/Vil/Io) 표기",
        ],
    },
}

# Category aliases for convenience
CATEGORY_ALIASES = {
    "all": ["drc_lvs", "timing", "power", "signal_integrity", "documentation"],
}



