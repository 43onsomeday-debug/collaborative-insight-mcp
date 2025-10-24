# 🤝 Collaborative Insight MCP

> 여러 AI가 협업하여 더 나은 답변을 만드는 똑똑한 시스템

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

---

## 🎯 이런 문제를 해결합니다

### 문제 상황
AI에게 질문할 때 이런 경험 있으시죠?

❌ **"내 질문이 애매해서 엉뚱한 답변이 나왔어요"**
❌ **"복잡한 문제는 답변이 부족해요"**  
❌ **"어떤 AI를 써야 할지 모르겠어요"**

### 해결 방법
✅ **자동으로 질문을 분석**해서 명확하게 만듭니다  
✅ **여러 AI가 협업**해서 복잡한 문제도 해결합니다  
✅ **최적의 AI를 자동 선택**해서 최고의 답변을 제공합니다

---

## 💡 이렇게 작동합니다

```
사용자의 질문 입력
      ↓
🔍 Phase 0: 질문 분석
"이 질문이 명확한가? 얼마나 복잡한가?"
      ↓
👥 Phase 1: 전문가 배정
"이 분야 전문가는 누구지?"
      ↓
📚 Phase 2: 정보 수집
"필요한 정보를 모아볼까?"
      ↓
❓ Phase 3: 명확화 (필요시)
"사용자에게 더 물어볼까?"
      ↓
📝 Phase 4: 설계서 작성
"어떻게 답변할지 계획을 세우자"
      ↓
🎯 Phase 5: AI 선택
"누가 가장 잘할 수 있을까?"
      ↓
⚙️ Phase 6: 실행
"실제로 답변을 만들자!"
      ↓
✅ Phase 7: 품질 검사
"답변이 충분한가? 정확한가?"
      ↓
🎉 최종 답변 전달!
```

---

## ⚡ 5분 만에 시작하기

### 1️⃣ 설치

```bash
# 프로젝트 다운로드
git clone https://github.com/43onsomeday-debug/collaborative-insight-mcp.git
cd collaborative-insight-mcp

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 2️⃣ API 키 설정

`.env` 파일을 만들고 API 키를 입력하세요:

```env
# 최소 하나는 필수입니다
ANTHROPIC_API_KEY=sk-ant-...    # Claude 사용
OPENAI_API_KEY=sk-...           # ChatGPT 사용  
GEMINI_API_KEY=AIza...          # Gemini 사용
```

💡 **API 키 받는 방법:**
- Claude: https://console.anthropic.com/
- ChatGPT: https://platform.openai.com/
- Gemini: https://makersuite.google.com/

### 3️⃣ 실행

```bash
# MCP 서버 시작
python server.py
```

✅ **성공!** 이제 Claude Desktop에서 사용할 수 있습니다.

---

## 📖 상세 가이드

### Claude Desktop 연동하기

1. **설정 파일 열기**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **서버 추가하기**

```json
{
  "mcpServers": {
    "collaborative-insight": {
      "command": "python",
      "args": [
        "C:\\경로\\collaborative-insight-mcp\\server.py"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "여기에-Claude-키",
        "OPENAI_API_KEY": "여기에-GPT-키",
        "GEMINI_API_KEY": "여기에-Gemini-키"
      }
    }
  }
}
```

3. **Claude Desktop 재시작**

4. **확인하기**
   - 새 대화 시작
   - "collaborative-insight" 도구가 보이면 성공!

---

## 🎓 각 Phase 상세 설명

### 📌 Phase 0: 요청 분석 및 분류

**역할:** 사용자 질문을 분석하고 분류합니다

**체크 항목:**
1. ✅ **명확성** - 질문이 구체적인가?
2. ✅ **완성도** - 필요한 정보가 다 있나?
3. ✅ **실행 가능성** - 실제로 답변할 수 있나?
4. ✅ **범위** - 너무 크거나 작지 않나?
5. ✅ **일관성** - 서로 모순되지 않나?

**복잡도 평가:**
- 1-2점: 아주 간단 (예: "안녕하세요")
- 3-4점: 간단 (예: "Python 설치 방법")
- 5-6점: 보통 (예: "웹사이트 만들기")
- 7점: 복잡 (예: "AI 기반 추천 시스템 설계")

**분류 결과:**
- **Type 1**: 단순 명확 → 1개 AI로 처리
- **Type 2**: 복잡함 → 여러 AI 협업 필요
- **Type 3**: 모호함 → 사용자에게 먼저 질문

**사용 예시:**
```python
analyze_request(
    user_request="온라인 쇼핑몰을 만들고 싶어요"
)

