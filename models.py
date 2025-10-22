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
# Phase 2: 정보 수집
# ============================================================================

class SourceInfo(BaseModel):
    """출처 정보"""
    url: str
    title: str
    published_date: Optional[str] = None
    reliability_score: float = Field(ge=0.0, le=10.0)
    is_official: bool = False


class ResearchItem(BaseModel):
    """조사 항목"""
    content: str
    source: SourceInfo
    relevance_score: float = Field(ge=0.0, le=10.0)


class Phase2Result(BaseModel):
    """Phase 2 결과"""
    research_items: List[ResearchItem]
    total_items: int
    target_items: int
    achievement_rate: float
    last_updated: datetime


# ============================================================================
# Phase 3: 명확화 대화
# ============================================================================

class QuestionAnswer(BaseModel):
    """질문-답변 쌍"""
    question_number: int
    question_text: str
    asked_by_expert: str
    user_answer: Dict[str, Any]
    timestamp: datetime


class ClarityAssessment(BaseModel):
    """명확도 평가"""
    specificity: float = Field(ge=0.0, le=1.0)
    consistency: float = Field(ge=0.0, le=1.0)
    completeness: float = Field(ge=0.0, le=1.0)
    
    @property
    def cumulative_clarity(self) -> float:
        return (self.specificity * 0.4 + 
                self.consistency * 0.3 + 
                self.completeness * 0.3)


class InsightDocument(BaseModel):
    """Insight 문서"""
    original_request: str
    clarified_request: str
    layer_clarity: Dict[str, float]
    overall_clarity: float
    qa_history: List[QuestionAnswer]
    user_characteristics: Dict[str, Any]
    constraints: Dict[str, Any]
    required_features: List[Dict[str, Any]]
    optional_features: List[Dict[str, Any]]


class Phase3Result(BaseModel):
    """Phase 3 결과"""
    insight: InsightDocument
    clarity_assessment: ClarityAssessment
    questions_asked: int
    status: Literal["success", "partial", "failed"]


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
    collaboration_records: List[Dict[str, Any]]
    user_interventions: List[Dict[str, Any]] = []


# ============================================================================
# Phase 5: LLM 선정
# ============================================================================

class LLMProfile(BaseModel):
    """LLM 프로필"""
    name: str
    provider: str
    permanent_features: Dict[str, Any]
    specializations: List[str]
    current_version: str
    last_update: datetime


class LLMScore(BaseModel):
    """LLM 적합성 점수"""
    technical_fit: float = Field(ge=0.0, le=10.0)
    recency: float = Field(ge=0.0, le=10.0)
    success_prediction: float = Field(ge=0.0, le=10.0)
    availability: float = Field(ge=0.0, le=10.0)
    peer_adjustment: float = Field(ge=-1.0, le=1.0, default=0.0)
    
    @property
    def final_score(self) -> float:
        base = (self.technical_fit * 0.4 + 
                self.recency * 0.3 + 
                self.success_prediction * 0.2 + 
                self.availability * 0.1)
        return base + self.peer_adjustment


class CollaborationPattern(str, Enum):
    """협업 패턴"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    VALIDATION = "validation"


class Phase5Result(BaseModel):
    """Phase 5 결과"""
    selected_llms: List[str]
    llm_scores: Dict[str, LLMScore]
    work_mode: Literal["solo", "collaboration"]
    collaboration_pattern: Optional[CollaborationPattern] = None
    role_assignments: Dict[str, str]


# ============================================================================
# Phase 7: 최종 검증
# ============================================================================

class ValidationResult(BaseModel):
    """검증 결과"""
    evaluator: str
    sufficiency: Literal["Pass", "Fail"]
    consistency: Literal["Pass", "Fail"]
    recency: Literal["Pass", "Fail"]
    completeness: Literal["Pass", "Fail"]
    issues_found: List[Dict[str, Any]] = []


class Phase7Result(BaseModel):
    """Phase 7 결과"""
    evaluations: List[ValidationResult]
    passed: bool
    revision_needed: bool
    revision_count: int = 0


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
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        arbitrary_types_allowed = True
    
    def update_timestamp(self):
        """타임스탬프 업데이트"""
        self.updated_at = datetime.now()
# ============================================================================
# Phase 2: 정보 수집 추가 모델
# ============================================================================

class ResearchItem(BaseModel):
    """리서치 항목"""
    query: str
    category: str
    priority: int = Field(ge=1, le=10)
    keywords: List[str] = []


class Phase2Result(BaseModel):
    """Phase 2 결과 (수정)"""
    research_items: List[ResearchItem]
    sources: List[SourceInfo]
    metadata: Dict[str, Any] = {}


# ============================================================================
# Phase 3: 명확화 추가 모델
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
    """Phase 3 결과 (수정)"""
    questions: List[ClarificationQuestion]
    responses: List[ClarificationResponse]
    clarification_needed: bool
    metadata: Dict[str, Any] = {}


# ============================================================================
# Phase 5: LLM 선정 추가 모델
# ============================================================================

class ModelCapability(str, Enum):
    """모델 능력"""
    REASONING = "reasoning"
    CODE_GENERATION = "code_generation"
    CREATIVE_WRITING = "creative_writing"
    ANALYSIS = "analysis"
    LONG_CONTEXT = "long_context"


class SelectionReason(BaseModel):
    """선정 이유"""
    criterion: str
    weight: float = Field(ge=0.0, le=1.0)
    score: float = Field(ge=0.0, le=1.0)


class LLMSelection(BaseModel):
    """LLM 선택"""
    model_id: str
    provider: str
    role: str
    capabilities: List[ModelCapability]
    reasons: List[SelectionReason]
    confidence: float = Field(ge=0.0, le=1.0)


class Phase5Result(BaseModel):
    """Phase 5 결과 (수정)"""
    selections: List[LLMSelection]
    optimized_prompts: Dict[str, str]
    metadata: Dict[str, Any] = {}


# ============================================================================
# Phase 7: 검증 추가 모델
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
    """검증 결과 (수정)"""
    passed: bool
    checks: List[ValidationCheck]
    issues: List[str]
    severity: str
    validated_at: datetime


class Phase7Result(BaseModel):
    """Phase 7 결과 (수정)"""
    validation_result: ValidationResult
    quality_metrics: QualityMetrics
    improvements: List[str]
    metadata: Dict[str, Any] = {}
