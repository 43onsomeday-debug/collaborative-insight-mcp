"""
Collaborative Insight Generation Framework - Data Models
상태 관리 및 데이터 구조 정의
"""
from __future__ import annotations
from enum import Enum
from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class RequestType(str, Enum):
    """요청 유형 분류"""
    TYPE_1 = "Type 1"  # 단순명확
    TYPE_2 = "Type 2"  # 복잡명확
    TYPE_3 = "Type 3"  # 모호


class ProcessingMode(str, Enum):
    """LLM 처리 방식"""
    SINGLE = "single"
    COLLABORATIVE = "collaborative"
    SINGLE_DEGRADED = "single_degraded"


class ExecutionMode(str, Enum):
    """Phase 2, 4 실행 모드"""
    SOLO = "단독"
    MULTI = "다중"
    UNAVAILABLE = "불가"


class ClarityLevel(str, Enum):
    """명확도 수준"""
    EXPLORING = "exploring"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    ALMOST_CERTAIN = "almost_certain"
    CERTAIN = "certain"


# ============================================================================
# Phase 0: 초기 요청 분석
# ============================================================================

class ClarityScore(BaseModel):
    """명확성 점수"""
    specific_situation: bool = Field(description="구체적 상황")
    purpose_stated: bool = Field(description="목적 명시")
    target_specified: bool = Field(description="대상 명시")
    background_knowledge: bool = Field(description="배경지식")
    scope_defined: bool = Field(description="범위 설정")
    
    @property
    def total_score(self) -> int:
        return sum([
            self.specific_situation,
            self.purpose_stated,
            self.target_specified,
            self.background_knowledge,
            self.scope_defined
        ])
    
    @property
    def is_clear(self) -> bool:
        return self.total_score >= 4


class ComplexityScore(BaseModel):
    """복잡도 점수"""
    creativity_needed: int = Field(default=0, ge=0, le=2)
    analysis_needed: int = Field(default=0, ge=0, le=2)
    integration_needed: int = Field(default=0, ge=0, le=1)
    critical_domain: int = Field(default=0, ge=0, le=2)
    
    @property
    def total_score(self) -> int:
        return (self.creativity_needed + self.analysis_needed + 
                self.integration_needed + self.critical_domain)
    
    @property
    def is_complex(self) -> bool:
        return self.total_score >= 4


class Phase0Result(BaseModel):
    """Phase 0 결과"""
    request_type: RequestType
    clarity_score: ClarityScore
    complexity_score: Optional[ComplexityScore] = None
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


# ============================================================================
# Phase 1: 계층 구조 및 전문가
# ============================================================================

class HierarchyLayer(str, Enum):
    """계층 레이어"""
    DOMAIN = "Domain"
    SUBDOMAIN = "Subdomain"
    CATEGORY = "Category"
    TASK = "Task"


class HierarchyStructure(BaseModel):
    """계층 구조"""
    domain: Optional[str] = None
    subdomain: Optional[str] = None
    category: Optional[str] = None
    task: Optional[str] = None
    
    def get_active_layers(self) -> List[HierarchyLayer]:
        """활성화된 계층 목록"""
        layers = []
        if self.domain:
            layers.append(HierarchyLayer.DOMAIN)
        if self.subdomain:
            layers.append(HierarchyLayer.SUBDOMAIN)
        if self.category:
            layers.append(HierarchyLayer.CATEGORY)
        if self.task:
            layers.append(HierarchyLayer.TASK)
        return layers


class Expert(BaseModel):
    """전문가 정보"""
    name: str
    layers: List[HierarchyLayer]
    expertise: str
    assigned_llm: Optional[str] = None


class Phase1Result(BaseModel):
    """Phase 1 결과"""
    hierarchy: HierarchyStructure
    experts: List[Expert]
    processing_mode: ProcessingMode
    llm_used: List[str]
    zen_mcp_status: str


# ============================================================================
# Phase 1.5: 환경 체크 (NEW)
# ============================================================================

class Phase1_5Result(BaseModel):
    """Phase 1.5 결과 - 환경 체크"""
    zen_mcp_connected: bool
    zen_mcp_message: str
    api_count: int
    available_apis: List[str]
    execution_mode: Dict[str, str]  # phase2, phase4, description
    estimated_costs: Dict[str, str]  # type1, type2, type3, note
    cache_enabled: bool = True
    cache_ttl_minutes: int = 5
    checked_at: str


# ============================================================================
# Phase 2: 정보 수집
# ============================================================================

class SourceInfo(BaseModel):
    """출처 정보"""
    url: str
    title: str
    published_date: Optional[str] = None
    reliability_score: float = Field(ge=0.0, le=10.0)
    relevance_score: float = Field(ge=0.0, le=10.0, default=5.0)
    is_official: bool = False


class ResearchItem(BaseModel):
    """리서치 항목"""
    query: str
    category: str
    priority: int = Field(ge=1, le=10)
    keywords: List[str] = []


