"""
Phase 2 테스트: 전략적 정보 수집
"""
import asyncio
from phases.phase1 import ExpertAssigner
from phases.phase2 import InformationGatherer


async def test_phase2_basic():
    """Phase 2 기본 테스트"""
    print("=" * 60)
    print("Phase 2 기본 테스트 시작")
    print("=" * 60)
    
    # 테스트 데이터
    user_request = "모바일 앱 UX 개선을 위한 디자인 시스템 구축"
    experts = [
        "Senior UX Designer",
        "Frontend Developer",
        "Product Manager"
    ]
    
    print(f"\n사용자 요청: {user_request}")
    print(f"배정된 전문가: {experts}")
    
    # Phase 2 실행
    result = await InformationGatherer.gather_information(
        user_request=user_request,
        experts=experts
    )
    
    print(f"\n[결과]")
    print(f"생성된 리서치 항목: {len(result.research_items)}개")
    print(f"수집된 소스: {len(result.sources)}개")
    print(f"메타데이터: {result.metadata}")
    
    print("\n[리서치 항목 상세]")
    for i, item in enumerate(result.research_items[:5], 1):
        print(f"\n{i}. 쿼리: {item.query}")
        print(f"   카테고리: {item.category}")
        print(f"   우선순위: {item.priority}")
        print(f"   키워드: {item.keywords[:5]}")
    
    print("\n[수집된 소스]")
    for i, source in enumerate(result.sources, 1):
        print(f"\n{i}. {source.title}")
        print(f"   URL: {source.url}")
        print(f"   관련도: {source.relevance_score}")
        print(f"   신뢰도: {source.reliability_score}")
        print(f"   요약: {source.snippet[:80]}...")
    
    return result


async def test_phase1_to_phase2_integration():
    """Phase 1 → Phase 2 통합 테스트"""
    print("\n\n" + "=" * 60)
    print("Phase 1 → Phase 2 통합 테스트")
    print("=" * 60)
    
    # 테스트 요청
    user_request = "AI 기반 고객 서비스 챗봇 개발"
    
    print(f"\n사용자 요청: {user_request}")
    
    # Phase 1: 전문가 배정
    print("\n[Step 1] Phase 1 실행 - 전문가 배정")
    phase1_result = await ExpertAssigner.assign_experts(
        user_request=user_request,
        hierarchy_present=True
    )
    
    expert_names = [expert.name for expert in phase1_result.experts]
    print(f"배정된 전문가: {expert_names}")
    
    # Phase 2: 정보 수집
    print("\n[Step 2] Phase 2 실행 - 정보 수집")
    phase2_result = await InformationGatherer.gather_information(
        user_request=user_request,
        experts=expert_names,
        context={"phase1": phase1_result.model_dump()}
    )
    
    print(f"\n[통합 결과]")
    print(f"전문가 수: {len(phase1_result.experts)}명")
    print(f"리서치 항목: {len(phase2_result.research_items)}개")
    print(f"수집된 소스: {len(phase2_result.sources)}개")
    
    print("\n[생성된 리서치 항목 Top 3]")
    for i, item in enumerate(phase2_result.research_items[:3], 1):
        print(f"{i}. [{item.category}] {item.query} (우선순위: {item.priority})")
    
    return phase1_result, phase2_result


async def test_keyword_extraction():
    """키워드 추출 테스트"""
    print("\n\n" + "=" * 60)
    print("키워드 추출 테스트")
    print("=" * 60)
    
    test_requests = [
        "블록체인 기반 NFT 마켓플레이스 개발",
        "실시간 협업 문서 편집기 구현",
        "머신러닝을 활용한 추천 시스템 설계"
    ]
    
    for request in test_requests:
        keywords = InformationGatherer._extract_keywords(request)
        print(f"\n요청: {request}")
        print(f"추출된 키워드: {keywords}")


async def main():
    """전체 테스트 실행"""
    try:
        # 1. 기본 테스트
        await test_phase2_basic()
        
        # 2. 통합 테스트
        await test_phase1_to_phase2_integration()
        
        # 3. 키워드 추출 테스트
        await test_keyword_extraction()
        
        print("\n\n" + "=" * 60)
        print("모든 Phase 2 테스트 완료!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
