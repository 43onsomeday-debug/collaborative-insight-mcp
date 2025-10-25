# 🤝 Collaborative Insight MCP

> 여러 AI가 협업하여 더 나은 답변을 만드는 똑똑한 시스템

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

---

## 📊 워크플로우 구조도 (최종 업데이트)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ 전역 타임아웃: 30분 (Phase 0-7 전체)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

사용자 요청
    ↓
┌───────────────────────────────────────┐
│ Phase 0: 요청 분석 (단독 LLM)          │ ←─────┐
│ - 명확성/복잡도 체크                   │        │ 재분류
│ - Type 1/2/3 분류                     │        │
└───────────────────────────────────────┘        │
    ↓                                            │
┌───────────────────────────────────────┐        │
│ Phase 1: 전문가 배정 (단독 LLM)        │        │
│ - 계층 구조 파악                       │        │
│ - 전문가 역할 정의                     │        │
└───────────────────────────────────────┘        │
    ↓                                            │
┌───────────────────────────────────────┐        │
│ Phase 1.5: 환경 체크 (단독 LLM) ✨NEW  │        │
│ - Zen MCP 연결 확인                    │        │
│   * 연결 실패 → 단독 LLM 모드          │        │
│ - LLM API 개수 확인 (0~4개)            │        │
│ - Phase 2, 4 실행 모드 결정:           │        │
│   * API 0개 → 단독 LLM 모드            │        │
│   * API 1~4개 → 다중 LLM 모드          │        │
│ - 예상 비용 표시:                      │        │
│   * Type 1: $0.5-2                    │        │
│   * Type 2: $2-10                     │        │
│   * Type 3: $5-20                     │        │
│                                       │        │
│ [최적화]                               │        │
│ - 캐시/TTL: 5분간 결과 재사용 ✨       │        │
│ - 전역 Context: 모든 Phase 공유 ✨     │        │
│ - 3단계 메시지: 간결한 상태 표시 ✨    │        │
└───────────────────────────────────────┘        │
    ↓                                            │
┌───────────────────────────────────────┐        │
│ Phase 2: 정보 수집 ✨UPDATED           │        │
│ ┌─────────────────────────────────┐   │        │
│ │【단독 모드】                     │   │        │
│ │ LLM1: 전문가A,B,C → ToT → 보관  │   │        │
│ │                                 │   │        │
│ │【다중 모드 (API 개수만큼)】      │   │        │
│ │ LLM1: 전문가A,B,C → ToT → 보관  │   │        │
│ │ LLM2: 전문가A,B,C → ToT → 보관  │   │        │
│ │ LLM3: 전문가A,B,C → ToT → 보관  │   │        │
│ │ LLM4: 전문가A,B,C → ToT → 보관  │   │        │
│ └─────────────────────────────────┘   │        │
│ * 연속 세션: Phase 4로 직접 전달 ✨     │        │
│ * 별도 저장소 불필요                   │        │
└───────────────────────────────────────┘        │
    ↓                                            │
    │ (Type 3만)                                 │
    ↓                                            │
┌───────────────────────────────────────┐        │
│ Phase 3: 명확화 (단독 LLM) ✨UPDATED    │        │
│ ┌─────────────────────────────────┐   │        │
│ │ * Phase 2 자료 기반              │   │        │
│ │ * 순환 프로세스 (최대 8-10회):   │   │        │
│ │                                 │   │        │
│ │ ┌─→ 질문 생성 (1개씩) ✨         │   │        │
│ │ │   └ 선택지 2-3개 제공 ✨       │   │        │
│ │ │                               │   │        │
│ │ │   [답변 대기]                 │   │        │
│ │ │   * 다른 프로세스 진행 불가   │   │        │
│ │ │                               │   │        │
│ │ └─  답변 수집                   │   │        │
│ │     ↓                           │   │        │
│ │   명확화 기준 충족?             │   │        │
│ │     No → 순환 반복 (10회 제한)  │   │        │
│ │     Yes ↓                       │   │        │
│ │   사용자 확인 → 요청 확정       │   │        │
│ └─────────────────────────────────┘   │        │
└───────────────────────────────────────┘        │
    ↓                                            │
    └──────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│ Phase 4: 설계서 작성 ✨UPDATED          │ ←─────┐
