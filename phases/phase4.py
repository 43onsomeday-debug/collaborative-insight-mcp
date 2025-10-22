"""
Phase 4: 설계 및 기획
"""
from datetime import datetime
from typing import List, Dict, Any
from models import (
    DesignDocument, DesignSection, SourceInfo,
    QualityLevel, Phase4Result
)


class DesignGenerator:
    """설계서 생성기"""
    
    @classmethod
    def determine_quality_level(
        cls,
        request_type: str,
        complexity_score: int
    ) -> QualityLevel:
        """
        품질 레벨 결정
        
        Lv1: Type 1 (단순명확)
        Lv2: Type 2 (복잡명확) 또는 복잡도 >= 4
        """
        if request_type == "Type 2" or complexity_score >= 4:
            return QualityLevel.LV2_CRITICAL
        else:
            return QualityLevel.LV1_STANDARD
    
    @classmethod
    def create_standard_sections(cls) -> List[DesignSection]:
        """
        표준 섹션 템플릿 생성
        """
        return [
            DesignSection(
                section_name="1. 프로젝트 개요",
                content="프로젝트의 배경, 목적, 범위를 정의합니다."
            ),
            DesignSection(
                section_name="2. 요구사항 분석",
                content="사용자 요구사항과 기능적/비기능적 요구사항을 정리합니다."
            ),
            DesignSection(
                section_name="3. 시스템 설계",
                content="아키텍처, 데이터 모델, 인터페이스 설계를 포함합니다."
            ),
            DesignSection(
                section_name="4. 구현 계획",
                content="개발 일정, 리소스, 마일스톤을 정의합니다."
            ),
            DesignSection(
                section_name="5. 위험 관리",
                content="예상 위험 요소와 대응 전략을 수립합니다."
            )
        ]
    
    @classmethod
    def create_critical_sections(cls) -> List[DesignSection]:
        """
        Lv2 섹션 템플릿 (더 상세함)
        """
        sections = cls.create_standard_sections()
        
        # Lv2에는 추가 섹션
        sections.extend([
            DesignSection(
                section_name="6. 품질 보증",
                content="테스트 전략, 품질 기준, 검증 방법을 정의합니다."
            ),
            DesignSection(
                section_name="7. 보안 및 규정 준수",
                content="보안 요구사항과 법적/규제적 준수 사항을 다룹니다."
            ),
            DesignSection(
                section_name="8. 유지보수 및 확장성",
                content="장기적 유지보수 계획과 확장 가능성을 고려합니다."
            )
        ])
        
        return sections
    
    @classmethod
    async def generate_design(
        cls,
        user_request: str,
        phase0_result: Any,
        phase1_result: Any,
        research_data: List[Dict] = None,
        llm_client: Any = None
    ) -> DesignDocument:
        """
        설계서 생성
        
        Args:
            user_request: 사용자 요청
            phase0_result: Phase 0 결과
            phase1_result: Phase 1 결과
            research_data: Phase 2 정보 수집 결과
            llm_client: LLM 클라이언트
        """
        # 품질 레벨 결정
        complexity = phase0_result.complexity_score.total_score if phase0_result.complexity_score else 0
        quality_level = cls.determine_quality_level(
            phase0_result.request_type.value,
            complexity
        )
        
        # 섹션 템플릿 선택
        if quality_level == QualityLevel.LV2_CRITICAL:
            sections = cls.create_critical_sections()
        else:
            sections = cls.create_standard_sections()
        
        # LLM을 사용하여 각 섹션 내용 생성
        if llm_client:
            for section in sections:
                # 실제 구현에서는 LLM API 호출
                prompt = f"""
                사용자 요청: {user_request}
                섹션: {section.section_name}
                
                이 섹션에 대한 상세한 내용을 작성해주세요.
                """
                # section.content = await llm_client.generate(prompt)
        
        # 참고 문헌 (research_data에서 추출)
        references = []
        if research_data:
            for item in research_data:
                if 'source' in item:
                    references.append(SourceInfo(
                        url=item['source'].get('url', ''),
                        title=item['source'].get('title', ''),
                        reliability_score=item['source'].get('reliability_score', 5.0),
                        is_official=item['source'].get('is_official', False)
                    ))
        
        # 설계서 생성
        return DesignDocument(
            title=f"설계서: {user_request[:50]}...",
            quality_level=quality_level,
            creation_date=datetime.now(),
            sections=sections,
            references=references,
            revision_count=0
        )
    
    @classmethod
    async def create_design(
        cls,
        user_request: str,
        phase0_result: Any,
        phase1_result: Any,
        research_data: List[Dict] = None,
        llm_client: Any = None
    ) -> Phase4Result:
        """
        전체 설계 프로세스
        """
        design_document = await cls.generate_design(
            user_request,
            phase0_result,
            phase1_result,
            research_data,
            llm_client
        )
        
        return Phase4Result(
            design_document=design_document,
            collaboration_records=[
                {
                    "expert": expert.name,
                    "contribution": f"Contributed to design"
                }
                for expert in phase1_result.experts
            ],
            user_interventions=[]
        )
