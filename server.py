"""
Collaborative Insight Generation Framework - MCP Server (Updated)
- Phase 1.5 추가: 환경 체크
- 전역 타임아웃: 30분
- Phase 2, 4: 단독/다중 모드 지원
"""
from fastmcp import FastMCP
from datetime import datetime
from typing import Optional
import json

from models import WorkflowState, RequestType, Phase1_5Result
from phases.phase0 import RequestAnalyzer
from phases.phase1 import ExpertAssigner
from phases.phase1_5 import EnvironmentChecker
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


def check_timeout(session_id: str) -> dict | None:
    """타임아웃 체크 (전역 30분)"""
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    if workflow.is_timeout():
        return {
            "error": "Session timeout",
            "message": f"세션이 {workflow.timeout_minutes}분을 초과했습니다.",
            "elapsed_minutes": (datetime.now() - workflow.started_at).total_seconds() / 60,
            "session_id": session_id
        }
    
    return None


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
        "next_phase": "assign_experts",
        "timeout_minutes": 30
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
    # 타임아웃 체크
    timeout_result = check_timeout(session_id)
    if timeout_result:
        return timeout_result
    
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase0_result:
        return {"error": "Phase 0 not completed"}
    
    # Phase 3가 필요했지만 완료되지 않았다면 경고
    if hasattr(workflow, 'waiting_for_answer') and workflow.waiting_for_answer:
        return {
            "error": "Clarification questions are still pending",
            "message": "명확화 질문에 먼저 답변해주세요",
            "current_question_index": workflow.current_question_index,
            "next_action": "clarify_user_intent"
        }
    
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
        "next_phase": "check_environment"
    }


# ============================================================================
# Tool 2.5: check_environment - Phase 1.5 (NEW)
# ============================================================================

@mcp.tool()
def check_environment(session_id: str) -> dict:
    """
    환경을 체크합니다 (Phase 1.5).
    - Zen MCP 연결 확인
    - LLM API 개수 확인
    - Phase 2, 4 실행 모드 결정
    - 예상 비용 표시
    
    Args:
        session_id: 세션 ID
    
    Returns:
        환경 체크 결과
    """
    # 타임아웃 체크
    timeout_result = check_timeout(session_id)
    if timeout_result:
        return timeout_result
    
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase1_result:
        return {"error": "Phase 1 not completed"}
    
    # Phase 1.5 실행
    result = EnvironmentChecker.check_environment(session_id)
    
    # Phase1_5Result 모델로 변환
    phase1_5_result = Phase1_5Result(**result)
    workflow.phase1_5_result = phase1_5_result
    workflow.current_phase = 1.5
    workflow.update_timestamp()
    
    # 다음 Phase 결정
    request_type = workflow.phase0_result.request_type if workflow.phase0_result else RequestType.TYPE_2
    
    if request_type == RequestType.TYPE_3:
        next_phase = "clarify_user_intent"
    else:
        next_phase = "gather_information"
    
    return {
        "session_id": session_id,
        "zen_mcp_status": {
            "connected": result["zen_mcp_connected"],
            "message": result["zen_mcp_message"]
        },
        "api_info": {
            "count": result["api_count"],
            "available": result["available_apis"]
        },
        "execution_mode": result["execution_mode"],
        "estimated_costs": result["estimated_costs"],
        "cache_info": {
            "enabled": result["cache_enabled"],
            "ttl_minutes": result["cache_ttl_minutes"]
        },
        "next_phase": next_phase,
        "message": "✅ 환경 체크 완료"
    }


# ============================================================================
# Tool 3: gather_information - Phase 2
# ============================================================================

@mcp.tool()
async def gather_information(session_id: str) -> dict:
    """
    전략적 정보를 수집합니다 (Phase 2).
    - 단독 모드: API 0개일 때 (Zen MCP Fallback)
    - 다중 모드: API 1~4개일 때
    
    Args:
        session_id: 세션 ID
    
    Returns:
        수집된 정보 결과
    """
    # 타임아웃 체크
    timeout_result = check_timeout(session_id)
    if timeout_result:
        return timeout_result
    
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase1_result:
        return {"error": "Phase 1 not completed"}
    
    # Phase 1.5 결과로 실행 모드 결정
    execution_mode = "단독"
    llms_used = []
    
    if workflow.phase1_5_result:
        execution_mode = workflow.phase1_5_result.execution_mode.get("phase2", "단독")
        llms_used = workflow.phase1_5_result.available_apis
    
    # Phase 2 실행
    expert_names = [expert.name for expert in workflow.phase1_result.experts]
    
    result = await InformationGatherer.gather_information(
        user_request=workflow.user_request,
        experts=expert_names,
        context={"phase1": workflow.phase1_result.model_dump()}
    )
    
    # execution_mode 추가
    result.execution_mode = execution_mode
    result.llms_used = llms_used
    
    workflow.phase2_result = result
    workflow.current_phase = 2
    workflow.update_timestamp()
    
    return {
        "session_id": session_id,
        "execution_mode": execution_mode,
        "llms_used": llms_used,
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
        "next_phase": "create_design",
        "message": f"✅ 정보 수집 완료 ({execution_mode} 모드)"
    }


