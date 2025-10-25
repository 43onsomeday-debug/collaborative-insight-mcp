"""
Phase 4: 설계 및 기획
- Phase 2 연속 세션 활용
- 단독/다중 모드 지원
- 섹션별 LLM 협의 프로세스
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from models import (
    DesignDocument, DesignSection, SourceInfo,
    QualityLevel, Phase4Result
)


class CollaborativeDesigner:
    """섹션별 협의 기반 설계서 생성"""
    
    @staticmethod
    async def collaborate_on_section(
        section_name: str,
        user_request: str,
        phase2_context: Dict[str, Any],
        available_llms: List[str]
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        섹션별 LLM 협의 프로세스
        
        Step 1: LLM1 제안 공유
        Step 2: LLM2 의견 + 제안
        Step 3: LLM3 의견 + 제안
        Step 4: LLM4 의견 + 제안
        Step 5: 협의 → 섹션 작성
        
        Args:
            section_name: 섹션 이름
            user_request: 사용자 요청
            phase2_context: Phase 2 연속 세션 데이터
            available_llms: 사용 가능한 LLM 목록
        
        Returns:
            (최종 섹션 내용, 협의 기록)
        """
        
        collaboration_records = []
        proposals = []
        
        # Step 1~4: 각 LLM의 제안 수집
        for i, llm_name in enumerate(available_llms[:4], 1):
            # 이전 제안들 참고
            previous_proposals = "\n\n".join([
                f"[{p['llm']}의 제안]\n{p['proposal']}"
                for p in proposals
            ])
            
            # LLM에게 제안 또는 의견 요청
            if i == 1:
                # 첫 번째 LLM: 초안 제안
                prompt = f"""
                섹션: {section_name}
                사용자 요청: {user_request}
                Phase 2 컨텍스트: {phase2_context}
                
                이 섹션의 초안을 작성해주세요.
                """
                proposal_type = "초안"
            else:
                # 이후 LLM: 이전 제안 검토 + 개선안
                prompt = f"""
                섹션: {section_name}
                
                이전 제안들:
                {previous_proposals}
                
                위 제안들을 검토하고:
                1. 강점과 약점 평가
                2. 개선 사항 제안
                3. 최종 통합안 제시
                """
                proposal_type = "개선안"
            
            # Mock LLM 응답 (실제로는 LLM API 호출)
            proposal = f"""
            [{llm_name}의 {proposal_type}]
            
            {section_name}에 대한 상세 내용:
            - 핵심 요소 1
            - 핵심 요소 2
            - 핵심 요소 3
            
            (Phase 2 ToT 결과 반영)
            """
            
            proposals.append({
                "step": i,
                "llm": llm_name,
                "type": proposal_type,
                "proposal": proposal
            })
            
            collaboration_records.append({
                "step": i,
                "llm": llm_name,
                "action": f"{proposal_type} 제시",
                "content_length": len(proposal)
            })
        
        # Step 5: 최종 협의 및 통합
        final_content = CollaborativeDesigner._synthesize_proposals(
            section_name,
            proposals,
            phase2_context
        )
        
        collaboration_records.append({
            "step": 5,
            "action": "협의 완료",
            "final_length": len(final_content),
            "llms_involved": len(proposals)
        })
        
        return final_content, collaboration_records
    
    @staticmethod
    def _synthesize_proposals(
        section_name: str,
        proposals: List[Dict[str, Any]],
        phase2_context: Dict[str, Any]
    ) -> str:
        """
        여러 LLM 제안을 통합
        
        Args:
            section_name: 섹션 이름
            proposals: 각 LLM의 제안 목록
            phase2_context: Phase 2 데이터
        
        Returns:
            통합된 최종 내용
        """
        
        # 실제로는 LLM이 모든 제안을 종합하여 최종안 작성
        # 여기서는 간단히 템플릿으로 대체
        
        synthesis = f"""
## {section_name}

### 개요
{len(proposals)}개 LLM의 협의를 통해 작성된 섹션입니다.

### 주요 내용
"""
        
        # Phase 2 ToT 결과 반영
        tot_insights = phase2_context.get("metadata", {}).get("tot_synthesis", {})
        if tot_insights:
            synthesis += "\n【Phase 2 인사이트 반영】\n"
            key_insights = tot_insights.get("key_insights", [])
            for insight in key_insights[:2]:  # 상위 2개만
                synthesis += f"- {insight}\n"
        
        synthesis += "\n### 세부 사항\n"
        synthesis += "1. 항목 1 (협의를 통해 도출)\n"
        synthesis += "2. 항목 2 (다수 LLM 동의)\n"
        synthesis += "3. 항목 3 (최적화된 접근)\n"
        
        return synthesis


