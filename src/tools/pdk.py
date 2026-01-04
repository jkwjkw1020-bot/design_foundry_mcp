"""Tool: pdk_document_guide

PDK 문서 타입별 구조와 활용 팁을 설명합니다.
"""

from __future__ import annotations

from typing import Dict, List

from ..server import server


DOC_GUIDES: Dict[str, Dict[str, List[str]]] = {
    "tech_file": {
        "contents": ["Layer map / purpose", "DRC grid/unit", "Routing directions, width/space tables"],
        "tips": ["Techlef/lef/def 호환성 확인", "Router tech file와 signoff deck 일치성 점검"],
    },
    "drc_deck": {
        "contents": ["Rule sections by layer", "Density/Antenna/DFM checks", "Recommended vs required rules"],
        "tips": ["Signoff deck 버전 관리", "Waiver 프로세스와 스크린샷 첨부 요건 확인"],
    },
    "lvs_deck": {
        "contents": ["Device extraction rules", "Black-box/marker layers", "Parasitic options"],
        "tips": ["Subckt 이름, pcell map 일관성", "Guard ring/ESD 디바이스 인식 확인"],
    },
    "spice_model": {
        "contents": ["Corner models (tt/ss/ff...)", "Voltage/Temp ranges", "Noise/Monte Carlo options"],
        "tips": ["BSIM 버전 및 params 확인", "Simulator 호환성(HSPICE/Spectre) 체크"],
    },
    "cell_library": {
        "contents": ["Liberty timing/power", "LEF abstracts", "AOCV/POCV tables"],
        "tips": ["Lib/LEF 버전 매칭", "CTS용 buffer/inverter set 검증"],
    },
    "io_library": {
        "contents": ["Pad cells, ESD clamps", "IBIS/AMI models", "ESD connection rules"],
        "tips": ["Pad ring 예제 레퍼런스", "Package 핀맵과 전원 분리 계획 일치"],
    },
    "memory_compiler": {
        "contents": ["Generator options", "Timing/power models", "Repair/fuse flow"],
        "tips": ["Corner별 타이밍 라이브러리 유효성", "BIST/BISR 절차 문서화"],
    },
    "design_guide": {
        "contents": ["Floorplan rules", "Clock/power methodology", "DFM recommendations"],
        "tips": ["Latest errata/clarification 섹션 확인", "참고 플로우 스크립트 활용"],
    },
}


@server.tool(
    name="pdk_document_guide",
    description=(
        "PDK 문서 타입별 구조/주요 내용/활용 팁을 Markdown으로 안내. "
        "document_type: tech_file/drc_deck/lvs_deck/spice_model/cell_library/"
        "io_library/memory_compiler/design_guide."
    ),
)
async def pdk_document_guide(
    document_type: str,
    specific_topic: str = "",
) -> str:
    """PDK 문서 구조와 활용 방법을 안내합니다."""
    doc = document_type.lower().strip()
    if not doc:
        return "입력 오류: document_type은 필수입니다."

    info = DOC_GUIDES.get(doc)
    if not info:
        return (
            f"지원하지 않는 document_type: `{document_type}`. "
            "tech_file/drc_deck/lvs_deck/spice_model/cell_library/io_library/"
            "memory_compiler/design_guide 중 선택하세요."
        )

    lines = [f"### PDK Document Guide: {document_type}"]
    if contents := info.get("contents"):
        lines.append("- Typical contents:")
        for c in contents[:8]:
            lines.append(f"  - {c}")
    if tips := info.get("tips"):
        lines.append("- Usage tips:")
        for t in tips[:8]:
            lines.append(f"  - {t}")
    if specific_topic:
        lines.append(f"- Specific topic: {specific_topic}")
    lines.append("\n> NDA 세부치는 포함하지 않으며, 최신 버전은 파운드리 포털에서 확인하세요.")
    return "\n".join(lines)