# ============================================================================
# Tool 4: clarify_user_intent - Phase 3
# ============================================================================

@mcp.tool()
def clarify_user_intent(
    session_id: str
) -> dict:
    """
    사용자 의도를 명확화하기 위한 질문을 **하나씩** 생성합니다 (Phase 3).
    사용자 답변을 기다리며, answer_clarification_question으로 답변을 받습니다.
    
    Args:
        session_id: 세션 ID
    
    Returns:
        현재 질문 (하나만) 및 대기 상태
    """
    # 타임아웃 체크
    timeout_result = check_timeout(session_id)
    if timeout_result:
        return timeout_result
    
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase0_result:
        return {"error": "Phase 0 not completed"}
    
    # 이미 생성된 질문이 없으면 모든 질문 생성
    if not hasattr(workflow, 'all_questions') or not workflow.all_questions:
        clarity_score = workflow.phase0_result.clarity_score.total_score
        
        result = Clarifier.generate_questions(
            user_request=workflow.user_request,
            clarity_score=clarity_score,
            context={
                "phase0": workflow.phase0_result.model_dump()
            }
        )
        
        if not result.clarification_needed:
            return {
                "session_id": session_id,
                "status": "no_clarification_needed",
                "message": "요청이 충분히 명확합니다",
                "next_phase": "assign_experts"
            }
        
        # 질문 목록 저장
        workflow.all_questions = result.questions
        workflow.current_question_index = 0
        workflow.collected_answers = []
        workflow.waiting_for_answer = True
        workflow.update_timestamp()
    
    # 현재 질문 인덱스 확인
    if workflow.current_question_index >= len(workflow.all_questions):
        # 모든 질문이 완료됨
        workflow.waiting_for_answer = False
        workflow.current_phase = 3
        
        return {
            "session_id": session_id,
            "status": "all_questions_answered",
            "message": "모든 명확화 질문이 완료되었습니다",
            "total_questions": len(workflow.all_questions),
            "answered": len(workflow.collected_answers),
            "next_phase": "재분류 필요 (analyze_request 다시 호출)"
        }
    
    # 현재 질문 하나만 반환
    current_question = workflow.all_questions[workflow.current_question_index]
    
    return {
        "session_id": session_id,
        "status": "waiting_for_answer",
        "question_number": workflow.current_question_index + 1,
        "total_questions": len(workflow.all_questions),
        "current_question": {
            "question": current_question.question,
            "category": current_question.category,
            "priority": current_question.priority
        },
        "message": "위 질문에 답변해주세요. answer_clarification_question 도구를 사용하여 답변하세요.",
        "next_action": "answer_clarification_question"
    }


# ============================================================================
# Tool 4-1: answer_clarification_question - 답변 받기
# ============================================================================

@mcp.tool()
def answer_clarification_question(
    session_id: str,
    answer: str
) -> dict:
    """
    명확화 질문에 대한 사용자 답변을 받습니다.
    
    Args:
        session_id: 세션 ID
        answer: 사용자의 답변
    
    Returns:
        다음 질문 또는 완료 상태
    """
    # 타임아웃 체크
    timeout_result = check_timeout(session_id)
    if timeout_result:
        return timeout_result
    
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not hasattr(workflow, 'waiting_for_answer') or not workflow.waiting_for_answer:
        return {"error": "No question is waiting for an answer"}
    
    if workflow.current_question_index >= len(workflow.all_questions):
        return {"error": "All questions have been answered"}
    
    # 현재 질문 가져오기
    current_question = workflow.all_questions[workflow.current_question_index]
    
    # 답변 저장
    from models import ClarificationResponse
    response = ClarificationResponse(
        question_id=current_question.question,
        answer=answer,
        satisfied=len(answer) > 10
    )
    workflow.collected_answers.append(response)
    
    # 다음 질문으로 이동
    workflow.current_question_index += 1
    workflow.update_timestamp()
    
    # 모든 질문이 완료되었는지 확인
    if workflow.current_question_index >= len(workflow.all_questions):
        workflow.waiting_for_answer = False
        workflow.current_phase = 3
        
        # Phase3Result 생성
        from models import Phase3Result
        workflow.phase3_result = Phase3Result(
            questions=workflow.all_questions,
            responses=workflow.collected_answers,
            clarification_needed=False,
            metadata={
                "completed": True,
                "total_questions": len(workflow.all_questions),
                "total_answers": len(workflow.collected_answers)
            }
        )
        
        return {
            "session_id": session_id,
            "status": "completed",
            "message": "모든 명확화 질문이 완료되었습니다! 이제 analyze_request를 다시 호출하여 재분류하세요.",
            "total_questions": len(workflow.all_questions),
            "answered": len(workflow.collected_answers),
            "next_phase": "재분류 (analyze_request)",
            "your_answer": answer
        }
    
    # 다음 질문 반환
    next_question = workflow.all_questions[workflow.current_question_index]
    
    return {
        "session_id": session_id,
        "status": "next_question",
        "previous_answer": answer,
        "question_number": workflow.current_question_index + 1,
        "total_questions": len(workflow.all_questions),
        "next_question": {
            "question": next_question.question,
            "category": next_question.category,
            "priority": next_question.priority
        },
        "message": "답변 감사합니다! 다음 질문에도 답변해주세요."
    }


