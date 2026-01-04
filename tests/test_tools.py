import pytest

from src.server import server
from src.tools import (
    terminology,
    design_rules,
    tapeout,
    process,
    pdk,
    communication,
    methodology,
)


@pytest.mark.asyncio
async def test_explain_foundry_term():
    resp = await terminology.explain_foundry_term("PODE")
    assert "PODE" in resp
    assert "Practical" in resp or "practical" in resp


@pytest.mark.asyncio
async def test_design_rule_qa_supported_node_category():
    resp = await design_rules.design_rule_qa(
        process_node="5nm",
        rule_category="metal",
        question="min spacing?",
    )
    assert "Design Rule" in resp
    assert "min" in resp.lower()


@pytest.mark.asyncio
async def test_design_rule_qa_unsupported_node():
    resp = await design_rules.design_rule_qa(
        process_node="999nm",
        rule_category="metal",
        question="?",
    )
    assert "지원되지 않는 공정 노드" in resp


@pytest.mark.asyncio
async def test_design_rule_qa_invalid_category():
    resp = await design_rules.design_rule_qa(
        process_node="5nm",
        rule_category="unknown",
        question="?",
    )
    assert "카테고리" in resp or "category" in resp.lower()


@pytest.mark.asyncio
async def test_tapeout_checklist_basic():
    resp = await tapeout.tapeout_checklist(
        design_type="digital",
        process_node="5nm",
        checklist_category="drc_lvs",
    )
    assert "- [ ]" in resp
    assert "Tape-out Checklist" in resp


@pytest.mark.asyncio
async def test_tapeout_checklist_invalid_type():
    resp = await tapeout.tapeout_checklist(
        design_type="unknown",
        process_node="5nm",
        checklist_category="drc_lvs",
    )
    assert "찾을 수 없습니다" in resp or "지원" in resp


@pytest.mark.asyncio
async def test_compare_process_nodes_default_aspects():
    resp = await process.compare_process_nodes("7nm", "5nm")
    assert "Process Node Comparison" in resp
    assert "| performance" in resp.lower() or "performance" in resp.lower()


@pytest.mark.asyncio
async def test_pdk_document_guide_known_type():
    resp = await pdk.pdk_document_guide("drc_deck")
    assert "PDK Document Guide" in resp
    assert "Rule" in resp or "rule" in resp


@pytest.mark.asyncio
async def test_pdk_document_guide_invalid_type():
    resp = await pdk.pdk_document_guide("invalid")
    assert "지원하지 않는" in resp


@pytest.mark.asyncio
async def test_communication_template_waiver():
    resp = await communication.foundry_communication_template(
        "drc_waiver_request",
        {"project_name": "Proj", "process": "5nm", "issue_description": "Spacing", "sender": "Team"},
    )
    assert "Waiver" in resp or "waiver" in resp
    assert "Proj" in resp


@pytest.mark.asyncio
async def test_communication_template_invalid_type():
    resp = await communication.foundry_communication_template("unknown", {})
    assert "지원하지 않는" in resp


@pytest.mark.asyncio
async def test_design_methodology_guide():
    resp = await methodology.design_methodology_guide("floorplan", "advanced")
    assert "Design Methodology" in resp
    assert "-" in resp


@pytest.mark.asyncio
async def test_design_methodology_invalid_topic():
    resp = await methodology.design_methodology_guide("unknown", "advanced")
    assert "지원하지 않는" in resp or "topic" in resp.lower()


MAX_BYTES = 24_576


def _basic_markdown_check(resp: str) -> None:
    assert resp.strip(), "응답이 비어 있습니다."
    assert len(resp.encode("utf-8")) < MAX_BYTES, "응답이 24KB를 초과합니다."
    # 매우 단순한 Markdown 여부 확인: 헤더/리스트/테이블/링크 기호 포함 여부
    assert any(tok in resp for tok in ("#", "- ", "* ", "|", "[")), "Markdown 패턴이 감지되지 않습니다."


@pytest.mark.asyncio
async def test_tool_responses_size_and_markdown():
    responses = [
        await terminology.explain_foundry_term("PODE"),
        await design_rules.design_rule_qa("5nm", "metal", "what is min spacing?"),
        await tapeout.tapeout_checklist("digital", "5nm", "drc_lvs"),
        await process.compare_process_nodes("7nm", "5nm"),
        await pdk.pdk_document_guide("drc_deck"),
        await communication.foundry_communication_template(
            "technical_inquiry",
            {"project_name": "Proj", "process": "5nm", "issue_description": "Need rule info", "sender": "Team"},
        ),
        await methodology.design_methodology_guide("floorplan", "advanced"),
    ]

    for resp in responses:
        _basic_markdown_check(resp)