│ ┌─────────────────────────────────┐   │        │
│ │ * Phase 2 연속 세션 활용 ✨      │   │        │ 설계 수정
│ │                                 │   │        │
│ │【단독 모드】                     │   │        │
│ │ - 섹션별 작성                   │   │        │
│ │                                 │   │        │
│ │【다중 모드】✨NEW                 │   │        │
│ │ * 섹션별 반복 협의:             │   │        │
│ │                                 │   │        │
│ │ [섹션1]                         │   │        │
│ │ Step 1: LLM1 제안 공유          │   │        │
│ │ Step 2: LLM2 의견 + 제안        │   │        │
│ │ Step 3: LLM3 의견 + 제안        │   │        │
│ │ Step 4: LLM4 의견 + 제안        │   │        │
│ │ Step 5: 협의 → 섹션1 작성       │   │        │
│ │                                 │   │        │
│ │ [섹션2~N] 반복                  │   │        │
│ │                                 │   │        │
│ │ → 최종 작업지시서 생성          │   │        │
│ └─────────────────────────────────┘   │        │
└───────────────────────────────────────┘        │
    ↓                                            │
┌───────────────────────────────────────┐        │
│ Phase 5: 실행자 선정 (단독 LLM)        │        │
│ - LLM 또는 외부 MCP/Agent 선정         │        │
└───────────────────────────────────────┘        │
    ↓                                            │
┌───────────────────────────────────────┐        │
│ Phase 6: 실행 (선정된 실행자)          │ ←─────┤
│ - Phase 4 지시서 기반 결과물 생성      │        │ 재작업
└───────────────────────────────────────┘        │
    ↓                                            │
┌───────────────────────────────────────┐        │
│ Phase 7: 품질 체크 (단독 LLM)          │        │
│ - 설계서 vs 결과물 검증                │        │
└───────────────────────────────────────┘        │
    ↓                                            │
    ├─ 설계 문제 ─────────────────────────────┘
    ├─ 실행 문제 ─────────────────────────────┘
    └─ 통과 → 최종 결과물 전달

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[플로우 요약]
Type 1: 0→1→1.5→2→4→6 (6단계)
Type 2: 0→1→1.5→2→4→5→6→7 (8단계)
Type 3: 0→1→1.5→2→3→0(재분류)→... (9+단계)

[LLM 사용]
단독: 0, 1, 1.5, 3, 5, 7
유동: 2, 4 (API 개수 따라 단독/다중)
```

---

## ✨ v1.1 주요 업데이트

### 🆕 Phase 1.5: 환경 체크 (NEW)
- **Zen MCP 연결 자동 감지**
- **LLM API 개수 확인** (0~4개)
- **실행 모드 자동 결정**:
  - API 0개 → 단독 모드 (Zen MCP Fallback)
  - API 1~4개 → 다중 협업 모드
- **예상 비용 표시** (Type별)
- **캐시/TTL 시스템** (5분간 재사용)

### 🔄 Phase 2: Tree of Thought (ToT) 구현
- **단독 모드**: 1개 LLM이 전문가 A,B,C 관점에서 ToT 수행
- **다중 모드**: 각 LLM이 독립적으로 ToT 수행 (최대 4개)
- **연속 세션**: Phase 4로 데이터 직접 전달
- **사고 가지(Branch) 생성 및 통합**

### 🔁 Phase 3: 순환 프로세스 구현
- **질문 1개씩 생성** (순차 진행)
- **선택지 2-3개 제공** (사용자 편의성)
- **최대 8-10회 반복**
- **만족도 기준**: 80% 이상 또는 최대 반복

### 🤝 Phase 4: 섹션별 협의 프로세스
- **단독 모드**: 단순 섹션별 작성
- **다중 모드**: 
  - Step 1: LLM1 초안 제안
  - Step 2-4: 다른 LLM들의 의견 + 개선안
  - Step 5: 최종 협의 및 통합
- **Phase 2 연속 세션 활용**

---

## 🎯 주요 기능

### ✅ 스마트 요청 분석
- 자동 명확도/복잡도 체크
- Type 1/2/3 자동 분류
- 30분 전역 타임아웃

### ✅ 환경 기반 최적화
- Zen MCP 자동 감지 및 Fallback
- API 개수 기반 모드 자동 선택
- 예상 비용 사전 표시

### ✅ Tree of Thought (ToT)
- 전문가별 사고 가지 생성
- 레벨별 인사이트 통합
- 다중 LLM 독립 수행

### ✅ 대화형 명확화
- 1개씩 질문 (순환)
- 선택지 제공
- Phase 2 자료 기반 질문 생성

### ✅ 협업 설계
- 섹션별 LLM 협의
- Step 1-5 체계적 프로세스
- Phase 2 연속 세션

---

## ⚡ 빠른 시작

### 1️⃣ 설치

```bash
git clone https://github.com/43onsomeday-debug/collaborative-insight-mcp.git
cd collaborative-insight-mcp
pip install -r requirements.txt
```

### 2️⃣ API 키 설정

`.env` 파일 생성:

```env
# 최소 1개 필수 (0개면 Zen MCP Fallback 사용)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
GROK_API_KEY=xai-...
```

### 3️⃣ 실행

```bash
python server.py
```

---

## 📖 각 Phase 상세 설명

### Phase 0: 요청 분석
- **역할**: 명확성/복잡도 체크, Type 분류
- **결과**: Type 1/2/3

### Phase 1: 전문가 배정
- **역할**: 계층 구조 파악, 전문가 배정
- **계층**: Domain → Subdomain → Category → Task

### Phase 1.5: 환경 체크 (NEW)
- **역할**: 실행 환경 확인 및 모드 결정
- **체크 항목**:
  - Zen MCP 연결
  - API 개수 (0~4개)
  - 실행 모드 (단독/다중)
  - 예상 비용
  - 캐시 설정

### Phase 2: 정보 수집
- **단독 모드**: LLM1 → 전문가 A,B,C → ToT
- **다중 모드**: LLM1~4 각각 ToT 수행
- **출력**: 통합된 인사이트 + Phase 4로 연속 세션

### Phase 3: 명확화 (Type 3만)
- **순환 프로세스**:
  1. 질문 1개 생성 (선택지 포함)
  2. 답변 대기
  3. 다음 질문 또는 완료
- **종료 조건**: 만족도 80% 또는 최대 10회

### Phase 4: 설계서 작성
- **단독 모드**: 섹션별 순차 작성
- **다중 모드**:
  - 각 섹션마다 Step 1-5 협의
  - LLM1 초안 → LLM2~4 의견 → 협의
- **입력**: Phase 2 연속 세션 데이터

### Phase 5: 실행자 선정
- 최적 LLM/MCP/Agent 선택

### Phase 6: 실행
- Phase 4 지시서 기반 실행

### Phase 7: 품질 체크
- 설계서 vs 결과물 검증

---

## 💡 사용 예시

### 예시 1: API 없음 (Zen MCP Fallback)
```
Phase 1.5:
✅ Zen MCP 연결됨
⚠️ API 0개 → 단독 LLM 모드

