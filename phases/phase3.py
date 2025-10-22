"""
Phase 3: 명확화 대화
"""
from typing import List, Dict, Any, Optional
from models import ClarificationQuestion, Phase3Result, ClarificationResponse


class Clarifier:
    """명확화 질문 생성 및 관리"""
    
    @staticmethod
    def generate_questions(
        user_request: str,
        clarity_score: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Phase3Result:
        """
        명확화 질문 생성
        
        Args:
            user_request: 사용자 요청
            clarity_score: Phase 0의 명확성 점수
            context: 이전 Phase의 컨텍스트
        
        Returns:
            Phase3Result: 질문 및 응답 결과
        """
        
        # 1. 명확화가 필요한지 판단
        needs_clarification = clarity_score < 4.0
        
        if not needs_clarification:
            return Phase3Result(
                questions=[],
                responses=[],
                clarification_needed=False,
                metadata={"reason": "요청이 충분히 명확함"}
            )
        
        # 2. 부족한 영역 식별
        missing_areas = Clarifier._identify_missing_areas(
            user_request, 
            clarity_score
        )
        
        # 3. 질문 생성
        questions = Clarifier._create_questions(missing_areas, user_request)
        
        return Phase3Result(
            questions=questions,
            responses=[],  # 사용자 응답 대기
            clarification_needed=True,
            metadata={
                "missing_areas": missing_areas,
                "question_count": len(questions)
            }
        )
    
    @staticmethod
    def _identify_missing_areas(request: str, clarity_score: float) -> List[str]:
        """부족한 정보 영역 식별"""
        
        missing = []
        
        # 목적 명확성
        if "목적" not in request.lower() and "하고 싶" not in request:
            missing.append("목적")
        
        # 범위 명확성
        if len(request.split()) < 10:
            missing.append("범위")
        
        # 제약사항
        if "제약" not in request and "조건" not in request:
            missing.append("제약사항")
        
        # 산출물
        if "만들" not in request and "생성" not in request and "개발" not in request:
            missing.append("기대 산출물")
        
        # 배경 정보
        if clarity_score < 3.0:
            missing.append("배경 정보")
        
        return missing
    
    @staticmethod
    def _create_questions(
        missing_areas: List[str], 
        request: str
    ) -> List[ClarificationQuestion]:
        """영역별 질문 생성"""
        
        question_templates = {
            "목적": {
                "question": "이 작업의 주요 목적이나 달성하고자 하는 목표는 무엇인가요?",
                "category": "Goal",
                "priority": 10
            },
            "범위": {
                "question": "어느 범위까지 작업이 필요한가요? 구체적인 범위나 경계를 알려주세요.",
                "category": "Scope",
                "priority": 9
            },
            "제약사항": {
                "question": "특별히 고려해야 할 제약사항이나 조건이 있나요? (예: 예산, 기간, 기술 스택 등)",
                "category": "Constraints",
                "priority": 8
            },
            "기대 산출물": {
                "question": "최종적으로 어떤 형태의 결과물을 기대하시나요?",
                "category": "Deliverables",
                "priority": 9
            },
            "배경 정보": {
                "question": "현재 상황이나 배경에 대해 더 자세히 설명해주실 수 있나요?",
                "category": "Context",
                "priority": 7
            }
        }
        
        questions = []
        
        for area in missing_areas:
            if area in question_templates:
                template = question_templates[area]
                
                question = ClarificationQuestion(
                    question=template["question"],
                    category=template["category"],
                    priority=template["priority"],
                    context=f"요청: {request[:100]}..."
                )
                
                questions.append(question)
        
        # 우선순위로 정렬
        questions.sort(key=lambda x: x.priority, reverse=True)
        
        return questions
    
    @staticmethod
    def process_responses(
        questions: List[ClarificationQuestion],
        user_answers: List[str]
    ) -> Phase3Result:
        """
        사용자 응답 처리
        
        Args:
            questions: 생성된 질문 목록
            user_answers: 사용자의 답변 목록
        
        Returns:
            Phase3Result: 응답 처리 결과
        """
        
        responses = []
        
        for question, answer in zip(questions, user_answers):
            response = ClarificationResponse(
                question_id=question.question,
                answer=answer,
                satisfied=len(answer) > 10  # 간단한 만족도 체크
            )
            responses.append(response)
        
        return Phase3Result(
            questions=questions,
            responses=responses,
            clarification_needed=False,
            metadata={
                "completed": True,
                "response_count": len(responses)
            }
        )
    
    @staticmethod
    def enhance_request(
        original_request: str,
        clarification_result: Phase3Result
    ) -> str:
        """
        명확화 결과를 바탕으로 요청 보강
        
        Args:
            original_request: 원본 요청
            clarification_result: 명확화 결과
        
        Returns:
            str: 보강된 요청
        """
        
        if not clarification_result.responses:
            return original_request
        
        # 원본 요청에 응답 내용 추가
        enhanced = f"{original_request}\n\n[추가 정보]\n"
        
        for response in clarification_result.responses:
            enhanced += f"- {response.answer}\n"
        
        return enhanced
