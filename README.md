# Collaborative Insight Generation Framework - MCP Server

AI 협업을 통한 통찰력 있는 답변 생성을 위한 MCP 서버입니다.

## 🎯 주요 기능

### Phase 0: 요청 분석 및 분류
- 명확성 5개 항목 체크
- 복잡도 7점 척도 평가
- Type 1/2/3 자동 분류

### Phase 1: 계층 구조 및 전문가 배정
- 15가지 계층 조합 지원
- Domain/Subdomain/Category/Task 분석
- 전문가 자동 배정

### Phase 4: 설계 및 기획
- Lv1/Lv2 품질 레벨 지원
- 자동 섹션 생성
- LLM 기반 상세 내용 작성

### Phase 6: 작업 실행
- 멀티 LLM 지원 (Claude, GPT, Gemini)
- 협업 패턴 (Sequential, Parallel, Validation)

## 📦 설치

```bash
# 1. 디렉토리 이동
cd C:\Users\user\collaborative-insight-mcp

# 2. 가상환경 생성 (선택사항)
python -m venv venv
.\venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
copy .env.template .env
# .env 파일을 열어 API 키를 입력하세요
```

## 🔑 API 키 설정

`.env` 파일에 다음 중 **최소 하나의 API 키**를 설정하세요:

```env
# Claude (Anthropic)
ANTHROPIC_API_KEY=sk-ant-...

# GPT (OpenAI)
OPENAI_API_KEY=sk-...

# Gemini (Google)
GEMINI_API_KEY=AIza...
```

## 🚀 실행

### 방법 1: Python으로 직접 실행

```bash
python server.py
```

### 방법 2: uvx로 실행 (권장)

```bash
uvx fastmcp install server.py
```

### 방법 3: Claude Desktop 연동

`claude_desktop_config.json`에 추가:

```json
{
  "mcpServers": {
    "collaborative-insight": {
      "command": "python",
      "args": [
        "C:\\Users\\user\\collaborative-insight-mcp\\server.py"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "your-key",
        "OPENAI_API_KEY": "your-key",
        "GEMINI_API_KEY": "your-key"
      }
    }
  }
}
```

## 📖 사용 예시

### 1. 요청 분석

```
analyze_request(
    user_request="웹사이트의 사용자 경험을 개선하고 싶어요"
)

→ {
    "session_id": "session_20241020...",
    "request_type": "Type 1",
    "clarity_score": 3,
    "reasoning": "단순명확 요청"
}
```

### 2. 전문가 배정

```
assign_experts(session_id="session_20241020...")

→ {
    "experts": [
        {"name": "Domain Expert", "expertise": "Web Development"},
        {"name": "Task Specialist", "expertise": "UX Improvement"}
    ],
    "processing_mode": "collaborative"
}
```

### 3. 설계서 생성

```
create_design(session_id="session_20241020...")

→ {
    "title": "설계서: 웹사이트의 사용자 경험을 개선...",
    "quality_level": "Lv1 Standard",
    "sections": [...]
}
```

### 4. 작업 실행

```
execute_task(
    session_id="session_20241020...",
    selected_llm="claude"
)

→ {
    "result": "구체적인 UX 개선 계획 및 구현 가이드...",
    "llm_used": "claude"
}
```

## 🛠️ Available Tools

| Tool | Description | Phase |
|------|-------------|-------|
| `analyze_request` | 요청 분석 및 분류 | Phase 0 |
| `assign_experts` | 전문가 배정 | Phase 1 |
| `create_design` | 설계서 생성 | Phase 4 |
| `execute_task` | 작업 실행 | Phase 6 |
| `get_workflow_status` | 상태 조회 | - |

## 🗂️ Resources

- `workflow://templates` - 워크플로우 템플릿

## 📁 프로젝트 구조

```
collaborative-insight-mcp/
├── models.py              # 데이터 모델
├── llm_integration.py     # LLM 통합
├── server.py              # MCP 서버 메인
├── phases/
│   ├── __init__.py
│   ├── phase0.py         # 요청 분석
│   ├── phase1.py         # 전문가 배정
│   ├── phase4.py         # 설계 생성
│   └── phase6.py         # 실행
├── requirements.txt
├── .env.template
└── README.md
```

## 🔄 워크플로우

```
사용자 요청
    ↓
Phase 0: 분석 및 분류
    ↓
Phase 1: 전문가 배정
    ↓
[Phase 2: 정보 수집] (선택)
    ↓
[Phase 3: 명확화] (모호한 경우)
    ↓
Phase 4: 설계 생성
    ↓
[Phase 5: LLM 선정] (자동)
    ↓
Phase 6: 실행
    ↓
[Phase 7: 검증] (선택)
    ↓
최종 결과
```

## 🎯 향후 개발 계획

- [ ] Phase 2 (정보 수집) 구현
- [ ] Phase 3 (대화형 명확화) 구현
- [ ] Phase 5 (LLM 자동 선정) 구현
- [ ] Phase 7 (검증) 구현
- [ ] Zen MCP 통합
- [ ] 웹 UI 대시보드
- [ ] 세션 영속화 (DB)

## 📝 라이센스

MIT License

## 👨‍💻 개발자

Collaborative Insight Framework Team

---

**Made with ❤️ using FastMCP**
