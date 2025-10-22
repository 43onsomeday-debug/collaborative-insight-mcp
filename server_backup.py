"""
Collaborative Insight Generation Framework - MCP Server
"""
from fastmcp import FastMCP
from datetime import datetime
from typing import Optional
import json

from models import WorkflowState, RequestType
from phases.phase0 import RequestAnalyzer
from phases.phase1 import ExpertAssigner
from phases.phase2 import InformationGatherer
from phases.phase3 import Clarifier
from phases.phase4 import DesignGenerator
from phases.phase5 import LLMSelector
from phases.phase6 import TaskExecutor
from llm_integration import LLMClient

# MCP 서버 초기화
mcp = FastMCP("Collaborative Insight Framework")

# LLM 클라이언트 초기화
llm_client = LLMClient()

# 세션 저장소 (실제 환경에서는 DB 사용)
sessions = {}


# ============================================================================
# Tool 1: analyze_request - Phase 0
# ============================================================================

@mcp.tool()
def analyze_request(
    user_request: str,
    session_id: Optional[str] = None
) -> dict:
    """
    사용자 요청을 분석하고 분류합니다 (Phase 0).
    
    Args:
        user_request: 분석할 사용자 요청
        session_id: 세션 ID (선택사항, 없으면 새로 생성)
    
    Returns:
        분석 결과 및 세션 정보
    """
    # Phase 0 실행
    result = RequestAnalyzer.analyze(user_request)
    
    # 세션 생성 또는 업데이트
    if not session_id:
        session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    workflow_state = WorkflowState(
        session_id=session_id,
        user_request=user_request,
        current_phase=0,
        phase0_result=result
    )
    
    sessions[session_id] = workflow_state
    
    return {
        "session_id": session_id,
        "request_type": result.request_type.value,
        "clarity_score": result.clarity_score.total_score,
        "complexity_score": result.complexity_score.total_score if result.complexity_score else None,
        "confidence": result.confidence,
        "reasoning": result.reasoning,
        "next_phase": "assign_experts"
    }


# ============================================================================
# Tool 2: assign_experts - Phase 1
# ============================================================================

@mcp.tool()
def assign_experts(session_id: str) -> dict:
    """
    계층 구조를 파악하고 전문가를 배정합니다 (Phase 1).
    
    Args:
        session_id: 세션 ID
    
    Returns:
        전문가 배정 결과
    """
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase0_result:
        return {"error": "Phase 0 not completed"}
    
    # Phase 1 실행
    complexity = workflow.phase0_result.complexity_score.total_score if workflow.phase0_result.complexity_score else 0
    
    result = ExpertAssigner.assign(
        workflow.user_request,
        complexity_score=complexity
    )
    
    workflow.phase1_result = result
    workflow.current_phase = 1
    workflow.update_timestamp()
    
    return {
        "session_id": session_id,
        "hierarchy": {
            "domain": result.hierarchy.domain,
            "subdomain": result.hierarchy.subdomain,
            "category": result.hierarchy.category,
            "task": result.hierarchy.task
        },
        "experts": [
            {
                "name": expert.name,
                "expertise": expert.expertise,
                "layers": [layer.value for layer in expert.layers]
            }
            for expert in result.experts
        ],
        "processing_mode": result.processing_mode.value,
        "next_phase": "gather_information"
    }


# ============================================================================
# Tool 3: gather_information - Phase 2
# ============================================================================