# 결과:
{
    "request_type": "Type 3",  # 모호함
    "clarity_score": 2,         # 정보 부족
    "complexity_score": 6,      # 복잡도 높음
    "reasoning": "구체적인 기능, 규모, 기술 스택이 불명확"
}
```

---

### 📌 Phase 1: 계층 구조 분석 및 전문가 배정

**역할:** 문제를 계층적으로 분석하고 적합한 전문가를 배정합니다

**15가지 계층 조합:**

| 레벨 | 설명 | 예시 |
|------|------|------|
| Domain | 큰 분야 | "웹 개발" |
| Subdomain | 세부 분야 | "프론트엔드" |
| Category | 카테고리 | "React 개발" |
| Task | 구체적 작업 | "컴포넌트 설계" |

**전문가 배정 방식:**

1. **Domain만** → Domain Expert 1명
2. **Domain + Subdomain** → 2명 협업
3. **Domain + Subdomain + Category** → 3명 협업
4. **Domain + Subdomain + Category + Task** → 4명 협업

**사용 예시:**
```python
assign_experts(session_id="session_123")

# 결과:
{
    "hierarchy": {
        "domain": "웹 개발",
        "subdomain": "프론트엔드",
        "category": "React",
        "task": "상태 관리"
    },
    "experts": [
        {"role": "Domain Expert", "expertise": "웹 개발 아키텍처"},
        {"role": "Subdomain Expert", "expertise": "프론트엔드 최적화"},
        {"role": "Category Expert", "expertise": "React 생태계"},
        {"role": "Task Specialist", "expertise": "Redux/Zustand"}
    ]
}
```

---

### 📌 Phase 2: 전략적 정보 수집

**역할:** 필요한 정보를 체계적으로 수집합니다

**정보 수집 전략:**

1. **기존 지식 활용**
   - 각 전문가가 보유한 지식
   - 이전 세션 데이터

2. **외부 정보 검색**
   - 최신 문서 검색
   - 관련 자료 수집

3. **정보 통합**
   - 중복 제거
   - 우선순위 정리

**정보 카테고리:**
- 📚 **기술 문서**: 공식 문서, API 레퍼런스
- 💡 **모범 사례**: 권장 패턴, 사례 연구
- ⚠️ **주의사항**: 알려진 이슈, 제한사항
- 🔧 **도구/라이브러리**: 필요한 패키지, 도구

**사용 예시:**
```python
gather_information(session_id="session_123")

# 결과:
{
    "collected_info": {
        "technical_docs": ["React 18 공식 문서", "Hooks 가이드"],
        "best_practices": ["상태 관리 패턴", "성능 최적화"],
        "warnings": ["useEffect 의존성 주의", "메모리 누수"],
        "tools": ["Redux Toolkit", "Zustand", "Jotai"]
    },
    "confidence_level": "high"
}
```

---

### 📌 Phase 3: 사용자 의도 명확화

**역할:** 모호한 질문을 명확하게 만듭니다

**언제 실행되나요?**
- Phase 0에서 Type 3 (모호함)으로 분류된 경우
- 명확성 점수가 3점 이하인 경우

**질문 생성 프로세스:**

1. **4개 AI가 독립적으로 질문 생성**
   - Claude: 기술적 관점
   - GPT: 실용적 관점
   - Gemini: 창의적 관점
   - Grok: 사용자 경험 관점

2. **합의 도달**
   - 4개 중 3개 이상이 동의한 질문만 사용
   - 가장 중요한 질문 1개씩 순차 진행

3. **대화형 명확화**
   - 한 번에 1개 질문만
   - 사용자 답변 후 다음 질문
   - 충분히 명확해지면 종료

**사용 예시:**
```python
# 1. 명확화 시작
clarify_user_intent(session_id="session_123")

# 결과:
{
    "current_question": "쇼핑몰의 주요 기능은 무엇인가요? (예: 결제, 장바구니, 리뷰)",
    "waiting_for_answer": true
}

# 2. 답변 입력
answer_clarification_question(
    session_id="session_123",
    answer="결제와 장바구니 기능이 필요해요"
)

