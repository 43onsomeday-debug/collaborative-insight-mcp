"""
테스트 스크립트
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from phases.phase0 import RequestAnalyzer
from phases.phase1 import ExpertAssigner
from phases.phase4 import DesignGenerator


async def test_workflow():
    """기본 워크플로우 테스트"""
    
    print("=" * 60)
    print("Collaborative Insight Framework - Test")
    print("=" * 60)
    
    # Test 1: Phase 0
    print("\n[Test 1] Phase 0: 요청 분석")
    print("-" * 60)
    
    user_request = "웹사이트의 사용자 경험을 개선하고 싶어요. 현재 사용자들이 불편해하는 부분을 분석하고 개선 방안을 제시해주세요."
    
    phase0_result = RequestAnalyzer.analyze(user_request)
    
    print(f"요청: {user_request}")
    print(f"\n분석 결과:")
    print(f"  - 요청 유형: {phase0_result.request_type.value}")
    print(f"  - 명확성 점수: {phase0_result.clarity_score.total_score}/5")
    if phase0_result.complexity_score:
        print(f"  - 복잡도 점수: {phase0_result.complexity_score.total_score}/7")
    print(f"  - 확신도: {phase0_result.confidence}")
    print(f"  - 판단 근거: {phase0_result.reasoning}")
    
    # Test 2: Phase 1
    print("\n\n[Test 2] Phase 1: 전문가 배정")
    print("-" * 60)
    
    complexity = phase0_result.complexity_score.total_score if phase0_result.complexity_score else 0
    phase1_result = ExpertAssigner.assign(user_request, complexity)
    
    print(f"\n계층 구조:")
    print(f"  - Domain: {phase1_result.hierarchy.domain}")
    print(f"  - Subdomain: {phase1_result.hierarchy.subdomain}")
    print(f"  - Category: {phase1_result.hierarchy.category}")
    print(f"  - Task: {phase1_result.hierarchy.task}")
    
    print(f"\n배정된 전문가:")
    for i, expert in enumerate(phase1_result.experts, 1):
        print(f"  {i}. {expert.name}")
        print(f"     - 전문성: {expert.expertise}")
        print(f"     - 계층: {[layer.value for layer in expert.layers]}")
    
    print(f"\n처리 모드: {phase1_result.processing_mode.value}")
    
    # Test 3: Phase 4
    print("\n\n[Test 3] Phase 4: 설계서 생성")
    print("-" * 60)
    
    phase4_result = await DesignGenerator.create_design(
        user_request,
        phase0_result,
        phase1_result
    )
    
    design_doc = phase4_result.design_document
    
    print(f"\n설계서:")
    print(f"  - 제목: {design_doc.title}")
    print(f"  - 품질 레벨: {design_doc.quality_level.value}")
    print(f"  - 섹션 수: {len(design_doc.sections)}")
    
    print(f"\n섹션 목록:")
    for section in design_doc.sections:
        print(f"  - {section.section_name}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] 모든 테스트 완료!")
    print("=" * 60)


def test_clarity_analysis():
    """명확성 분석 다양한 케이스 테스트"""
    
    print("\n[추가 테스트] 다양한 요청 명확성 분석")
    print("-" * 60)
    
    test_cases = [
        "안녕하세요",
        "도와주세요",
        "웹사이트를 만들고 싶어요",
        "고객 관리 시스템을 위한 React 기반 대시보드를 개발하고 싶습니다. 사용자 인증, 데이터 시각화, 실시간 알림 기능이 필요합니다.",
    ]
    
    for i, request in enumerate(test_cases, 1):
        result = RequestAnalyzer.analyze(request)
        print(f"\n{i}. {request}")
        print(f"   → {result.request_type.value} (명확성: {result.clarity_score.total_score}/5, 확신도: {result.confidence})")


if __name__ == "__main__":
    # 기본 워크플로우 테스트
    asyncio.run(test_workflow())
    
    # 추가 테스트
    test_clarity_analysis()