class Phase2Result(BaseModel):
    """Phase 2 결과"""
    research_items: List[ResearchItem]
    sources: List[SourceInfo]
    execution_mode: str = "단독"  # 단독 or 다중
    llms_used: List[str] = []
    metadata: Dict[str, Any] = {}


# ============================================================================
# Phase 3: 명확화 대화
# ============================================================================

class ClarificationQuestion(BaseModel):
    """명확화 질문"""
    question: str
    category: str
    priority: int = Field(ge=1, le=10)
    context: str = ""


class ClarificationResponse(BaseModel):
    """명확화 응답"""
    question_id: str
    answer: str
    satisfied: bool = False


class Phase3Result(BaseModel):
    """Phase 3 결과"""
    questions: List[ClarificationQuestion]
    responses: List[ClarificationResponse]
    clarification_needed: bool
    metadata: Dict[str, Any] = {}


# ============================================================================
# Phase 4: 설계 및 기획
# ============================================================================

class QualityLevel(str, Enum):
    """품질 레벨"""
    LV1_STANDARD = "Lv1 Standard"
    LV2_CRITICAL = "Lv2 Critical"


class DesignSection(BaseModel):
    """설계서 섹션"""
    section_name: str
    content: str
    citations: List[str] = []


class DesignDocument(BaseModel):
    """설계서"""
    title: str
    quality_level: QualityLevel
    creation_date: datetime
    sections: List[DesignSection]
    references: List[SourceInfo]
    revision_count: int = 0


class Phase4Result(BaseModel):
    """Phase 4 결과"""
    design_document: DesignDocument
    execution_mode: str = "단독"  # 단독 or 다중
    collaboration_records: List[Dict[str, Any]] = []
    user_interventions: List[Dict[str, Any]] = []


# ============================================================================
# Phase 5: LLM 선정
# ============================================================================

class ModelCapability(str, Enum):
    """모델 능력"""
    REASONING = "reasoning"
    CODE_GENERATION = "code_generation"
    CREATIVE_WRITING = "creative_writing"
    ANALYSIS = "analysis"
    LONG_CONTEXT = "long_context"


class SelectionReason(str, Enum):
    """선정 이유"""
    TECHNICAL_FIT = "technical_fit"
    COST_EFFICIENCY = "cost_efficiency"
    SPEED = "speed"
    RELIABILITY = "reliability"
    SPECIALIZATION = "specialization"


class LLMSelection(BaseModel):
    """LLM 선택"""
    model_name: str
    provider: str
    reason: SelectionReason
    confidence: float = Field(ge=0.0, le=1.0)


class Phase5Result(BaseModel):
    """Phase 5 결과"""
    selections: List[LLMSelection]
    metadata: Dict[str, Any] = {}


# ============================================================================
# Phase 7: 검증
# ============================================================================

class ValidationLevel(str, Enum):
    """검증 레벨"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ValidationCheck(BaseModel):
    """검증 체크"""
    check_name: str
    level: ValidationLevel
    passed: bool
    score: float = Field(ge=0.0, le=1.0)
    issues: List[str] = []
    timestamp: datetime


class QualityMetrics(BaseModel):
    """품질 메트릭"""
    overall_score: float = Field(ge=0.0, le=1.0)
    completeness: float = Field(ge=0.0, le=1.0)
    accuracy: float = Field(ge=0.0, le=1.0)
    consistency: float = Field(ge=0.0, le=1.0)
    usability: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)


class ValidationResult(BaseModel):
    """검증 결과"""
    passed: bool
    checks: List[ValidationCheck]
    issues: List[str]
    severity: str
    validated_at: datetime


class Phase7Result(BaseModel):
    """Phase 7 결과"""
    validation_result: ValidationResult
    quality_metrics: QualityMetrics
    improvements: List[str]
    metadata: Dict[str, Any] = {}


# ============================================================================
# 전체 워크플로우 상태
# ============================================================================

class WorkflowState(BaseModel):
    """전체 워크플로우 상태"""
    session_id: str
    user_request: str
    current_phase: int = 0
    
    phase0_result: Optional[Phase0Result] = None
    phase1_result: Optional[Phase1Result] = None
    phase1_5_result: Optional[Phase1_5Result] = None  # NEW
    phase2_result: Optional[Phase2Result] = None
    phase3_result: Optional[Phase3Result] = None
    phase4_result: Optional[Phase4Result] = None
    phase5_result: Optional[Phase5Result] = None
    phase7_result: Optional[Phase7Result] = None
    
    # Phase 3 대화형 명확화를 위한 추가 필드
    all_questions: Optional[List[ClarificationQuestion]] = None
    current_question_index: int = 0
    collected_answers: Optional[List[ClarificationResponse]] = None
    waiting_for_answer: bool = False
    
    # 전역 설정
    timeout_minutes: int = 30
    started_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        arbitrary_types_allowed = True
    
    def update_timestamp(self):
        """타임스탬프 업데이트"""
        self.updated_at = datetime.now()
    
    def is_timeout(self) -> bool:
        """타임아웃 체크"""
        elapsed = (datetime.now() - self.started_at).total_seconds() / 60
        return elapsed > self.timeout_minutes