# 결과:
{
    "next_question": "예상 사용자 수는 얼마나 되나요?",
    "waiting_for_answer": true
}

# 3. 명확화 완료
answer_clarification_question(
    session_id="session_123",
    answer="일일 1000명 정도요"
)

# 결과:
{
    "clarification_complete": true,
    "updated_request": "일일 1000명 규모의 결제/장바구니 기능이 있는 온라인 쇼핑몰"
}
```

---

### 📌 Phase 4: 설계서 생성

**역할:** 답변을 위한 상세 설계서를 작성합니다

**품질 레벨:**

**Lv1 STANDARD** (일반 작업)
- ✅ 필수 섹션만 포함
- ✅ 기본적인 설명
- ✅ 빠른 작성 (5-7개 섹션)

**Lv2 CRITICAL** (중요 작업)
- ✅ 모든 섹션 포함
- ✅ 상세한 설명
- ✅ 단계별 가이드 (10-15개 섹션)

**설계서 구조:**

```
1. 개요
   - 목적
   - 범위
   - 핵심 요구사항

2. 아키텍처
   - 시스템 구조
   - 기술 스택
   - 구성 요소

3. 상세 설계
   - 각 기능별 설계
   - 데이터 모델
   - API 설계

4. 구현 계획
   - 단계별 작업
   - 우선순위
   - 예상 시간

5. 테스트 전략
   - 테스트 계획
   - 검증 방법

6. 위험 관리
   - 예상 문제
   - 대응 방안
```

**사용 예시:**
```python
create_design(session_id="session_123")

# 결과:
{
    "title": "온라인 쇼핑몰 설계서",
    "quality_level": "Lv2 Critical",
    "sections": [
        {
            "title": "1. 시스템 개요",
            "content": "React 기반 SPA, Node.js 백엔드..."
        },
        {
            "title": "2. 프론트엔드 아키텍처",
            "content": "컴포넌트 구조, 상태 관리..."
        },
        // ... 13개 섹션
    ],
    "estimated_complexity": "medium-high"
}
```

---

### 📌 Phase 5: LLM 선택

**역할:** 작업에 가장 적합한 AI를 선택합니다

**LLM 프로필 레지스트리:**

| AI | 장점 | 적합한 작업 |
|----|------|-------------|
| **Claude** | 코드 분석, 깊은 이해 | 복잡한 코드, 아키텍처 설계 |
| **GPT** | 범용성, 빠른 응답 | 일반적인 작업, 글쓰기 |
| **Gemini** | 다국어, 창의성 | 콘텐츠 생성, 번역 |
| **Grok** | 실시간 정보, 트렌드 | 최신 정보, 뉴스 분석 |

**선택 알고리즘:**

```
점수 = (기술 적합도 × 40%) 
     + (최신성 × 30%) 
     + (성공률 × 20%) 
     + (가용성 × 10%)
```

**사용 예시:**
```python
select_llm(session_id="session_123")

# 결과:
{
    "selected_llm": "claude",
    "reasoning": {
        "technical_fit": 0.95,    # React 아키텍처에 강함
        "recency": 0.80,          # 최신 정보
        "success_rate": 0.90,     # 과거 성공률
        "availability": 1.0       # 현재 사용 가능
    },
    "final_score": 0.89,
    "alternatives": [
        {"llm": "gpt", "score": 0.75},
        {"llm": "gemini", "score": 0.65}
    ]
}
```

---

### 📌 Phase 6: 작업 실행

**역할:** 선택된 AI가 실제 작업을 수행합니다

**실행 모드:**

1. **단독 실행** (Type 1)
   - 1개 AI가 처리
   - 빠른 응답

2. **협업 실행** (Type 2)
   - Sequential: 순차적 작업
   - Parallel: 병렬 작업
   - Validation: 교차 검증

**협업 패턴 예시:**

**Sequential (순차):**
```
Claude → GPT → Gemini
(설계)  (구현)  (최적화)
```

**Parallel (병렬):**
```
    → Claude (백엔드)
동시 → GPT (프론트엔드)
    → Gemini (문서화)
```

**Validation (검증):**
```
Claude가 작성
   ↓
GPT가 검토
   ↓
Gemini가 최종 확인
```

**사용 예시:**
```python
execute_task(
    session_id="session_123",
    selected_llm="claude"
)

