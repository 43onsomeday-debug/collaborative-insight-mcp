"""
Phase 7: 검증 및 품질 평가
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from models import (
    ValidationResult, ValidationCheck, ValidationLevel,
    QualityMetrics, Phase7Result
)


class Validator:
    """결과 검증 및 품질 평가"""
    
    @staticmethod
    def validate_result(
        result: Any,
        original_request: str,
        design_document: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> Phase7Result:
        """
        생성된 결과 검증
        
        Args:
            result: Phase 6의 실행 결과
            original_request: 원본 사용자 요청
            design_document: Phase 4의 설계서
            context: 추가 컨텍스트
        
        Returns:
            Phase7Result: 검증 결과
        """
        
        # 1. 검증 체크 수행
        validation_checks = Validator._perform_checks(
            result,
            original_request,
            design_document
        )
        
        # 2. 품질 메트릭 계산
        quality_metrics = Validator._calculate_metrics(
            result,
            validation_checks
        )
        
        # 3. 전체 검증 결과 생성
        validation_result = Validator._create_validation_result(
            validation_checks,
            quality_metrics
        )
        
        # 4. 개선 제안 생성
        improvements = Validator._suggest_improvements(
            validation_checks,
            quality_metrics
        )
        
        return Phase7Result(
            validation_result=validation_result,
            quality_metrics=quality_metrics,
            improvements=improvements,
            metadata={
                "validated_at": datetime.now().isoformat(),
                "check_count": len(validation_checks)
            }
        )
    
    @staticmethod
    def _perform_checks(
        result: Any,
        original_request: str,
        design_document: Any
    ) -> List[ValidationCheck]:
        """검증 체크 수행"""
        
        checks = []
        
        # 1. 완성도 체크
        completeness_check = Validator._check_completeness(
            result,
            design_document
        )
        checks.append(completeness_check)
        
        # 2. 정확도 체크
        accuracy_check = Validator._check_accuracy(
            result,
            original_request
        )
        checks.append(accuracy_check)
        
        # 3. 일관성 체크
        consistency_check = Validator._check_consistency(result)
        checks.append(consistency_check)
        
        # 4. 실용성 체크
        usability_check = Validator._check_usability(result)
        checks.append(usability_check)
        
        return checks
    
    @staticmethod
    def _check_completeness(
        result: Any,
        design_document: Any
    ) -> ValidationCheck:
        """완성도 검증"""
        
        passed = True
        issues = []
        score = 1.0
        
        # 설계서의 모든 섹션이 결과에 반영되었는지 확인
        if hasattr(design_document, 'sections'):
            expected_sections = len(design_document.sections)
            
            # 결과에서 섹션 수 추정 (간단한 휴리스틱)
            result_str = str(result)
            result_sections = result_str.count('\n\n') + 1
            
            if result_sections < expected_sections * 0.7:
                passed = False
                issues.append(f"예상 섹션({expected_sections})의 70% 미만 포함")
                score = result_sections / expected_sections
        
        return ValidationCheck(
            check_name="완성도",
            level=ValidationLevel.CRITICAL,
            passed=passed,
            score=score,
            issues=issues,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def _check_accuracy(
        result: Any,
        original_request: str
    ) -> ValidationCheck:
        """정확도 검증"""
        
        passed = True
        issues = []
        score = 1.0
        
        # 요청의 주요 키워드가 결과에 포함되어 있는지 확인
        result_str = str(result).lower()
        request_words = original_request.lower().split()
        
        # 주요 키워드 (2글자 이상)
        keywords = [w for w in request_words if len(w) > 2][:10]
        
        if keywords:
            matched = sum(1 for kw in keywords if kw in result_str)
            score = matched / len(keywords)
            
            if score < 0.5:
                passed = False
                issues.append(f"요청의 주요 키워드({len(keywords)}개 중 {matched}개만 포함)")
        
        return ValidationCheck(
            check_name="정확도",
            level=ValidationLevel.HIGH,
            passed=passed,
            score=score,
            issues=issues,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def _check_consistency(result: Any) -> ValidationCheck:
        """일관성 검증"""
        
        passed = True
        issues = []
        score = 1.0
        
        result_str = str(result)
        
        # 기본 일관성 체크
        # 1. 문단 구조
        paragraphs = result_str.split('\n\n')
        if len(paragraphs) < 2:
            issues.append("문단 구조가 부족함")
            score *= 0.8
        
        # 2. 길이 균형
        if paragraphs:
            lengths = [len(p) for p in paragraphs]
            avg_length = sum(lengths) / len(lengths)
            
            # 너무 짧거나 긴 문단 체크
            unbalanced = sum(1 for l in lengths if l < avg_length * 0.3 or l > avg_length * 3)
            if unbalanced > len(paragraphs) * 0.3:
                issues.append("문단 길이 불균형")
                score *= 0.9
        
        if issues:
            passed = len(issues) == 0
        
        return ValidationCheck(
            check_name="일관성",
            level=ValidationLevel.MEDIUM,
            passed=passed,
            score=score,
            issues=issues,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def _check_usability(result: Any) -> ValidationCheck:
        """실용성 검증"""
        
        passed = True
        issues = []
        score = 1.0
        
        result_str = str(result)
        
        # 1. 최소 길이 체크
        if len(result_str) < 100:
            passed = False
            issues.append("결과가 너무 짧음 (최소 100자 필요)")
            score = len(result_str) / 100
        
        # 2. 구조화 체크 (헤더, 리스트 등)
        has_structure = any([
            '\n#' in result_str,  # 마크다운 헤더
            '\n-' in result_str,  # 리스트
            '\n1.' in result_str,  # 번호 리스트
        ])
        
        if not has_structure:
            issues.append("구조화된 포맷 부족")
            score *= 0.9
        
        return ValidationCheck(
            check_name="실용성",
            level=ValidationLevel.MEDIUM,
            passed=passed,
            score=score,
            issues=issues,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def _calculate_metrics(
        result: Any,
        checks: List[ValidationCheck]
    ) -> QualityMetrics:
        """품질 메트릭 계산"""
        
        # 전체 점수 계산
        if checks:
            overall_score = sum(check.score for check in checks) / len(checks)
        else:
            overall_score = 0.0
        
        # 통과한 체크 수
        passed_checks = sum(1 for check in checks if check.passed)
        
        # 레벨별 가중치
        level_weights = {
            ValidationLevel.CRITICAL: 1.0,
            ValidationLevel.HIGH: 0.8,
            ValidationLevel.MEDIUM: 0.6,
            ValidationLevel.LOW: 0.4
        }
        
        weighted_score = sum(
            check.score * level_weights.get(check.level, 0.5)
            for check in checks
        )
        
        if checks:
            weighted_score /= len(checks)
        
        return QualityMetrics(
            overall_score=overall_score,
            completeness=next((c.score for c in checks if c.check_name == "완성도"), 0.0),
            accuracy=next((c.score for c in checks if c.check_name == "정확도"), 0.0),
            consistency=next((c.score for c in checks if c.check_name == "일관성"), 0.0),
            usability=next((c.score for c in checks if c.check_name == "실용성"), 0.0),
            confidence=weighted_score
        )
    
    @staticmethod
    def _create_validation_result(
        checks: List[ValidationCheck],
        metrics: QualityMetrics
    ) -> ValidationResult:
        """검증 결과 생성"""
        
        # 전체 통과 여부
        passed = all(check.passed for check in checks)
        
        # 모든 이슈 수집
        all_issues = []
        for check in checks:
            all_issues.extend(check.issues)
        
        # 심각도 결정
        if metrics.overall_score >= 0.9:
            severity = "low"
        elif metrics.overall_score >= 0.7:
            severity = "medium"
        elif metrics.overall_score >= 0.5:
            severity = "high"
        else:
            severity = "critical"
        
        return ValidationResult(
            passed=passed,
            checks=checks,
            issues=all_issues,
            severity=severity,
            validated_at=datetime.now()
        )
    
    @staticmethod
    def _suggest_improvements(
        checks: List[ValidationCheck],
        metrics: QualityMetrics
    ) -> List[str]:
        """개선 제안 생성"""
        
        suggestions = []
        
        # 완성도 개선
        if metrics.completeness < 0.8:
            suggestions.append(
                "완성도를 높이기 위해 누락된 섹션을 추가하거나 기존 내용을 보강하세요."
            )
        
        # 정확도 개선
        if metrics.accuracy < 0.7:
            suggestions.append(
                "원본 요청의 주요 키워드와 의도를 더 명확히 반영하세요."
            )
        
        # 일관성 개선
        if metrics.consistency < 0.8:
            suggestions.append(
                "문단 구조와 스타일을 일관되게 유지하세요."
            )
        
        # 실용성 개선
        if metrics.usability < 0.8:
            suggestions.append(
                "결과를 더 구조화하고 읽기 쉽게 포맷팅하세요."
            )
        
        # 개선사항이 없으면
        if not suggestions:
            suggestions.append("검증 결과가 우수합니다! 추가 개선사항이 필요하지 않습니다.")
        
        return suggestions