@mcp.tool()
async def gather_information(session_id: str) -> dict:
    """
    전략적 정보를 수집합니다 (Phase 2).
    
    Args:
        session_id: 세션 ID
    
    Returns:
        수집된 정보 결과
    """
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase1_result:
        return {"error": "Phase 1 not completed"}
    
    # Phase 2 실행
    expert_names = [expert.name for expert in workflow.phase1_result.experts]
    
    result = await InformationGatherer.gather_information(
        user_request=workflow.user_request,
        experts=expert_names,
        context={"phase1": workflow.phase1_result.model_dump()}
    )
    
    workflow.phase2_result = result
    workflow.current_phase = 2
    workflow.update_timestamp()
    
    return {
        "session_id": session_id,
        "research_items_count": len(result.research_items),
        "research_items": [
            {
                "query": item.query,
                "category": item.category,
                "priority": item.priority
            }
            for item in result.research_items[:10]
        ],
        "sources_count": len(result.sources),
        "sources": [
            {
                "title": source.title,
                "url": source.url,
                "relevance_score": source.relevance_score
            }
            for source in result.sources[:5]
        ],
        "next_phase": "create_design"
    }


# ============================================================================
# Tool 4: clarify_user_intent - Phase 3
# ============================================================================

@mcp.tool()
def clarify_user_intent(
    session_id: str
) -> dict:
    """
    사용자 의도를 명확화하기 위한 질문을 생성합니다 (Phase 3).
    
    Args:
        session_id: 세션 ID
    
    Returns:
        생성된 명확화 질문들
    """
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase0_result:
        return {"error": "Phase 0 not completed"}
    
    # Phase 3 실행 - 명확화 질문 생성
    clarity_score = workflow.phase0_result.clarity_score.total_score
    
    result = Clarifier.generate_questions(
        user_request=workflow.user_request,
        clarity_score=clarity_score,
        context={
            "phase0": workflow.phase0_result.model_dump()
        }
    )
    
    workflow.phase3_result = result
    workflow.current_phase = 3
    workflow.update_timestamp()
    
    if not result.clarification_needed:
        return {
            "session_id": session_id,
            "status": "no_clarification_needed",
            "message": "요청이 충분히 명확합니다",
            "next_phase": "assign_experts"
        }
    
    return {
        "session_id": session_id,
        "status": "needs_clarification",
        "questions": [
            {
                "question": q.question,
                "category": q.category,
                "priority": q.priority
            }
            for q in result.questions
        ],
        "question_count": len(result.questions),
        "next_phase": "User should answer questions and re-analyze"
    }


# ============================================================================
# Tool 5: create_design - Phase 4
# ============================================================================

@mcp.tool()
async def create_design(session_id: str) -> dict:
    """
    설계서를 생성합니다 (Phase 4).
    
    Args:
        session_id: 세션 ID
    
    Returns:
        생성된 설계서
    """
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase0_result or not workflow.phase1_result:
        return {"error": "Previous phases not completed"}
    
    # Phase 4 실행
    result = await DesignGenerator.create_design(
        workflow.user_request,
        workflow.phase0_result,
        workflow.phase1_result,
        llm_client=llm_client
    )
    
    workflow.phase4_result = result
    workflow.current_phase = 4
    workflow.update_timestamp()
    
    design_doc = result.design_document
    
    return {
        "session_id": session_id,
        "title": design_doc.title,
        "quality_level": design_doc.quality_level.value,
        "sections": [
            {
                "name": section.section_name,
                "content": section.content
            }
            for section in design_doc.sections
        ],
        "references_count": len(design_doc.references),
        "next_phase": "select_llm"
    }


# ============================================================================
# Tool 6: select_llm - Phase 5
# ============================================================================

@mcp.tool()
def select_llm(
    session_id: str
) -> dict:
    """
    작업에 적합한 LLM을 선정합니다 (Phase 5).
    
    Args:
        session_id: 세션 ID
    
    Returns:
        선정된 LLM 정보
    """
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase4_result:
        return {"error": "Phase 4 not completed"}
    
    # Phase 5 실행 - LLM 선정
    complexity = workflow.phase0_result.complexity_score.total_score if workflow.phase0_result and workflow.phase0_result.complexity_score else 5
    
    result = LLMSelector.select_models(
        design_document=workflow.phase4_result.design_document,
        complexity_score=complexity,
        context={
            "phase0": workflow.phase0_result.model_dump() if workflow.phase0_result else None,
            "phase1": workflow.phase1_result.model_dump() if workflow.phase1_result else None,
            "phase2": workflow.phase2_result.model_dump() if workflow.phase2_result else None
        }
    )
    
    workflow.phase5_result = result
    workflow.current_phase = 5
    workflow.update_timestamp()
    
    return {
        "session_id": session_id,
        "selected_models": [
            {
                "model_name": sel.model_name,
                "provider": sel.provider,
                "reason": sel.reason.value,
                "confidence": sel.confidence
            }
            for sel in result.selections
        ],
        "model_count": len(result.selections),
        "next_phase": "execute_task"
    }