# 결과:
{
    "execution_mode": "collaborative",
    "pattern": "sequential",
    "results": {
        "phase_1": {
            "llm": "claude",
            "output": "아키텍처 설계 완료...",
            "status": "success"
        },
        "phase_2": {
            "llm": "gpt",
            "output": "컴포넌트 구현 완료...",
            "status": "success"
        }
    },
    "final_output": "완성된 쇼핑몰 프로젝트..."
}
```

---

### 📌 Phase 7: 품질 검사

**역할:** 최종 결과물의 품질을 검증합니다

**4가지 품질 기준:**

1. **충분성 (Sufficiency)**
   - 요청한 내용이 모두 포함되었나?
   - 필요한 설명이 충분한가?

2. **일관성 (Consistency)**
   - 내용이 서로 모순되지 않나?
   - 스타일이 일관적인가?

3. **최신성 (Currency)**
   - 최신 정보를 사용했나?
   - 오래된 방식은 없나?

4. **완성도 (Completeness)**
   - 모든 단계가 완료되었나?
   - 빠진 부분은 없나?

**검증 프로세스:**

```
4개 AI가 독립 평가
    ↓
각 기준별로 Pass/Fail
    ↓
4개 중 3개 이상 Pass → 해당 기준 통과
    ↓
4개 기준 모두 통과 → 최종 승인
    ↓
통과 못하면 → 재작업 (최대 2회)
```

**사용 예시:**
```python
# 자동으로 실행됨 (수동 호출 불필요)

# 검증 결과:
{
    "quality_check": {
        "sufficiency": {
            "pass": true,
            "votes": {"claude": "pass", "gpt": "pass", "gemini": "pass", "grok": "pass"}
        },
        "consistency": {
            "pass": true,
            "votes": {"claude": "pass", "gpt": "pass", "gemini": "pass", "grok": "fail"}
        },
        "currency": {
            "pass": false,  # 3개 이상 통과 못함
            "votes": {"claude": "fail", "gpt": "fail", "gemini": "pass", "grok": "pass"}
        },
        "completeness": {
            "pass": true,
            "votes": {"claude": "pass", "gpt": "pass", "gemini": "pass", "grok": "pass"}
        }
    },
    "overall_pass": false,
    "rework_needed": ["최신 React 19 기능 반영 필요"],
    "rework_count": 1
}
```

---

## 🎬 실제 사용 사례

### 사례 1: 간단한 질문 (Type 1)

**질문:** "Python에서 리스트를 정렬하는 방법"

**처리 과정:**
```
Phase 0: Type 1 분류 (단순 명확)
    ↓
Phase 1: Python Expert 1명 배정
    ↓
Phase 6: Claude가 직접 답변
    ↓
결과: "list.sort() 또는 sorted() 사용..."
```

⏱️ **소요 시간:** 약 5초

---

### 사례 2: 복잡한 프로젝트 (Type 2)

**질문:** "온라인 강의 플랫폼을 만들고 싶어요"

**처리 과정:**
```
Phase 0: Type 2 분류 (복잡)
    ↓
Phase 1: 4명 전문가 배정
    - 웹 개발 전문가
    - 동영상 전문가
    - 결제 전문가
    - UX 전문가
    ↓
Phase 2: 정보 수집
    - Udemy 사례 분석
    - 동영상 플랫폼 기술
    - 결제 시스템 조사
    ↓
Phase 4: 상세 설계서 작성 (Lv2)
    - 15개 섹션
    - 단계별 구현 계획
    ↓
Phase 5: Claude + GPT 협업 선택
    ↓
Phase 6: 순차 협업 실행
    - Claude: 아키텍처 설계
    - GPT: 구현 코드 작성
    ↓
Phase 7: 품질 검사
    - 4개 AI가 검증
    - 모든 기준 통과
    ↓
결과: 완성된 프로젝트 설계 + 코드
```

⏱️ **소요 시간:** 약 2-3분

---

### 사례 3: 모호한 질문 (Type 3)

**질문:** "뭔가 만들고 싶어요"

**처리 과정:**
```
Phase 0: Type 3 분류 (모호)
    ↓
Phase 3: 명확화 시작
    Q1: "어떤 종류의 것을 만들고 싶으신가요?"
    A1: "웹사이트요"
    
    Q2: "어떤 목적의 웹사이트인가요?"
    A2: "개인 블로그요"
    
    Q3: "어떤 기능이 필요한가요?"
    A3: "글 쓰기, 댓글, 검색"
    
    → 명확화 완료!
    ↓
