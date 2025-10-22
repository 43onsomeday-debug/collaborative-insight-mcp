"""
Phase 1: 계층 구조 파악 및 전문가 배정
"""
from typing import List, Dict
from models import (
    HierarchyStructure, HierarchyLayer, Expert,
    ProcessingMode, Phase1Result
)


class ExpertAssigner:
    """전문가 배정기"""
    
    # 15가지 계층 조합 정의
    HIERARCHY_COMBINATIONS = {
        1: {"domain": True, "subdomain": False, "category": False, "task": False},
        2: {"domain": True, "subdomain": True, "category": False, "task": False},
        3: {"domain": True, "subdomain": False, "category": True, "task": False},
        4: {"domain": True, "subdomain": False, "category": False, "task": True},
        5: {"domain": True, "subdomain": True, "category": True, "task": False},
        6: {"domain": True, "subdomain": True, "category": False, "task": True},
        7: {"domain": True, "subdomain": False, "category": True, "task": True},
        8: {"domain": True, "subdomain": True, "category": True, "task": True},
        9: {"domain": False, "subdomain": True, "category": False, "task": False},
        10: {"domain": False, "subdomain": True, "category": True, "task": False},
        11: {"domain": False, "subdomain": True, "category": False, "task": True},
        12: {"domain": False, "subdomain": False, "category": True, "task": False},
        13: {"domain": False, "subdomain": False, "category": True, "task": True},
        14: {"domain": False, "subdomain": True, "category": True, "task": True},
        15: {"domain": False, "subdomain": False, "category": False, "task": True},
    }
    
    @classmethod
    def detect_hierarchy(cls, user_request: str) -> HierarchyStructure:
        """
        계층 구조 감지
        """
        request_lower = user_request.lower()
        
        hierarchy = HierarchyStructure()
        
        # Domain 감지
        domain_keywords = ['분야', '영역', '산업', '업계', '도메인',
                          'field', 'domain', 'industry', 'sector']
        if any(word in request_lower for word in domain_keywords):
            # 실제로는 LLM이 분석하겠지만, 여기서는 간단히 추출
            hierarchy.domain = "Detected Domain"
        
        # Subdomain 감지
        subdomain_keywords = ['세부', '하위', '전문', '특정',
                             'specific', 'specialized', 'sub']
        if any(word in request_lower for word in subdomain_keywords):
            hierarchy.subdomain = "Detected Subdomain"
        
        # Category 감지
        category_keywords = ['카테고리', '유형', '종류', '분류',
                           'category', 'type', 'kind', 'class']
        if any(word in request_lower for word in category_keywords):
            hierarchy.category = "Detected Category"
        
        # Task 감지
        task_keywords = ['작업', '태스크', '할일', '해야',
                        'task', 'work', 'job', 'do']
        if any(word in request_lower for word in task_keywords):
            hierarchy.task = "Detected Task"
        
        return hierarchy
    
    @classmethod
    def assign_experts(
        cls,
        hierarchy: HierarchyStructure,
        processing_mode: ProcessingMode
    ) -> List[Expert]:
        """
        계층 구조에 따라 전문가 배정
        """
        experts = []
        active_layers = hierarchy.get_active_layers()
        
        if not active_layers:
            # 기본 전문가
            experts.append(Expert(
                name="General Expert",
                layers=[],
                expertise="General problem solving"
            ))
        else:
            # 각 계층별 전문가 배정
            if HierarchyLayer.DOMAIN in active_layers:
                experts.append(Expert(
                    name="Domain Expert",
                    layers=[HierarchyLayer.DOMAIN],
                    expertise=f"Expertise in {hierarchy.domain}"
                ))
            
            if HierarchyLayer.SUBDOMAIN in active_layers:
                experts.append(Expert(
                    name="Subdomain Specialist",
                    layers=[HierarchyLayer.SUBDOMAIN],
                    expertise=f"Specialized in {hierarchy.subdomain}"
                ))
            
            if HierarchyLayer.CATEGORY in active_layers:
                experts.append(Expert(
                    name="Category Expert",
                    layers=[HierarchyLayer.CATEGORY],
                    expertise=f"Expert in {hierarchy.category}"
                ))
            
            if HierarchyLayer.TASK in active_layers:
                experts.append(Expert(
                    name="Task Specialist",
                    layers=[HierarchyLayer.TASK],
                    expertise=f"Specialized in {hierarchy.task}"
                ))
        
        return experts
    
    @classmethod
    def determine_processing_mode(
        cls,
        complexity_score: int,
        expert_count: int
    ) -> ProcessingMode:
        """
        처리 모드 결정
        """
        if complexity_score <= 3 or expert_count == 1:
            return ProcessingMode.SINGLE
        else:
            return ProcessingMode.COLLABORATIVE
    
    @classmethod
    def assign(
        cls,
        user_request: str,
        complexity_score: int = 0,
        llm_used: List[str] = None
    ) -> Phase1Result:
        """
        전체 배정 프로세스
        """
        # 1. 계층 구조 감지
        hierarchy = cls.detect_hierarchy(user_request)
        
        # 2. 처리 모드 결정
        active_layer_count = len(hierarchy.get_active_layers())
        processing_mode = cls.determine_processing_mode(
            complexity_score, 
            active_layer_count
        )
        
        # 3. 전문가 배정
        experts = cls.assign_experts(hierarchy, processing_mode)
        
        # 4. LLM 배정 (간단한 로직)
        if llm_used is None:
            llm_used = ["claude"]  # 기본값
        
        for expert in experts:
            expert.assigned_llm = llm_used[0] if llm_used else "claude"
        
        return Phase1Result(
            hierarchy=hierarchy,
            experts=experts,
            processing_mode=processing_mode,
            llm_used=llm_used,
            zen_mcp_status="Not integrated yet"
        )
