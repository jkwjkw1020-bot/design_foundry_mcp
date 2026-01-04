# Design Foundry MCP Server

반도체 설계-파운드리 협업을 돕는 Remote MCP 서버입니다. PDK 용어 설명, 디자인 룰 Q&A, 테이프아웃 체크리스트, 공정 노드 비교, PDK 문서 가이드, FAE 커뮤니케이션 템플릿, 설계 방법론 가이드를 제공합니다.

## 특징
- MCP 최소 버전: 2025-03-26, Streamable HTTP, Stateless
- Python + FastMCP(FastAPI 기반)
- 모든 Tool 응답은 Markdown 텍스트, 24KB 미만 유지
- 7개 도구 제공 (explain_foundry_term 등)

## 빠른 시작
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.server
# 기본 포트 8000, HOST/PORT 환경변수로 조정
```

## Docker
```bash
docker build -t design-foundry-mcp .
docker run -p 8000:8000 design-foundry-mcp
```

## 제공 도구 요약
- `explain_foundry_term(term, foundry="general", context="")`
- `design_rule_qa(process_node, rule_category, question, foundry="general")`
- `tapeout_checklist(design_type, process_node, checklist_category="all")`
- `compare_process_nodes(node1, node2, comparison_aspects=["performance","power","area","cost"])`
- `pdk_document_guide(document_type, specific_topic="")`
- `foundry_communication_template(communication_type, context)`
- `design_methodology_guide(methodology_topic, process_node="advanced")`

## 테스트
```bash
pytest
```

## CI
GitHub Actions 워크플로우 `.github/workflows/ci.yml` 포함: Python 3.11, 종속성 캐시 후 pytest 실행.

## 주의사항
- NDA 정보를 포함하지 않으며 공개 일반 정보만 제공합니다.
- 파운드리별 수치/제약은 반드시 FAE 공식 가이드를 확인하세요.