Phase 0: 재분석 → Type 2
    ↓
Phase 1~7: 정상 진행
    ↓
결과: 블로그 플랫폼 완성
```

⏱️ **소요 시간:** 약 3-5분 (사용자 답변 시간 포함)

---

## 🛠️ API 레퍼런스

### 🔹 analyze_request

**설명:** 사용자 요청을 분석하고 분류합니다

**파라미터:**
```python
{
    "user_request": str,      # 필수: 사용자의 질문
    "session_id": str | None  # 선택: 기존 세션 ID (없으면 새로 생성)
}
```

**반환값:**
```python
{
    "session_id": str,          # 세션 ID
    "request_type": str,        # "Type 1" | "Type 2" | "Type 3"
    "clarity_score": int,       # 1-5
    "complexity_score": int,    # 1-7
    "reasoning": str,           # 분류 이유
    "next_phase": str          # 다음 Phase
}
```

**예시:**
```python
result = analyze_request(
    user_request="Python으로 웹 크롤러 만들기"
)
```

---

### 🔹 clarify_user_intent

**설명:** 모호한 질문을 명확하게 만듭니다 (Type 3에만 사용)

**파라미터:**
```python
{
    "session_id": str  # 필수: 세션 ID
}
```

**반환값:**
```python
{
    "current_question": str,      # 현재 질문
    "question_number": int,       # 몇 번째 질문
    "total_questions": int,       # 총 질문 수
    "waiting_for_answer": bool   # true
}
```

---

### 🔹 answer_clarification_question

**설명:** 명확화 질문에 답변합니다

**파라미터:**
```python
{
    "session_id": str,  # 필수: 세션 ID
    "answer": str       # 필수: 사용자 답변
}
```

**반환값:**
```python
{
    "next_question": str | None,        # 다음 질문 (또는 None)
    "clarification_complete": bool,     # 명확화 완료 여부
    "updated_request": str | None      # 업데이트된 질문 (완료시)
}
```

---

### 🔹 assign_experts

**설명:** 전문가를 배정합니다

**파라미터:**
```python
{
    "session_id": str  # 필수: 세션 ID
}
```

**반환값:**
```python
{
    "hierarchy": {
        "domain": str,
        "subdomain": str | None,
        "category": str | None,
        "task": str | None
    },
    "experts": [
        {
            "role": str,
            "expertise": str
        }
    ],
    "processing_mode": str  # "single" | "collaborative"
}
```

---

### 🔹 gather_information

**설명:** 필요한 정보를 수집합니다

**파라미터:**
```python
{
    "session_id": str  # 필수: 세션 ID
}
```

**반환값:**
```python
{
    "collected_info": {
        "technical_docs": [str],
        "best_practices": [str],
        "warnings": [str],
        "tools": [str]
    },
    "sources": [str],
    "confidence_level": str  # "low" | "medium" | "high"
}
```

---

### 🔹 create_design

**설명:** 설계서를 생성합니다

**파라미터:**
```python
{
    "session_id": str  # 필수: 세션 ID
}
```

**반환값:**
```python
{
    "title": str,
    "quality_level": str,  # "Lv1 Standard" | "Lv2 Critical"
    "sections": [
        {
            "title": str,
            "content": str,
            "subsections": [str] | None
        }
    ],
    "estimated_complexity": str,
    "estimated_time": str
}
```

---

### 🔹 select_llm

**설명:** 최적의 AI를 선택합니다

**파라미터:**
```python
{
    "session_id": str  # 필수: 세션 ID
}
```

**반환값:**
```python
{
    "selected_llm": str,  # "claude" | "gpt" | "gemini" | "grok"
    "reasoning": {
        "technical_fit": float,
        "recency": float,
        "success_rate": float,
        "availability": float
    },
    "final_score": float,
    "alternatives": [
        {
            "llm": str,
            "score": float
        }
    ]
}
```

---

### 🔹 execute_task

**설명:** 실제 작업을 실행합니다

**파라미터:**
```python
{
    "session_id": str,           # 필수: 세션 ID
    "selected_llm": str | None   # 선택: 특정 AI 지정 (없으면 자동 선택)
}
```

**반환값:**
```python
{
    "execution_mode": str,  # "single" | "collaborative"
    "pattern": str | None,  # "sequential" | "parallel" | "validation"
    "results": {
        "phase_1": {
            "llm": str,
            "output": str,
            "status": str
        }
    },
    "final_output": str,
    "quality_check": {
        "passed": bool,
        "issues": [str] | None
    }
}
```

---

### 🔹 get_workflow_status

**설명:** 현재 워크플로우 상태를 조회합니다

**파라미터:**
```python
{
    "session_id": str  # 필수: 세션 ID
}
```

**반환값:**
```python
{
    "session_id": str,
    "current_phase": int,          # 0-7
    "phase_name": str,
    "completed_phases": [int],
    "status": str,                 # "in_progress" | "completed" | "failed"
    "last_update": str,           # ISO timestamp
    "workflow_data": {
        "request": str,
        "request_type": str,
        "experts": [...],
        "design": {...},
        "results": {...}
    }
}
```

---

## ❓ 트러블슈팅

### 문제: "API 키가 유효하지 않습니다"

**원인:**
- API 키가 잘못 입력됨
- API 키가 만료됨
- 환경 변수가 설정되지 않음

**해결:**
```bash
# 1. .env 파일 확인
cat .env

