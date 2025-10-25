"""
Phase 2: 전략적 정보 수집
- Tree of Thought (ToT) 적용
- 단독/다중 모드 지원
- Phase 4로의 연속 세션
"""
from typing import List, Dict, Any, Optional
from models import ResearchItem, SourceInfo, Phase2Result


class TreeOfThought:
    """Tree of Thought (ToT) 구현"""
    
    @staticmethod
    def generate_thought_branches(
        expert_name: str,
        user_request: str,
        depth: int = 3
    ) -> List[Dict[str, Any]]:
        """
        전문가별 사고 가지(branch) 생성
        
        Args:
            expert_name: 전문가 이름
            user_request: 사용자 요청
            depth: 사고 깊이 (기본 3단계)
        
        Returns:
            사고 가지 목록
        """
        branches = []
        
        # Root: 핵심 질문
        root_thought = {
            "level": 0,
            "thought": f"{expert_name} 관점에서 '{user_request}'를 어떻게 접근할까?",
            "score": 1.0
        }
        branches.append(root_thought)
        
        # Branch 1: 문제 분해
        branch1 = {
            "level": 1,
            "thought": f"이 문제를 {expert_name} 영역의 하위 문제들로 분해",
            "sub_thoughts": [
                f"요구사항 분석 관점",
                f"기술적 실현 가능성",
                f"리스크 요인"
            ],
            "score": 0.9
        }
        branches.append(branch1)
        
        # Branch 2: 해결 방안 탐색
        branch2 = {
            "level": 2,
            "thought": f"{expert_name}로서 추천하는 접근 방법",
            "sub_thoughts": [
                f"Best Practice 적용",
                f"대안 솔루션 검토",
                f"통합 전략"
            ],
            "score": 0.85
        }
        branches.append(branch2)
        
        # Branch 3: 검증 및 보완
        branch3 = {
            "level": 3,
            "thought": f"제안 방안의 타당성 검증",
            "sub_thoughts": [
                f"장단점 분석",
                f"실행 가능성 평가",
                f"보완 사항"
            ],
            "score": 0.8
        }
        branches.append(branch3)
        
        return branches
    
    @staticmethod
    def synthesize_thoughts(
        all_branches: List[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        여러 전문가의 사고 가지를 통합
        
        Args:
            all_branches: 모든 전문가의 사고 가지
        
        Returns:
            통합된 인사이트
        """
        synthesis = {
            "total_branches": sum(len(branches) for branches in all_branches),
            "expert_count": len(all_branches),
            "key_insights": [],
            "consensus_points": [],
            "divergent_views": []
        }
        
        # 레벨별 사고 수집
        for level in range(4):
            level_thoughts = []
            for branches in all_branches:
                level_thoughts.extend([
                    b for b in branches if b.get("level") == level
                ])
            
            if level_thoughts:
                synthesis["key_insights"].append({
                    f"level_{level}": [t["thought"] for t in level_thoughts]
                })
        
        return synthesis


class InformationGatherer:
    """정보 수집 및 리서치 관리"""
    
    @staticmethod
    async def gather_information(
        user_request: str,
        experts: List[str],
        execution_mode: str = "단독",
        available_llms: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Phase2Result:
        """
        전략적 정보 수집 수행
        
        Args:
            user_request: 사용자 요청
            experts: 배정된 전문가 목록
            execution_mode: 실행 모드 ("단독" or "다중")
            available_llms: 사용 가능한 LLM 목록
            context: 이전 Phase의 컨텍스트
        
        Returns:
            Phase2Result: 수집된 정보 결과
        """
        
        if execution_mode == "단독":
            return await InformationGatherer._solo_mode_gather(
                user_request, experts, context
            )
        else:  # "다중"
            return await InformationGatherer._multi_mode_gather(
                user_request, experts, available_llms or [], context
            )
    
    @staticmethod
    async def _solo_mode_gather(
        user_request: str,
        experts: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Phase2Result:
        """
        단독 LLM 모드 정보 수집
        LLM1: 전문가A,B,C → ToT → 보관
        """
        
        # 1. Tree of Thought 생성
        all_branches = []
        for expert in experts[:3]:  # 상위 3명 전문가
            branches = TreeOfThought.generate_thought_branches(
                expert, user_request
            )
            all_branches.append(branches)
        
        # 2. ToT 통합
        tot_synthesis = TreeOfThought.synthesize_thoughts(all_branches)
        
        # 3. 키워드 추출
        keywords = InformationGatherer._extract_keywords(user_request)
        
        # 4. 리서치 항목 생성
        research_items = []
        for i, expert in enumerate(experts[:3]):
            research_areas = InformationGatherer._define_research_areas(
                expert, user_request
            )
            
            for area in research_areas:
                item = ResearchItem(
                    query=area['query'],
                    category=area['category'],
                    priority=area['priority'],
                    keywords=keywords
                )
                research_items.append(item)
        
        # 5. 우선순위 정렬 & 중복 제거
        research_items.sort(key=lambda x: x.priority, reverse=True)
        unique_items = InformationGatherer._deduplicate_items(research_items)
        
        # 6. Mock 소스 수집
        collected_sources = InformationGatherer._mock_collect_sources(unique_items)
        
        return Phase2Result(
            research_items=unique_items[:10],
            sources=collected_sources,
            execution_mode="단독",
            llms_used=["primary_llm"],
            metadata={
                "tot_synthesis": tot_synthesis,
                "total_queries": len(unique_items),
                "experts_count": len(experts),
                "keywords": keywords,
                "mode": "single_llm_with_tot"
            }
        )
    
    @staticmethod
    async def _multi_mode_gather(
        user_request: str,
        experts: List[str],
        available_llms: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Phase2Result:
        """
        다중 LLM 모드 정보 수집
        LLM1, LLM2, LLM3, LLM4: 각각 전문가A,B,C → ToT → 보관
        """
        
        all_llm_results = []
        
        # 각 LLM이 독립적으로 ToT 수행
        for llm_name in available_llms[:4]:  # 최대 4개 LLM
            llm_branches = []
            
            for expert in experts[:3]:  # 각 LLM당 상위 3명 전문가
                branches = TreeOfThought.generate_thought_branches(
                    expert, user_request
                )
                llm_branches.append(branches)
            
            # LLM별 ToT 통합
            llm_synthesis = TreeOfThought.synthesize_thoughts(llm_branches)
            
            all_llm_results.append({
                "llm": llm_name,
                "tot_synthesis": llm_synthesis,
                "branch_count": len(llm_branches)
            })
        
        # 키워드 추출
        keywords = InformationGatherer._extract_keywords(user_request)
        
        # 모든 LLM 결과를 통합하여 리서치 항목 생성
        research_items = []
        for expert in experts[:3]:
            research_areas = InformationGatherer._define_research_areas(
                expert, user_request
            )
            
            for area in research_areas:
                item = ResearchItem(
                    query=area['query'],
                    category=area['category'],
                    priority=area['priority'],
                    keywords=keywords
                )
                research_items.append(item)
        
        # 우선순위 정렬 & 중복 제거
        research_items.sort(key=lambda x: x.priority, reverse=True)
        unique_items = InformationGatherer._deduplicate_items(research_items)
        
        # Mock 소스 수집
        collected_sources = InformationGatherer._mock_collect_sources(unique_items)
        
        return Phase2Result(
            research_items=unique_items[:15],  # 다중 모드는 더 많은 항목
            sources=collected_sources,
            execution_mode="다중",
            llms_used=available_llms[:4],
            metadata={
                "all_llm_results": all_llm_results,
                "total_queries": len(unique_items),
                "experts_count": len(experts),
                "keywords": keywords,
                "mode": "multi_llm_with_tot",
                "llm_count": len(available_llms[:4])
            }
        )
    
    @staticmethod
    def _extract_keywords(request: str) -> List[str]:
        """요청에서 키워드 추출"""
        words = request.split()
        stop_words = {'을', '를', '이', '가', '은', '는', '에', '의', '고', '하고'}
        keywords = [w for w in words if w not in stop_words and len(w) > 1]
        return keywords[:10]
    
    @staticmethod
    def _define_research_areas(expert: str, request: str) -> List[Dict[str, Any]]:
        """전문가별 리서치 영역 정의"""
        
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
        
        for key in research_templates:
            if key in expert:
                return research_templates[key]
        
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
        """Mock 데이터 소스 수집"""
        
        sources = []
        
        for i, item in enumerate(items[:5]):
            source = SourceInfo(
                title=f"참고 자료: {item.query[:30]}...",
                url=f"https://example.com/source-{i+1}",
                relevance_score=0.9 - (i * 0.1),
                reliability_score=8.0 - (i * 0.5),
                is_official=i < 2
            )
            sources.append(source)
        
        return sources