Phase 2:
LLM1(Zen MCP): 전문가 A,B,C → ToT → 보관

Phase 4:
단독 모드로 설계서 작성
```

### 예시 2: API 3개 (다중 협업)
```
Phase 1.5:
✅ API 3개 (Claude, GPT, Gemini) → 다중 모드
💰 예상 비용: Type 2 기준 $2-10

Phase 2:
LLM1(Claude): 전문가 A,B,C → ToT
LLM2(GPT): 전문가 A,B,C → ToT
LLM3(Gemini): 전문가 A,B,C → ToT

Phase 4:
각 섹션마다:
  Step 1: Claude 초안
  Step 2: GPT 의견 + 제안
  Step 3: Gemini 의견 + 제안
  Step 4: 협의 → 작성
```

---

## 🛠️ 기술 스택

- **Python 3.8+**
- **FastMCP** (MCP 서버)
- **Anthropic Claude**
- **OpenAI GPT**
- **Google Gemini**
- **Pydantic** (데이터 모델)

---

## 📦 프로젝트 구조

```
collaborative-insight-mcp/
├── phases/
│   ├── phase0.py          # 요청 분석
│   ├── phase1.py          # 전문가 배정
│   ├── phase1_5.py        # 환경 체크 ✨NEW
│   ├── phase2.py          # 정보 수집 (ToT) ✨UPDATED
│   ├── phase3.py          # 명확화 (순환) ✨UPDATED
│   ├── phase4.py          # 설계서 작성 (협의) ✨UPDATED
│   ├── phase5.py          # 실행자 선정
│   ├── phase6.py          # 실행
│   └── phase7.py          # 품질 체크
├── models.py              # 데이터 모델
├── llm_integration.py     # LLM 통합
├── server.py              # MCP 서버
└── README.md              # 이 파일
```

---

## 🤝 기여하기

1. Fork
2. Branch 생성: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Pull Request

---

## 📄 라이센스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 참조

---

## 🙏 감사의 말

- **FastMCP** - MCP 프레임워크
- **Anthropic** - Claude API
- **OpenAI** - GPT API
- **Google** - Gemini API

---

<div align="center">

**Made with ❤️ by Collaborative Insight Framework Team**

[GitHub](https://github.com/43onsomeday-debug/collaborative-insight-mcp)

</div>