# ============================================================================
# Tool 7: execute_task - Phase 6 (간단한 버전)
# ============================================================================

@mcp.tool()
async def execute_task(
    session_id: str,
    selected_llm: str = "claude"
) -> dict:
    """
    작업을 실행합니다 (Phase 6).
    
    Args:
        session_id: 세션 ID
        selected_llm: 사용할 LLM (claude/gpt/gemini)
    
    Returns:
        실행 결과
    """
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase4_result:
        return {"error": "Design not created"}
    
    # 간단한 실행 (실제로는 Phase 5 + Phase 6)
    design_doc = workflow.phase4_result.design_document
    
    # 프롬프트 생성
    sections_text = "\n\n".join([
        f"{section.section_name}\n{section.content}"
        for section in design_doc.sections
    ])
    
    prompt = f"""
사용자 요청: {workflow.user_request}

설계서:
{sections_text}

위 설계서를 바탕으로 실제 구현 가능한 결과물을 생성해주세요.
"""
    
    # LLM 실행
    result = await llm_client.generate(
        prompt=prompt,
        model=selected_llm
    )
    
    workflow.current_phase = 6
    workflow.update_timestamp()
    
    return {
        "session_id": session_id,
        "result": result,
        "llm_used": selected_llm
    }


# ============================================================================
# Tool 8: get_workflow_status - 상태 조회
# ============================================================================

@mcp.tool()
def get_workflow_status(session_id: str) -> dict:
    """
    워크플로우 상태를 조회합니다.
    
    Args:
        session_id: 세션 ID
    
    Returns:
        현재 워크플로우 상태
    """
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    return {
        "session_id": session_id,
        "current_phase": workflow.current_phase,
        "user_request": workflow.user_request,
        "request_type": workflow.phase0_result.request_type.value if workflow.phase0_result else None,
        "processing_mode": workflow.phase1_result.processing_mode.value if workflow.phase1_result else None,
        "phases_completed": {
            "phase0": workflow.phase0_result is not None,
            "phase1": workflow.phase1_result is not None,
            "phase2": workflow.phase2_result is not None,
            "phase3": workflow.phase3_result is not None,
            "phase4": workflow.phase4_result is not None,
            "phase5": workflow.phase5_result is not None,
            "phase7": workflow.phase7_result is not None
        },
        "created_at": workflow.created_at.isoformat(),
        "updated_at": workflow.updated_at.isoformat()
    }


# ============================================================================
# Resource: workflow_templates
# ============================================================================

@mcp.resource("workflow://templates")
def get_workflow_templates() -> str:
    """워크플로우 템플릿 제공"""
    templates = {
        "Type 1 (단순명확)": {
            "phases": ["Phase 0", "Phase 1", "Phase 4", "Phase 6"],
            "description": "간단한 요청을 위한 빠른 워크플로우"
        },
        "Type 2 (복잡명확)": {
            "phases": ["Phase 0", "Phase 1", "Phase 2", "Phase 4", "Phase 5", "Phase 6", "Phase 7"],
            "description": "복잡한 요청을 위한 완전한 워크플로우"
        },
        "Type 3 (모호)": {
            "phases": ["Phase 0", "Phase 3", "재분류", "..."],
            "description": "명확화가 필요한 요청을 위한 대화형 워크플로우"
        }
    }
    
    return json.dumps(templates, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # MCP 서버 실행
    mcp.run()