# 2. API 키 형식 확인
# Claude: sk-ant-로 시작
# GPT: sk-로 시작
# Gemini: AIza로 시작

# 3. 환경 변수 다시 로드
source .env  # Mac/Linux
# 또는 터미널 재시작
```

---

### 문제: "서버가 시작되지 않습니다"

**원인:**
- Python 버전이 낮음 (3.8 미만)
- 필요한 패키지가 설치되지 않음
- 포트가 이미 사용 중

**해결:**
```bash
# 1. Python 버전 확인
python --version  # 3.8 이상이어야 함

# 2. 패키지 재설치
pip install -r requirements.txt --force-reinstall

# 3. 포트 확인 (Windows)
netstat -ano | findstr :3000

# 4. 다른 포트 사용
# server.py에서 포트 번호 변경
```

---

### 문제: "Type 3로 분류되었는데 질문이 명확한데요?"

**원인:**
- 질문이 짧거나 맥락이 부족함
- 전문 용어가 많음
- 여러 가지를 한 번에 물어봄

**해결:**
```
# 개선 전:
"웹사이트 만들기"

# 개선 후:
"React와 Node.js를 사용해서 
일일 방문자 500명 규모의 
블로그 웹사이트를 만들고 싶습니다"
```

**팁:**
- ✅ 구체적인 기술 스택 명시
- ✅ 규모/범위 명시
- ✅ 최종 목표 명시

---

### 문제: "답변 품질이 기대보다 낮아요"

**원인:**
- API 키가 무료 티어 (제한적)
- 질문이 너무 광범위함
- 적절한 AI가 선택되지 않음

**해결:**

**1. 질문을 더 구체적으로:**
```
# 나쁨:
"프로그래밍 배우고 싶어요"

# 좋음:
"Python으로 데이터 분석을 하고 싶은데,
Pandas와 NumPy를 사용하는 기초 예제를 
단계별로 알려주세요"
```

**2. API 티어 확인:**
- 유료 API는 더 높은 품질과 속도 제공
- 각 서비스의 요금제 확인

**3. 수동 LLM 선택:**
```python
# 특정 AI 강제 지정
execute_task(
    session_id="session_123",
    selected_llm="claude"  # 코드 작업에 강함
)
```

---

### 문제: "Phase 7 검증에서 계속 실패해요"

**원인:**
- 요구사항이 너무 까다로움
- 정보가 부족함
- 최신 정보가 필요한데 구버전 사용

**해결:**

**1. 재작업 로그 확인:**
```python
status = get_workflow_status(session_id="session_123")
print(status["workflow_data"]["quality_check"]["rework_reasons"])
```

**2. 정보 업데이트:**
- Phase 2에서 최신 정보 수집 강화
- 공식 문서 링크 제공

**3. 요구사항 조정:**
- 너무 완벽을 추구하지 말고 단계적 개선

---

### 문제: "Claude Desktop에서 도구가 안 보여요"

**원인:**
- 설정 파일 경로가 잘못됨
- JSON 문법 오류
- Claude Desktop을 재시작하지 않음

**해결:**

**1. 설정 파일 위치 확인:**
```bash
# Windows
%APPDATA%\Claude\claude_desktop_config.json

