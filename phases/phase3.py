"""
Phase 3: 명확화 대화
- 순환 프로세스 (최대 8-10회)
- 질문 1개씩 생성 및 답변 대기
- 선택지 2-3개 제공
"""
from typing import List, Dict, Any, Optional
from models import ClarificationQuestion, Phase3Result, ClarificationResponse


class Clarifier:
    """명확화 질문 생성 및 관리"""
    
    # 순환 제한
    MAX_ITERATIONS = 10
    
    @staticmethod
    def generate_next_question(
        user_request: str,
        phase2_data: Optional[Dict[str, Any]],
        previous_answers: List[ClarificationResponse],
        iteration: int = 0
    ) -> Optional[ClarificationQuestion]:
        """
        다음 질문 1개 생성 (순환 프로세스)
        
        Args:
            user_request: 사용자 요청
            phase2_data: Phase 2 수집 데이터
            previous_answers: 이전까지 수집된 답변
            iteration: 현재 반복 횟수
        
        Returns:
            ClarificationQuestion or None (더 이상 질문 불필요)
        """
        
        # 최대 반복 체크
        if iteration >= Clarifier.MAX_ITERATIONS:
            return None
        
        # 이미 답변된 카테고리 파악
        answered_categories = {
            ans.question_id.split(":")[0] 
            for ans in previous_answers
        }
        
        # Phase 2 데이터 기반 부족한 영역 식별
        missing_areas = Clarifier._identify_missing_areas_from_phase2(
            user_request,
            phase2_data,
            answered_categories
        )
        
        if not missing_areas:
            return None  # 더 이상 질문 불필요
        
        # 다음 우선순위 영역 선택
        next_area = missing_areas[0]
        
        # 질문 생성 (선택지 포함)
        question = Clarifier._create_question_with_choices(
            next_area,
            user_request,
            iteration
        )
        
        return question
    
    @staticmethod
    def _identify_missing_areas_from_phase2(
        user_request: str,
        phase2_data: Optional[Dict[str, Any]],
        answered_categories: set
    ) -> List[str]:
        """
        Phase 2 자료 기반으로 부족한 영역 식별
        
        Args:
            user_request: 사용자 요청
            phase2_data: Phase 2 데이터
            answered_categories: 이미 답변한 카테고리
        
        Returns:
            부족한 영역 목록 (우선순위 순)
        """
        
        all_areas = [
            "목적",
            "범위",
            "제약사항",
            "기대_산출물",
            "대상_사용자",
            "배경_정보",
            "우선순위",
            "일정"
        ]
        
        missing = []
        
        for area in all_areas:
            # 이미 답변한 영역 스킵
            if area in answered_categories:
                continue
            
            # Phase 2 데이터에서 해당 영역 정보 확인
            if phase2_data:
                tot_synthesis = phase2_data.get("metadata", {}).get("tot_synthesis", {})
                key_insights = tot_synthesis.get("key_insights", [])
                
                # 영역별 정보 부족 체크
                area_covered = False
                for insight in key_insights:
                    for level_key, thoughts in insight.items():
                        if any(area in str(thought) for thought in thoughts):
                            area_covered = True
                            break
                
                if not area_covered:
                    missing.append(area)
            else:
                # Phase 2 데이터 없으면 모든 영역 확인 필요
                missing.append(area)
        
        return missing
    
    @staticmethod
    def _create_question_with_choices(
        area: str,
        user_request: str,
        iteration: int
    ) -> ClarificationQuestion:
        """
        선택지가 포함된 질문 생성
        
        Args:
            area: 질문할 영역
            user_request: 사용자 요청
            iteration: 반복 횟수
        
        Returns:
            ClarificationQuestion
        """
        
        question_templates = {
            "목적": {
                "question": "이 작업의 주요 목적은 무엇인가요?",
                "choices": [
                    "1. 새로운 기능/서비스 개발",
                    "2. 기존 시스템 개선/최적화",
                    "3. 문제 해결/버그 수정"
                ],
                "category": "Goal",
                "priority": 10
            },
            "범위": {
                "question": "작업 범위를 어느 정도로 설정하시겠습니까?",
                "choices": [
                    "1. 최소 기능만 (MVP)",
                    "2. 핵심 기능 + 주요 확장",
                    "3. 완전한 기능 구현"
                ],
                "category": "Scope",
                "priority": 9
            },
            "제약사항": {
                "question": "주요 제약사항이나 고려사항이 있나요?",
                "choices": [
                    "1. 예산/비용 제한",
                    "2. 기술 스택 제한",
                    "3. 일정/시간 제약"
                ],
                "category": "Constraints",
                "priority": 8
            },
            "기대_산출물": {
                "question": "최종 산출물의 형태는 무엇인가요?",
                "choices": [
                    "1. 문서/가이드",
                    "2. 코드/프로그램",
                    "3. 디자인/설계안"
                ],
                "category": "Deliverables",
                "priority": 9
            },
            "대상_사용자": {
                "question": "주요 대상 사용자는 누구인가요?",
                "choices": [
                    "1. 일반 사용자",
                    "2. 개발자/기술자",
                    "3. 비즈니스/관리자"
                ],
                "category": "Target",
                "priority": 8
            },
            "배경_정보": {
                "question": "현재 상황이나 배경에 대해 설명해주세요.",
                "choices": [
                    "1. 신규 프로젝트 시작",
                    "2. 기존 프로젝트 확장",
                    "3. 문제 상황 해결"
                ],
                "category": "Context",
                "priority": 7
            },
            "우선순위": {
                "question": "가장 중요한 요소는 무엇인가요?",
                "choices": [
                    "1. 품질/완성도",
                    "2. 속도/일정",
                    "3. 비용/효율성"
                ],
                "category": "Priority",
                "priority": 7
            },
            "일정": {
                "question": "예상 일정이나 마감일이 있나요?",
                "choices": [
                    "1. 긴급 (1주 이내)",
                    "2. 보통 (1개월 이내)",
                    "3. 여유 (3개월 이상)"
                ],
                "category": "Schedule",
                "priority": 6
            }
        }
        
        if area not in question_templates:
            # 기본 질문
            return ClarificationQuestion(
                question=f"{area}에 대해 더 자세히 알려주세요.",
                category="General",
                priority=5,
                context=f"[반복 {iteration+1}/{Clarifier.MAX_ITERATIONS}] {user_request[:100]}..."
            )
        
        template = question_templates[area]
        
        # 선택지를 context에 포함
        choices_text = "\n".join(template["choices"])
        full_context = (
            f"[반복 {iteration+1}/{Clarifier.MAX_ITERATIONS}]\n"
            f"요청: {user_request[:80]}...\n\n"
            f"선택지:\n{choices_text}\n\n"
            f"(번호 선택 또는 직접 입력 가능)"
        )
        
        return ClarificationQuestion(
            question=template["question"],
            category=template["category"],
            priority=template["priority"],
            context=full_context
        )
    
    @staticmethod
    def process_answer(
        question: ClarificationQuestion,
        user_answer: str,
        iteration: int
    ) -> ClarificationResponse:
        """
        답변 처리 및 만족도 체크
        
        Args:
            question: 질문
            user_answer: 사용자 답변
            iteration: 반복 횟수
        
        Returns:
            ClarificationResponse
        """
        
        # 답변 충분성 체크
        is_sufficient = len(user_answer.strip()) > 5
        
        response = ClarificationResponse(
            question_id=f"{question.category}:{iteration}",
            answer=user_answer,
            satisfied=is_sufficient
        )
        
        return response
    
    @staticmethod
    def check_clarification_complete(
        collected_answers: List[ClarificationResponse],
        iteration: int
    ) -> tuple[bool, str]:
        """
        명확화 완료 여부 체크
        
        Args:
            collected_answers: 수집된 답변 목록
            iteration: 현재 반복 횟수
        
        Returns:
            (완료 여부, 이유)
        """
        
        # 최소 3개 질문 답변 필요
        if len(collected_answers) < 3:
            return False, f"최소 3개 질문 필요 (현재 {len(collected_answers)}개)"
        
        # 만족스러운 답변 비율 체크
        satisfied_count = sum(1 for ans in collected_answers if ans.satisfied)
        satisfaction_rate = satisfied_count / len(collected_answers)
        
        # 80% 이상 만족 또는 최대 반복 도달
        if satisfaction_rate >= 0.8:
            return True, f"만족도 {satisfaction_rate*100:.0f}% 달성"
        
        if iteration >= Clarifier.MAX_ITERATIONS - 1:
            return True, f"최대 반복 횟수 도달 ({iteration+1}/{Clarifier.MAX_ITERATIONS})"
        
        return False, f"계속 진행 (만족도 {satisfaction_rate*100:.0f}%)"
    
    @staticmethod
    def generate_initial_result(
        user_request: str,
        phase2_data: Optional[Dict[str, Any]] = None
    ) -> Phase3Result:
        """
        Phase 3 초기 결과 생성 (첫 질문 포함)
        
        Args:
            user_request: 사용자 요청
            phase2_data: Phase 2 데이터
        
        Returns:
            Phase3Result (첫 질문 포함)
        """
        
        # 첫 질문 생성
        first_question = Clarifier.generate_next_question(
            user_request=user_request,
            phase2_data=phase2_data,
            previous_answers=[],
            iteration=0
        )
        
        if not first_question:
            # 질문 불필요 (이미 충분히 명확)
            return Phase3Result(
                questions=[],
                responses=[],
                clarification_needed=False,
                metadata={
                    "reason": "요청이 충분히 명확함",
                    "phase2_coverage": "complete"
                }
            )
        
        return Phase3Result(
            questions=[first_question],
            responses=[],
            clarification_needed=True,
            metadata={
                "iteration": 0,
                "max_iterations": Clarifier.MAX_ITERATIONS,
                "status": "waiting_for_first_answer"
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
        enhanced = f"{original_request}\n\n【명확화 정보】\n"
        
        for i, response in enumerate(clarification_result.responses, 1):
            category = response.question_id.split(":")[0]
            enhanced += f"{i}. {category}: {response.answer}\n"
        
        return enhanced