class DesignGenerator:
    """설계서 생성기"""
    
    @classmethod
    def determine_quality_level(
        cls,
        request_type: str,
        complexity_score: int
    ) -> QualityLevel:
        """품질 레벨 결정"""
        if request_type == "Type 2" or complexity_score >= 4:
            return QualityLevel.LV2_CRITICAL
        else:
            return QualityLevel.LV1_STANDARD
    
    @classmethod
    def create_standard_sections(cls) -> List[str]:
        """표준 섹션 이름 목록"""
        return [
            "1. 프로젝트 개요",
            "2. 요구사항 분석",
            "3. 시스템 설계",
            "4. 구현 계획",
            "5. 위험 관리"
        ]
    
    @classmethod
    def create_critical_sections(cls) -> List[str]:
        """Lv2 섹션 이름 목록 (더 상세함)"""
        sections = cls.create_standard_sections()
        sections.extend([
            "6. 품질 보증",
            "7. 보안 및 규정 준수",
            "8. 유지보수 및 확장성"
        ])
        return sections
    
    @classmethod
    async def generate_design(
        cls,
        user_request: str,
        phase0_result: Any,
        phase1_result: Any,
        phase2_result: Any,
        execution_mode: str = "단독",
        available_llms: Optional[List[str]] = None,
        llm_client: Any = None
    ) -> DesignDocument:
        """
        설계서 생성
        
        Args:
            user_request: 사용자 요청
            phase0_result: Phase 0 결과
            phase1_result: Phase 1 결과
            phase2_result: Phase 2 결과 (연속 세션)
            execution_mode: 실행 모드 ("단독" or "다중")
            available_llms: 사용 가능한 LLM 목록
            llm_client: LLM 클라이언트
        """
        
        # 품질 레벨 결정
        complexity = phase0_result.complexity_score.total_score if phase0_result.complexity_score else 0
        quality_level = cls.determine_quality_level(
            phase0_result.request_type.value,
            complexity
        )
        
        # 섹션 목록 선택
        if quality_level == QualityLevel.LV2_CRITICAL:
            section_names = cls.create_critical_sections()
        else:
            section_names = cls.create_standard_sections()
        
        # Phase 2 연속 세션 컨텍스트
        phase2_context = {
            "research_items": phase2_result.research_items if phase2_result else [],
            "sources": phase2_result.sources if phase2_result else [],
            "metadata": phase2_result.metadata if phase2_result else {}
        }
        
        sections = []
        
        if execution_mode == "단독":
            # 단독 모드: 간단한 섹션별 작성
            for section_name in section_names:
                content = cls._generate_section_solo(
                    section_name,
                    user_request,
                    phase2_context
                )
                
                sections.append(DesignSection(
                    section_name=section_name,
                    content=content,
                    citations=[]
                ))
        
        else:  # 다중 모드
            # 섹션별 LLM 협의
            for section_name in section_names:
                content, collaboration_records = await CollaborativeDesigner.collaborate_on_section(
                    section_name=section_name,
                    user_request=user_request,
                    phase2_context=phase2_context,
                    available_llms=available_llms or []
                )
                
                sections.append(DesignSection(
                    section_name=section_name,
                    content=content,
                    citations=[]
                ))
        
        # 참고 문헌
        references = []
        if phase2_result and phase2_result.sources:
            references = phase2_result.sources
        
        return DesignDocument(
            title=f"설계서: {user_request[:50]}...",
            quality_level=quality_level,
            creation_date=datetime.now(),
            sections=sections,
            references=references,
            revision_count=0
        )
    
    @classmethod
    def _generate_section_solo(
        cls,
        section_name: str,
        user_request: str,
        phase2_context: Dict[str, Any]
    ) -> str:
        """
        단독 모드 섹션 생성
        
        Args:
            section_name: 섹션 이름
            user_request: 사용자 요청
            phase2_context: Phase 2 컨텍스트
        
        Returns:
            섹션 내용
        """
        
        content = f"""
## {section_name}

### 개요
{section_name}에 대한 상세 내용입니다.

### Phase 2 데이터 반영
"""
        
        # Phase 2 ToT 결과 활용
        tot_synthesis = phase2_context.get("metadata", {}).get("tot_synthesis", {})
        if tot_synthesis:
            content += f"- 전문가 브랜치 수: {tot_synthesis.get('total_branches', 0)}\n"
            content += f"- 참여 전문가 수: {tot_synthesis.get('expert_count', 0)}\n"
        
        content += "\n### 세부 내용\n"
        content += "1. 핵심 항목 1\n"
        content += "2. 핵심 항목 2\n"
        content += "3. 핵심 항목 3\n"
        
        return content
    
    @classmethod
    async def create_design(
        cls,
        user_request: str,
        phase0_result: Any,
        phase1_result: Any,
        phase2_result: Any,
        execution_mode: str = "단독",
        available_llms: Optional[List[str]] = None,
        llm_client: Any = None
    ) -> Phase4Result:
        """
        전체 설계 프로세스
        """
        
        design_document = await cls.generate_design(
            user_request,
            phase0_result,
            phase1_result,
            phase2_result,
            execution_mode,
            available_llms,
            llm_client
        )
        
        collaboration_records = []
        if execution_mode == "다중":
            collaboration_records = [
                {
                    "section": section.section_name,
                    "mode": "collaborative",
                    "llms_count": len(available_llms or [])
                }
                for section in design_document.sections
            ]
        
        return Phase4Result(
            design_document=design_document,
            execution_mode=execution_mode,
            collaboration_records=collaboration_records,
            user_interventions=[]
        )
