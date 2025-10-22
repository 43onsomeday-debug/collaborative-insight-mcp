"""
Phase 2: 전략적 정보 수집
"""
from typing import List, Dict, Any, Optional
from models import ResearchItem, SourceInfo, Phase2Result


class InformationGatherer:
    """정보 수집 및 리서치 관리"""
    
    @staticmethod
    async def gather_information(
        user_request: str,
        experts: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Phase2Result:
        """
        전략적 정보 수집 수행
        
        Args:
            user_request: 사용자 요청
            experts: 배정된 전문가 목록
            context: 이전 Phase의 컨텍스트
        
        Returns:
            Phase2Result: 수집된 정보 결과
        """
        
        # 1. 키워드 추출
        keywords = InformationGatherer._extract_keywords(user_request)
        
        # 2. 리서치 항목 생성
        research_items = []
        
        for expert in experts[:3]:  # 상위 3명 전문가 기준
            # 전문가별 리서치 영역 정의
            research_areas = InformationGatherer._define_research_areas(
                expert, 
                user_request
            )
            
            for area in research_areas:
                item = ResearchItem(
                    query=area['query'],
                    category=area['category'],
                    priority=area['priority'],
                    keywords=keywords
                )
                research_items.append(item)
        
        # 3. 우선순위 정렬
        research_items.sort(key=lambda x: x.priority, reverse=True)
        
        # 4. 중복 제거
        unique_items = InformationGatherer._deduplicate_items(research_items)
        
        # 5. 수집된 정보 (Mock - 실제로는 web_search 도구 사용)
        collected_sources = InformationGatherer._mock_collect_sources(unique_items)
        
        return Phase2Result(
            research_items=unique_items[:10],  # 상위 10개
            sources=collected_sources,
            metadata={
                "total_queries": len(unique_items),
                "experts_count": len(experts),
                "keywords": keywords
            }
        )
    
    @staticmethod
    def _extract_keywords(request: str) -> List[str]:
        """요청에서 키워드 추출"""
        # 간단한 키워드 추출 (실제로는 더 정교한 NLP 사용)
        words = request.split()
        
        # 불용어 제거
        stop_words = {'을', '를', '이', '가', '은', '는', '에', '의', '고', '하고'}
        keywords = [w for w in words if w not in stop_words and len(w) > 1]
        
        return keywords[:10]  # 상위 10개
    
    @staticmethod
    def _define_research_areas(expert: str, request: str) -> List[Dict[str, Any]]:
        """전문가별 리서치 영역 정의"""
        
        # 전문가 유형별 리서치 영역
        research_templates = {
            "UX": [
                {
                    "query": f"{request} 사용자 경험 모범 사례",
                    "category": "Best Practices",
                    "priority": 9
                },
                {
                    "query": f"{request} UX 디자인 가이드라인",
                    "category": "Guidelines",
                    "priority": 8
                }
            ],
            "개발": [
                {
                    "query": f"{request} 기술 스택 추천",
                    "category": "Technical",
                    "priority": 9
                },
                {
                    "query": f"{request} 구현 예제",
                    "category": "Examples",
                    "priority": 7
                }
            ],
            "기획": [
                {
                    "query": f"{request} 프로젝트 계획",
                    "category": "Planning",
                    "priority": 8
                },
                {
                    "query": f"{request} 요구사항 분석",
                    "category": "Requirements",
                    "priority": 9
                }
            ]
        }
        
        # 전문가 이름에서 키워드 매칭
        for key in research_templates:
            if key in expert:
                return research_templates[key]
        
        # 기본 리서치 영역
        return [
            {
                "query": f"{request} 가이드",
                "category": "General",
                "priority": 5
            }
        ]
    
    @staticmethod
    def _deduplicate_items(items: List[ResearchItem]) -> List[ResearchItem]:
        """중복 항목 제거"""
        seen = set()
        unique = []
        
        for item in items:
            if item.query not in seen:
                seen.add(item.query)
                unique.append(item)
        
        return unique
    
    @staticmethod
    def _mock_collect_sources(items: List[ResearchItem]) -> List[SourceInfo]:
        """Mock 데이터 소스 수집 (실제로는 web_search 사용)"""
        
        sources = []
        
        for i, item in enumerate(items[:5]):  # 상위 5개만
            source = SourceInfo(
                title=f"참고 자료: {item.query[:30]}...",
                url=f"https://example.com/source-{i+1}",
                snippet=f"{item.query}에 대한 상세 정보입니다. "
                        f"카테고리: {item.category}, 우선순위: {item.priority}",
                relevance_score=0.9 - (i * 0.1),
                reliability_score=8.0 - (i * 0.5),  # 추가
                source_type="web"
            )
            sources.append(source)
        
        return sources
    
    @staticmethod
    async def search_web(query: str) -> List[Dict[str, Any]]:
        """
        웹 검색 수행 (MCP web_search 도구 활용)
        실제 구현시 MCP의 web_search 도구를 호출
        """
        # TODO: MCP web_search 도구 통합
        # 현재는 Mock 데이터 반환
        
        return [
            {
                "title": f"검색 결과: {query}",
                "url": "https://example.com",
                "snippet": f"{query}에 대한 정보..."
            }
        ]