# ============================================================================
# Tool 5: create_design - Phase 4
# ============================================================================

@mcp.tool()
async def create_design(session_id: str) -> dict:
    """
    설계서를 생성합니다 (Phase 4).
    - 단독 모드: API 0개일 때
    - 다중 모드: API 1~4개일 때 (섹션별 협의)
    
    Args:
        session_id: 세션 ID
    
    Returns:
        생성된 설계서
    """
    # 타임아웃 체크
    timeout_result = check_timeout(session_id)
    if timeout_result:
        return timeout_result
    
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase0_result or not workflow.phase1_result:
        return {"error": "Previous phases not completed"}
    
    # Phase 1.5 결과로 실행 모드 결정
    execution_mode = "단독"
    
    if workflow.phase1_5_result:
        execution_mode = workflow.phase1_5_result.execution_mode.get("phase4", "단독")
    
    # Phase 4 실행
    result = await DesignGenerator.create_design(
        workflow.user_request,
        workflow.phase0_result,
        workflow.phase1_result,
        llm_client=llm_client
    )
    
    # execution_mode 추가
    result.execution_mode = execution_mode
    
    workflow.phase4_result = result
    workflow.current_phase = 4
    workflow.update_timestamp()
    
    design_doc = result.design_document
    
    return {
        "session_id": session_id,
        "execution_mode": execution_mode,
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
        "next_phase": "select_llm",
        "message": f"✅ 설계서 생성 완료 ({execution_mode} 모드)"
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
    # 타임아웃 체크
    timeout_result = check_timeout(session_id)
    if timeout_result:
        return timeout_result
    
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
# Tool 7: execute_task - Phase 6
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
    # 타임아웃 체크
    timeout_result = check_timeout(session_id)
    if timeout_result:
        return timeout_result
    
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    workflow = sessions[session_id]
    
    if not workflow.phase4_result:
        return {"error": "Design not created"}
    
    # 간단한 실행
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
        "llm_used": selected_llm,
        "next_phase": "완료 또는 quality_check (Phase 7)"
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
    
    # 타임아웃 체크
    is_timeout = workflow.is_timeout()
    elapsed_minutes = (datetime.now() - workflow.started_at).total_seconds() / 60
    
    status = {
        "session_id": session_id,
        "current_phase": workflow.current_phase,
        "user_request": workflow.user_request,
        "request_type": workflow.phase0_result.request_type.value if workflow.phase0_result else None,
        "processing_mode": workflow.phase1_result.processing_mode.value if workflow.phase1_result else None,
        "timeout_status": {
            "is_timeout": is_timeout,
            "elapsed_minutes": round(elapsed_minutes, 2),
            "timeout_limit_minutes": workflow.timeout_minutes
        },
        "phases_completed": {
            "phase0": workflow.phase0_result is not None,
            "phase1": workflow.phase1_result is not None,
            "phase1_5": workflow.phase1_5_result is not None,
            "phase2": workflow.phase2_result is not None,
            "phase3": workflow.phase3_result is not None,
            "phase4": workflow.phase4_result is not None,
            "phase5": workflow.phase5_result is not None,
            "phase7": workflow.phase7_result is not None
        },
        "created_at": workflow.created_at.isoformat(),
        "updated_at": workflow.updated_at.isoformat()
    }
    
    # Phase 1.5 정보 추가
    if workflow.phase1_5_result:
        status["environment"] = {
            "zen_mcp_connected": workflow.phase1_5_result.zen_mcp_connected,
            "api_count": workflow.phase1_5_result.api_count,
            "execution_mode": workflow.phase1_5_result.execution_mode
        }
    
    # Phase 3 대기 상태 추가
    if hasattr(workflow, 'waiting_for_answer'):
        status["clarification_status"] = {
            "waiting_for_answer": workflow.waiting_for_answer,
            "current_question_index": workflow.current_question_index if hasattr(workflow, 'current_question_index') else 0,
            "total_questions": len(workflow.all_questions) if hasattr(workflow, 'all_questions') else 0,
            "answered_questions": len(workflow.collected_answers) if hasattr(workflow, 'collected_answers') else 0
        }
    
    return status


if __name__ == "__main__":
    # MCP 서버 실행
    mcp.run()