# Mac
~/Library/Application Support/Claude/claude_desktop_config.json

# Linux
~/.config/Claude/claude_desktop_config.json
```

**2. JSON 문법 검증:**
```bash
# 온라인 도구 사용
# https://jsonlint.com/
```

**3. 로그 확인:**
```bash
# Windows
%APPDATA%\Claude\logs\mcp*.log

# Mac
~/Library/Logs/Claude/mcp*.log
```

**4. Claude Desktop 완전 재시작:**
- 작업 관리자에서 완전 종료
- 다시 시작

---

## 🤝 기여하기

이 프로젝트를 개선하고 싶으신가요?

### 기여 방법

1. **버그 리포트**
   - GitHub Issues에 버그 제보
   - 재현 방법 포함

2. **기능 제안**
   - 어떤 기능이 필요한지 설명
   - 사용 사례 포함

3. **코드 기여**
   ```bash
   # 1. Fork
   # 2. 브랜치 생성
   git checkout -b feature/새기능
   
   # 3. 커밋
   git commit -m "Add: 새 기능 추가"
   
   # 4. Push
   git push origin feature/새기능
   
   # 5. Pull Request
   ```

4. **문서 개선**
   - 오타 수정
   - 예시 추가
   - 번역

### 개발 가이드라인

**코드 스타일:**
- Python: PEP 8
- 주석: 한글 또는 영어
- Docstring: 필수

**테스트:**
```bash
# 테스트 실행
pytest tests/

# 특정 Phase 테스트
pytest tests/test_phase0.py
```

**커밋 메시지:**
```
Add: 새 기능 추가
Fix: 버그 수정
Update: 기존 기능 개선
Docs: 문서 수정
Test: 테스트 추가/수정
```

---

## 📊 프로젝트 로드맵

### ✅ 완료 (v1.0)
- [x] Phase 0: 요청 분석
- [x] Phase 1: 전문가 배정
- [x] Phase 2: 정보 수집
- [x] Phase 3: 명확화
- [x] Phase 4: 설계 생성
- [x] Phase 5: LLM 선택
- [x] Phase 6: 실행
- [x] Phase 7: 품질 검사
- [x] MCP 서버 구현
- [x] Claude Desktop 연동

### 🚧 진행 중 (v1.1)
- [ ] Zen MCP 통합
- [ ] 세션 영속화 (데이터베이스)
- [ ] 웹 UI 대시보드
- [ ] 성능 최적화

### 📅 계획 중 (v2.0)
- [ ] 플러그인 시스템
- [ ] 커스텀 Phase 추가 기능
- [ ] 다국어 지원 (영어, 중국어)
- [ ] 클라우드 배포 옵션
- [ ] 팀 협업 기능

---

## 📞 지원 및 커뮤니티

### 도움이 필요하신가요?

**📧 이메일:** support@collaborative-insight.com  
**💬 Discord:** https://discord.gg/collaborative-insight  
**🐛 버그 제보:** https://github.com/43onsomeday-debug/collaborative-insight-mcp/issues  
**📚 문서:** https://docs.collaborative-insight.com

### 커뮤니티

- 💡 아이디어 공유
- 🤝 협업 파트너 찾기
- 📰 업데이트 소식
- 🎓 튜토리얼 및 팁

---

## 📄 라이센스

이 프로젝트는 **MIT 라이센스** 하에 공개되었습니다.

```
MIT License

Copyright (c) 2025 Collaborative Insight Framework Team

본 소프트웨어 및 관련 문서 파일("소프트웨어")의 복사본을 
얻는 모든 사람에게 무료로 제공됩니다...
```

자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트를 기반으로 합니다:

- **FastMCP** - MCP 서버 프레임워크
- **Anthropic Claude** - AI 모델
- **OpenAI GPT** - AI 모델
- **Google Gemini** - AI 모델

그리고 이 프로젝트에 기여해주신 모든 분들께 감사드립니다! 🎉

---

## 🌟 Star History

이 프로젝트가 도움이 되었다면 ⭐️ 스타를 눌러주세요!

---

<div align="center">

**Made with ❤️ by Collaborative Insight Framework Team**

[GitHub](https://github.com/43onsomeday-debug/collaborative-insight-mcp) • 
[Documentation](https://docs.collaborative-insight.com) • 
[Discord](https://discord.gg/collaborative-insight)

</div>
