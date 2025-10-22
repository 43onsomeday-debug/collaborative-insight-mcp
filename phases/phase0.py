"""
Phase 0: 요청 분석 및 분류
"""
from typing import Dict
from models import (
    RequestType, ClarityScore, ComplexityScore, 
    Phase0Result
)


class RequestAnalyzer:
    """요청 분석기"""
    
    @staticmethod
    def analyze_clarity(user_request: str) -> ClarityScore:
        """
        명확성 분석 (5개 항목)
        """
        request_lower = user_request.lower()
        
        # 1. 구체적 상황
        specific_situation = any([
            len(user_request) > 30,  # 충분한 길이
            any(word in request_lower for word in [
                '에서', '때문에', '경우', '상황', '문제',
                'when', 'where', 'because', 'situation', 'problem'
            ])
        ])
        
        # 2. 목적 명시
        purpose_stated = any(word in request_lower for word in [
            '위해', '하려고', '목적', '목표', '원해', '필요',
            'to', 'for', 'want', 'need', 'purpose', 'goal', 'aim'
        ])
        
        # 3. 대상 명시
        target_specified = any([
            any(word in request_lower for word in [
                '사용자', '고객', '학생', '환자', '직원',
                'user', 'customer', 'student', 'patient', 'employee'
            ]),
            any(word in request_lower for word in [
                '제품', '서비스', '시스템', '앱', '웹사이트',
                'product', 'service', 'system', 'app', 'website'
            ])
        ])
        
        # 4. 배경지식
        background_knowledge = any([
            len(user_request) > 100,
            any(word in request_lower for word in [
                '현재', '기존', '지금까지', '과거',
                'currently', 'existing', 'current', 'past'
            ])
        ])
        
        # 5. 범위 설정
        scope_defined = any(word in request_lower for word in [
            '범위', '제한', '제외', '포함', '한정',
            'scope', 'limit', 'exclude', 'include', 'only', 'just'
        ])
        
        return ClarityScore(
            specific_situation=specific_situation,
            purpose_stated=purpose_stated,
            target_specified=target_specified,
            background_knowledge=background_knowledge,
            scope_defined=scope_defined
        )
    
    @staticmethod
    def analyze_complexity(user_request: str) -> ComplexityScore:
        """
        복잡도 분석 (4개 항목, 최대 7점)
        """
        request_lower = user_request.lower()
        score = ComplexityScore()
        
        # 1. 창의성 요구 (0-2점)
        creativity_keywords = ['창의', '혁신', '새로운', '독특', '차별화',
                              'creative', 'innovative', 'new', 'unique', 'novel']
        if any(word in request_lower for word in creativity_keywords):
            score.creativity_needed = 2
        elif any(word in request_lower for word in ['아이디어', 'idea', 'concept']):
            score.creativity_needed = 1
        
        # 2. 분석 필요 (0-2점)
        analysis_keywords = ['분석', '평가', '비교', '검토', '조사',
                           'analyze', 'evaluate', 'compare', 'review', 'research']
        if any(word in request_lower for word in analysis_keywords):
            score.analysis_needed = 2
        elif any(word in request_lower for word in ['확인', 'check', 'verify']):
            score.analysis_needed = 1
        
        # 3. 정보 통합 (0-1점)
        integration_keywords = ['통합', '결합', '종합', '합성',
                               'integrate', 'combine', 'synthesize', 'merge']
        if any(word in request_lower for word in integration_keywords):
            score.integration_needed = 1
        
        # 4. 중요 도메인 (0-2점)
        critical_keywords = ['법률', '의료', '금융', '안전', '보안',
                           'legal', 'medical', 'financial', 'safety', 'security']
        if any(word in request_lower for word in critical_keywords):
            score.critical_domain = 2
        elif any(word in request_lower for word in ['건강', 'health', '돈', 'money']):
            score.critical_domain = 1
        
        return score
    
    @staticmethod
    def calculate_confidence(
        clarity_score: ClarityScore,
        complexity_score: ComplexityScore = None
    ) -> float:
        """
        확신도 계산
        - 5점 또는 0점: 1.0
        - 4점 또는 1점: 0.8
        - 2점 또는 3점: 0.6
        """
        total = clarity_score.total_score
        
        if total == 5 or total == 0:
            return 1.0
        elif total == 4 or total == 1:
            return 0.8
        else:
            return 0.6
    
    @classmethod
    def analyze(
        cls,
        user_request: str,
        reclassify_mode: bool = False
    ) -> Phase0Result:
        """
        요청 분석 및 분류
        
        Args:
            user_request: 사용자 요청
            reclassify_mode: 재분류 모드 (Phase 3 이후)
        """
        # Step 1: 명확성 체크
        clarity_score = cls.analyze_clarity(user_request)
        
        # Step 2: 명확성 판단
        is_clear = clarity_score.is_clear
        
        # Step 3: 복잡도 평가 (명확한 경우만)
        complexity_score = None
        if is_clear or reclassify_mode:
            complexity_score = cls.analyze_complexity(user_request)
        
        # 확신도 계산
        confidence = cls.calculate_confidence(clarity_score, complexity_score)
        
        # 분류 결정
        if not is_clear and not reclassify_mode:
            request_type = RequestType.TYPE_3
            reasoning = f"명확성 점수 {clarity_score.total_score}/5 - 모호한 요청"
        elif complexity_score and complexity_score.is_complex:
            request_type = RequestType.TYPE_2
            reasoning = f"복잡도 점수 {complexity_score.total_score}/7 - 복잡명확"
        else:
            request_type = RequestType.TYPE_1
            reasoning = "단순명확 요청"
        
        return Phase0Result(
            request_type=request_type,
            clarity_score=clarity_score,
            complexity_score=complexity_score,
            confidence=confidence,
            reasoning=reasoning
        )
